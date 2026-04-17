"""Clear cell outputs & execution counts from every notebook under notebooks/.

Run once before pushing to GitHub.  This:
  * removes all stored stdout/display data,
  * resets execution counts,
  * eliminates any leftover Chinese (or otherwise noisy) output data,
  * dramatically shrinks the .ipynb file sizes.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def clear_notebook(p: Path):
    nb = json.loads(p.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

def main():
    nbs = sorted(p for p in (ROOT / "notebooks").rglob("*.ipynb")
                 if ".ipynb_checkpoints" not in p.parts)
    for p in nbs:
        before = p.stat().st_size
        clear_notebook(p)
        after = p.stat().st_size
        print(f"  cleared: {p.relative_to(ROOT)}  ({before:,} -> {after:,} bytes)")
    print(f"Cleared {len(nbs)} notebooks.")

if __name__ == "__main__":
    main()
