import json,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]; D=json.loads((R/"content/lessons.json").read_text(encoding="utf-8")); T=(R/"templates/lesson.html").read_text(encoding="utf-8"); O=R/"public/pages"; O.mkdir(parents=True,exist_ok=True)
E=lambda x:html.escape(str(x),quote=True)
for i,d in enumerate(D):
    nav='<a href="../index.html">🏠 Home</a>'
    if i: nav=f'<a href="{E(D[i-1]["slug"])}.html">← {E(D[i-1]["letter"])}</a>'+nav
    if i+1<len(D): nav+=f'<a href="{E(D[i+1]["slug"])}.html">{E(D[i+1]["letter"])} →</a>'
    words=''.join(f'<div class="word"><div class="emoji">{E(w["emoji"])}</div><b>{E(w["word"])}</b><div>{E(d["letter"])} for {E(w["word"])}</div></div>' for w in d["words"])
    quiz=''
    for n,q in enumerate(d["quiz"],1):
        opts=''.join(f'<button class="answer" onclick="answer(this,{str(o==q["answer"]).lower()})">{E(o)}</button>' for o in q["options"])
        quiz+=f'<div class="q"><p><b>Question {n}:</b> {E(q["question"])}</p><div class="answers">{opts}</div><div class="feedback"></div></div>'
    vals={"TITLE":E(d["title"]),"DESCRIPTION":E(d["description"]),"LETTER":E(d["letter"]),"SMALL":E(d["small"]),"MAIN_WORD":E(d["main_word"]),"INTRO":E(d["intro"]),"EMOJI":E(d["main_emoji"]),"NAV":nav,"WORDS":words,"QUIZ":quiz,"SLUG":E(d["slug"])}
    page=T
    for k,v in vals.items(): page=page.replace("{{"+k+"}}",v)
    (O/(d["slug"]+".html")).write_text(page,encoding="utf-8")
cards=''.join(f'<a class="word" href="pages/{E(d["slug"])}.html"><div class="emoji">{E(d["main_emoji"])}</div><b>{E(d["title"])}</b><div>Learn letter {E(d["letter"])}</div></a>' for d in D)
(R/"public/index.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kids Learning A-Z</title><meta name="description" content="Interactive alphabet lessons for kids."><link rel="stylesheet" href="assets/style.css"></head><body><main class="wrap"><section class="hero"><h1>🌈 Kids Learning A-Z</h1><p>Learn letters with big visuals, tracing, voice practice and working quizzes.</p></section><section class="section"><h2>🔤 Choose a Lesson</h2><div class="words">{cards}</div></section></main><footer>Kids Learning</footer></body></html>',encoding="utf-8")
print("Generated",len(D),"pages")
