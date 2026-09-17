# Kids Learning Next-Level Static CMS

**Edit content -> run one build command -> all pages update.**

- `content/lessons.json` = your content
- `templates/lesson.html` = one master design
- `public/assets/style.css` = design
- `public/assets/app.js` = voice + quiz
- `scripts/build.py` = automatic page generator
- `public/` = final Cloudflare Pages website

Run:
`python scripts/build.py`

For 1000+ pages, add more lesson records to the JSON (or later split content into multiple files). Keep content genuinely useful and unique rather than making near-duplicate pages.
