import {evaluate, decide} from './rules.mjs';
const base = new URL('../', import.meta.url);
const load = async path => {const response = await fetch(new URL(path, base)); if (!response.ok) throw new Error(`Failed to load ${path}`); return response.json();};
const [resumes, jobs, rules] = await Promise.all([load('data/resumes.json'), load('data/jobs.json'), load('data/rules.json')]);
const $ = id => document.getElementById(id);
const el = (tag, text, className) => {const node=document.createElement(tag);node.textContent=text;if(className)node.className=className;return node;};
for (const job of jobs) $('job').add(new Option(job.title, job.id));
for (const resume of resumes) $('resume').add(new Option(`${resume.name} · ${resume.id}`, resume.id));
let current = null;
const selected = () => [resumes.find(r => r.id === $('resume').value), jobs.find(j => j.id === $('job').value)];
function updateScenario(){const [resume]=selected();$('experience').textContent=resume.experience;$('claims').textContent=`Self-reported skills: ${resume.skills.join(', ') || 'none'} · ${resume.years} fictional years`;current=null;$('result').textContent='Select Analyze evidence to run the shared rule.';$('record').disabled=true;$('message').textContent='';}
function renderAudit(){const list=$('auditList');list.replaceChildren();const audit=JSON.parse(localStorage.getItem('recruitment-demo-audit') || '[]');for(const item of audit){list.append(el('li',`${item.resume_id} × ${item.job_id}: ${item.audit.decision} by ${item.audit.reviewer} — ${item.audit.reason} (score ${item.score}; ${item.state})`));}if(!audit.length)list.append(el('li','No human decisions recorded.'));}
function analyze(){const [resume,job]=selected();current=evaluate(resume,job,rules);const box=$('result');box.replaceChildren();box.append(el('div',`${current.score} / 100`,'score'),el('p',`State: ${current.state} · No automatic decision`,'status'));
  for(const entry of current.evidence){const row=el('div','',`trace ${entry.supported?'yes':'no'}`);row.append(el('strong',`${entry.supported?'✓':'—'} ${entry.skill}`),el('span',entry.source ? `Source: “${entry.source}”` : 'No matching evidence supplied.'));box.append(row);}
  box.append(el('p',`Missing: ${current.missing.join(', ') || 'none'}`));const risk=el('div','Risk flags: ');if(current.risk.length){for(const flag of current.risk)risk.append(el('span',flag,'tag'));}else risk.append(el('span','none'));box.append(risk);if(resume.conflicts?.length)box.append(el('p',`Conflict note: ${resume.conflicts.join('; ')}`,'no'));
  $('record').disabled=false;$('message').textContent='Evidence ready for human review.';}
function record(){if(!current)return;try{const result=decide(current,$('reviewer').value.trim(),$('decision').value,$('reason').value.trim(),rules);const audit=JSON.parse(localStorage.getItem('recruitment-demo-audit') || '[]');audit.unshift(result);localStorage.setItem('recruitment-demo-audit',JSON.stringify(audit));renderAudit();$('message').textContent=`Recorded ${result.decision} by ${result.audit.reviewer}; ${result.state}.`;current=null;$('record').disabled=true;}catch(error){$('message').textContent=error.message==='HUMAN_GATE_REQUIRED'?'Reviewer, reason and human action are all required.':error.message;}}
$('job').addEventListener('change',updateScenario);$('resume').addEventListener('change',updateScenario);$('analyze').addEventListener('click',analyze);$('record').addEventListener('click',record);$('reset').addEventListener('click',()=>{localStorage.removeItem('recruitment-demo-audit');renderAudit();$('message').textContent='Local audit reset.';});
updateScenario();renderAudit();
