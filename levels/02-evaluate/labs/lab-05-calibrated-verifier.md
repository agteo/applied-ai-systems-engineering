# Lab 5: Calibrated Verifier

## Objective

Build or evaluate a narrow semantic verifier whose confidence can safely route
cases to automatic acceptance, stronger review, or human adjudication.

The model may be a local classifier, an embedding-based system, a hosted
constrained decision model, or a structured-output generative model. At least
one offline implementation must remain available.

## Build

Choose one judgment that deterministic code cannot fully answer, such as:

- whether retrieved policy evidence is relevant to the request
- whether the final answer accounts for every material exception
- whether the task should be escalated for human review

Create a labelled dataset with representative positive, negative, ambiguous,
and safety-critical cases. Split it into:

```text
training or prompt development
threshold selection and calibration
final held-out evaluation
```

Do not use final held-out labels to choose the operating threshold.

For every prediction, preserve the verifier version, question or rubric
version, selected value, full probability distribution where available, input
version, and latency. Keep the invariant the reference bundle keeps:
`confidence` is the probability of the value you selected, derived from the
distribution rather than carried beside it, so the two cannot drift apart.

## Measure

Report:

- class counts and error costs
- precision, recall, and confusion matrix
- Brier score or log loss
- reliability by confidence bucket
- selective accuracy and coverage at candidate thresholds
- false accepts and false rejects, including raw counts
- p50/p95 latency and measured cost

Then choose an operating policy such as:

```text
accept automatically when confidence >= high_threshold
send to a reasoning verifier in the middle band
send to human review below low_threshold or on safety disagreement
```

The thresholds must follow from a declared constraint, for example:

```text
Maximize automation coverage subject to precision >= 0.98 and zero observed
safety false accepts in the threshold-selection set.
```

If no threshold satisfies your constraint, say so and stop. That is a finding,
not a failure — and it is what the reference verifier does.

## Adversarial Check

Add at least ten hard cases designed after inspecting the verifier's failures.
Examples include irrelevant evidence with overlapping keywords, confident but
unsupported conclusions, reversed approval conditions, and incomplete answers
that look polished.

Keep these cases as a named adversarial slice rather than blending them into the
aggregate.

## Deliverable

Submit:

1. Dataset and split manifest.
2. Versioned verifier contract or rubric.
3. Predictions with probabilities and provenance.
4. Calibration and risk-coverage report.
5. Selected thresholds and escalation policy, or a stated refusal.
6. Adversarial-slice results.
7. A recommendation: adopt, reject, or keep testing.

## Checks

Run your own predictions through the committed metrics rather than
hand-rolling them:

```bash
python3 - <<'PY'
import json
from evals.verifier_calibration import (
    brier_score, expected_calibration_error, confusion_at,
    reliability_buckets, select_threshold,
)

rows = [json.loads(line) for line in open("your-predictions.jsonl") if line.strip()]
dev = [row for row in rows if row["label_role"] == "threshold_selection"]
held = [row for row in rows if row["label_role"] == "verifier_eval"]

selection = select_threshold(dev, min_precision=0.98, max_false_accepts=0)
print("policy:", selection)
print("held-out ECE:", expected_calibration_error(held))
print("held-out Brier:", brier_score(held))
if selection.get("threshold") is not None:
    print("held-out errors:", confusion_at(held, selection["threshold"]))
for bucket in reliability_buckets(held):
    print(bucket)
PY
```

Your rows need `label` (`success`/`failure`), `probabilities`, and
`label_role`. The lab passes when you can answer:

- What fraction of cases can be automated at the required precision?
- How many false accepts and false rejects were observed, as raw counts?
- Was the threshold chosen without looking at final test labels?
- Which cases require a stronger verifier rather than a lower threshold?
- What change in data distribution would invalidate the operating policy?

## Reference

Compare against
[`evals/verifier_calibration/strongbench/calibration-report.md`](../../../evals/verifier_calibration/strongbench/calibration-report.md).

```bash
python3 -m evals.verifier_calibration
```

The reference verifier reads only the trace, because that is all a production
verifier has. Read the slice table before the reliability tables. It says the
verifier looks acceptable where it was developed — expected calibration error
**0.08** on the threshold-selection split, four false accepts — and then shows
**83 false accepts** on the adversarial slice, where the top confidence band
averages **0.91** confidence against an observed success rate of **0.03**.

The answers were polished. The totals were wrong. Nothing in the aggregate said
so, and raising the threshold does not help, because the cases this verifier
misses are the ones it is most confident about. That is the shape of the
problem you are looking for in your own numbers.
