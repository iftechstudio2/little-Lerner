import json, html, re, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/"public"
OUTPUTS=[ROOT, PUBLIC]
CONTENT=ROOT/"content"
SITE=json.loads((CONTENT/"site.json").read_text(encoding="utf-8"))
LIB=json.loads((CONTENT/"library.json").read_text(encoding="utf-8"))
LESSONS=json.loads((CONTENT/"lessons.json").read_text(encoding="utf-8"))

E=lambda x:html.escape(str(x),quote=True)

def slug(s):
    s=s.lower().replace("–","-").replace("&","and")
    s=re.sub(r"[^a-z0-9]+","-",s).strip("-")
    return s or "page"

def category_intro(c):
    return {
      "preschool-reading":"Build early reading confidence with short, picture-friendly lessons that connect spoken words, letters and simple meaning.",
      "kids-stories":"Read a short story, notice what happens, talk about the idea and complete a small activity.",
      "kids-quizzes":"Use quick questions to recall what you know, explain your thinking and practice again.",
      "alphabet-phonics":"Explore letters, beginning sounds, letter forms and simple word-building activities.",
      "numbers-math":"Practice counting, comparing, number recognition and early mathematical thinking.",
      "colors-shapes":"Notice colors and shapes in everyday objects and use them to describe the world.",
      "animals-nature":"Learn names, features and simple observations about animals and the natural world.",
      "writing-tracing":"Strengthen pencil control through lines, curves, tracing and early writing practice.",
      "brain-thinking":"Slow down, compare clues, notice patterns and explain how you reached an answer.",
      "rhymes-sounds":"Use rhythm, repetition and listening games to make language practice memorable.",
      "vocabulary":"Learn useful words in context, say them aloud and use them in short sentences.",
      "world-around-me":"Connect learning to people, places, routines and familiar parts of everyday life.",
      "healthy-habits":"Learn practical vocabulary and routines that help children talk about healthy everyday choices.",
      "feelings-social":"Build language for emotions, kindness, sharing, turn-taking and respectful communication.",
      "safety-skills":"Practice simple everyday safety ideas with a parent or teacher and connect them to real situations.",
      "little-science":"Ask a question, notice a change, make a simple observation and explain what you discovered.",
      "creative-learning":"Use shapes, colors, stories and imagination to create something of your own.",
      "digital-skills":"Learn basic technology vocabulary and safe, age-appropriate device habits with adult guidance.",
      "daily-practice":"Use short focused sessions to build consistency without making learning feel overwhelming.",
      "learning-challenges":"Review a skill through small, achievable challenges that reward effort and careful thinking.",
      "practice-packs":"Work through focused practice activities online, then continue on paper when useful."
    }.get(c["id"],c["description"])

def default_book(c,b):
    t=b
    cid=c["id"]
    if cid=="kids-stories":
        lesson=f"{t} is a short story designed to help children notice characters, actions and a simple idea. Read it slowly, pause at important moments, and ask what might happen next."
        activity="Retell the beginning, middle and ending in your own words. Then draw one moment from the story and explain why you chose it."
        remember="Good readers do more than repeat words: they notice what happened and explain their thinking."
        q=("What is a useful way to understand a short story?",["Notice what happens and explain it","Skip the story","Only read the title"],0)
    elif cid=="numbers-math":
        lesson=f"In {t}, practice one small number skill at a time. Touch or point to each object, say the numbers clearly, and check your count instead of rushing."
        activity="Use five to ten safe everyday objects. Count them, group them, then describe which group has more, fewer or the same when appropriate."
        remember="Careful counting means matching one number word to one object and checking your result."
        q=("What helps careful counting?",["Touching or pointing to each object once","Counting as fast as possible","Skipping objects"],0)
    elif cid in ("alphabet-phonics","preschool-reading","writing-tracing","vocabulary"):
        lesson=f"{t} helps build early language and reading skills. Say each important word aloud, notice its first sound or letters, and connect the word to something familiar."
        activity="Choose three examples from the lesson. Say each one, spell or trace what you can, and use one example in a short sentence."
        remember="New words become easier to remember when children hear them, see them and use them."
        q=("What can help you learn a new word?",["Hear it, see it and use it","Never say it","Only look at the title"],0)
    elif cid=="colors-shapes":
        lesson=f"Use {t} to practice noticing visual features. Look carefully at an object and describe its color, shape, size or position before choosing an answer."
        activity="Find three safe objects nearby. Describe one color and one shape for each, then compare two of them."
        remember="Looking carefully and describing one feature at a time makes visual learning easier."
        q=("What is a useful first step in visual learning?",["Look carefully at the features","Guess without looking","Ignore the object"],0)
    elif cid=="animals-nature":
        lesson=f"{t} invites children to observe living things and learn useful words. Talk about what an animal or natural object looks like, where it may be found and what makes it interesting."
        activity="Choose one example from the lesson. Draw it, name two features and tell an adult one question you still have."
        remember="Observation starts with noticing details and asking simple questions."
        q=("What is a good observation habit?",["Notice details and ask questions","Make up details without looking","Stop after the title"],0)
    elif cid=="brain-thinking":
        lesson=f"{t} is about careful thinking. Compare the clues, look for a pattern or relationship, and explain why your choice makes sense."
        activity="Solve the activity twice. The second time, say your reasoning out loud before choosing the answer."
        remember="Strong problem solving includes both an answer and a reason."
        q=("What should you do before choosing an answer?",["Compare the clues","Choose randomly","Ignore the instructions"],0)
    elif cid=="healthy-habits":
        lesson=f"{t} turns an everyday routine into a learning opportunity. Learn the key words, put the steps in a sensible order and discuss why the routine matters."
        activity="With a parent or teacher, describe the routine as three simple steps. Put them in order and practice saying them."
        remember="A routine is easier to follow when its steps are clear and repeatable."
        q=("What makes an everyday routine easier to follow?",["Clear steps in a sensible order","Changing every step randomly","Skipping the instructions"],0)
    elif cid=="feelings-social":
        lesson=f"{t} gives children language for everyday social situations. Notice the feeling or social problem, name it respectfully and think of a helpful next step."
        activity="Act out one simple situation with an adult. Name the feeling, listen to the other person and suggest a kind next step."
        remember="Naming feelings and listening carefully can make communication clearer."
        q=("What is a helpful social skill?",["Listen and explain feelings respectfully","Interrupt everyone","Hide every feeling"],0)
    elif cid=="safety-skills":
        lesson=f"{t} introduces a simple safety idea for everyday life. Real-world safety rules should always be practiced with a trusted adult and followed according to local guidance."
        activity="Ask a parent or teacher to show you the safe way to handle the situation described in the book. Repeat the key steps aloud."
        remember="Safety learning should connect clear steps with real adult guidance."
        q=("How should children practice safety skills?",["With trusted adult guidance","By guessing in a dangerous situation","By ignoring safety rules"],0)
    elif cid=="little-science":
        lesson=f"{t} encourages curiosity. Start with what you can observe, describe what changed or what you notice, and ask a simple question about why it happens."
        activity="Make one safe observation with an adult. Draw what you saw and complete the sentence: 'I noticed ___, and I wonder ___.'"
        remember="Science begins with careful observation, questions and evidence."
        q=("What is a useful science habit?",["Observe and ask questions","Guess without observing","Avoid questions"],0)
    elif cid=="creative-learning":
        lesson=f"{t} gives you a starting point, not a single correct answer. Use the prompt to make something, then explain one choice you made and one thing you would change."
        activity="Create your own version using simple shapes, colors or words. Give it a title and tell an adult about one creative choice."
        remember="Creative learning values ideas, choices and reflection."
        q=("What is important in a creative activity?",["Make choices and explain your ideas","Copy without thinking","Avoid trying new ideas"],0)
    elif cid=="digital-skills":
        lesson=f"{t} introduces one basic digital idea in a child-friendly way. Use devices with adult guidance, protect personal information and take regular breaks."
        activity="With an adult, practice the skill on a safe device. Then explain what the button, key or action does before trying it again."
        remember="Digital skills include both using technology and using it safely."
        q=("What should children do when learning digital skills?",["Use devices with adult guidance","Share private information","Skip safety guidance"],0)
    elif cid=="daily-practice":
        lesson=f"{t} is designed for a short, focused practice session. Pick one small goal, work carefully, check your effort and stop for a break when needed."
        activity="Set a short timer with an adult. Complete the activity without rushing, then say one thing you improved."
        remember="Small, consistent practice can build confidence over time."
        q=("What is a good daily-practice goal?",["One small skill done carefully","Doing everything at once","Rushing through tasks"],0)
    elif cid=="learning-challenges":
        lesson=f"{t} turns review into a small challenge. Read the instructions, try each part carefully and use mistakes as clues for another attempt."
        activity="Complete the challenge once, then repeat only the part that was difficult. Explain what changed on your second try."
        remember="A challenge is useful when it helps you practice and learn from mistakes."
        q=("What can a mistake provide?",["A clue for another attempt","A reason to stop forever","No information"],0)
    elif cid=="practice-packs":
        lesson=f"{t} breaks practice into small repeatable tasks. Start with a simple example, check your work and then try a new example without copying."
        activity="Complete three short practice items. Circle the one that felt easiest and tell an adult why."
        remember="Practice works best when you repeat a skill with small changes."
        q=("How should practice progress?",["Repeat the skill with small changes","Copy one answer forever","Never check your work"],0)
    elif cid=="rhymes-sounds":
        lesson=f"{t} uses rhythm, sound and repetition to strengthen listening and language. Say the words slowly first, then add the rhythm when the words feel familiar."
        activity="Repeat the sound pattern three times. Then change one word or action and see whether you can keep the rhythm."
        remember="Listening carefully helps children notice order, rhythm and repeated sounds."
        q=("What skill do sound activities practice?",["Listening carefully","Only drawing","Only counting"],0)
    else:
        lesson=f"{t} is a focused learning book from the {c['title']} shelf. Learn one idea at a time, connect it to something familiar, and explain what you noticed."
        activity="Choose one idea from the lesson. Try it with a parent or teacher, then explain what you did and what you learned."
        remember="Learning becomes stronger when you explore, practice and explain."
        q=("What is a useful learning habit?",["Explore, practice and explain","Skip the activity","Stop after the title"],0)
    return {"icon":c["icon"],"summary":c["description"],"lesson":lesson,"activity":activity,"remember":remember,"quiz":[{"question":q[0],"options":q[1],"answer":q[2]}]}

def shell(title,desc,body,root=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{root}assets/style.css"></head><body><header class="site-header"><div class="site-nav"><a class="brand" href="{root}index.html"><span class="brand-icon">🌈</span><span>Little Learner</span></a><button class="menu-btn" type="button" onclick="toggleMenu()" aria-label="Open navigation" aria-expanded="false">☰</button></div><nav id="siteMenu" class="site-menu"><a href="{root}index.html">🏠 Home</a><a href="{root}index.html#categories">📚 Categories</a><a href="{root}about.html">ℹ️ About</a><a href="{root}contact.html">✉️ Contact</a><a href="{root}privacy.html">🔒 Privacy</a><a href="{root}terms.html">📄 Terms</a></nav></header>{body}<footer class="site-footer"><div class="footer-grid"><div><h3>🌈 Little Learner</h3><p>Learn, practice and have fun.</p></div><div><h3>Explore</h3><p><a href="{root}index.html#categories">Categories</a><br><a href="{root}alphabet.html">Alphabet</a></p></div><div><h3>Parents</h3><p><a href="{root}about.html">About</a><br><a href="{root}contact.html">Contact</a><br><a href="{root}privacy.html">Privacy</a><br><a href="{root}terms.html">Terms</a></p></div></div><div class="copyright">© {SITE.get("year",2026)} Little Learner</div></footer><script src="{root}assets/app.js"></script></body></html>'''

def write(rel,content):
    for out in OUTPUTS:
        p=out/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content,encoding="utf-8")

# clean generated output only; source files remain untouched
# The repository root is the GitHub Pages publishing source. Remove only old generated/legacy site output.
for rel in ["index.html","category.html","book.html","about.html","contact.html","privacy.html","terms.html","alphabet.html","numbers.html","colors.html","animals.html","pages"]:
    p=ROOT/rel
    if p.is_dir(): shutil.rmtree(p)
    elif p.exists(): p.unlink()
if PUBLIC.exists():
    for p in list(PUBLIC.iterdir()):
        if p.name!=".gitkeep":
            if p.is_dir(): shutil.rmtree(p)
            else: p.unlink()
PUBLIC.mkdir(parents=True,exist_ok=True)
(PUBLIC/"assets").mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/"assets/style.css",PUBLIC/"assets/style.css")
shutil.copy2(ROOT/"assets/app.js",PUBLIC/"assets/app.js")

cat_links=[]
book_links=[]
for ci,c in enumerate(LIB["categories"]):
    cat_slug=slug(c["id"])
    cards=[]
    for bi,title in enumerate(c["books"]):
        bslug=slug(title)
        data=default_book(c,title)
        href=f"books/{bslug}.html"
        cards.append(f'<a class="book-card" href="../{href}"><span class="cover">{E(data["icon"])}</span><span><small>BOOK {bi+1:02d}</small><b>{E(title)}</b><em>{E(c["description"])}</em></span></a>')
        book_links.append((href,title,c["title"],data))
    body=f'<main><section class="page-hero wrap"><a class="back-link" href="../index.html#categories">← All categories</a><div class="hero-copy"><span class="hero-icon">{E(c["icon"])}</span><span><span class="eyebrow">LEARNING SHELF {ci+1:02d}</span><h1>{E(c["title"])}</h1><p>{E(category_intro(c))}</p></span></div></section><section class="wrap section"><div class="section-title"><span class="eyebrow">BOOKS IN THIS SHELF</span><h2>{len(c["books"])} learning books</h2><p>Open any book for a complete lesson, activity, read-aloud option and quiz.</p></div><div class="book-grid">{"".join(cards)}</div></section></main>'
    write(f"categories/{cat_slug}/index.html",shell(c["title"]+" — Little Learner",c["description"],body,"../../"))
    cat_links.append((f"categories/{cat_slug}/index.html",c))

for href,title,cat_title,data in book_links:
    quiz=data["quiz"][0];qid="quiz-"+slug(title)
    options="".join(f'<button class="answer" type="button" onclick="answerBook(this,{str(i==quiz["answer"]).lower()},"{qid}")">{E(o)}</button>' for i,o in enumerate(quiz["options"]))
    text=f"{title}. {data['lesson']} {data['remember']}"
    body=f'''<main class="book-page wrap"><div class="book-topbar"><a class="back-link" href="../categories/{slug(next(c for c in LIB["categories"] if c["title"]==cat_title)["id"])}/">← Back to shelf</a><span class="book-badge">📚 {E(cat_title)}</span></div><article class="complete-book" data-speak="{E(text)}"><div class="big-book-cover"><span>{E(data["icon"])}</span><small>{E(cat_title)}</small><b>{E(title)}</b></div><div class="book-intro"><span class="eyebrow">DIGITAL LEARNING BOOK</span><h1>{E(title)}</h1><p class="book-lead">{E(data["summary"])}</p></div><section class="lesson-block"><span class="eyebrow">STEP 1</span><h2>📖 Let’s Learn</h2><div class="story-visual">{E(data["icon"])}</div><p>{E(data["lesson"])}</p></section><section class="lesson-block"><span class="eyebrow">STEP 2</span><h2>🧩 Try It Yourself</h2><div class="activity-card"><b>🎯 Your mission</b><p>{E(data["activity"])}</p></div></section><section class="lesson-block"><span class="eyebrow">STEP 3</span><h2>🗣️ Say It & Remember It</h2><p>{E(data["remember"])}</p><button class="speak" type="button" onclick="speakCurrentBook()">🔊 Read Aloud</button></section><section class="lesson-block quiz" id="{qid}"><span class="eyebrow">STEP 4</span><h2>⭐ Quick Check</h2><div class="q"><p><b>{E(quiz["question"])}</b></p><div class="answers">{options}</div><div class="feedback" aria-live="polite"></div></div><div class="score">Score: <span class="score-value">0</span> / 1</div><button class="retry" type="button" onclick="resetBookQuiz('{qid}')">🔄 Try Again</button></section><div class="finish-box">🎉 <h2>Great job, Little Learner!</h2><p>You finished this book. Practice again whenever you like.</p></div></article></main>'''
    write(href,shell(title+" — Little Learner",data["summary"],body,"../"))

# Home
catcards="".join(f'<a class="cat-card" href="{E("categories/"+slug(c["id"])+"/")}"><span>{E(c["icon"])}</span><b>{E(c["title"])}</b><small>{E(c["description"])}</small></a>' for c in LIB["categories"])
lesson_cards="".join(f'<a class="mini-card" href="pages/{E(d["slug"])}.html"><span>{E(d["main_emoji"])}</span><b>{E(d["title"])}</b><small>Letter {E(d["letter"])}</small></a>' for d in LESSONS)
home_body=f'''<main><section class="hero-home"><div class="hero-content"><span class="welcome-pill">🌟 A happy place to learn</span><h1>Little Learner</h1><p class="hero-lead">{E(SITE["description"])}</p><div class="hero-actions"><a class="primary-btn" href="#categories">📚 Explore Categories</a><a class="secondary-btn" href="alphabet.html">🔤 Start with A–Z</a></div><div class="trust-row"><span>👨‍👩‍👧 Parent-friendly</span><span>📱 Responsive</span><span>🧩 Learn by doing</span></div></div></section><section id="categories" class="library-shell"><div class="wrap"><div class="section-title center"><span class="eyebrow">DIGITAL EDUCATION LIBRARY</span><h2>📚 Choose a Learning Category</h2><p>Every shelf has complete book pages. Adding a book only requires content data; the design is generated automatically.</p></div><div class="category-grid">{catcards}</div></div></section><section class="wrap section"><div class="section-title"><span class="eyebrow">A–Z FOUNDATION</span><h2>🔤 Alphabet Lessons</h2><p>Start with 26 static, indexable letter lessons.</p></div><div class="mini-grid">{lesson_cards}</div></section><section class="parent-section wrap"><div class="parent-box"><div class="parent-icon">👨‍👩‍👧‍👦</div><div><span class="eyebrow">FOR PARENTS</span><h2>One content system, thousands of pages</h2><p>Content lives in structured files. The builder creates the pages, links, metadata, sitemap and navigation automatically, so you do not have to edit HTML for every new book.</p></div></div></section></main>'''
write("index.html",shell("Little Learner — Kids Digital Learning Library",SITE["description"],home_body))

# A-Z hub
azbody=f'<main><section class="page-hero wrap"><div class="hero-copy"><span class="hero-icon">🔤</span><span><span class="eyebrow">FOUNDATION</span><h1>Alphabet A–Z</h1><p>Learn letters with visuals, vocabulary, tracing, voice practice and quizzes.</p></span></div></section><section class="wrap section"><div class="mini-grid">{"".join(f"""<a class="mini-card" href="pages/{E(d["slug"])}.html"><span>{E(d["main_emoji"])}</span><b>{E(d["title"])}</b><small>Letter {E(d["letter"])}</small></a>""" for d in LESSONS)}</div></section></main>'
write("alphabet.html",shell("Alphabet A–Z — Little Learner","Interactive alphabet lessons for kids.",azbody))

# Simple informative pages
about='<main class="wrap section"><div class="page-card"><span class="hero-icon">📖</span><h1>About Little Learner</h1><p>Little Learner is a static educational library built around short lessons, activities, practice and quick checks for young learners.</p><h2>How it works</h2><p>Each page is generated from structured content and a shared design system. This keeps navigation and design consistent as the library grows.</p></div></main>'
contact='<main class="wrap section"><div class="page-card"><span class="hero-icon">✉️</span><h1>Contact</h1><p>For corrections, suggestions or content questions, add the project’s real contact email before publishing this page.</p></div></main>'
privacy='<main class="wrap section"><div class="page-card"><span class="hero-icon">🔒</span><h1>Privacy Policy</h1><p>This page is a site-specific template. Before advertising or analytics are enabled, replace this text with a policy that accurately describes the data, cookies, services and contact method actually used by the site.</p></div></main>'
terms='<main class="wrap section"><div class="page-card"><span class="hero-icon">📄</span><h1>Terms of Use</h1><p>Use this site for general educational practice. Parents and guardians should supervise age-appropriate activities and verify real-world safety guidance.</p></div></main>'
for fn,title,desc,body in [("about.html","About | Little Learner","About Little Learner educational lessons.",about),("contact.html","Contact | Little Learner","Contact Little Learner.",contact),("privacy.html","Privacy Policy | Little Learner","Privacy policy for Little Learner.",privacy),("terms.html","Terms of Use | Little Learner","Terms for using Little Learner.",terms)]:
    write(fn,shell(title,desc,body))

write("404.html",shell("Page Not Found — Little Learner","The page you requested could not be found.",'<main class="wrap section"><div class="page-card"><span class="hero-icon">🔎</span><h1>Page not found</h1><p>That page does not exist or may have moved.</p><a class="primary-btn" href="index.html">Back to Little Learner</a></div></main>'))

# Sitemap: only emit when a real base URL is configured.
base=SITE.get("base_url","").rstrip("/")
if base:
    urls=[f"{base}/",f"{base}/alphabet.html",f"{base}/about.html",f"{base}/contact.html",f"{base}/privacy.html",f"{base}/terms.html"]
    urls += [f"{base}/{x[0]}" for x,_ in cat_links]
    urls += [f"{base}/{x[0]}" for x in book_links]
    urls += [f"{base}/pages/{d['slug']}.html" for d in LESSONS]
    xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f"<url><loc>{E(u)}</loc></url>" for u in urls)+"</urlset>"
    write("sitemap.xml",xml)
write("robots.txt","User-agent: *\nAllow: /\n"+(f"Sitemap: {base}/sitemap.xml\n" if base else ""))
print(f"Generated {len(book_links)} book pages, {len(cat_links)} category pages, {len(LESSONS)} lesson pages and core pages.")
