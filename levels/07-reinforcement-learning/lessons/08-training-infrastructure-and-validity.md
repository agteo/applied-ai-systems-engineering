# Lesson 8: Training Infrastructure and Reward Validity

## Core Idea

A rising reward curve tells you the training system found higher-scoring
behavior. It does not by itself establish improved real task performance. To
interpret it, preserve the environment, verifier, reward, policy and evaluation
versions and inspect behavior against evidence the policy did not train on.

The repo currently contains an offline rollout-analysis bundle and training
plans, not a completed RL run. See the [experiment plan](../../../rl_reliability/strongbench/experiment-plan.md)
and [reward-hacking review](../../../rl_reliability/strongbench/reward-hacking-review.md).

## Training System Anatomy

A coordinator assigns tasks and seeds to rollout workers. Each worker loads a
versioned policy, runs episodes in an isolated environment, and emits traces,
termination reasons, verifier components and resource usage. A trainer consumes
eligible rollouts, applies updates, and writes checkpoints containing model,
optimizer and scheduler state, random state and training progress where supported.
A separate evaluator measures frozen checkpoints on held-out tasks and safety
slices. Tracking records versions, actual budget, throughput, utilization,
errors and samples so another engineer can reconstruct the decision.

Retries, timeouts, worker failures and stale policies change the data a trainer
sees. Record them; ensure retries do not contaminate state or double-count
rollouts. Restart from a checkpoint only if the saved state and environment
versions support the intended continuation; otherwise disclose the discontinuity.
Utilization is a diagnostic, not a quality metric.

## Example: Reward Improves, Success Does Not

The following numbers are **illustrative**, not a run from this repository.
A pre-training policy averages reward 0.4 and succeeds on 42/100 held-out tasks.
A candidate averages reward 0.8 and succeeds on 41/100 held-out tasks. A review
finds more attempts that cite policy identifiers without retrieving them. The
training verifier rewards the citation string; an independent process check
flags the missing retrieval. Suppose both candidates have 0 observed violations
on a 10-task safety slice: that small sample cannot establish that risk is zero.

The reward increase is real within this hypothetical record, but it does not
show improved task success. Investigate verifier and label quality, run matched
comparisons with uncertainty, preserve held-out cases, and reject or defer the
candidate under the predeclared decision rule. A verifier fix changes the
measurement instrument: version it and re-evaluate both policies rather than
comparing unlike scores.

## Optional Bounded Implementation

An actual training path requires a suitable model, data rights, isolated
runtime, compute and a validated environment adapter. Before running, specify a
smoke test, maximum GPU-hours and spend, model and environment versions, held-out
seeds and task families, safety invariants, termination and rollback conditions,
and who can approve or stop compute use. Save training logs, checkpoints,
learning curves, sampled rollouts, independent benchmark results, failure
analysis and actual usage. A successful smoke run only shows the pipeline works.

An automated agent can propose or execute approved experiments, but must not
silently expand its budget or edit held-out data, verifier rules or adoption
criteria. Human review and an explicit stopping mechanism remain part of the
experiment design. Autonomous experimentation is an optional extension.

## Common Failure Modes

- Treating training reward or GPU utilization as evidence of capability.
- Evaluating only on training tasks or changing the verifier between baselines.
- Resuming a checkpoint without compatible optimizer, seed or environment state.
- Ignoring failed rollouts, retries or safety slices in the aggregate.
- Reporting an illustrative case or training configuration as a completed run.

## Exercise

For the illustrative case above, identify the train-time proxy and independent
outcome, compute the held-out difference in successes, and explain why the safety
sample is inconclusive. Propose a verifier fix and an evaluation that compares
both policies under the same revised rules. Complete
[Lab 6](../labs/lab-06-training-validity.md) for the full decision.

## Checkpoint

You can trace a training result from policy and worker through verifier,
checkpoint and independent evaluation, name its limits, and defend a decision
under the declared budget and safety constraints.
