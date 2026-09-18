import html, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
public=ROOT/"public"
files=list(public.rglob("*.html"))
assert files, "No generated HTML files"
for p in files:
    s=p.read_text(encoding="utf-8")
    assert "<title>" in s and "</title>" in s, f"Missing title: {p}"
    assert '<meta name="description"' in s, f"Missing description: {p}"
    for href in re.findall(r'href=["\']([^"\'#?]+)',s):
        if href.startswith(("http:","https:","mailto:","tel:","javascript:")): continue
        target=(p.parent/href).resolve()
        if not target.exists():
            raise AssertionError(f"Broken local link {href} in {p}")
print(f"Validated {len(files)} HTML pages.")
