#!/usr/bin/env python3
"""Ensure every notebook in notebooks/ starts with an "Open in Colab" badge.

The badge links to the notebook's own path on GitHub so students can launch it
in Colab with one click. Running this repeatedly is safe: an existing badge
cell is replaced, not duplicated.

Usage:
    python tools/add_colab_badge.py            # update every notebook
    python tools/add_colab_badge.py a.ipynb    # update just these
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GITHUB_SLUG = "BrainardLab/PythonTeachingCode"
BRANCH = "main"
REPO_ROOT = Path(__file__).resolve().parent.parent
BADGE_MARKER = "colab-badge.svg"


def badge_source(rel_path: str) -> list[str]:
    url = f"https://colab.research.google.com/github/{GITHUB_SLUG}/blob/{BRANCH}/{rel_path}"
    return [
        f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})\n",
        "\n",
        "_Run this notebook in the browser — no install needed._",
    ]


def make_badge_cell(rel_path: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {"id": "colab-badge"},
        "source": badge_source(rel_path),
    }


def update_notebook(path: Path) -> bool:
    nb = json.loads(path.read_text())
    rel_path = path.relative_to(REPO_ROOT).as_posix()
    cells = nb.get("cells", [])

    if cells and cells[0].get("cell_type") == "markdown" and \
            BADGE_MARKER in "".join(cells[0].get("source", [])):
        cells[0] = make_badge_cell(rel_path)
    else:
        cells.insert(0, make_badge_cell(rel_path))

    nb["cells"] = cells
    path.write_text(json.dumps(nb, indent=1) + "\n")
    return True


def main(argv: list[str]) -> int:
    if argv:
        targets = [Path(a) for a in argv]
    else:
        targets = sorted((REPO_ROOT / "notebooks").glob("*.ipynb"))

    if not targets:
        print("No notebooks found.")
        return 0

    for path in targets:
        update_notebook(path)
        print(f"badge ok: {path.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
