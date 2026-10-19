# Lesson 8: Isolation and Verifier Validation

## Core Idea

An environment makes behavior measurable only if each episode begins in the
intended state and its checks can distinguish success from a plausible failure.
A simulator with copied state is not automatically a sandbox for arbitrary code.
Treat episode isolation, execution isolation, and verifier validity as separate
contracts with separate evidence.

## Episode State and Reset

The finance reference creates an initial state and `run_scripted_policy` copies
it before each rollout. Compare the initial and terminal hashes in
[rollouts](../../../environments/strongbench_finance/rollouts.jsonl), then read
[the implementation](../../../environments/strongbench_finance/__init__.py).
A reset contract should state which state is restored, which seed and task are
used, what remains intentionally persistent, and how failures are handled.

Test a clean episode, two sequential episodes, and concurrent episodes. Verify
that each initial state matches its expected snapshot and that changes in one
cannot affect the other. A fresh initial hash is useful evidence, but a hash
alone does not inspect hidden resources or shared services. A reference that
copies in-memory state provides no isolation guarantee for files, network or
external services.

## Execution Boundaries

Before exposing untrusted agent code, define who can execute what, allowed file
paths, network egress, credentials, CPU, memory, time and output limits, and the
lifecycle of temporary state. Test controls using harmless probes in an
appropriately isolated environment. A container, a Python mock, or a stated
policy is not by itself proof that all boundaries are enforced. Record the actual
runtime configuration and limitations; stop rather than use production resources
when a safe test environment is unavailable.

## Validate the Verifier

Build a labeled set before measuring verifier quality: valid completions,
ordinary failures, unauthorized actions, corrupted unrelated records and
adversarial shortcuts. Compare each verifier's result with trusted labels and
inspect disagreements. A false accept is a failed task accepted as success; a
false reject is a valid task rejected. Report counts and denominators per slice,
not only accuracy. Review label uncertainty and what the verifier cannot observe.

In the finance [probe rollouts](../../../environments/strongbench_finance/probe-rollouts.jsonl),
the reward hacker supplies a correct total without looking up receipts. The
`deterministic_total` check alone cannot expose that shortcut; process and policy
checks can catch this particular probe. Do not generalize that result to every
possible attack. Compare with the [code-repair transfer note](../../../environments/code_repair/transfer-note.md):
contracts can be shared while domain-specific state and evidence differ.

## Calibrate Difficulty

The task generator derives labels from task features. Compare those labels with
observed pass rates for multiple policies on the same held-out tasks and inspect
disagreement. A task hard for one policy may be easy for another; low counts and
nonrepresentative policies limit the conclusion. Do not use difficulty labels as
proof of a reliable ordering without this evidence.

## Common Failure Modes

- Shallow-copying nested mutable state and leaking one episode into another.
- Calling a process or container a sandbox without testing its actual boundaries.
- Treating a final state snapshot as proof that no forbidden action happened.
- Measuring a verifier against labels produced by the same verifier.
- Reporting a 100% catch rate on a single probe as general safety.

## Exercise

Run the existing [finance tests](../../../environments/tests/test_phase6_strongbench_finance.py),
then complete [Lab 5](../labs/lab-05-reset-and-isolation.md) and
[Lab 6](../labs/lab-06-verifier-validation.md). Explain one failure that a state
hash could miss and one task for which a correct answer could hide an unsafe
trajectory. Compare the finance and code-repair contracts.

## Checkpoint

You can distinguish reset evidence, execution isolation evidence and verifier
accuracy; state what was tested and what remains unknown.
