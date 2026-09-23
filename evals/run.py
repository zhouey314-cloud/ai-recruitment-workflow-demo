import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from recruitment import evaluate
def main():
    rs={r['id']:r for r in json.loads(Path('data/resumes.json').read_text())}
    jobs={j['id']:j for j in json.loads(Path('data/jobs.json').read_text())}
    cases=[json.loads(x) for x in Path('evals/golden.jsonl').read_text().splitlines() if x.strip()]
    cases+= [json.loads(x) for x in Path('evals/regression.jsonl').read_text().splitlines() if x.strip()]
    failures=[]
    for c in cases:
        r=c.get('resume',rs.get(c.get('resume_id')));j=c.get('job',jobs.get(c.get('job_id')))
        result=evaluate(r,j)
        supported=[x['skill'] for x in result['evidence'] if x['supported']]
        if ('expected_supported' in c and supported!=c['expected_supported']) or ('expected_score' in c and result['score']!=c['expected_score']):failures.append(c.get('case',c.get('resume_id')))
    print(json.dumps({'fixture_cases':len(cases),'failures':failures,'model_quality':'NOT_RUN','provenance':'synthetic_unverified'}))
    if failures:raise SystemExit(1)
if __name__=='__main__':main()
