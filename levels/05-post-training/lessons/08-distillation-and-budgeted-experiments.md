# Lesson 8: Distillation and Budgeted Experiments

## Core Idea

Distillation uses a teacher's outputs or judgments to create learning signals for
another model. In a practical agent workflow, a stronger teacher can produce
candidate corrections for a smaller student. A teacher response is a proposal,
not ground truth: it may be confidently wrong, contain unauthorized actions, or
reflect data the student should not memorize.

The intervention decision starts in Level 4. Here the question is narrower: can
changing weights, including with teacher-generated examples, outperform a prompt,
tool, retrieval or harness change on the same task under real constraints?

## From Failure to Training Example

1. Start with an observed failure and its trace, task and version provenance.
   Identify whether the failure belongs to the model, tools, context or grader.
2. Split by task family or source before creating variants. Freeze independent
   evaluation tasks and prevent near-duplicates or corrections from leaking.
3. Provide only permitted data to the teacher. Record teacher version, prompt,
   generation settings, licenses and provider terms applicable to the intended
   use. Do not assume every model's outputs may be used for training.
4. Check each proposed correction against trusted policy, deterministic checks
   and, where necessary, human review. Reject unsafe actions, unsupported claims,
   and examples whose correctness cannot be established; keep a rejection log.
5. Convert accepted examples to the student model's chat template. Retain links
   to the source failure and correction. Inspect class balance and synthetic
   template repetition; a plausible answer is not necessarily a correct label.
6. Compare the original student, student with a prompt or harness improvement,
   teacher if available, and trained student using the same held-out cases and
   compatible system interfaces. Report paired results, safety slices, cost,
   latency, uncertainty and failure modes. Separate training and inference cost.

For a concrete data trail inspect the [failure annotations](../../../evals/operations/strongbench/annotated-failures.jsonl),
[SFT export](../../../model_improvement/strongbench/sft-train.jsonl),
[rejected rows](../../../model_improvement/strongbench/sft-rejected.jsonl), and
[dataset card](../../../datasets/strongbench/dataset-card.md). These artifacts
are preparation, not evidence that a teacher or student was trained.

## Budget the Experiment Before Running

Set a ceiling on GPU-hours and spend, data generation calls, evaluation calls,
wall time and the number of candidate runs. Define a smoke test for mechanical
correctness, a small set of justified configurations, and stop conditions for
cost, safety failures, non-finite loss and repeated infrastructure errors.
Log data and code versions, seeds, model and tokenizer revisions, configuration,
checkpoint provenance, evaluation configuration and actual consumption. An
agent may propose configurations, but it must operate inside the same budget,
isolation and human approval controls as any other automation.

A smoke test establishes that the pipeline runs. It does not establish the
student improved. Select on development data and evaluate the selected candidate
once against an untouched held-out set; state when more testing is needed.

## Common Failure Modes

- Training on teacher output without validating correctness or usage rights.
- Reusing failure corrections from the final evaluation as training examples.
- Comparing an adapted system with a weaker prompt or a different tool set and
  attributing the whole difference to the weights.
- Reporting only loss or teacher agreement, while ignoring safety and actual
  task outcomes.
- Presenting a dry-run configuration or generated data as a completed run.

## Exercise

Choose one failure in the annotations. Design a teacher prompt and a rejection
check, identify its split before generation, and write a budgeted comparison of
student, harness-improved student and trained student. Use the
[comparison report](../../../model_improvement/strongbench/comparison-report.md)
to distinguish existing measurements from proposed runs. Identify which evidence
would lead you not to train or not to adopt.

## Checkpoint

You can explain the provenance and trust of each example, the protected
comparison, the budget and stop rules, and the evidence required to claim that
post-training added value.
