export function evaluate(resume, job, rules) {
  if (!resume || !job || !Array.isArray(resume.skills) || !Array.isArray(resume.evidence)) throw new Error('INVALID_RESUME');
  const evidence = job.skills.map(skill => {
    const source = resume.evidence.find(item => item.toLowerCase().includes(skill.toLowerCase())) ?? null;
    return {skill, supported: source !== null, source};
  });
  const score = Math.round(100 * evidence.filter(item => item.supported).length / Math.max(1, job.skills.length));
  const missing = evidence.filter(item => !item.supported).map(item => item.skill);
  const risk = [];
  if (!resume.evidence.length) risk.push('NO_EVIDENCE');
  if (missing.some(skill => resume.skills.some(claim => claim.toLowerCase() === skill.toLowerCase()))) risk.push('SELF_REPORTED_UNSUPPORTED');
  if (resume.conflicts?.length) risk.push('CONFLICT_FLAG');
  return {resume_id: resume.id, job_id: job.id, score, evidence, missing, risk, state: rules.review_state, decision: null, synthetic_unverified: true};
}

export function decide(result, reviewer, decision, reason, rules) {
  if (result.state !== rules.review_state || !reviewer.trim() || !reason.trim() || !rules.allowed_human_decisions.includes(decision)) throw new Error('HUMAN_GATE_REQUIRED');
  return {...result, decision, state: 'HUMAN_DECIDED', audit: {reviewer, reason, decision}};
}
