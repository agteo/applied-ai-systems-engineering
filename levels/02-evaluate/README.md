# Level 2: Evaluate

## Goal

Build reproducible evaluations that show whether an agent works, where it works, where it fails, and whether a change improved behavior.

Level 1 asked: can we build an agent?

Level 2 asks: how do we know the agent is good?

## Learning Outcomes

By the end of this level, learners can:

1. Design an eval dataset for realistic agent tasks.
2. Separate task success, answer quality, tool correctness, cost, and latency.
3. Implement deterministic graders for structured outputs.
4. Use rubric graders for subjective quality.
5. Use LLM-as-judge carefully and calibrate it against human review.
6. Detect regressions between agent versions.
7. Produce an eval report that supports an engineering decision.
8. Measure calibration and choose confidence thresholds for automation,
   escalation, or abstention.
9. Evaluate verifier false accepts and false rejects against trusted labels.
10. Design paired comparisons, report uncertainty and evaluator limitations, and
    interpret representative public benchmarks and their versions.
11. Distinguish final outcome, observed actions, and resulting environment state.

## Required Build

Learners build the first benchmark for StrongBench Expense Agent v1.

The benchmark should include at least 100 tasks covering policy questions, receipt lookup, reimbursement calculation, approval requirements, ambiguity, and unsafe requests.

## Evaluation Architecture

```text
Task Dataset
    |
    v
Agent Run
    |
    v
Trace + Final Answer
    |
    +-- deterministic graders
    +-- rubric graders
    +-- LLM judge
    +-- classifier / decision verifier
    +-- human review sample
    |
    v
Eval Report
```

## Concepts

### Eval Dataset

An eval dataset is a set of tasks designed to measure behavior. It should include expected outcomes, grading metadata, and enough variation to reveal failure modes.

### Golden Tasks

Golden tasks are hand-authored cases with trusted expected answers. They are expensive to create but useful for regression testing.

### Graders

Graders convert an agent run into scores, labels, or comments.

Use deterministic graders where possible. Use LLM judges for qualities that are hard to encode directly, then calibrate those judges against human review.

### Metrics

The main Level 2 metrics are:

- task success rate
- structured output validity
- policy citation accuracy
- tool-call correctness
- approval safety
- cost
- latency
- judge agreement with human review
- Brier score or log loss
- calibration error and reliability by confidence bucket
- automation coverage at a required precision or safety level
- verifier false-accept and false-reject rates

### Experiment Design and Benchmark Literacy

Specify the hypothesis, baseline, intervention, task sampling, metric and decision
rule before comparing agents. Run both versions on the same tasks and report the
paired changes, sample sizes and uncertainty. Protect held-out data from tuning,
check judge bias, and report critical slices separately. A fixed benchmark may not
represent deployment traffic, and small slices cannot establish low failure rates.

Public benchmarks such as BFCL, τ-bench, GAIA, SWE-bench and IFEval measure
different task families. Record the version, harness and scoring protocol before
interpreting a score; use custom workflow evaluations for local requirements.
See [Lab 6](labs/lab-06-paired-process-evaluation.md).

### Outcomes, Actions, and State

Check what the agent answered, what its trace shows it did, and what state it
left behind. A correct answer can coexist with an unauthorized action or a damaged
record. A trace alone cannot prove the resulting state; a state snapshot alone
cannot prove no forbidden action occurred. When the environment does not expose
the evidence needed, report the check as unavailable rather than passing it.

### Regression

An eval should be reusable. If a prompt, model, tool, or retrieval change improves one area while damaging another, the benchmark should make that visible.

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | Why evals matter | Evaluation questions |
| 2 | Eval dataset design | Task schema |
| 3 | Deterministic graders | Output and policy graders |
| 4 | Rubrics and judges | Calibrated judge prompt |
| 5 | Metrics and confidence | Score summary |
| 6 | Regression evaluation | Version comparison |
| 7 | Eval reports | Decision-ready report |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Eval Task Schema](labs/lab-01-eval-task-schema.md) | Design task records for the benchmark. |
| [Lab 2: Deterministic Graders](labs/lab-02-deterministic-graders.md) | Grade structured output, citations, and approvals. |
| [Lab 3: Rubric Judge](labs/lab-03-rubric-judge.md) | Build and calibrate an LLM judge. |
| [Lab 4: Eval Report](labs/lab-04-eval-report.md) | Turn scores into an engineering recommendation. |
| [Lab 5: Calibrated Verifier](labs/lab-05-calibrated-verifier.md) | Evaluate probabilities and choose an automation threshold. |
| [Lab 6: Paired and Process Evaluation](labs/lab-06-paired-process-evaluation.md) | Compare versions and evaluate outcomes, actions, and state. |

## Project

The Level 2 project is [StrongBench Expense Agent Benchmark v1](project/strongbench-expense-agent-benchmark-v1.md).

## Exit Criteria

To complete Level 2, the learner must submit:

1. At least 100 eval tasks.
2. A documented task schema.
3. At least three deterministic graders.
4. One rubric grader or LLM judge.
5. A human-reviewed judge-agreement sample.
6. A benchmark report comparing at least two agent configurations.
7. A short note explaining what the benchmark does not measure.
8. A calibrated-verifier report with a threshold selected on development data.
9. A paired comparison and a process/state evaluation with stated evidence limits.
10. A comparison of two public benchmarks and their applicability to the task.

The learner should be able to explain whether an observed improvement supports
a decision, including the paired task results, uncertainty, safety slices,
evaluator limitations and what the benchmark does not measure. A difference in
two separate confidence intervals is not a substitute for analyzing the paired
difference.
