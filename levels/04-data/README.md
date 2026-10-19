# Level 4: Agent Improvement Systems

## Goal

Select, test, and operationalize an intervention using failure evidence and constraints. Turn agent traces, failures, human corrections, and synthetic examples into a defensible dataset when data can support improvement.

Level 3 asked: why did the agent fail?

Level 4 asks: which intervention should we try, what evidence would justify it,
and what data would support this or a later improvement cycle?

## Learning Outcomes

By the end of this level, learners can:

1. Design schemas for agent training and evaluation data.
2. Clean and deduplicate messy traces.
3. Convert failures into demonstrations, corrections, and preference examples.
4. Generate synthetic examples with quality filters.
5. Separate training, development, and evaluation data.
6. Document dataset provenance, limitations, and quality metrics.
7. Publish a dataset card.
8. Build classifier, verifier, calibration, and adversarial datasets without
   contaminating final evaluation.
9. Compare prompt, tool, retrieval, harness, routing, data, model and human
   workflow interventions against evidence, risk, cost and latency.
10. Test a targeted change against a baseline and defend a release decision.

## Improvement Loop

Use the Level 3 evidence to compare candidate interventions, choose an owner and
one testable change, freeze a baseline and evaluation, run the comparison, inspect
regressions and costs, then decide whether to ship, restrict, delay or gather more
evidence. Data work remains essential where examples, labels or verifier coverage
are the constraint. See [the improvement lesson](lessons/08-agent-improvement-systems.md)
and [Lab 5](labs/lab-05-intervention-selection.md).

## Pipeline

```text
Production traces
      +
Eval failures
      +
Human examples
      +
Synthetic examples
      +
Human decision labels and disagreements
      |
      v
Clean -> Classify -> Deduplicate -> Filter -> Score -> Dataset
```

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | Agent data types | Data inventory |
| 2 | Schemas and formats | JSONL schema |
| 3 | Cleaning and deduplication | Cleaned dataset |
| 4 | Synthetic data | Generated examples |
| 5 | Preference and correction data | Preference pairs |
| 6 | Splits and contamination | Split manifest |
| 7 | Dataset cards | Dataset card |
| 8 | Agent improvement systems | Intervention decision and experiment |

Decision-system projects must additionally inventory class labels, hard
negatives, disagreement cases, confidence-bearing predictions, and the frozen
calibration and adversarial sets used to evaluate verifiers.

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Trace to Dataset](labs/lab-01-trace-to-dataset.md) | Convert traces into structured examples. |
| [Lab 2: Cleaning Filters](labs/lab-02-cleaning-filters.md) | Deduplicate and filter low-quality rows. |
| [Lab 3: Synthetic Examples](labs/lab-03-synthetic-examples.md) | Generate examples from diagnosed failures. |
| [Lab 4: Dataset Card](labs/lab-04-dataset-card.md) | Document the dataset for future training. |
| [Lab 5: Intervention Selection](labs/lab-05-intervention-selection.md) | Compare and test improvement options under constraints. |

## Project

The Level 4 project combines [Agent Training Dataset v1](project/agent-training-dataset-v1.md) with the intervention decision and experiment in [Lab 5](labs/lab-05-intervention-selection.md).

## Exit Criteria

To complete Level 4, the learner must submit:

1. A dataset schema.
2. A raw data inventory.
3. A cleaned and filtered dataset.
4. Training, development, and held-out splits.
5. Quality metrics.
6. Provenance documentation.
7. A dataset card.
8. For a learned verifier: separate training, calibration/threshold-selection,
   and final held-out evaluation sets.
9. An intervention comparison, reproducible experiment and release recommendation
   with cost, latency, safety, uncertainty and follow-up evidence.
