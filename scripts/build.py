import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content' / 'lessons.json').read_text(encoding='utf-8'))
TEMPLATE = (ROOT / 'templates' / 'lesson.html').read_text(encoding='utf-8')
OUT = ROOT / 'public/pages'
OUT.mkdir(parents=True, exist_ok=True)
E = lambda x: html.escape(str(x), quote=True)

for i, d in enumerate(DATA):
    nav = '<a href="../index.html">🏠 Home</a>'
    if i:
        nav = f'<a href="{E(DATA[i-1]["slug"])}.html">← {E(DATA[i-1]["letter"])}</a>' + nav
    if i + 1 < len(DATA):
        nav += f'<a href="{E(DATA[i+1]["slug"])}.html">{E(DATA[i+1]["letter"])} →</a>'

    words = ''.join(
        f'<div class="word"><div class="emoji">{E(w["emoji"])}</div><b>{E(w["word"])}</b><small>{E(d["letter"])} for {E(w["word"])}</small></div>'
        for w in d['words']
    )

    quiz = ''
    for n, q in enumerate(d['quiz'], 1):
        opts = ''.join(
            f'<button class="answer" type="button" onclick="answer(this,{str(o == q["answer"]).lower()})">{E(o)}</button>'
            for o in q['options']
        )
        quiz += f'<div class="q"><p><b>Question {n}:</b> {E(q["question"])}</p><div class="answers">{opts}</div><div class="feedback"></div></div>'

    vals = {
        'TITLE': E(d['title']), 'DESCRIPTION': E(d['description']),
        'LETTER': E(d['letter']), 'SMALL': E(d['small']),
        'MAIN_WORD': E(d['main_word']), 'INTRO': E(d['intro']),
        'EMOJI': E(d['main_emoji']), 'NAV': nav, 'WORDS': words,
        'QUIZ': quiz, 'SLUG': E(d['slug'])
    }
    page = TEMPLATE
    for k, v in vals.items():
        page = page.replace('{{' + k + '}}', v)
    (OUT / (d['slug'] + '.html')).write_text(page, encoding='utf-8')

cards = ''.join(
    f'<a class="word" href="pages/{E(d["slug"])}.html"><div class="emoji">{E(d["main_emoji"])}</div><b>{E(d["title"])}</b><small>Lesson {E(d["letter"])}</small></a>'
    for d in DATA
)

home = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Little Learner — Kids Learning</title><meta name="description" content="Fun, book-style learning lessons for kids with big visuals, tracing, voice practice and quizzes."><link rel="stylesheet" href="assets/style.css"></head><body>
<header class="site-header"><nav class="site-nav"><a class="brand" href="index.html"><span class="brand-icon">🌈</span> Little Learner</a><button class="menu-btn" onclick="toggleMenu()">☰</button></nav><div id="siteMenu" class="site-menu"><a href="index.html">🏠 Home</a><a href="alphabet.html">🔤 Alphabet</a><a href="numbers.html">🔢 Numbers</a><a href="colors.html">🎨 Colors</a><a href="animals.html">🐾 Animals</a><a href="about.html">ℹ️ About</a><a href="contact.html">✉️ Contact</a><a href="privacy.html">🔒 Privacy</a><a href="terms.html">📄 Terms</a></div></header>
<main class="wrap"><section class="hero"><div class="hero-icon">🌈</div><h1>Little Learner</h1><p>Learn, practice and have fun — one book-style lesson at a time.</p><div class="hero-actions"><a class="primary-btn" href="#alphabet">📚 Start Learning</a><a class="secondary-btn" href="alphabet.html">🔤 A–Z Lessons</a></div></section><section class="section" id="alphabet"><span class="eyebrow">BOOK 01</span><h2>🔤 Alphabet A–Z</h2><p>Big letters, simple words, tracing, voice practice and working quizzes.</p><div class="words">{cards}</div></section><section class="section"><h2>📖 Learn Like a Book</h2><p>Every lesson follows a clear learning flow: see the letter, learn the main word, explore vocabulary, trace, listen and take a quiz.</p></section></main>
<footer class="site-footer"><div class="footer-grid"><div><h3>🌈 Little Learner</h3><p>Learn, practice and have fun.</p></div><div><h3>Categories</h3><p><a href="alphabet.html">Alphabet</a><br><a href="numbers.html">Numbers</a><br><a href="colors.html">Colors</a><br><a href="animals.html">Animals</a></p></div><div><h3>Pages</h3><p><a href="about.html">About</a><br><a href="contact.html">Contact</a><br><a href="privacy.html">Privacy</a><br><a href="terms.html">Terms</a></p></div></div><div class="copyright">© 2026 Little Learner</div></footer><script src="assets/app.js"></script></body></html>'''
(ROOT / 'public/index.html').write_text(home, encoding='utf-8')
print('Generated', len(DATA), 'lesson pages plus the automated Home page.')
