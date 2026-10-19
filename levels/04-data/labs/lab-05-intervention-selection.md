# Lab 5: Intervention Selection

Use Level 3 evidence to choose and test an improvement without assuming model
training is the answer. Work against the StrongBench agent or an equivalent
runnable system.

## Tasks

1. Select a failure supported by a trace, grader output or state evidence.
   Compare at least three candidate interventions across harness, tools,
   retrieval, instructions, routing, data or model. State the expected effect,
   owner, implementation effort, risk, and cost/latency implications of each.
2. Choose one intervention and write a pre-run experiment: baseline and candidate
   versions, hypothesis and alternative explanation, task IDs and frozen graders,
   safety invariants, paired metric, cost/latency budget and decision rule.
3. Implement the change and run the same tasks on both configurations. Report
   paired counts and slice results, the measurement method, regressions, cost and
   latency. If a measurement cannot be collected, mark it unknown rather than
   inventing a value. Protect final held-out cases from iteration.
4. Make a ship, restrict, or delay recommendation, including shadow testing,
   monitoring, incident owner, human escalation and rollback triggers. Explain
   what evidence would change the decision.
5. Describe whether the existing Level 4 dataset could help this or a later
   intervention. Do not claim a trained model improved without a training run
   and an independent evaluation.

## Deliverables

An intervention matrix, experiment record and reproducible before/after results,
a regression case tied to the failure, and a release recommendation. Link the
Level 4 dataset card and describe its intended use and limitations.

## Checks

- The chosen intervention addresses an evidenced cause and is compared with at
  least two alternatives; the decision is justified under stated constraints.
- Same-task results and safety checks are reproducible, or the limitations are
  disclosed. Aggregate improvements do not hide a critical regression.
- The release recommendation has concrete monitoring and rollback conditions,
  and the dataset and any unrun training remain accurately described.

## Reference

Use the [failure report](../../../evals/operations/strongbench/failure-report.md),
[experiment record](../../../evals/operations/strongbench/intervention-experiment.md),
[dataset card](../../../datasets/strongbench/dataset-card.md), and
[Level 5 decision materials](../../../model_improvement/strongbench/).
