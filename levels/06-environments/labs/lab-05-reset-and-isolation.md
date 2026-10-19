# Lab 5: Reset and Isolation

Prove that episode state does not leak and describe the separate execution
boundaries required if an agent can run untrusted code.

## Tasks

1. State the reset contract: seed, initial snapshot, task identity, persistent
   resources, and expected cleanup after success, failure and timeout.
2. Run one finance task twice sequentially and two tasks concurrently. Check
   each rollout's initial hash against a fresh initial state, and verify the
   supplied base state remains unchanged. Use the same seed intentionally.
3. In a disposable learner copy, replace a deep copy with a shallow copy or
   shared object. Show a test that fails after a nested write. Restore the
   implementation and rerun the check. Do not change the shared reference.
4. Specify a separate sandbox boundary: filesystem, network egress, secrets,
   process, time, memory and output limits, teardown and observability. If a
   suitable isolated runtime is available, test harmless probes there; otherwise
   provide a test plan and mark enforcement unverified. Never probe production.
5. Compare the shared environment contract with code repair. Identify what must
   be reset in each domain and what the common runner does not guarantee.

## Checks

From the repository root, run this read-only probe:

```bash
python3 - <<'PY'
from concurrent.futures import ThreadPoolExecutor
from environments.strongbench_finance import generate_tasks, initial_state, run_scripted_policy, state_hash
base = initial_state(42)
expected = state_hash(base)
tasks = generate_tasks(seed=42, count=2)
sequential = [run_scripted_policy(task, base) for task in tasks]
with ThreadPoolExecutor(max_workers=2) as pool:
    parallel = list(pool.map(lambda task: run_scripted_policy(task, base), tasks))
assert all(r['initial_state_hash'] == expected for r in sequential + parallel)
assert state_hash(base) == expected
print('Sequential and concurrent rollouts preserved the supplied initial state.')
PY
```

This probes these in-memory rollouts, not arbitrary code or external resource
isolation. Submit a failing leakage test from your disposable copy, its passing
result after repair, and a boundary table separating tested and untested controls.

## Reference

Read the [finance environment](../../../environments/strongbench_finance/__init__.py),
[environment contract](../../../environments/contract.py), and
[code-repair transfer note](../../../environments/code_repair/transfer-note.md).
