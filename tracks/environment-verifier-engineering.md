# Environment and Verifier Engineering

## Focus

Environment and Verifier Engineering teaches learners to build reproducible worlds where agents can act, fail, recover, and be scored.

A verifier answers:

> Did the agent actually accomplish the task?

That is stronger than asking whether the final response sounds good.

## Verifier Types

| Type | Example |
| --- | --- |
| Deterministic verifier | `assert invoice.total == 183.42` |
| State verifier | Check that a simulated database, calendar, ticket, or approval state changed correctly. |
| Constraint verifier | Score partial completion across required conditions. |
| Decision-model verifier | Use a classifier, reranker, reward model, or other constrained decision model for a narrow semantic judgment. |
| Reasoning verifier | Use a tool-capable reasoning model for evidence-heavy judgments that require decomposition. |
| Human verifier | Adjudicate consequential uncertainty and produce trusted labels. |

These form a verifier cascade rather than interchangeable grader names.
Deterministic checks should veto objective failures; calibrated decision models
handle narrow judgments; reasoning verifiers handle ambiguity; humans resolve
the consequential residue.

## Core Skills

- task design
- state modeling
- action and observation schemas
- simulated tools
- sandboxing
- deterministic checks
- state and constraint verification
- reward component design
- reward hacking analysis
- calibration, risk-coverage, and escalation thresholds
- false-accept and false-reject measurement
- process vs outcome verification
- verifier versioning and adversarial evaluation
- rollout logging

## Reference Stack

The preferred reference stack is:

```text
Python + pytest
Docker
local simulator
Inspect AI for eval integration
Prime Intellect / Verifiers as an advanced hosted adapter
```

BrowserGym, Browserbase, E2B, and METR Task Standard are useful comparison paths for browser, sandbox, and portable task environments.

## Portfolio Evidence

A learner completing this track should have:

- a simulated environment
- generated task sets
- state transition logs
- deterministic and state verifiers
- constraint scoring examples
- reward functions with known limitations
- rollout logs
- reward hacking examples
- a calibrated semantic verifier and operating policy
- an adversarial verifier evaluation set

Portfolio example:

- [`examples/portfolio/environment-verifier-engineering.md`](../examples/portfolio/environment-verifier-engineering.md)
