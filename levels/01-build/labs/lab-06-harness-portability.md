# Lab 6: Harness Portability

Build or compare two adapters that use the same agent harness. The goal is to
show that tool permissions, state, and evaluation interfaces belong to the
harness even when model behavior changes.

## Setup

Inspect `agent.py`, `models.py`, `schemas.py`, and `tools.py` in the reference
agent. The supplied scripted adapter is an offline planner, not a trained model;
the Anthropic adapter requires a configured provider and may incur cost. For a
fully offline exercise, write a second test adapter that emits different valid
and invalid calls. Label that comparison as a harness contract test, not a
comparison of two real models. As an extension, run two actual models through
compatible adapters and record their identifiers and configuration.

## Tasks

1. Draw the boundary between adapter, context assembly, state, tools, approval,
   final-answer validation, and trace capture. Describe what is retained across
   steps and what would be lost or distorted by context compaction. Identify a
   memory retention or deletion rule for a hypothetical persistent deployment;
   do not claim the reference agent implements persistent memory.
2. Use the same tasks and tool schemas with both adapters. Capture their traces
   and structured outputs. Record model/adapter version and relevant settings.
3. Probe an invalid tool argument and an attempted restricted action. Confirm
   that the harness or tool boundary prevents execution, regardless of the
   adapter's proposal. Check approval state and record the observed result.
4. Document how reusable instructions are included and how an escalation to a
   different model or a human would be triggered. Identify which controls must
   remain enforced after escalation.
5. Compare behavior, cost and latency where measured. Differences in answers
   or action sequences are findings, not automatic contract failures.

## Deliverables

A boundary diagram, two trace bundles, a table of shared contracts and observed
results, and a short note on context, memory, permissions, escalation and
limitations. Identify any control the reference implementation does not supply.

## Checks

Run the offline reference from `examples/strongbench-expense-agent`:

```bash
python solutions/lab_06_harness_portability.py
```

It checks invalid arguments and denial by the simulated approval tool. The
reference agent has no submit tool and does not implement a general permission
engine; identify that limitation in your boundary analysis.


- Both adapters use the same schemas and harness entry point; trace and final
  answer checks run on each bundle, or failures are documented with causes.
- The invalid and restricted probes show the boundary response and whether an
  action executed. A model's promise to refuse is not evidence of enforcement.
- The comparison identifies an offline test double honestly and does not claim
  that equal interfaces imply equal model quality.

## Reference

Compare the [offline reference solution](../../../examples/strongbench-expense-agent/solutions/lab_06_harness_portability.py), then read the [model adapters](../../../examples/strongbench-expense-agent/strongbench_agent/models.py),
[harness](../../../examples/strongbench-expense-agent/strongbench_agent/agent.py),
[tool definitions](../../../examples/strongbench-expense-agent/strongbench_agent/tools.py),
and [trace checker](../../../examples/strongbench-expense-agent/strongbench_agent/check_traces.py).
