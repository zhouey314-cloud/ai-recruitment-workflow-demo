"""Synthetic decision support. Never makes employment decisions."""
import json
from pathlib import Path

RULES = json.loads((Path(__file__).resolve().parent / 'data/rules.json').read_text())

def parse_resume(record:dict)->dict:
    required={'id','name','skills','years','evidence'}
    if not required.issubset(record) or not isinstance(record['skills'],list) or not isinstance(record['evidence'],list):raise ValueError('INVALID_RESUME')
    return record

def extract_evidence(resume:dict,job:dict)->list[dict]:
    items=[]
    for skill in job['skills']:
        mentions=[e for e in resume['evidence'] if skill.lower() in e.lower()]
        items.append({'skill':skill,'supported':bool(mentions),'source':mentions[0] if mentions else None})
    return items

def evaluate(resume:dict,job:dict)->dict:
    parse_resume(resume)
    evidence=extract_evidence(resume,job)
    points=sum(1 for e in evidence if e['supported'])
    score=round(100*points/max(1,len(job['skills'])))
    missing=[e['skill'] for e in evidence if not e['supported']]
    risk=[]
    if not resume['evidence']:risk.append('NO_EVIDENCE')
    if any(skill.lower() in {s.lower() for s in resume['skills']} for skill in missing):risk.append('SELF_REPORTED_UNSUPPORTED')
    if resume.get('conflicts'):risk.append('CONFLICT_FLAG')
    return {'resume_id':resume['id'],'job_id':job['id'],'score':score,'evidence':evidence,'missing':missing,'risk':risk,'state':RULES['review_state'],'decision':None,'synthetic_unverified':True}

def decide(result:dict,reviewer:str,decision:str,reason:str)->dict:
    if result['state']!=RULES['review_state'] or not reviewer.strip() or not reason.strip() or decision not in RULES['allowed_human_decisions']:raise ValueError('HUMAN_GATE_REQUIRED')
    result['decision']=decision;result['state']='HUMAN_DECIDED';result['audit']={'reviewer':reviewer,'reason':reason,'decision':decision};return result

def main():
    data=json.loads(Path('data/resumes.json').read_text());jobs=json.loads(Path('data/jobs.json').read_text())
    results=[evaluate(r,j) for r in data for j in jobs]
    Path('output').mkdir(exist_ok=True);Path('output/report.json').write_text(json.dumps(results,indent=2))
    print(f'{len(results)} synthetic comparisons; all waiting for human review. output/report.json')
if __name__=='__main__':main()
