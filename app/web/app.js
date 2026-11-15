let config;
let busy = false;
const form = document.querySelector('#question-form');
const question = document.querySelector('#question');
const status = document.querySelector('#status');
const result = document.querySelector('#result');
const buttons = [...document.querySelectorAll('button')];
const citedPassages = new Map();

function setBusy(value) {
  busy = value;
  buttons.forEach(button => button.disabled = value);
  form.setAttribute('aria-busy', String(value));
}
function inline(text, parent) {
  // A small allowlisted renderer: model text never becomes HTML.
  const pieces = text.split(/(\*\*[^*]+\*\*|(?:\[|【)PHOTO-\d+-C\d+(?:\]|】))/g);
  for (const part of pieces) {
    const citation = part.match(/^(?:\[|【)(PHOTO-\d+-C\d+)(?:\]|】)$/);
    if (citation && citedPassages.has(citation[1])) {
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'citation'; button.textContent = citation[1];
      button.setAttribute('aria-label', 'Read passage '+citation[1]);
      button.onclick = () => { const detail = citedPassages.get(citation[1]); detail.open = true; detail.scrollIntoView({behavior:'smooth', block:'center'}); detail.querySelector('summary').focus(); };
      parent.append(button);
    } else if (part.startsWith('**') && part.endsWith('**')) {
      const strong = document.createElement('strong'); strong.textContent = part.slice(2,-2); parent.append(strong);
    } else parent.append(document.createTextNode(part));
  }
}
function renderAnswer(text) {
  const container = document.querySelector('#answer'); container.replaceChildren();
  let list;
  for (const line of text.split('\n').map(s => s.trim()).filter(Boolean)) {
    if (/^[-*]\s/.test(line)) {
      if (!list) { list = document.createElement('ul'); container.append(list); }
      const li = document.createElement('li'); inline(line.replace(/^[-*]\s/,''),li); list.append(li);
    } else {
      list = null; const paragraph = document.createElement('p'); inline(line,paragraph); container.append(paragraph);
    }
  }
}
function render(data) {
  const sources = document.querySelector('#sources'); sources.replaceChildren(); citedPassages.clear();
  for (const passage of data.passages || []) {
    const detail = document.createElement('details');
    const summary = document.createElement('summary'); summary.textContent = passage.source_id+' · '+(passage.section || 'Source passage');
    const body = document.createElement('div');
    const paragraph = document.createElement('p'); paragraph.textContent = passage.text;
    body.append(paragraph);
    if (passage.url) {
      try {
        const url = new URL(passage.url);
        if (url.protocol === 'https:' && ['home.nps.gov','www.nps.gov'].includes(url.hostname)) {
          const link = document.createElement('a'); link.href = url.href; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Open original NPS article ↗'; body.append(link);
        }
      } catch {}
    }
    detail.append(summary,body); sources.append(detail); citedPassages.set(passage.source_id,detail);
  }
  renderAnswer(data.answer);
  if (data.setup_context) document.querySelector('.context p').textContent = data.setup_context;
  document.querySelector('.review-note').textContent = data.answer_method === 'source_checklist_v1' ? 'Checklist text comes from checked source-derived paraphrases. Review relevance, completeness and the original source; selected evidence can still be incomplete or inappropriate.' : 'Saved prototype test: the original generated explanation may add unsupported details. Check each recommendation against its passage.';
  document.querySelector('#asked-question').textContent = data.question;
  document.querySelector('#source-count').textContent = `${(data.passages || []).length} passages`;
  document.querySelector('#result-title').textContent = data.status === 'generated' ? 'Your starting point' : 'A little more evidence needed';
  document.querySelector('#result-mode').textContent = data.mode === 'saved_example' ? 'SAVED TEST · NOT LIVE' : 'LIVE RESPONSE';
  result.classList.remove('hidden');
  result.scrollIntoView({behavior:'smooth',block:'start'});
}
async function request(path, body) {
  if (busy) return;
  setBusy(true); status.className = 'loading'; status.textContent = path.includes('example') ? 'Opening the saved test…' : 'Looking through the source and preparing your answer…';
  result.classList.add('hidden');
  try {
    if (!config) throw new Error('The app is not ready. Reload this page.');
    const response = await fetch(path, {method:'POST',headers:{'Content-Type':'application/json','X-App-Token':config.token},body:JSON.stringify(body)});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Something went wrong. Please try again.');
    render(data); status.textContent = '';
  } catch(error) { status.className = ''; status.textContent = error.message || 'The connection was interrupted. Please try again.'; }
  finally { setBusy(false); }
}
question.addEventListener('input', () => document.querySelector('#count').textContent = `${question.value.length.toLocaleString()} / 1,000`);
form.addEventListener('submit', event => { event.preventDefault(); if (!question.value.trim()) { status.textContent = 'Write a photography question first.'; question.focus(); return; } request('/api/ask',{question:question.value}); });
document.querySelectorAll('[data-case]').forEach(button => button.addEventListener('click', () => request('/api/example',{case:button.dataset.case})));
fetch('/api/config').then(response => {if(!response.ok) throw new Error(); return response.json();}).then(data => {
  config = data;
  if (data.expanded) {
    document.querySelector('#landscape-tag').classList.remove('hidden');
    document.querySelector('#collection-summary').textContent = 'Two NPS guides cover night-sky experiments and landscape fundamentals: waterfall blur, aperture, composition and golden-hour light. General guidance, not EOS R1 procedures.';
    document.querySelector('#document-count').textContent = '02';
    document.querySelector('#document-unit').textContent = 'articles';
    document.querySelector('#passage-count').textContent = '07';
    document.querySelector('#additional-source').classList.remove('hidden');
  }
  document.querySelector('#connection').textContent = data.mode === 'live' ? '● Live · Qdrant + Groq' : 'Preview · saved examples';
}).catch(() => { document.querySelector('#connection').textContent = 'Connection unavailable'; status.textContent = 'Could not reach the local app. Make sure its terminal is running.'; });
