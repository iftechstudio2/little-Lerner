const libraryData=[
['📖','Preschool Reading Books','First books for little readers',['My First Alphabet Book','ABC Picture Words','First Reading Words','Read With Pictures']],
['🌙','Kids Story Books','Short stories with gentle learning moments',['The Little Garden','The Helpful Little Bird','A Day at the Park','The Lost Toy']],
['🧩','Kids Quiz Books','Quick questions for practice and recall',['ABC Quiz Book','First Words Quiz','Numbers Quiz','Picture Quiz Book']],
['🔤','Alphabet & Phonics','Letters, sounds and early word building',['A–Z Letter Book','Capital & Small Letters','Letter Sound Practice','Beginning Sounds']],
['🔢','Numbers & Early Math','Counting and early number skills',['My First Numbers','Counting Book','Number Tracing','More or Less']],
['🎨','Colors & Shapes','Visual learning through colors and shapes',['My First Colors','Color Hunt','My First Shapes','Shapes Around Us']],
['🐾','Animals & Nature','Vocabulary from the world around us',['Animal ABC','Farm Animals','Wild Animals','Nature Words']],
['✏️','Writing & Tracing','Early pencil and handwriting practice',['ABC Tracing','Number Tracing','Lines & Curves','First Writing Words']],
['🧠','Brain Games & Thinking','Observation, matching and simple reasoning',['Find the Match','Odd One Out','What Comes Next?','Memory Challenge']],
['🎵','Rhymes, Songs & Sounds','Playful language and listening activities',['ABC Song Book','Counting Rhymes','Animal Sounds','Action Songs']],
['🗣️','Vocabulary Builder','Useful everyday words for young learners',['My First 50 Words','Food Words','Home Words','School Words']],
['🌍','World Around Me','Familiar people, places and everyday life',['My Family','My Home','My Community','My Neighborhood']],
['🍎','Food & Healthy Habits','Food vocabulary and healthy routines',['Healthy Foods','My Healthy Day','Clean Hands','Brush Your Teeth']],
['😊','Feelings & Social Skills','Emotions, sharing, kindness and routines',['My Feelings','Kind Words','Sharing Is Caring','Taking Turns']],
['🛡️','Safety & Everyday Skills','Age-appropriate safety and independence topics',['Road Safety','Safe at Home','Emergency Helpers','My Daily Routine']],
['🔬','Little Science','Curiosity-driven introductions to the world',['Day & Night','Weather','Plants Grow','Animal Homes']],
['🎭','Creative Learning','Drawing, imagination and creative prompts',['Draw With Shapes','Color & Create','Finish the Picture','Imagine & Tell']],
['💻','Digital Learning Skills','Simple parent-guided technology concepts',['Mouse Basics','Keyboard Letters','Screen Smart','Digital Vocabulary']],
['📅','Daily Learning Practice','Short activities for a consistent routine',['5-Minute Letter Practice','5-Minute Number Practice','Picture Review','Daily Word Builder']],
['🏆','Learning Challenges','Small challenges that make practice exciting',['ABC Challenge','Counting Challenge','Shape Challenge','Word Challenge']],
['📝','Printable-Style Practice','Clean practice sheets recreated for the web',['Letter Practice Pack','Number Practice Pack','Word Practice Pack','Mixed Skills Pack']]
];

function renderLibrary(){const rail=document.getElementById('categoryRail'),grid=document.getElementById('libraryGrid');if(!rail||!grid)return;rail.innerHTML=libraryData.map((c,i)=>`<a class="cat-pill" href="#cat-${i+1}"><span>${c[0]}</span><b>${i+1}. ${c[1]}</b></a>`).join('');grid.innerHTML=libraryData.map((c,i)=>`<article class="library-card" id="cat-${i+1}"><div class="library-card-top"><div class="shelf-icon">${c[0]}</div><div><span class="cat-no">SHELF ${String(i+1).padStart(2,'0')}</span><h3>${c[1]}</h3><p>${c[2]}</p></div></div><div class="book-grid">${c[3].map((b,j)=>`<a class="book-card" href="#book-${i+1}-${j+1}" onclick="openBook(event,'${b.replace(/'/g,"\\'")}')"><span class="book-cover">${['📘','📗','📙','📕'][j]}</span><span><b>${b}</b><small>Open learning book</small></span><strong>›</strong></a>`).join('')}</div><a class="back-top" href="#library">↑ Back to shelves</a></article>`).join('')}
function openBook(e,name){e.preventDefault();let old=document.querySelector('.book-toast');if(old)old.remove();let t=document.createElement('div');t.className='book-toast';t.innerHTML=`<div>📚</div><b>${name}</b><span>This learning book is ready to be expanded with lessons, activities and practice.</span><button onclick="this.parentElement.remove()">Got it</button>`;document.body.appendChild(t);setTimeout(()=>t.classList.add('show'),10)}
function toggleMenu(){const m=document.getElementById('siteMenu');if(m)m.classList.toggle('open')}
function speakText(t){if('speechSynthesis'in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=.82;u.pitch=1.05;speechSynthesis.speak(u)}else alert('Voice is not supported in this browser.')}
function answer(btn,ok){const q=btn.closest('.q');if(!q||q.dataset.done==='1')return;const quiz=btn.closest('.quiz'),f=q.querySelector('.feedback');if(ok){q.dataset.done='1';f.textContent='🎉 Correct! Great job!';f.style.color='#2e7d32';q.querySelectorAll('button').forEach(b=>{b.disabled=true;b.style.opacity='.6'});const s=quiz.querySelector('.score span')||quiz.querySelector('.score'),n=parseInt(s.textContent)||0;s.textContent=n+1}else{f.textContent='❌ Try Again! You can do it!';f.style.color='#d32f2f'}}
function resetQuiz(id){const q=document.getElementById(id);if(!q)return;q.querySelectorAll('.q').forEach(x=>{delete x.dataset.done;x.querySelector('.feedback').textContent='';x.querySelectorAll('button').forEach(b=>{b.disabled=false;b.style.opacity='1'})});const s=q.querySelector('.score span')||q.querySelector('.score');s.textContent='0'}
document.addEventListener('DOMContentLoaded',()=>{renderLibrary();document.querySelectorAll('#siteMenu a').forEach(a=>a.addEventListener('click',()=>{document.getElementById('siteMenu')?.classList.remove('open')}))});