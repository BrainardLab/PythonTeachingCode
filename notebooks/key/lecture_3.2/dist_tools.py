"""Shared analysis + plotting for the "is it normal?" teaching notebooks.

Each notebook loads a data set, wraps the quantity of interest in a
``Distribution``, and calls :func:`analyze`.  Every plot and every printed
number is produced here, so editing this one file keeps all of the notebooks
(stock returns, human height, city sizes, ...) in lock step.

Typical use in a notebook
-------------------------
    import dist_tools as dt

    d = dt.Distribution(
        values=my_series,            # a pandas Series, already cleaned
        quantity="Adult height",     # axis label, without units
        unit="cm",
        noun="women",                # plural noun for one row of data
        source="NHANES 2015-2018",
        note="non-Hispanic white, ages 20-59",
        bin_width=1.0,               # histogram bar width, in data units
    )
    dt.analyze(d)                    # summary table + 6 plots

For the city-size notebook, build one ``Distribution`` for the raw counts and
another for ``np.log10(counts)`` and call :func:`analyze` on each.
"""

from __future__ import annotations   # allow "float | None" annotations on Python 3.9

from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

SCALES = ("full", "zoom", "log")


@dataclass
class Distribution:
    values: pd.Series               # quantity of interest, cleaned (no NaNs)
    quantity: str                   # axis label without units, e.g. "Adult height"
    unit: str                       # e.g. "cm", "%", "people", "log10 people"
    noun: str = "observations"      # plural noun for one datum ("women", "cities")
    source: str = ""                # provenance, printed in the summary
    note: str = ""                  # optional extra summary line (filters, dates)
    bin_width: float | None = None  # histogram bar width in data units; None -> auto
    zoom_top: float = 10            # y-axis cap for the "zoomed" panel
    value_fmt: str = "{:.4g}"       # how to print values in the summary

    @property
    def xlabel(self) -> str:
        return f"{self.quantity} ({self.unit})"

    def bin_edges(self) -> np.ndarray:
        lo, hi = float(self.values.min()), float(self.values.max())
        if self.bin_width:
            start = np.floor(lo / self.bin_width) * self.bin_width
            stop = np.ceil(hi / self.bin_width) * self.bin_width
            return np.arange(start, stop + self.bin_width, self.bin_width)
        return np.linspace(lo, hi, 91)


# --------------------------------------------------------------------------- #
#  One panel                                                                  #
# --------------------------------------------------------------------------- #
def hist_panel(values, bins, xlabel, title, mean, std, *, noun="observations",
               scale="full", mark_sigma=False, zoom_top=10):
    """Histogram of ``values`` with the curve ``Normal(mean, std)`` drawn on top.

    The "normal fit" is nothing more than ``mean`` and ``std`` -- no shape or
    tail fitting is done (for a Gaussian those are exactly what a
    maximum-likelihood fit returns).

    scale : "full"  linear y-axis, autoscaled  -> the curve matches the bulk
            "zoom"  linear y-axis capped low   -> rare extreme values show up
            "log"   logarithmic y-axis         -> every frequency on one axis
    mark_sigma : dashed guides at -3 and +3 (used on the z-score plots)
    """
    bw = bins[1] - bins[0]
    grid = np.linspace(bins[0], bins[-1], 1000)
    expected = stats.norm.pdf(grid, mean, std) * len(values) * bw

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(values, bins=bins, color="steelblue", alpha=0.6,
            label=f"Actual {noun}")
    ax.plot(grid, expected, "r-", lw=2, label="normal fit")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(f"Number of {noun}")
    ax.set_title(title)

    if scale == "zoom":
        ax.set_ylim(0, zoom_top)
    elif scale == "log":
        ax.set_yscale("log")
        ax.set_ylim(bottom=0.5)

    if mark_sigma:
        for edge in (-3, 3):
            ax.axvline(edge, color="0.4", ls="--", lw=1)
            ax.annotate(f"{edge:+d}σ", xy=(edge, 0),
                        xycoords=("data", "axes fraction"),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", color="0.4", fontsize=9)

    ax.legend()
    plt.tight_layout()
    plt.show()


# --------------------------------------------------------------------------- #
#  A row of three panels (native units, or z-score)                           #
# --------------------------------------------------------------------------- #
def plot_views(d: Distribution, axis: str = "value"):
    """Draw the three panels (full / zoom / log) for one distribution.

    axis="value"  -> x-axis in native units
    axis="zscore" -> x-axis rescaled to (value - mean) / std
    """
    v = d.values
    mu, sigma = v.mean(), v.std()
    edges = d.bin_edges()

    if axis == "zscore":
        values = (v - mu) / sigma
        bins = (edges - mu) / sigma
        mean, std = 0.0, 1.0
        xlabel = f"{d.quantity} (z-score: standard deviations from the mean)"
        mark = True
        tag = "  —  z-score axis"
    else:
        values, bins = v, edges
        mean, std = mu, sigma
        xlabel = d.xlabel
        mark = False
        tag = ""

    titles = {
        "full": f"{d.quantity}{tag} — full view",
        "zoom": f"{d.quantity}{tag} — zoomed to 0-{d.zoom_top:g}",
        "log": f"{d.quantity}{tag} — log vertical scale",
    }
    for scale in SCALES:
        hist_panel(values, bins, xlabel, titles[scale], mean, std,
                   noun=d.noun, scale=scale, mark_sigma=mark,
                   zoom_top=d.zoom_top)


# --------------------------------------------------------------------------- #
#  Printed summary                                                            #
# --------------------------------------------------------------------------- #
def summarize(d: Distribution):
    v = d.values
    mu, sigma, n = v.mean(), v.std(), len(v)
    val = d.value_fmt.format
    pos = d.value_fmt.replace("+", "").format          # no forced sign

    if d.source:
        print(f"Source:  {d.source}")
    if d.note:
        print(f"Sample:  {d.note}")
    print(f"{d.noun.capitalize()} included:  {n:,}")
    print(f"Range:   {val(v.min())} to {val(v.max())} {d.unit}")
    print(f"Mean:    {val(mu)} {d.unit}")
    print(f"Std dev (1 sigma):  {pos(sigma)} {d.unit}")
    print()

    head = f"{'window':>16} | {'normal predicts':>15} | {('actual ' + d.noun):>16}"
    print(head)
    print("-" * len(head))
    for k in (1, 2, 3, 4, 5):
        predicted = n * 2 * (1 - stats.norm.cdf(k))
        actual = int(np.sum(np.abs(v - mu) > k * sigma))
        print(f"  beyond {k} sigma  | {predicted:>15.2f} | {actual:>16,}")
    print()

    if not isinstance(v.index, pd.RangeIndex):
        lo_lab, hi_lab = v.idxmin(), v.idxmax()
        lo_lab = lo_lab.date() if isinstance(lo_lab, pd.Timestamp) else lo_lab
        hi_lab = hi_lab.date() if isinstance(hi_lab, pd.Timestamp) else hi_lab
        print(f"Smallest: {val(v.min())} {d.unit}  ({(v.min() - mu) / sigma:+.1f} sigma)  [{lo_lab}]")
        print(f"Largest:  {val(v.max())} {d.unit}  ({(v.max() - mu) / sigma:+.1f} sigma)  [{hi_lab}]")
    print(f"Skewness (0 = symmetric):      {stats.skew(v):+.2f}")
    print(f"Excess kurtosis (0 = normal):  {stats.kurtosis(v):+.2f}")


# --------------------------------------------------------------------------- #
#  Everything                                                                 #
# --------------------------------------------------------------------------- #
def analyze(d: Distribution, zscore: bool = True):
    """Print the summary table, then draw the native-unit panels and (by
    default) the z-score panels."""
    summarize(d)
    plot_views(d, axis="value")
    if zscore:
        plot_views(d, axis="zscore")
