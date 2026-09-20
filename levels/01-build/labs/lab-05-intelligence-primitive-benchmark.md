# Lab 5: Intelligence Primitive Benchmark

## Objective

Choose an intelligence primitive from evidence rather than treating a large
generative model as the default for every decision.

Labs 1-4 built one loop where a single model owns every decision. This lab asks
what that model should *keep*.

## Task

Use one bounded StrongBench routing problem: what shape of work a request
needs, before any answer is written.

```text
policy_only          the policy corpus answers it
receipt              a stored receipt must be fetched
calculate            a reimbursement total must be computed
receipt_calculate    both
approval             a human approval step is required
```

Every task needs `search_policy`, so routing on the first tool is a constant.
Route on what the task needs *beyond* it.

Evaluate at least four candidates:

1. Deterministic rules.
2. An embedding, zero-shot, or trained classifier.
3. A constrained decision model, locally or through an optional hosted
   provider.
4. A structured-output generative model.

Add a fifth candidate that composes two or more of them into a confidence-gated
cascade. If a hosted candidate is unavailable, mark it `not measured`; do not
replace missing evidence with vendor claims.

## Shared Contract

All candidates must consume the same versioned state and produce the same
decision record:

```json
{
  "value": "calculate",
  "probabilities": {
    "policy_only": 0.04,
    "receipt": 0.03,
    "calculate": 0.87,
    "receipt_calculate": 0.05,
    "approval": 0.01
  },
  "confidence": 0.87,
  "model": "candidate/version",
  "question_version": "work-shape-v1",
  "input_version": "strongbench-benchmark-v1"
}
```

`probabilities` is a distribution over every class, not the winning entry
alone, and `confidence` is read out of it rather than carried beside it.
Candidates that cannot expose a meaningful distribution set both
`probabilities` and `confidence` to `null`. Do not invent confidence by asking
a model for an unsupported verbal estimate.

**Label the data from something no candidate produced.** The committed
`required_tools` field is the oracle here. Labelling with one candidate's own
behaviour scores that candidate against itself, and it will look perfect.

## Adoption Gate

Write the gate before running the benchmark. It must include:

- held-out task quality
- the unsafe-action slice, reported separately and never netted into the total
- calibration and coverage when probabilities are available
- p50/p95 latency
- measured cost
- privacy, deployment, and fallback constraints

## Report

Report a Pareto frontier rather than one universal score. A candidate dominated
on every relevant dimension can be rejected. Trade-offs that depend on the
deployment should remain visible.

| Candidate | Quality | Unsafe misses | Coverage | p95 | Cost | Evidence status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| rules | | | | | | measured / not measured |
| classifier | | | | | | measured / not measured |
| constrained decision model | | | | | | measured / not measured |
| generative model | | | | | | measured / not measured |
| cascade | | | | | | measured / not measured |

## Deliverable

Submit the shared contract, candidate implementations or configurations,
versioned benchmark data, result table, slice analysis, adoption gate, and one
of: adopt, reject, or keep testing.

## Checks

The lab passes when your table answers all five:

- Does every candidate consume the same input and emit the same record shape?
- Is the label independent of every candidate's own output?
- Is the unsafe slice reported as a raw count, separate from accuracy?
- Does at least one row read `not measured` rather than a guess?
- Does the recommendation name the condition that would change it?

Check the contract invariant mechanically against your own output:

```bash
python3 - <<'PY'
import json
rows = [json.loads(line) for line in open("your-decisions.jsonl") if line.strip()]
for row in rows:
    probabilities = row["probabilities"]
    if probabilities is None:
        assert row["confidence"] is None, f"{row['model']}: confidence without a distribution"
        continue
    assert abs(sum(probabilities.values()) - 1.0) < 1e-6, f"{row['model']}: not a distribution"
    assert row["confidence"] == probabilities[row["value"]], f"{row['model']}: confidence drifted"
print(f"{len(rows)} decision records, contract holds")
PY
```

## Reference Solution

Write your own version first, then compare:
[`solutions/lab_05_intelligence_primitive_benchmark.py`](../../../examples/strongbench-expense-agent/solutions/lab_05_intelligence_primitive_benchmark.py).

```bash
cd examples/strongbench-expense-agent
python solutions/lab_05_intelligence_primitive_benchmark.py
```

Four candidates on the same fifty held-out tasks, no third-party dependencies —
the classifier is a bag-of-words nearest centroid in about thirty lines,
because "use a classifier" should not mean "install a framework" before you
know whether the classifier helps.

Read the safety column before the accuracy column. The classifier is the joint
most accurate candidate and has the **worst** safety record of the four: it
misses approval-required tasks that the slower generative candidate catches,
and the aggregate score never says so. Rules are within ten points of it at a
fraction of the latency.

There is no winner in that table. There is a frontier, and which point you take
depends on what your deployment cannot afford to lose.

[How to compare](../../../examples/strongbench-expense-agent/solutions/README.md).
