# Lab 5: Calibrated Verifier

## Objective

Build or evaluate a narrow semantic verifier whose confidence can safely route
cases to automatic acceptance, stronger review, or human adjudication.

The model may be a local classifier, an embedding-based system, a hosted Type 1
decision model such as Jev, or a structured-output generative model. At least
one offline implementation must remain available.

## Build

Choose one judgment that deterministic code cannot fully answer, such as:

- whether retrieved policy evidence is relevant to the request
- whether the final answer accounts for every material exception
- whether the task should be escalated for human review

Create a human-reviewed dataset with representative positive, negative,
ambiguous, and safety-critical cases. Split it into:

```text
training or prompt development
threshold selection and calibration
final held-out evaluation
```

Do not use final held-out labels to choose the operating threshold.

For every prediction, preserve the verifier version, question or rubric
version, selected value, full probability distribution where available, input
version, and latency.

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
5. Selected thresholds and escalation policy.
6. Adversarial-slice results.
7. A recommendation: adopt, reject, or keep testing.

## Pass Conditions

The lab passes when the learner can answer:

- What fraction of cases can be automated at the required precision?
- How many false accepts and false rejects were observed?
- Was the threshold chosen without looking at final test labels?
- Which cases require a stronger verifier rather than a lower threshold?
- What change in data distribution would invalidate the operating policy?

