# Recruitment decision support — case study

## Problem
An HR reviewer needs to inspect why a fictional profile matched a fictional role without software making an employment decision.

## Context
This is a synthetic decision-support demo with 12 fictional profiles and 3 fictional roles. No real applicant, protected attribute or HR integration is present.

## Constraints
Employment decisions are high-impact. Self-authored fixtures cannot establish hiring validity or fairness; the browser has no authenticated reviewer identity.

## My Role
I implemented Python evidence scoring and human gate, a browser workbench using the same fixtures/rules, risk flags, a local audit and cross-language parity tests.

## Architecture
Each job skill gets credit only when its literal phrase occurs in supplied evidence. The system records the source phrase, unsupported skills and risk flags, then stops at `HUMAN_REVIEW`. A named fictional reviewer must supply an action and reason to record a demo decision.

## Key Decisions
Keep score deterministic and explainable, preserve the human gate in both languages, and label all cases `synthetic_unverified`.

## Hardest Problem
Connecting the static Pages screen to the actual Python logic without implying a server-side HR system. The browser reads the same JSON fixtures and rule configuration; CI compares all 36 Python/browser result objects.

## Failure/Tradeoff
Substring evidence can credit a misleading phrase or miss a synonym. A browser-only audit can be edited and is not trustworthy for real employment records.

## Testing
13 Python tests, 5 synthetic fixture cases and 36 parity cases pass. Browser tested the required fields, recorded/reloaded/reset a fictional decision and replayed the eval page.

## Eval
This is deterministic mechanics verification, not model quality or hiring fairness. `model_quality=NOT_RUN`; see [eval spec](../evals/PROJECT_EVAL_SPEC.md).

## Current Evidence
[Interactive synthetic workbench](https://zhouey314-cloud.github.io/ai-recruitment-workflow-demo/) · [browser eval](https://zhouey314-cloud.github.io/ai-recruitment-workflow-demo/eval/) · [Python source](../recruitment.py) · [parity test](../tests/parity.mjs).

## Limitations
No resume parsing, model, protected-group validation, authenticated reviewer, secure storage or real hiring outcome.

## What I Would Do in Production
First obtain domain-owner policy and lawful data/consent; then add verified evidence, authenticated human review, privacy controls, fairness assessment and expert-owned regression labels.

## What I Learned
An explainable score can support a conversation, but should not be described as a validated hiring signal.
