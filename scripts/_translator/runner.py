"""Apply Chinese->English substitutions to every notebook under notebooks/."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB_ROOT = ROOT / "notebooks"

from dict_part1 import T1
from dict_part2 import T2
from dict_part3 import T3

T = {}
for d in (T1, T2, T3):
    T.update(d)

# Apply longest first so sub-fragments don't clobber longer matches.
ORDERED = sorted(T.items(), key=lambda kv: -len(kv[0]))


def translate_text(text: str) -> str:
    for zh, en in ORDERED:
        if zh in text:
            text = text.replace(zh, en)
    return text


def translate_source(src):
    if isinstance(src, list):
        out = [translate_text(line) for line in src]
        changed = out != src
        return out, changed
    new = translate_text(src)
    return new, new != src


def patch(path: Path) -> bool:
    with path.open("r", encoding="utf-8") as f:
        nb = json.load(f)
    modified = False
    for cell in nb.get("cells", []):
        new_src, changed = translate_source(cell.get("source", ""))
        if changed:
            cell["source"] = new_src
            modified = True
    if modified:
        with path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
    return modified


def main():
    nbs = sorted(p for p in NB_ROOT.rglob("*.ipynb")
                 if ".ipynb_checkpoints" not in p.parts)
    print(f"Patching {len(nbs)} notebooks...")
    for p in nbs:
        touched = patch(p)
        print(("  patched: " if touched else "  skipped: ") + str(p.relative_to(ROOT)))
    # Report remaining Chinese occurrences
    cjk = re.compile(r"[\u4e00-\u9fff]")
    remaining = 0
    for p in nbs:
        data = p.read_text(encoding="utf-8")
        remaining += len(cjk.findall(data))
    print(f"Remaining Chinese characters across notebooks: {remaining}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    main()
