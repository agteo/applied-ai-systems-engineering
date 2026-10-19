# Lab 6: Verifier Validation and Difficulty

Construct an independent set of valid, invalid and adversarial cases and measure
what the verifier actually catches.

## Tasks

1. Define trusted labels and evidence requirements before reading verifier
   outputs. Include valid alternative trajectories, incorrect final state,
   forbidden actions, unrelated-record corruption, missing evidence and at least
   one shortcut that achieves the expected answer without the required process.
2. Run your verifier on these cases. Report true accepts, false accepts, true
   rejects and false rejects, with denominators and per-slice results. Examine
   disagreements and label uncertainty. Keep new probes separate from cases used
   to tune the verifier.
3. Inspect the finance reward-hacking policy and compare its deterministic total
   with process checks. Explain which shortcut it demonstrates and which attacks
   it does not cover. Add a domain-specific probe from code repair or your own
   environment; avoid claiming a single caught probe establishes general safety.
4. Compare task difficulty labels with held-out results from at least two
   policies. Report slice counts and disagreements; a policy-relative pass rate
   and a generator-derived difficulty label are different measurements.

## Checks

Run the existing finance and code-repair verifier tests from the repo root:

```bash
python3 -m pytest environments/tests/test_phase6_strongbench_finance.py environments/tests/test_workstream_d_code_repair.py
```

Submit the labeled cases, confusion counts, evidence and blind spots, a known
bad policy caught by your checks, and a known limitation. The task-difficulty
comparison must name policies, versions, task counts and sample limitations.

## Reference

Use the [finance verifier report](../../../environments/strongbench_finance/verifier-report.md),
[probe rollouts](../../../environments/strongbench_finance/probe-rollouts.jsonl),
[code-repair tests](../../../environments/tests/test_workstream_d_code_repair.py), and
[task generation lesson](../lessons/04-task-generation.md).
