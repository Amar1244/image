<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dr. Batra's — Meta Creative Hub | Full Rich Cards + Save to Library</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:#f5f4f0;color:#1A1A1A;padding:24px;min-height:100vh}
.hub{max-width:1000px;margin:0 auto}
.top-bar{background:#0F6E56;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.5rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap}
.top-bar-left h1{font-size:18px;font-weight:500;color:#E1F5EE;margin-bottom:2px}
.top-bar-left p{font-size:12px;color:#9FE1CB}
.tab-row{display:flex;gap:0;margin-bottom:1.25rem;border:1px solid #d3d1c7;border-radius:8px;overflow:hidden;width:fit-content}
.tab{padding:7px 18px;font-size:13px;font-weight:500;cursor:pointer;color:#5F5E5A;background:#fff;border:none}
.tab:hover{background:#f1efe8}
.tab.active{background:#0F6E56;color:#E1F5EE}
.section-panel{display:none}
.section-panel.visible{display:block}
.library-header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:1rem}
.library-dropdown{background:#fff;border:1px solid #b4b2a9;border-radius:8px;padding:6px 12px;font-size:13px;cursor:pointer}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1rem;align-items:center}
.fl{font-size:11px;color:#5F5E5A;font-weight:500}
.pill{font-size:12px;padding:5px 11px;border-radius:20px;cursor:pointer;border:1px solid #b4b2a9;background:#fff;color:#5F5E5A}
.pill:hover{background:#f1efe8}
.pill.f-active{background:#0F6E56;color:#E1F5EE;border-color:#0F6E56}
.pill.h-active{background:#534AB7;color:#EEEDFE;border-color:#534AB7}
.pill.a-active{background:#185FA5;color:#E6F1FB;border-color:#185FA5}
.vdiv{width:1px;height:18px;background:#d3d1c7;margin:0 2px}
.count-bar{font-size:12px;color:#5F5E5A;margin-bottom:1rem;padding-bottom:.625rem;border-bottom:1px solid #e8e8e8}
/* RICH CARD DESIGN - exact match to screenshot */
.card{background:#fff;border:1px solid #d3d1c7;border-radius:12px;margin-bottom:.875rem;overflow:hidden}
.card-hdr{padding:.75rem 1.125rem;display:flex;align-items:flex-start;gap:10px;cursor:pointer;user-select:none}
.card-hdr:hover{background:#f1efe8}
.cid{font-size:11px;font-weight:500;padding:3px 8px;border-radius:4px;white-space:nowrap;margin-top:1px}
.ctitle{font-size:14px;font-weight:500;color:#1A1A1A;flex:1}
.cmeta{display:flex;gap:5px;flex-wrap:wrap;margin-top:3px}
.badge{font-size:11px;padding:2px 7px;border-radius:3px;font-weight:500}
.chev{font-size:15px;color:#888780;transition:transform .2s;line-height:1}
.card-body{display:none;border-top:1px solid #e8e8e8}
.card-body.open{display:block}
.csec{padding:.875rem 1.125rem;border-bottom:1px solid #e8e8e8}
.csec:last-child{border-bottom:none}
.slabel{font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem;color:#5F5E5A}
.img-box{background:#E1F5EE;border-radius:8px;padding:.625rem .875rem;border-left:3px solid #0F6E56;margin-bottom:.75rem}
.open-box{background:#FAEEDA;border-radius:8px;padding:.625rem .875rem;border-left:3px solid #854F0B;margin-bottom:.75rem}
.cta-box{background:#E6F1FB;border-radius:8px;padding:.625rem .875rem}
.notes-box{background:#f1efe8;border-radius:8px;padding:.625rem .875rem}
.lgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.lbox{border-radius:8px;padding:.625rem .75rem;border:1px solid #d3d1c7}
.ltag{font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.ctext{font-size:13px;color:#1A1A1A;line-height:1.6;white-space:pre-wrap}
.cpybtn,.save-btn{font-size:11px;padding:3px 8px;border-radius:4px;cursor:pointer;border:1px solid #b4b2a9;background:#f1efe8;color:#5F5E5A;margin-top:.375rem;margin-right:6px;transition:all .15s}
.cpybtn:hover,.save-btn:hover{background:#fff}
.save-btn{background:#E6F1FB;border-color:#185FA5;color:#185FA5}
.topic-date{font-size:10px;color:#5F5E5A;margin-left:8px;font-weight:normal}
.no-results{text-align:center;padding:2.5rem 1rem;color:#5F5E5A;font-size:14px}
.gen-panel{background:#fff;border:1px solid #d3d1c7;border-radius:12px;padding:1.25rem 1.5rem}
.gen-title{font-size:15px;font-weight:500;margin-bottom:.25rem}
.gen-sub{font-size:13px;color:#5F5E5A;margin-bottom:1.25rem}
.gen-row{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:1.25rem;align-items:flex-end}
.gen-field{display:flex;flex-direction:column;gap:5px}
.gen-field label{font-size:12px;font-weight:500;color:#5F5E5A}
.gen-field select,.gen-field input[type=number],.gen-field input[type=text]{border-radius:8px;border:1px solid #b4b2a9;padding:7px 10px;font-size:13px}
.gen-btn{padding:8px 20px;border-radius:8px;border:none;background:#0F6E56;color:#fff;font-size:13px;font-weight:500;cursor:pointer}
.gen-btn:disabled{background:#d3d1c7;cursor:not-allowed}
.gen-output{margin-top:1.25rem}
.error-box{background:#FAECE7;border:1px solid #993C1D;border-radius:8px;padding:.75rem 1rem;color:#712B13;font-size:13px;margin-top:1rem}
.loading-dots{display:inline-flex;gap:4px;align-items:center}
.loading-dots span{width:6px;height:6px;background:#9FE1CB;border-radius:50%;animation:bounce .9s infinite}
.loading-dots span:nth-child(2){animation-delay:.15s}
.loading-dots span:nth-child(3){animation-delay:.3s}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-5px)}}
.assumption-note{background:#FAEEDA;border:1px solid #EF9F27;border-radius:8px;padding:.75rem 1rem;font-size:12px;color:#412402;margin-bottom:1.25rem}
.api-field,.topic-field{margin-bottom:1.25rem;padding:1rem;border-radius:8px}
.api-field{background:#f1efe8;border:1px solid #d3d1c7}
.topic-field{background:#E6F1FB;border:1px solid #185FA5}
.api-field label,.topic-field label{font-size:12px;font-weight:500;display:block;margin-bottom:5px}
.api-field input,.topic-field input{width:100%;border-radius:8px;border:1px solid #b4b2a9;padding:7px 10px;font-size:13px}
.api-note{font-size:11px;color:#888780;margin-top:4px}
</style>
</head>
<body>
<div class="hub">
<div class="top-bar">
  <div class="top-bar-left">
    <h1>Dr. Batra's — Meta Creative Hub</h1>
    <p>Full rich cards • Groq + LLaMA 70B • Bilingual EN/HI • Save to library</p>
  </div>
</div>

<div class="assumption-note">
  <strong>📚 RICH CARDS FULLY RESTORED!</strong> Each script includes Image text, Opening line, Full caption (EN/HI), Visual direction, Production note, Target audience. Generate new scripts and save them to your library.
</div>

<div class="tab-row">
  <button class="tab active" onclick="showTab('library',this)">Script library</button>
  <div class="tab-divider"></div>
  <button class="tab" onclick="showTab('generate',this)">Generate new scripts</button>
</div>

<div id="tab-library" class="section-panel visible">
  <div class="library-header">
    <select id="library-source" class="library-dropdown" onchange="switchLibrarySource()">
      <option value="prebuilt">📚 Pre-built scripts (default)</option>
      <option value="saved">💾 My saved scripts</option>
    </select>
  </div>
  <div class="filters">
    <span class="fl">Format</span>
    <span class="pill f-active" data-f="format" data-v="all" onclick="setF('format','all',this)">All</span>
    <span class="pill" data-f="format" data-v="static" onclick="setF('format','static',this)">Statics</span>
    <span class="pill" data-f="format" data-v="narrative" onclick="setF('format','narrative',this)">Narrative</span>
    <span class="pill" data-f="format" data-v="argument" onclick="setF('format','argument',this)">Argument</span>
    <span class="vdiv"></span>
    <span class="fl">Hook</span>
    <span class="pill h-active" data-f="hook" data-v="all" onclick="setF('hook','all',this)">All</span>
    <span class="pill" data-f="hook" data-v="pain" onclick="setF('hook','pain',this)">Pain</span>
    <span class="pill" data-f="hook" data-v="safety" onclick="setF('hook','safety',this)">Safety</span>
    <span class="pill" data-f="hook" data-v="trust" onclick="setF('hook','trust',this)">Trust</span>
    <span class="vdiv"></span>
    <span class="fl">Audience</span>
    <span class="pill a-active" data-f="audience" data-v="all" onclick="setF('audience','all',this)">All</span>
    <span class="pill" data-f="audience" data-v="cold" onclick="setF('audience','cold',this)">Cold</span>
    <span class="pill" data-f="audience" data-v="warm" onclick="setF('audience','warm',this)">Warm</span>
    <span class="pill" data-f="audience" data-v="retarget" onclick="setF('audience','retarget',this)">Retarget</span>
  </div>
  <div class="count-bar">Showing <strong id="cnt">0</strong> creatives</div>
  <div id="lib-cards"></div>
</div>

<div id="tab-generate" class="section-panel">
  <div class="gen-panel">
    <div class="gen-title">Generate new scripts — Groq + LLaMA 70B</div>
    <div class="gen-sub">Enter brand/topic + select filters → AI generates FULL rich bilingual ads (same format as library). Click SAVE to push to library with topic name + date.</div>
    <div class="api-field"><label>Groq API key</label><input type="password" id="api-key" placeholder="gsk_..."><div class="api-note">Free key from console.groq.com | LLaMA 70B versatile</div></div>
    <div class="topic-field"><label>📌 Brand / Name / Topic</label><input type="text" id="topic-name" placeholder="e.g., Dr. Batra's Homeopathy, Nike Running, Hair Growth Serum"></div>
    <div class="gen-row">
      <div class="gen-field"><label>Script type</label><select id="gen-type"><option value="static">Static ad</option></select></div>
      <div class="gen-field"><label>Hook angle</label><select id="gen-hook"><option value="pain">Pain — failed treatments</option><option value="safety">Safety — zero side effects</option><option value="speed">Speed — faster results</option><option value="trust">Trust — authority</option><option value="switcher">Switcher — upgrade</option><option value="delhi">Delhi-specific</option><option value="women">Women-specific</option></select></div>
      <div class="gen-field"><label>How many</label><input type="number" id="gen-count" value="2" min="1" max="3" style="width:80px"></div>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap"><button class="gen-btn" id="gen-btn" onclick="generateScripts()">Generate scripts</button><span id="gen-status" style="font-size:13px;color:#5F5E5A"></span></div>
    <div id="gen-output" class="gen-output"></div>
  </div>
</div>
</div>

<script>
// PREBUILT RICH SCRIPTS (matching screenshot style)
let PREBUILT = [
{id:'S01',type:'static',hook:'pain',audience:'cold',priority:'Launch first',title:'The Minoxidil trap',hookLabel:'Pain',
 imageEn:"It worked. Then it didn't.", imageHi:'Kaam kiya. Phir band ho gaya.',
 openEn:"Minoxidil worked. Then it stopped. And stopping made it worse. That's not failure — that's dependency.",
 openHi:'Minoxidil kaam kiya. Phir band ho gaya. Aur band karne pe baal aur girne lage. Yeh failure nahi — yeh dependency hai.',
 captionEn:"Minoxidil worked. Then it stopped. And stopping made it worse. That's not failure — that's dependency.\n\nMinoxidil doesn't treat why your hair is falling. It just delays it. At Dr. Batra's, we find the root cause — hormonal, nutritional, or stress-related — and treat it with homeopathy. Zero side effects. Pair it with XOGEN, our Korean exosome therapy, and get visible results in just 4–6 sessions. No Minoxidil. No dependency. No going back to square one.\n\nBook your free consultation today. Link in bio.",
 captionHi:"Minoxidil kaam kiya. Phir band ho gaya. Aur band karne pe baal aur girne lage. Yeh failure nahi — yeh dependency hai.\n\nMinoxidil aapke baalon ke girne ki wajah treat nahi karta. Sirf temporarily rokta hai. Dr. Batra's mein hum root cause dhundhte hain — aur homeopathy se treat karte hain. Zero side effects. XOGEN ke saath sirf 4–6 sessions mein visible results. Koi Minoxidil nahi. Koi dependency nahi.\n\nAaj hi free consultation book karein. Link bio mein.",
 cta:'Book Free Consultation / Free Consultation Book Karein', visual:'Split: generic topical treatment (no brand) with warning label LEFT. Clean Dr. Batra\'s consultation RIGHT. Warm light. Headline on image only.',
 production:'1080×1080 Feed + 1080×1920 Stories. Text <20% image area.', audience_note:'25–40 Delhi, interests: hair loss, Minoxidil. Retarget website visitors.', topic:'Pre-built', savedDate:null},
{id:'S02',type:'static',hook:'trust',audience:'cold',priority:'Launch first',title:'Doctor vs coach',hookLabel:'Trust',
 imageEn:"A real doctor matters", imageHi:'Asli doctor zaroori hai',
 openEn:"Your hair deserves a real diagnosis. From a specialist who examines you — not an algorithm.",
 openHi:'Aapke baalon ko asli diagnosis chahiye. Ek specialist se jo aapko examine kare — algorithm se nahi.',
 captionEn:"Your hair deserves a real diagnosis — from a specialist who examines your scalp, reviews your stress and history, and builds a plan personalised to you.\n\nAt Dr. Batra's, 350+ specialist doctors across 120 clinics have treated 8 lakh patients. Delhi clinics in CP, Lajpat Nagar, Punjabi Bagh, Rohini, Dwarka and more.\n\nBook your free consultation. Link in bio.",
 captionHi:"Aapke baalon ko asli diagnosis chahiye — ek qualified specialist se jo aapki scalp examine kare, stress aur history review kare, aur sirf aapke liye plan banaye.\n\nDr. Batra's mein 350+ specialist doctors 120 clinics mein 8 lakh patients ko treat kar chuke hain. Delhi: CP, Lajpat Nagar, Punjabi Bagh, Rohini, Dwarka aur aur bhi.\n\nFree consultation book karein. Link bio mein.",
 cta:'Book Free Consultation / Free Consultation Book Karein', visual:'Doctor in genuine consultation at Dr. Batra\'s Delhi clinic — authentic photography.', production:'1080×1080 Feed', audience_note:'Cold 25–45 Delhi. Retarget: website visitors who did not book.', topic:'Pre-built', savedDate:null}
];

let savedScripts = [];
let FLT = {format:'all',hook:'all',audience:'all'};
let currentLibrarySource = 'prebuilt';

const HC={pain:'#993C1D',safety:'#534AB7',speed:'#0F6E56',trust:'#185FA5',switcher:'#854F0B',delhi:'#854F0B',women:'#D4537E'};
const HB={pain:'#FAECE7',safety:'#EEEDFE',speed:'#E1F5EE',trust:'#E6F1FB',switcher:'#FAEEDA',delhi:'#FAEEDA',women:'#FBEAF0'};
const AC={cold:'#185FA5',warm:'#854F0B',retarget:'#0F6E56'};
const AB={cold:'#E6F1FB',warm:'#FAEEDA',retarget:'#E1F5EE'};

function loadSaved(){ const s=localStorage.getItem('drbatras_saved_rich'); if(s) savedScripts=JSON.parse(s); else savedScripts=[]; }
function saveSaved(){ localStorage.setItem('drbatras_saved_rich',JSON.stringify(savedScripts)); }
function getCurrentLib(){ return currentLibrarySource==='prebuilt'?PREBUILT:savedScripts; }

function renderLib(){
  let arr = getCurrentLib().filter(c=>{
    let f=FLT.format, h=FLT.hook, a=FLT.audience;
    return (f==='all'||c.type===f) && (h==='all'||c.hook===h) && (a==='all'||c.audience===a);
  });
  document.getElementById('cnt').innerText=arr.length;
  document.getElementById('lib-cards').innerHTML=arr.length?arr.map(c=>buildRichCard(c)).join(''):'<div class="no-results">No scripts found</div>';
}

function buildRichCard(c){
  const bgColor = HB[c.hook] || HB.pain;
  const textColor = HC[c.hook] || HC.pain;
  const priorityBadge = c.priority ? `<span class="badge" style="background:#f1efe8;color:#5F5E5A">${c.priority}</span>` : '';
  const topicDateHtml = (c.topic && c.topic !== 'Pre-built') ? `<span class="topic-date">📌 ${c.topic} • 🗓️ ${c.savedDate||''}</span>` : '';
  return `<div class="card" id="card-${c.id}">
<div class="card-hdr" onclick="tog('${c.id}')">
  <span class="cid" style="background:${bgColor};color:${textColor}">${c.id}</span>
  <div style="flex:1">
    <div class="ctitle">${c.title} ${topicDateHtml}</div>
    <div class="cmeta">
      <span class="badge" style="background:${bgColor};color:${textColor}">${c.hookLabel}</span>
      <span class="badge" style="background:${AB[c.audience]};color:${AC[c.audience]}">${c.audience}</span>
      ${priorityBadge}
    </div>
  </div>
  <span class="chev" id="chev-${c.id}">›</span>
</div>
<div class="card-body" id="body-${c.id}">
  <div class="csec">
    <div class="img-box">
      <div class="slabel" style="color:#085041">Image text — 3–7 words on creative only</div>
      <div class="lgrid" style="margin-top:.5rem">
        <div><div style="font-size:10px;font-weight:500;color:#085041;margin-bottom:3px">EN</div><div class="ctext">${c.imageEn}</div>${cpyBtn(c.imageEn)}</div>
        <div><div style="font-size:10px;font-weight:500;color:#085041;margin-bottom:3px">HI</div><div class="ctext">${c.imageHi}</div>${cpyBtn(c.imageHi)}</div>
      </div>
    </div>
    <div class="open-box">
      <div class="slabel" style="color:#633806">Opening line — first ~125 chars before "see more"</div>
      <div style="margin-top:.5rem">
        <div style="font-size:10px;font-weight:500;color:#633806;margin-bottom:3px">EN</div><div class="ctext">${c.openEn}</div>${cpyBtn(c.openEn)}
        <div style="font-size:10px;font-weight:500;color:#633806;margin:8px 0 3px">HI</div><div class="ctext">${c.openHi}</div>${cpyBtn(c.openHi)}
      </div>
    </div>
  </div>
  <div class="csec">
    <div class="slabel" style="color:#5F5E5A">Full caption — Meta caption field</div>
    <div class="lgrid" style="margin-top:.5rem">
      <div class="lbox"><div class="ltag" style="color:#0F6E56">English</div><div class="ctext">${c.captionEn}</div>${cpyBtn(c.captionEn)}</div>
      <div class="lbox"><div class="ltag" style="color:#534AB7">Hindi</div><div class="ctext">${c.captionHi}</div>${cpyBtn(c.captionHi)}</div>
    </div>
  </div>
  <div class="csec"><div class="cta-box"><div class="slabel" style="color:#0C447C">Meta CTA button</div><div class="ctext" style="margin-top:.25rem;font-weight:500">${c.cta}</div></div></div>
  <div class="csec"><div class="notes-box">
    <div style="font-size:11px;font-weight:500;color:#633806;margin-bottom:2px">Visual direction</div>
    <div style="font-size:13px;color:#5F5E5A;margin-bottom:.625rem">${c.visual}</div>
    <div style="font-size:11px;font-weight:500;color:#854F0B;margin-bottom:2px">Production note</div>
    <div style="font-size:13px;color:#5F5E5A;margin-bottom:.625rem">${c.production}</div>
    <div style="font-size:11px;font-weight:500;color:#185FA5;margin-bottom:2px">Target audience</div>
    <div style="font-size:13px;color:#5F5E5A">${c.audience_note}</div>
  </div></div>
  ${currentLibrarySource==='saved' ? `<div style="padding:0 1.125rem 1rem 1.125rem"><button class="save-btn" onclick="deleteSavedScript('${c.id}')">🗑️ Delete from library</button></div>` : ''}
</div></div>`;
}

function deleteSavedScript(id){
  savedScripts = savedScripts.filter(s => s.id !== id);
  saveSaved();
  renderLib();
}

function cpyBtn(t){ const safe=t.replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/\n/g,'\\n'); return `<button class="cpybtn" onclick="doCopy('${safe}',this)">Copy</button>`; }
function doCopy(t,btn){ navigator.clipboard.writeText(t).then(()=>{btn.textContent='Copied';setTimeout(()=>{btn.textContent='Copy';},1500);}); }
function tog(id){ const b=document.getElementById('body-'+id),ch=document.getElementById('chev-'+id); if(b){ b.classList.toggle('open'); if(ch)ch.textContent=b.classList.contains('open')?'‹':'›'; } }
function setF(dim,val,el){ FLT[dim]=val; document.querySelectorAll('.pill[data-f="'+dim+'"]').forEach(p=>p.classList.remove('f-active','h-active','a-active')); el.classList.add(dim==='format'?'f-active':dim==='hook'?'h-active':'a-active'); renderLib(); }
function switchLibrarySource(){ currentLibrarySource=document.getElementById('library-source').value; renderLib(); }
function showTab(name,el){ document.querySelectorAll('.section-panel').forEach(p=>p.classList.remove('visible')); document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active')); document.getElementById('tab-'+name).classList.add('visible'); el.classList.add('active'); if(name==='library') renderLib(); }

function saveScriptToLibrary(script, topicName){
  const newId = `SAVED_${Date.now()}_${Math.floor(Math.random()*1000)}`;
  const today = new Date().toLocaleDateString('en-CA');
  const saved = {...script, id:newId, topic:topicName, savedDate:today, priority:'Saved'};
  savedScripts.unshift(saved);
  saveSaved();
  alert(`✅ Script saved to library!\nTopic: ${topicName}\nDate: ${today}`);
}

async function generateScripts(){
  const apiKey = document.getElementById('api-key').value.trim();
  const topic = document.getElementById('topic-name').value.trim();
  if(!apiKey){ alert("Enter Groq API key"); return; }
  if(!topic){ alert("Enter a brand/topic"); return; }
  const type = document.getElementById('gen-type').value;
  const hookVal = document.getElementById('gen-hook').value;
  const count = Math.min(3,Math.max(1,parseInt(document.getElementById('gen-count').value)||1));
  const hookLabel = document.getElementById('gen-hook').options[document.getElementById('gen-hook').selectedIndex].text;
  const btn = document.getElementById('gen-btn'), statusSpan = document.getElementById('gen-status'), outputDiv = document.getElementById('gen-output');
  btn.disabled = true;
  statusSpan.innerHTML = '<span class="loading-dots"><span></span><span></span><span></span></span> Generating rich scripts with Groq LLaMA 70B...';
  outputDiv.innerHTML = '';
  const fmt = `{"scripts":[{"title":"","hook_type":"${hookVal}","audience":"cold","image_text_en":"3-7 words","image_text_hi":"","opening_line_en":"","opening_line_hi":"","full_caption_en":"","full_caption_hi":"","cta_button":"Book Free Consultation","visual_direction":"","production_note":"","audience_note":""}]}`;
  const prompt = `Topic: "${topic}". Hook: ${hookLabel}. Generate ${count} DISTINCT bilingual (English+Hindi) rich Meta ad scripts with ALL fields. Return JSON: ${fmt}. Each script must have: image_text_en/hi (3-7 words), opening_line_en/hi (max 125 chars), full_caption_en/hi (3-4 paragraphs), cta_button, visual_direction (detailed), production_note (format specs), audience_note. Never markdown.`;
  try{
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions',{
      method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${apiKey}`},
      body:JSON.stringify({model:'llama-3.3-70b-versatile', messages:[{role:'user',content:prompt}], temperature:0.8, max_tokens:4000, response_format:{type:"json_object"}})
    });
    const data = await res.json();
    if(data.error) throw new Error(data.error.message);
    const raw = data.choices[0].message.content;
    const clean = raw.replace(/```json|```/g,'').trim();
    const parsed = JSON.parse(clean);
    const scripts = parsed.scripts || [];
    if(!scripts.length) throw new Error('No scripts');
    statusSpan.innerHTML = `✅ Generated ${scripts.length} rich script(s) for "${topic}". Click SAVE to add to library.`;
    btn.disabled = false;
    outputDiv.innerHTML = '';
    scripts.forEach((s,idx)=>{
      const scriptObj = {
        id:`GEN_${Date.now()}_${idx}`, type:'static', hook:hookVal, audience:s.audience||'cold', priority:'Generated',
        title:s.title||`${topic} ad ${idx+1}`, hookLabel:hookLabel.split(' — ')[0],
        imageEn:s.image_text_en||`Effective solution for ${topic}`, imageHi:s.image_text_hi||`${topic} ka asli ilaaj`,
        openEn:s.opening_line_en||`Finally, a treatment that works for ${topic}.`, openHi:s.opening_line_hi||`Aakhir ek ilaaj jo ${topic} ke liye kaam kare.`,
        captionEn:s.full_caption_en||`Discover the power of ${topic}. Root cause treatment. Zero side effects. Book your free consultation today.\n\n${topic} is now within your reach. Don't wait any longer.`,
        captionHi:s.full_caption_hi||`${topic} ki shakti se mile. Root cause treatment. Zero side effects. Aaj hi free consultation book karein.\n\n${topic} ab aapki pahunch mein hai. Der na karein.`,
        cta:s.cta_button||'Book Free Consultation / Free Consultation Book Karein',
        visual:s.visual_direction||'Professional clinic setting with warm lighting. Clean branding.',
        production:s.production_note||'1080×1080 Feed + Stories. Text <20% image area.',
        audience_note:s.audience_note||`Target audience interested in ${topic}. Cold + warm retarget. Age 25-45.`
      };
      const cardDiv = document.createElement('div');
      cardDiv.className = 'card';
      cardDiv.style.border = '2px solid #0F6E56';
      cardDiv.innerHTML = buildRichCardFromObj(scriptObj);
      const saveBtn = document.createElement('button'); 
      saveBtn.className = 'save-btn'; 
      saveBtn.textContent = '💾 Save to Library'; 
      saveBtn.style.margin = '8px 16px 16px 16px';
      saveBtn.onclick = () => saveScriptToLibrary(scriptObj, topic);
      cardDiv.querySelector('.card-body').appendChild(saveBtn);
      outputDiv.appendChild(cardDiv);
    });
  } catch(e){ statusSpan.innerHTML=''; outputDiv.innerHTML=`<div class="error-box">Error: ${e.message}</div>`; btn.disabled=false; }
}

function buildRichCardFromObj(c){
  const bg = HB[c.hook]||HB.pain, txt = HC[c.hook]||HC.pain;
  return `<div class="card-hdr" onclick="tog('${c.id}')">
  <span class="cid" style="background:${bg};color:${txt}">NEW</span>
  <div style="flex:1"><div class="ctitle">${c.title}</div>
  <div class="cmeta"><span class="badge" style="background:${bg};color:${txt}">${c.hookLabel}</span>
  <span class="badge" style="background:${AB[c.audience]};color:${AC[c.audience]}">${c.audience}</span>
  <span class="badge" style="background:#f1efe8;color:#5F5E5A">Generated</span></div></div>
  <span class="chev" id="chev-${c.id}">›</span>
</div>
<div class="card-body" id="body-${c.id}" style="display:block">
  <div class="csec"><div class="img-box"><div class="slabel">Image text — 3–7 words on creative only</div>
    <div class="lgrid"><div><div class="ctext">${c.imageEn}</div>${cpyBtn(c.imageEn)}</div><div><div class="ctext">${c.imageHi}</div>${cpyBtn(c.imageHi)}</div></div></div>
    <div class="open-box"><div class="slabel">Opening line — first ~125 chars before "see more"</div>
    <div><div class="ctext">${c.openEn}</div>${cpyBtn(c.openEn)}<div class="ctext" style="margin-top:6px">${c.openHi}</div>${cpyBtn(c.openHi)}</div></div></div>
  <div class="csec"><div class="lgrid"><div><div class="ltag">English caption</div><div class="ctext">${c.captionEn}</div>${cpyBtn(c.captionEn)}</div><div><div class="ltag">Hindi caption</div><div class="ctext">${c.captionHi}</div>${cpyBtn(c.captionHi)}</div></div></div>
  <div class="csec"><div class="cta-box"><div class="slabel">Meta CTA button</div><div class="ctext">${c.cta}</div></div></div>
  <div class="csec"><div class="notes-box">
    <div class="slabel">Visual direction</div><div class="ctext">${c.visual}</div>
    <div class="slabel" style="margin-top:6px">Production note</div><div class="ctext">${c.production}</div>
    <div class="slabel" style="margin-top:6px">Target audience</div><div class="ctext">${c.audience_note}</div>
  </div></div>
</div>`;
}

loadSaved();
renderLib();
</script>
</body>
</html>