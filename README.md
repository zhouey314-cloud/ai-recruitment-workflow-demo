# AI Recruitment Workflow Demo

**An inspectable review workflow, not a hiring engine.** This demo ties each rule score to resume evidence and leaves every decision to a human reviewer. All roles and candidates are fictional.

**LIVE_DEMO / SYNTHETIC CANDIDATES** · [Try the workbench](https://zhouey314-cloud.github.io/ai-recruitment-workflow-demo/) · [Case study](docs/case-study.md) · [Resume bullets](docs/resume-bullets.md) · [Interview notes](docs/interview-notes.md)

[![CI](https://github.com/zhouey314-cloud/ai-recruitment-workflow-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zhouey314-cloud/ai-recruitment-workflow-demo/actions/workflows/ci.yml)

![Live browser workbench with fictional role and candidate selected](docs/images/workbench-live.png)

The screenshot shows the deployed workbench's initial state, using fictional data. The demo contains 12 fictional resumes and 3 fictional jobs; the rule trace appears after **Analyze evidence**.

## Demo / quick start

Live interactive fictional workbench: <https://zhouey314-cloud.github.io/ai-recruitment-workflow-demo/>. [Browser eval replay](https://zhouey314-cloud.github.io/ai-recruitment-workflow-demo/eval/) shows the synthetic fixture results. The browser reads the same fixture data and rule configuration as Python; CI checks parity across all 36 combinations. There is no HR integration or real candidate data.

### A two-minute review

1. Open the [workbench](https://zhouey314-cloud.github.io/ai-recruitment-workflow-demo/) and select **AI application engineer** with **Sample Candidate 01**. **Record human decision** starts disabled.
2. Click **Analyze evidence**. Inspect the quoted Python and API evidence and the missing evaluation skill. Switch to **Sample Candidate 04** and analyze again: an empty evidence list should produce missing skills and a flag, not an automatic decision.
3. Use a fictional reviewer name, choose **Hold for clarification**, and add a fictional reason. Click **Record human decision**, check the local audit, then use **Reset local audit**. No applicant or reviewer data needs to leave this browser; do not enter real names or resumes.

[Fixed CI snapshot (`18827a9`)](https://github.com/zhouey314-cloud/ai-recruitment-workflow-demo/actions/runs/36246053618) · [What the fixtures prove and what they do not](evals/PROJECT_EVAL_SPEC.md)

Python 3.10+: `python3 recruitment.py`; `python3 evals/run.py`; `python3 -m unittest discover -s tests`; `node tests/parity.mjs` after generating the Python report. Serve the repository root with `python3 -m http.server 8000` and open `http://localhost:8000/` for the browser demo. Output is `output/report.json` with 36 comparisons. The interactive audit is only in browser localStorage and can be reset; it is not secure persistence.

## Problem and architecture

Job → structured resume parse → cited skill evidence → simple rule score → `HUMAN_REVIEW` → recorded interview/hold/decline → audit. Every decision remains a human action. Self-reported skills with no evidence receive no points. [Scoring rubric and failure examples](docs/architecture.md) explain the boundary.

![Architecture](docs/images/architecture.svg)

## Eval / verification

Thirteen Python unit tests, five synthetic fixture checks and 36 Python/browser parity checks cover evidence trace, unsupported claims, conflict flags and human gating. These validate deterministic mechanics only. `synthetic_unverified` is not a measured hiring outcome or a bias/fairness claim. No LLM provider runs. No real candidates or HR platform data. See [eval specification](evals/PROJECT_EVAL_SPEC.md), [resume bullets](docs/resume-bullets.md) and [interview notes](docs/interview-notes.md).

## Status / limitations / privacy

`IMPLEMENTED_AND_TESTED`: parser contract, evidence rubric, trace, browser workbench, local human gate and browser-only audit. `MOCK`: all fictional records and reviewer inputs. `DEPLOYED_STATIC_APP`: GitHub Pages hosts the interactive browser demo, not a secure backend. `NOT_IMPLEMENTED`: real parsing, model, fairness assessment, authenticated reviewer, tamper-proof audit and HR integration. Never use the score to automatically hire or reject a real person.

## License

[MIT](LICENSE).
