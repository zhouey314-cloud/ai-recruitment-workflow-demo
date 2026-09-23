# Evaluation specification and release gate

Scope: deterministic, synthetic recruitment decision-support mechanics. This is not an AI model quality, hiring validity or fairness evaluation. All cases are `synthetic_unverified`; no externally verified ground truth exists.

## Baseline before interactive workbench

- Python unit tests: 9/9 pass.
- Python fixture eval: 5/5 pass, 0 failures; `model_quality=NOT_RUN`.
- 12 fictional resumes × 3 fictional jobs = 36 generated comparisons, all `HUMAN_REVIEW`.

## Current gate

1. `python3 -m unittest discover -s tests`: 13/13.
2. `python3 evals/run.py`: 5/5 synthetic fixture cases; 0 failures.
3. `python3 recruitment.py && node tests/parity.mjs`: all 36 Python/browser objects identical, including evidence, score, missing skills, risk flags and review state.
4. Browser review: choose a fixture, inspect citation and missing skills, verify decision is disabled until analysis, reviewer/action/reason required, local audit and reset, evaluation page.
5. No model or real applicant data; `model_quality=NOT_RUN`.

## Known failure modes and boundaries

- **False negative / Parsing:** synonymous evidence without literal job-skill phrase receives no credit. Human must investigate.
- **False positive / Business rule:** a phrase containing the skill name may be insufficient proof. Human must verify.
- **Conflict / Knowledge:** `CONFLICT_FLAG` is a reminder, not an adjudication.
- **Fairness / Unknown:** no protected-group dataset or domain-expert labels. No fairness claim.
- **Workflow / Security:** browser-only reviewer/audit has no authentication or tamper resistance. Not for real hiring.

Release gate: any fixture regression, Python/browser mismatch, bypassable required human fields or real-data upload would block this demo release.
