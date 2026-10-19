# Lab 6: Failure-to-Distillation Experiment

Design a comparison that can show whether teacher-generated data and modified
weights add value. The required offline path is an experiment design and data
audit; a real teacher or training run is optional and must be labeled separately.

## Tasks

1. Select at least three source failures and inspect their trace, diagnosis and
   existing corrections. Document source IDs, allowed use and split assignment
   before making new examples. Quarantine related tasks and near duplicates.
2. Design a teacher prompt and generate or hand-author illustrative corrections.
   Record the source of each; hand-authored examples are not teacher outputs.
   Apply deterministic checks and human review where available. Keep rejected
   examples and explain why correctness or usage rights may be uncertain.
3. Pre-register the four candidates: original small model, prompt/harness
   improvement, teacher where available, and student trained on accepted data.
   Keep tasks, tools, evaluator versions and held-out data comparable. Include
   safety, paired outcomes, uncertainty, latency, training and inference costs.
4. Set GPU-hour, spend, run-count and wall-time budgets, a smoke test, stop rules,
   checkpoint and experiment logging, and an adoption rule that can reject the
   trained student. See the [training-run plan](../../../model_improvement/strongbench/reference-training-run-plan.md).
5. Optional: run the experiment on suitable compute with permitted models and
   data; preserve actual configs, metrics and artifacts. If not run, mark results
   pending and make no claim about teacher or student performance.

## Deliverables

A provenance and split manifest, accepted/rejected examples, experiment and
budget plan, comparison table with evidence status, and adoption decision or
explicit deferral. A completed Track 5B requires the real run, adapter and report
specified by its project.

## Checks

- Each example identifies its source and split; held-out and related variants
  never enter teacher-generated training data or student training. Evaluating a
  teacher on held-out tasks does not permit reusing those outputs for training.
- Teacher outputs have correctness and permission checks, not just format checks.
- The decision rule includes paired quality, safety, latency and actual costs;
  unrun candidates are marked pending, never reported as measured.

## Reference

Compare the [training data](../../../model_improvement/strongbench/sft-train.jsonl),
[rejected rows](../../../model_improvement/strongbench/sft-rejected.jsonl),
[comparison report](../../../model_improvement/strongbench/comparison-report.md),
and [run plan](../../../model_improvement/strongbench/reference-training-run-plan.md).
