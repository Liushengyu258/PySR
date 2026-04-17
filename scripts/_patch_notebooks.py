"""One-off helper to inject a path-setup cell into every notebook and
redirect CSV references that used to sit at the project root so they now
point into ``data/``.

Run from anywhere:
    python scripts/_patch_notebooks.py
"""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_ROOT = PROJECT_ROOT / "notebooks"

SETUP_MARKER = "# [auto] project-root setup"
SETUP_SRC = f"""{SETUP_MARKER}
import os, sys
from pathlib import Path

# Walk upward to find the project root (folder containing .gitignore)
_p = Path.cwd().resolve()
while _p != _p.parent and not (_p / '.gitignore').exists():
    _p = _p.parent
PROJECT_ROOT = _p

# Switch cwd to the project root so every relative path
# (Stage1_Exploration/, Refined_Results_v4/, ...) keeps working
os.chdir(PROJECT_ROOT)
# Let the notebooks do `from viz_config import VizConfig`
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / 'data'
print(f'[setup] PROJECT_ROOT = {{PROJECT_ROOT}}')
"""

# Old path -> new path (assumes cwd has been switched to PROJECT_ROOT)
CSV_REPLACEMENTS = {
    "'train_dataset_ready.csv'": "'data/train_dataset_ready.csv'",
    '"train_dataset_ready.csv"': '"data/train_dataset_ready.csv"',
    "'cases.csv'": "'data/cases.csv'",
    '"cases.csv"': '"data/cases.csv"',
    "'summary_0_499.csv'": "'data/summary_0_499.csv'",
    '"summary_0_499.csv"': '"data/summary_0_499.csv"',
    "'cfd_lhs_cases.csv'": "'data/cfd_lhs_cases.csv'",
    '"cfd_lhs_cases.csv"': '"data/cfd_lhs_cases.csv"',
    "cases_file='cases.csv'": "cases_file='data/cases.csv'",
    "summary_file='summary_0_499.csv'": "summary_file='data/summary_0_499.csv'",
}


def patch_source(src):
    """Apply string replacements to either a str or list-of-str cell source."""
    changed = False
    if isinstance(src, list):
        new_lines = []
        for line in src:
            original = line
            for old, new in CSV_REPLACEMENTS.items():
                if old in line:
                    line = line.replace(old, new)
            if line != original:
                changed = True
            new_lines.append(line)
        return new_lines, changed
    else:  # str
        new = src
        for old, new_val in CSV_REPLACEMENTS.items():
            new = new.replace(old, new_val)
        return new, (new != src)


def already_has_setup(nb):
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        text = "".join(src) if isinstance(src, list) else src
        if SETUP_MARKER in text:
            return True
    return False


def patch_notebook(path: Path):
    with path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    modified = False

    if not already_has_setup(nb):
        setup_cell = {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": SETUP_SRC.splitlines(keepends=True),
        }
        nb.setdefault("cells", []).insert(0, setup_cell)
        modified = True

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        new_src, changed = patch_source(cell.get("source", ""))
        if changed:
            cell["source"] = new_src
            modified = True

    if modified:
        with path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print(f"  patched: {path.relative_to(PROJECT_ROOT)}")
    else:
        print(f"  skipped: {path.relative_to(PROJECT_ROOT)}")


def main():
    nbs = sorted(NB_ROOT.rglob("*.ipynb"))
    nbs = [p for p in nbs if ".ipynb_checkpoints" not in p.parts]
    print(f"Found {len(nbs)} notebooks under {NB_ROOT}")
    for p in nbs:
        patch_notebook(p)
    print("Done.")


if __name__ == "__main__":
    main()
