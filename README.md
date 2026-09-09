# Python Teaching Code

Teaching notebooks for the Brainard Lab. Every notebook can be run in the
browser with [Google Colab](https://colab.research.google.com/) — no local
install required.

## Run a notebook in Colab

Any notebook in this repo opens in Colab through a URL of this form:

```
https://colab.research.google.com/github/BrainardLab/PythonTeachingCode/blob/main/<path-to-notebook>.ipynb
```

Or browse interactively: open <https://colab.research.google.com>, choose
**GitHub**, enter `BrainardLab/PythonTeachingCode`, and pick a notebook.

Colab gives each session a fresh, temporary machine. Changes are **not** saved
back to GitHub. To keep your edits use *File → Save a copy in Drive*, or
*File → Download → .ipynb*.

## Notebooks

### Lecture 3.2

Notebooks in `notebooks/key/lecture_3.2/`:

| Notebook | Open in Colab |
| --- | --- |
| [lecture_3.2_Group_A.ipynb](notebooks/key/lecture_3.2/lecture_3.2_Group_A.ipynb) — in-class predict-then-plot, pooled Group A height game | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BrainardLab/PythonTeachingCode/blob/main/notebooks/key/lecture_3.2/lecture_3.2_Group_A.ipynb) |
| [StockChangeDistribution.ipynb](notebooks/key/lecture_3.2/StockChangeDistribution.ipynb) — daily S&P 500 moves (fat tails) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BrainardLab/PythonTeachingCode/blob/main/notebooks/key/lecture_3.2/StockChangeDistribution.ipynb) |
| [HeightDistribution.ipynb](notebooks/key/lecture_3.2/HeightDistribution.ipynb) — adult women's height, NHANES (nicely normal) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BrainardLab/PythonTeachingCode/blob/main/notebooks/key/lecture_3.2/HeightDistribution.ipynb) |
| [CityPopulationDistribution.ipynb](notebooks/key/lecture_3.2/CityPopulationDistribution.ipynb) — US city sizes, raw and log10 (lognormal) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BrainardLab/PythonTeachingCode/blob/main/notebooks/key/lecture_3.2/CityPopulationDistribution.ipynb) |

`StockChangeDistribution`, `HeightDistribution`, and `CityPopulationDistribution`
each compare a real data set against a normal distribution using the **same**
plots and summary table. The shared code lives in
[notebooks/key/lecture_3.2/dist_tools.py](notebooks/key/lecture_3.2/dist_tools.py);
each notebook only loads its data, wraps it in a `dist_tools.Distribution`, and
calls `dist_tools.analyze()`. Edit `dist_tools.py` once and all three notebooks
change together. Each notebook downloads `dist_tools.py` from GitHub at run time
when it isn't already present, so Colab works with no extra steps.
`tools/build_notebooks.py` regenerates the three notebooks' shared scaffolding.

## Adding a new notebook

1. Put the `.ipynb` file anywhere under `notebooks/`.
2. Run `python tools/add_colab_badge.py` to insert an "Open in Colab" badge as
   the first cell (idempotent — safe to re-run on every notebook; it recurses
   into subfolders).
3. Add a row to a table above.
4. Commit and push:

   ```bash
   git add notebooks/ README.md
   git commit -m "Add your_notebook"
   git push
   ```

The pushed notebook is immediately runnable in Colab via its badge link.

## Running locally (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```
