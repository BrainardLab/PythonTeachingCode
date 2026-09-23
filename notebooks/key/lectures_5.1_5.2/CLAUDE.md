# SpuriousCorrelations.ipynb — working notes

Teaching notebook for lectures 5.1–5.2 on correlation vs. causation, built
from examples on [tylervigen.com/spurious-correlations](https://www.tylervigen.com/spurious-correlations).
Committed at `notebooks/key/lectures_5.1_5.2/SpuriousCorrelations.ipynb`
(commits `a3f2447`, then extended in later sessions — check `git log` on
this file for the current state, since these notes describe it as of
2026-09-23 and may drift).

## What's in the notebook

Six paired-variable examples, each with the same treatment:
1. A dual-axis line plot vs. year (`plot_spurious`), title uses "and" not
   "vs." (e.g. "X and Y"), no stats in the title.
2. Two square scatterplots (`plot_scatter`, `ax.set_box_aspect(1)`), one
   per choice of which variable is on the x-axis, each in its own cell so
   it can be copied out individually. Scatterplot titles *do* show r and p.
3. Printed `r = ..., p = ...` under the line plot (Pearson, via
   `scipy.stats.pearsonr`; p < 0.001 is shown as "< 0.001" in plot titles,
   full precision in printed text).

Shared helpers live in one code cell near the top: `plot_spurious`,
`plot_scatter`, and `_r_p_label` (formats the r/p string for scatterplot
titles). Only imports: `numpy`, `matplotlib.pyplot`, `scipy.stats` — all
preinstalled on Colab, no local files needed, so the Colab badge (first
cell) works with zero setup.

### The five baseline examples (scraped from Vigen's static pages)

Each Vigen correlation page embeds an exact numeric `<table>` next to the
chart SVG — that table was scraped directly, not read off the chart
pixels, so the numbers are exact.

| # | Pair | Years | r, p |
|---|---|---|---|
| 1 | Margarine consumption vs. Maine divorce rate | 2000–2009 | 0.993, p=1.3e-8 |
| 2 | UFO sightings in Utah vs. US patents granted | 1975–2020 | 0.927, p=2.2e-20 |
| 3 | Public school 9th-grade enrollment vs. Bank of America stock | 2002–2022 | 0.815, p=6.7e-6 |
| 4 | Popularity of "Stevie" vs. Lululemon stock (LULU) | 2008–2022 | 0.980, p=1.6e-10 |
| 5 | Will Smith movie appearances vs. Kosovo electricity generation | 2008–2021 | 0.849, p=1.2e-4 |

Pair 3 replaced an original "Uranus distance vs. nuclear plants" example
at the user's request (Vigen page id 1828).

### Example 6: Helen vs. Lululemon (deliberately not cherry-picked)

Unlike the other five (which were selected *because* they correlate,
either as Vigen's pre-built pages or, for Stevie, picked from his
correlation-search tool for having a high r), this pair was chosen with
**no expectation of a relationship** — baby name popularity vs. an
unrelated retailer's stock — specifically to test what an arbitrary real
pairing shows.

- Years 2008–2025 (18 points).
- Helen births: Vigen's SSA-sourced numbers for 2008–2022, cross-checked
  against a second Vigen page (Helen×Citigroup) for consistency; 2023–2025
  from SSA's latest published counts, cross-verified against two
  independent sources (nameberry.com, nametrends.info) that agreed to
  within 1–2 births/year.
- LULU: same "first trading day of year, unadjusted open" convention as
  example 4 (see below).
- **Result: r ≈ -0.50, p ≈ 0.034** — a moderate negative correlation that
  clears the conventional p<0.05 bar, despite the pair being genuinely
  unrelated. The notebook uses this as a live demonstration of the
  data-dredging point: with enough independent attempts, ~1 in 20 will
  look "significant" by chance, and 18 points is a small enough sample
  for a few coincidental swings to produce exactly that.
- Found via Vigen's `/spurious/discover` search tool → variable page for
  "Helen" (id=2582) → its `request-correlation.php?id1=2582&id2=<id>` AJAX
  endpoint (the same one his UI uses) to generate real candidate pairings.
  Went with LULU by request rather than one of the auto-suggested (already
  correlated) candidates.

## Source verification (the notebook's own "Data verification" section)

Before extending anything, each of the 5 baseline pairs' cited sources was
checked against real, current data. Full results are in the notebook's
"Data verification: how well do Vigen's sources hold up?" markdown cell
(near the end, before "Why this happens"). Summary:

| Variable | Verdict |
|---|---|
| Margarine (USDA/Census) | ✅ exact match, all 10 years; source discontinued 2011 (one more real year, 2010, exists and nothing after) |
| Maine divorce rate (CDC/NCHS) | ✅ exact match, all 10 years; still published, real data through 2023 |
| US patents (USPTO) | ✅ exact match, 6/6 spot-checked years (via Wayback Machine — live USPTO page 404s); that specific all-patent-types/calendar-year table was discontinued after 2020, never updated |
| UFO sightings (NUFORC) | ❓ unverifiable — site blocks automated access (Cloudflare), data loads via JS even in archived snapshots |
| School enrollment (NCES) | 🟡 approximate match only (~0.1% off, likely a later revision) |
| BofA stock (BAC) | ❌ no match — tried year-end close and annual-average close against real BAC history, neither reproduces Vigen's numbers; pricing convention unidentified |
| "Stevie" births (SSA) | ✅ exact match 2008–2015, ~99%+ match 2016–2022 (SSA revises recent years) |
| Lululemon stock (LULU) | ✅ matches to the cent, 14/15 years, once you use **opening price on the first trading day of each calendar year, unadjusted** — NOT year-end close or annual average, which don't match at all |
| Will Smith movie count (TMDB) | 🟡 verified only 2008–2011 (4/14 years); no API key available, TMDB is crowdsourced/re-edited so no reliable method found for later years |
| Kosovo electricity (EIA) | ✅ essentially exact for 2016–2019 (4/14 spot-checked); earlier/later years differ somewhat (EIA revises preliminary international data) |

Only two pairs (margarine/divorce, Stevie/Lululemon) verify essentially
exactly on **both** variables. That asymmetry is deliberate content in the
notebook, not a gap to fix.

### Extension: Stevie/Lululemon through 2025

Because both variables in pair 4 verified almost exactly, the notebook
re-plots that pair with 3 more real years (2023–2025) appended, in a
"Checking Vigen's data, and extending it to 2025" subsection right after
the pair's original plots. Result: r barely moves (0.980 → 0.976), but the
2023–2025 tail is visibly the first stretch where the two lines stop
tracking. A closing note (not part of the correlation, since there's no
matching 2026 birth count yet) flags that LULU's Sept-2026 price (~$100)
is below every plotted year even as Stevie's popularity kept climbing.

### Pairs that were investigated but NOT extended

Margarine (source dead after 2010), UFO/patents (patents source dead
after 2020, UFO source unverifiable), school enrollment/BofA stock (BAC
convention never identified), Will Smith/Kosovo (movie count unverifiable
past 2011) — all deliberately left at their original ranges rather than
faking an extension. This was itself the point of a user request: verify
before extending, and say plainly when you can't.

## Important gap: no generator script is committed

The notebook was built by an ad hoc Python script (`build_notebook.py`)
that assembled the `.ipynb` JSON directly — an `EXAMPLES` list of dicts
(key, title, label1/unit1, label2/unit2, years, s1, s2) fed through a loop
that emitted the markdown + code cells, plus special-cased blocks for the
Stevie extension and the Helen commentary. **That script lived only in a
Claude session's scratchpad directory and was never committed** — it's
gone. The committed `.ipynb` is the only artifact.

If you (or a future Claude session) need to make a structural change that
touches every example (e.g. restyle all plots, add a 7th example, change
the scatterplot layout), the options are:
1. Hand-edit the notebook's cell JSON directly (each cell's `source` is
   plain Python/Markdown text — inspect with
   `jq '.cells[N]' SpuriousCorrelations.ipynb`).
2. Ask Claude to write a fresh generator script from the current notebook
   content (straightforward — the structure above is regular enough to
   reverse-engineer) and this time commit it, e.g. as
   `tools/build_spurious_correlations.py`, following the existing
   convention in `tools/build_notebooks.py` (used for the lecture_3.2
   notebooks).

Either way, after any edit: re-run `python tools/add_colab_badge.py
notebooks/key/lectures_5.1_5.2/SpuriousCorrelations.ipynb`, then execute
and save with outputs (`jupyter nbconvert --to notebook --execute
--output <tmp> ...`, then overwrite the tracked file with the executed
version) — the committed notebook is meant to already have its outputs
populated, matching the convention in `notebooks/key/lecture_3.2/`.

## Other conventions followed here

- `requirements.txt` now includes `ipywidgets` (added while fixing an
  unrelated notebook, `notebooks/key/lab_W4/False_Positives_Negatives.ipynb`,
  in the same overall work session) and `scipy` (already present).
- README.md has a "Lectures 5.1–5.2" section with this notebook listed —
  keep that description in sync if the notebook's example set changes.
