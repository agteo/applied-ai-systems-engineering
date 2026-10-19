# L5 Post-training Run: Instructions and Reproducibility Requirements

**Status: full training environment and reference run pending.** The repository
provides prepared examples, an optional configuration and a dry-run validator;
it does not provide a validated end-to-end training runtime, trained adapter,
training logs or learning curves. Bring your own suitable local or hosted
compute, model, training software and evaluation integration. These instructions
are framework-independent: the exact installation and training commands depend
on your choices and are not supplied as a tested recipe.

The no-GPU exercise is to complete steps 1–4 as a plan. Completing Track 5B
requires an actual run, checkpoint and comparison as described below.

## 1. Choose and document your setup

- Choose a base model and compatible tokenizer and record immutable revisions,
  licenses, and any access restrictions. Confirm model, data and teacher-output
  terms permit training and intended publication.
- Supply an isolated runtime with sufficient memory and storage for the chosen
  model, adapter, optimizer, checkpoints and evaluation. Record hardware,
  operating system, Python, accelerator drivers, library versions, precision and
  distributed configuration. Do not put credentials in submitted artifacts.
- Choose an SFT/LoRA-capable trainer and evaluator. Document their versions,
  installation steps and exact commands, including how the trained adapter is
  loaded into the same agent/tool interface. Compatibility and capacity depend
  on your setup; verify them before budgeting a full run.

## 2. Prepare data and evaluation

1. Review the repository's [SFT training data](sft-train.jsonl),
   [development data](sft-dev.jsonl), [rejection log](sft-rejected.jsonl) and
   [dataset card](../../datasets/strongbench/dataset-card.md). Audit provenance,
   correctness, privacy and any teacher-generated content.
2. Identify the task families and source traces represented by each split.
   Reserve an independent held-out set, including safety cases, that has not
   been used for model selection, prompt tuning or correction generation. The
   repository's Level 2 benchmark is not automatically held out: verify that
   training examples and near duplicates derived from it are excluded. If you
   cannot establish independence, create new held-out cases and disclose it.
3. Apply the chosen model's chat template. Record train/dev/held-out manifests,
   counts, hashes, tokenization and truncation policy; keep held-out examples out
   of training and teacher-generated corrections. Check any new data manually
   and against objective policy and safety rules.
4. Freeze the task set, grader, agent harness and evaluation settings. Choose
   metrics, critical slices and an adoption rule before training. Select models
   and hyperparameters on development data only.

## 3. Record baselines and budget

Run the untrained model and a prompt or harness-improved alternative on the same
evaluation tasks and tool contracts. Evaluate the teacher only if available;
mark unavailable results as such. Record task-level outcomes, safety incidents,
latency and inference cost. Specify maximum GPU-hours, spend, wall time and run
count, plus stop rules for unsafe behavior, non-finite loss or infrastructure
failure. Predeclare how you will choose a checkpoint and decide whether to adopt.

## 4. Validate the planned run

From the repository root, run the existing offline configuration check:

```bash
python3 -m model_improvement.strongbench.train_lora --dry-run
```

This validates the template and data preparation; it does not train a model or
validate a third-party runtime. In your own runtime, run a short smoke test that
loads the model, reads the training data, performs an update, saves a checkpoint
and reloads it. Record the command and outcome. Stop and fix a failed smoke test
before the budgeted run; a passing smoke test is not an improvement result.

## 5. Train and evaluate

Run the bounded experiment in your own runtime. Capture exact commands and
resolved configuration, train/development losses, sampled outputs, checkpoints,
errors, runtime and actual resource use. Choose the checkpoint using the
predeclared development rule. Evaluate it and the baselines with the frozen
held-out tasks, graders, tools and safety checks. Report task-level paired
outcomes, slice counts, uncertainty, regressions, latency, training and inference
cost, and known evaluation limitations. Report a negative or inconclusive result
as such; do not infer task improvement from lower training loss.

## Reproducibility requirements and submission

Submit a run manifest containing:

- Repository commit and any local diff; model/tokenizer immutable revisions and
  licenses; trainer, runtime and package versions; hardware and precision.
- Dataset, task, prompt, tool, grader and environment versions; split manifests,
  counts and hashes; data access and publication limits.
- Seeds, model and LoRA configuration, preprocessing and chat template, exact
  commands, budget, stop rules, checkpoint-selection rule and actual consumption.
- Checkpoint or adapter and loading instructions when permitted; otherwise an
  access-controlled location or explicit explanation. Include logs, learning
  curves, sampled outputs, task-level baseline/candidate results, safety review
  and a decision against the predeclared criteria.

Provide enough information for another learner with authorized access to repeat
the process. Seeds alone do not guarantee identical results across hardware,
library versions or nondeterministic operations; record those limitations.
Reference [Lab 6](../../levels/05-post-training/labs/lab-06-distillation-experiment.md)
and the [Track 5B project](../../levels/05-post-training/project/base-vs-prompted-vs-finetuned.md).
