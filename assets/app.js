(function(){
  "use strict";
  window.toggleMenu=function(){
    const menu=document.getElementById("siteMenu");
    if(!menu)return;
    menu.classList.toggle("open");
    const btn=document.querySelector(".menu-btn");
    if(btn)btn.setAttribute("aria-expanded",String(menu.classList.contains("open")));
  };
  window.speakText=function(text){
    if(!("speechSynthesis" in window)){alert("Voice reading is not supported in this browser.");return;}
    window.speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(text); u.rate=.88; u.pitch=1.05;
    window.speechSynthesis.speak(u);
  };
  window.speakCurrentBook=function(){const a=document.querySelector("[data-speak]");if(a)speakText(a.getAttribute("data-speak"));};
  window.answerBook=function(button,correct,quizId){
    const box=document.getElementById(quizId); if(!box||box.dataset.done==="1")return;
    const feedback=box.querySelector(".feedback"), score=box.querySelector(".score-value");
    if(correct){box.dataset.done="1";button.classList.add("correct");if(score)score.textContent="1";if(feedback)feedback.textContent="✓ Correct! Great thinking.";box.querySelectorAll(".answer").forEach(b=>b.disabled=true);}
    else{button.classList.add("wrong");if(feedback)feedback.textContent="Not quite — look at the lesson and try again.";setTimeout(()=>button.classList.remove("wrong"),450);}
  };
  window.resetBookQuiz=function(quizId){
    const box=document.getElementById(quizId);if(!box)return;box.dataset.done="0";
    box.querySelectorAll(".answer").forEach(b=>{b.disabled=false;b.classList.remove("correct","wrong");});
    const f=box.querySelector(".feedback");if(f)f.textContent="";const s=box.querySelector(".score-value");if(s)s.textContent="0";
  };
  document.addEventListener("click",e=>{if(e.target.closest(".site-menu a")){const m=document.getElementById("siteMenu");if(m)m.classList.remove("open");}});
})();