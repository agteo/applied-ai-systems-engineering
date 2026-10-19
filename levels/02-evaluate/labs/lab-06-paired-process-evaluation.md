# Lab 6: Paired and Process Evaluation

A correct answer does not prove an agent acted safely. Design a comparison that
measures improvement and makes missing evidence visible.

## Tasks

1. Pre-register a hypothesis, baseline, one intervention, task sampling method,
   primary metric, safety slices, decision rule, and evaluation budget. Freeze the
   graders and reserve held-out cases before tuning. Identify which randomness
   (task selection, model sampling, or both) your uncertainty addresses.
2. Evaluate both configurations on the same task IDs. Report the four paired
   counts: both pass, only A passes, only B passes, and both fail. The difference
   in pass rates is `(only B - only A) / n`. For example, on 100 tasks, 65 both
   pass, 5 only A, 13 only B and 17 neither gives 70% versus 78%, an 8-point
   difference. Report an appropriate interval for the paired difference, its
   method and assumptions; do not infer significance from separate intervals.
3. Evaluate each case on three axes: final outcome, recorded actions, and final
   state. Construct or inspect a fixture where the answer is correct but a
   forbidden tool call occurs, and another where an unrelated record changes.
   Record initial state, allowed action policy, trace, and final state. These are
   learner-created fixtures unless an existing environment supplies them.
4. Report missing observations as **unknown**. Decide whether a correct answer
   with a forbidden action passes your safety gate and explain why. Test your
   grader against a known-bad trace and a corrupted state, and document any
   case it cannot detect.
5. Compare two public benchmarks, such as BFCL and τ-bench, by task family,
   version, scoring, harness and likely blind spots for an expense workflow.
   Use their official documentation; do not treat leaderboard scores as proof
   of production readiness.

## Deliverables

An experiment plan, paired-results table and interval, an outcome/action/state
matrix with evidence, grader checks, a benchmark comparison and a decision note
that names uncertainty, safety regressions and contamination risks.

## Checks

- The paired counts sum to the task count and reproduce both pass rates. The
  interval measures the paired difference, not two unrelated rates.
- A forbidden action fails its policy check even when the answer is correct; a
  changed unrelated record fails the state invariant. Missing trace or state is
  unknown, not pass. State whether observations were simulated or captured.
- The decision is conditional on sample size and representativeness; zero
  observed failures is not proof of zero risk.

## Reference

Use the [benchmark tasks](../../../evals/strongbench_benchmark/tasks.jsonl),
[grader implementation](../../../evals/strongbench_benchmark/graders/deterministic.py),
[finance environment](../../../environments/strongbench_finance/), and
[metrics lesson](../lessons/05-metrics-and-confidence.md). The current output
graders do not by themselves establish every action and state invariant above.
