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

| Notebook | Open in Colab |
| --- | --- |
| [notebooks/00_colab_quickstart.ipynb](notebooks/00_colab_quickstart.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BrainardLab/PythonTeachingCode/blob/main/notebooks/00_colab_quickstart.ipynb) |

## Adding a new notebook

1. Put the `.ipynb` file in `notebooks/`.
2. Run `python tools/add_colab_badge.py` to insert an "Open in Colab" badge as
   the first cell (idempotent — safe to re-run on every notebook).
3. Add a row to the table above.
4. Commit and push:

   ```bash
   git add notebooks/your_notebook.ipynb README.md
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
