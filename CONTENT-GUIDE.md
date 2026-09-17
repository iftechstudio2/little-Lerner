# ✏️ Add a New Lesson — No HTML Needed

You do **not** need to write a full HTML page for every lesson.

Open:

`content/lessons.json`

Each lesson is a content record. Keep the same fields:

- `slug` — URL/page name, e.g. `letter-a`
- `title` — page title
- `letter` — capital letter
- `small` — lowercase letter
- `main_word` — main teaching word
- `main_emoji` — main visual
- `intro` — short lesson explanation
- `description` — SEO-friendly useful description
- `words` — supporting vocabulary
- `quiz` — questions, options and the correct answer

## Automatic flow

`content/lessons.json` → master template → `scripts/build.py` → generated pages → GitHub Pages

The included GitHub Action runs the builder automatically whenever content/template files change on `main`.

## Important

For a 1000+ page site, add genuinely useful and sufficiently distinct educational content. Do not create hundreds of pages that only swap one word while the rest is identical.
