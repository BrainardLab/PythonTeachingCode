"""Regenerate the "is it normal?" notebooks from one source, so their
scaffolding (bootstrap cell, cell order, prose) stays identical.

    python tools/build_notebooks.py

This writes StockChangeDistribution / HeightDistribution /
CityPopulationDistribution .ipynb with EMPTY outputs. After running it:

    python tools/add_colab_badge.py
    jupyter nbconvert --to notebook --execute --inplace notebooks/*Distribution.ipynb

The analysis itself (plots + summary table) lives in notebooks/dist_tools.py,
not here -- that is what keeps the notebooks in lock step at run time.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "notebooks" / "key" / "lecture_3.2"

BOOTSTRAP = '''\
# --- Make dist_tools.py importable ---------------------------------------
# Locally it sits next to this notebook. On Colab we grab it from GitHub.
import os, urllib.request
if not os.path.exists("dist_tools.py"):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/BrainardLab/PythonTeachingCode"
        "/main/notebooks/key/lecture_3.2/dist_tools.py",
        "dist_tools.py",
    )

# Optional: pick up edits to dist_tools.py without restarting the kernel.
# Skipped silently where the autoreload extension is unavailable (e.g. the
# Python 3.13 build currently on Google Colab).
try:
    _ip = get_ipython()
    _ip.run_line_magic("load_ext", "autoreload")
    _ip.run_line_magic("autoreload", "2")
except Exception:
    pass

import numpy as np
import pandas as pd
import dist_tools as dt'''

RAW_HIST_MD = (
    "**The histogram on its own.** Look at the shape of the data first, with no\n"
    "normal curve drawn on top. The same three panels appear again just below,\n"
    "this time with the fit added."
)


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": text.splitlines(keepends=True)}


def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }


# ------------------------------------------------------------------ stock ---
stock = notebook([
    md("# Stock change distribution\n\n"
       "Daily percent changes in the S&P 500 index, compared with a normal\n"
       "(bell-curve) distribution. This is the **fat-tailed** case: the middle\n"
       "looks normal, but large moves happen far more often than a normal\n"
       "distribution allows.\n\n"
       "All three notebooks in this set (stock changes, human height, city\n"
       "sizes) share `dist_tools.py`, so the plots and the summary table stay\n"
       "identical across them."),
    code(BOOTSTRAP),
    code('# Colab does not ship yfinance; %pip installs into the running kernel.\n'
         '%pip install -q yfinance\n'
         'import yfinance as yf'),
    code('ticker = "^GSPC"                     # S&P 500  (try "^DJI" for the Dow Jones)\n'
         'raw = yf.download(ticker, start="2000-01-01", auto_adjust=True,\n'
         '                  progress=False, multi_level_index=False)\n'
         '\n'
         'prices = raw["Close"].dropna()      # daily closing index level, in points\n'
         '\n'
         '# Daily percent change from the previous close. prices / prices.shift(1)\n'
         '# is always positive, so this is always defined; it is simply negative\n'
         '# on down days.\n'
         'change = (prices.pct_change() * 100).dropna()\n'
         '\n'
         'stock = dt.Distribution(\n'
         '    values=change,\n'
         '    quantity="Daily change in the S&P 500",\n'
         '    unit="%",\n'
         '    noun="trading days",\n'
         '    source=f"Yahoo Finance via yfinance, ticker {ticker}",\n'
         '    note=f"{change.index.min().date()} to {change.index.max().date()}",\n'
         '    bin_width=0.5,\n'
         ')'),
    md(RAW_HIST_MD),
    code("dt.raw_histogram(stock)"),
    code("dt.analyze(stock)"),
    md("## What to notice\n\n"
       "- In the **full view** the normal fit tracks the central hump well.\n"
       "- On the **log scale** and in the **z-score** panels the histogram has\n"
       "  bars many standard deviations out where the normal fit has effectively\n"
       "  dropped to zero.\n"
       "- The summary table makes it quantitative: days beyond 3, 4, 5 sigma\n"
       "  happen tens to hundreds of times more often than a normal predicts,\n"
       "  and the excess kurtosis is large and positive."),
])

# ----------------------------------------------------------------- height ---
height = notebook([
    md("# Height distribution\n\n"
       "Standing height of adult women from a deliberately **homogeneous**\n"
       "sample (one sex, one age band, one self-reported race/ethnicity group).\n"
       "With the sources of variation narrowed like this, height is about as\n"
       "close to normal as real data gets -- the opposite of the stock-change\n"
       "notebook.\n\n"
       "Data: [NHANES](https://wwwn.cdc.gov/nchs/nhanes/), the CDC's National\n"
       "Health and Nutrition Examination Survey. We pool the 2015-2016 and\n"
       "2017-2018 cycles. Files are read straight from the CDC as SAS `.xpt`."),
    code(BOOTSTRAP),
    code('import io, urllib.request\n'
         '\n'
         'def _xpt(url):\n'
         '    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})\n'
         '    return pd.read_sas(io.BytesIO(urllib.request.urlopen(req, timeout=90).read()),\n'
         '                       format="xport")\n'
         '\n'
         'frames = []\n'
         'for year, suffix in [("2015", "I"), ("2017", "J")]:\n'
         '    base = f"https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/"\n'
         '    demo = _xpt(base + f"DEMO_{suffix}.xpt")     # demographics\n'
         '    bmx = _xpt(base + f"BMX_{suffix}.xpt")       # body measures\n'
         '    frames.append(demo.merge(bmx[["SEQN", "BMXHT"]], on="SEQN"))\n'
         '\n'
         'people = pd.concat(frames, ignore_index=True)\n'
         '\n'
         '# RIAGENDR: 1 male, 2 female     RIDRETH3 == 3: non-Hispanic white\n'
         '# RIDAGEYR: age in years         BMXHT: standing height in cm\n'
         'homogeneous = people[\n'
         '    (people.RIAGENDR == 2)\n'
         '    & (people.RIDAGEYR.between(20, 59))\n'
         '    & (people.RIDRETH3 == 3)\n'
         '].dropna(subset=["BMXHT"])\n'
         '\n'
         'height_cm = homogeneous["BMXHT"].reset_index(drop=True)\n'
         '\n'
         'height = dt.Distribution(\n'
         '    values=height_cm,\n'
         '    quantity="Adult height",\n'
         '    unit="cm",\n'
         '    noun="women",\n'
         '    source="NHANES 2015-2016 + 2017-2018 (CDC)",\n'
         '    note="non-Hispanic white women, ages 20-59",\n'
         '    bin_width=1.0,\n'
         ')'),
    md(RAW_HIST_MD),
    code("dt.raw_histogram(height)"),
    code("dt.analyze(height)"),
    md("## What to notice\n\n"
       "- The normal fit tracks the histogram closely everywhere, including on\n"
       "  the log scale.\n"
       "- Counts beyond 3 sigma are a handful, in line with the normal\n"
       "  prediction; skewness and excess kurtosis are both near zero.\n"
       "- Try widening the sample (drop the race/ethnicity filter, or mix in\n"
       "  men) and watch the fit degrade -- mixing groups with different means\n"
       "  is a common way to break normality."),
])

# ------------------------------------------------------------------- city ---
city = notebook([
    md("# City size distribution\n\n"
       "Populations of US places (1,000+ residents), from\n"
       "[GeoNames](https://www.geonames.org/). Raw city sizes are **not**\n"
       "normal -- not even close -- and this notebook shows that in plain\n"
       "numbers first. Then we take `log10(population)` and look again: on a\n"
       "log scale the bulk of the distribution is roughly bell-shaped\n"
       "(city sizes are approximately *lognormal*)."),
    code(BOOTSTRAP),
    code('import io, urllib.request, zipfile\n'
         '\n'
         '# cities1000.zip is ~11 MB. Swap in cities15000.zip for a smaller,\n'
         '# faster download (fewer, larger places).\n'
         'name = "cities1000"\n'
         'req = urllib.request.Request(\n'
         '    f"https://download.geonames.org/export/dump/{name}.zip",\n'
         '    headers={"User-Agent": "Mozilla/5.0"})\n'
         'blob = urllib.request.urlopen(req, timeout=120).read()\n'
         'txt = zipfile.ZipFile(io.BytesIO(blob)).read(f"{name}.txt").decode("utf-8")\n'
         '\n'
         'cols = ["geonameid", "name", "asciiname", "altnames", "lat", "lon",\n'
         '        "fclass", "fcode", "country", "cc2", "admin1", "admin2",\n'
         '        "admin3", "admin4", "population", "elevation", "dem", "tz", "moddate"]\n'
         'cities = pd.read_csv(io.StringIO(txt), sep="\\t", header=None,\n'
         '                     names=cols, low_memory=False)\n'
         '\n'
         'us = cities[(cities.country == "US") & (cities.population > 0)]\n'
         'pop = (us.set_index("name")["population"]\n'
         '         .sort_values(ascending=False)\n'
         '         .astype(float))\n'
         '\n'
         'SOURCE = f"GeoNames {name} (populated places, US only)"\n'
         '\n'
         'city_raw = dt.Distribution(\n'
         '    values=pop,\n'
         '    quantity="US city population",\n'
         '    unit="people",\n'
         '    noun="cities",\n'
         '    source=SOURCE,\n'
         '    value_fmt="{:,.0f}",\n'
         ')\n'
         '\n'
         'city_log = dt.Distribution(\n'
         '    values=np.log10(pop),\n'
         '    quantity="US city population, log10",\n'
         '    unit="log10 people",\n'
         '    noun="cities",\n'
         '    source=SOURCE,\n'
         '    bin_width=0.1,\n'
         '    value_fmt="{:.2f}",\n'
         ')'),
    md("### Raw city sizes (straight numbers)"),
    md(RAW_HIST_MD),
    code("dt.raw_histogram(city_raw)"),
    code("dt.analyze(city_raw)"),
    md("### The same data, log10 of population"),
    md(RAW_HIST_MD),
    code("dt.raw_histogram(city_log)"),
    code("dt.analyze(city_log)"),
    md("## What to notice\n\n"
       "- **Raw:** almost every city sits in the first bar and a thin tail\n"
       "  stretches out for millions of people. The normal fit is meaningless --\n"
       "  its standard deviation is set by a few huge cities, it puts the bulk\n"
       "  of its probability on negative populations, and skew and kurtosis are\n"
       "  enormous.\n"
       "- **log10:** the histogram is now roughly bell-shaped and the normal\n"
       "  fit is vastly better -- counts within 1 and 2 sigma nearly match the\n"
       "  normal prediction. So population is closer to *lognormal* than\n"
       "  normal.\n"
       "- It is not a perfect bell: the data is censored below 1,000 (note the\n"
       "  cliff at log10 = 3), and the upper tail is still a little heavy --\n"
       "  rank-size plots of city populations are famously close to a straight\n"
       "  line on log-log axes (Zipf's law)."),
])

for name, nb in [("StockChangeDistribution", stock),
                 ("HeightDistribution", height),
                 ("CityPopulationDistribution", city)]:
    path = OUT / f"{name}.ipynb"
    path.write_text(json.dumps(nb, indent=1) + "\n")
    print("wrote", path)
