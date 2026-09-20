# Lab 6: Intelligence Primitive Benchmark

## Objective

Choose an intelligence primitive from evidence rather than treating a large
generative model as the default for every decision.

## Task

Use one bounded StrongBench routing or verification problem, such as choosing
the next action from:

```text
search_policy
lookup_receipt
calculate_reimbursement
request_human_approval
finish
```

Evaluate at least four candidates:

1. Deterministic rules.
2. An embedding, zero-shot, or trained classifier.
3. A constrained decision system, locally or through an optional hosted
   provider such as Jev.
4. A structured-output generative model.

Add a fifth candidate that composes two or more of them into a confidence-gated
cascade. If a hosted candidate is unavailable, mark it `not measured`; do not
replace missing evidence with vendor claims.

## Shared Contract

All candidates must consume the same versioned state and produce the same
decision record:

```json
{
  "value": "lookup_receipt",
  "probabilities": {"lookup_receipt": 0.91},
  "confidence": 0.91,
  "model": "candidate/version",
  "question_version": "next-action-v1"
}
```

Candidates that cannot expose a meaningful distribution should set that field
to `null`. Do not invent confidence by asking a model for an unsupported verbal
estimate.

## Adoption Gate

Write the gate before running the benchmark. It must include:

- held-out task quality
- the unsafe-action slice
- calibration and coverage when probabilities are available
- p50/p95 latency
- measured cost
- privacy, deployment, and fallback constraints

## Report

Report a Pareto frontier rather than one universal score. A candidate dominated
on every relevant dimension can be rejected. Trade-offs that depend on the
deployment should remain visible.

| Candidate | Quality | Calibration | Coverage | p95 | Cost | Evidence status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| rules | | | | | | measured / not measured |
| classifier | | | | | | measured / not measured |
| Type 1 decision system | | | | | | measured / not measured |
| generative model | | | | | | measured / not measured |
| cascade | | | | | | measured / not measured |

## Deliverable

Submit the shared contract, candidate implementations or configurations,
versioned benchmark data, result table, slice analysis, adoption gate, and one
of: adopt, reject, or keep testing.

The lesson is not that a particular provider wins. It is that the selected
component earned its role for this workload.

