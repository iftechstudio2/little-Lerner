import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/"public"
files=list(PUBLIC.rglob("*.html"))
assert files, "No generated HTML files"
for p in files:
    s=p.read_text(encoding="utf-8")
    assert "<title>" in s and "</title>" in s, f"Missing title: {p}"
    assert '<meta name="description"' in s, f"Missing description: {p}"
    for attr in ("href","src"):
        pattern=attr + r'=["\x27]([^"\x27#?]+)'
        for ref in re.findall(pattern,s):
            if ref.startswith(("http:","https:","mailto:","tel:","javascript:")): continue
            target=(p.parent/ref).resolve()
            if not target.exists():
                raise AssertionError(f"Broken local {attr} {ref} in {p}")
print(f"Validated {len(files)} HTML pages and their local links/assets.")