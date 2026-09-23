import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {evaluate, decide} from '../web/rules.mjs';
const read = path => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8'));
const resumes = read('../data/resumes.json');
const jobs = read('../data/jobs.json');
const rules = read('../data/rules.json');
const python = read('../output/report.json');
assert.equal(python.length, resumes.length * jobs.length);
let compared = 0;
for (const resume of resumes) for (const job of jobs) {
  assert.deepEqual(evaluate(resume, job, rules), python[compared++]);
}
const pending = evaluate(resumes[0], jobs[0], rules);
assert.throws(() => decide(pending, '', 'DECLINE', 'reason', rules), /HUMAN_GATE_REQUIRED/);
assert.throws(() => decide(pending, 'Reviewer', 'DECLINE', '', rules), /HUMAN_GATE_REQUIRED/);
assert.equal(decide(pending, 'Reviewer', 'HOLD', 'Check evidence', rules).state, 'HUMAN_DECIDED');
console.log(`${compared} Python/browser rule parity cases passed; human gate passed`);
