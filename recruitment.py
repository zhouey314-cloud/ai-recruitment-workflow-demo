"""Synthetic decision support. Never makes employment decisions."""
import json
from pathlib import Path

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
    return {'resume_id':resume['id'],'job_id':job['id'],'score':score,'evidence':evidence,'missing':[e['skill'] for e in evidence if not e['supported']],'state':'HUMAN_REVIEW','decision':None,'synthetic_unverified':True}

def decide(result:dict,reviewer:str,decision:str,reason:str)->dict:
    if result['state']!='HUMAN_REVIEW' or not reviewer.strip() or not reason.strip() or decision not in {'INTERVIEW','HOLD','DECLINE'}:raise ValueError('HUMAN_GATE_REQUIRED')
    result['decision']=decision;result['state']='HUMAN_DECIDED';result['audit']={'reviewer':reviewer,'reason':reason,'decision':decision};return result

def main():
    data=json.loads(Path('data/resumes.json').read_text());jobs=json.loads(Path('data/jobs.json').read_text())
    results=[evaluate(r,j) for r in data for j in jobs]
    Path('output').mkdir(exist_ok=True);Path('output/report.json').write_text(json.dumps(results,indent=2))
    print(f'{len(results)} synthetic comparisons; all waiting for human review. output/report.json')
if __name__=='__main__':main()
