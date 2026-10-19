# Lesson 8: Agent Improvement Systems

## Core Idea

An improvement is a tested change to the system, not a choice of a more
powerful model. Diagnose the failure, identify the component that can change it,
and compare plausible interventions within the constraints of the workflow.
Data is one lever: it can improve retrieval, verifiers, supervised examples and
models, but a data pipeline does not itself prove better agent behavior.

## Work from Evidence to a Decision

The [StrongBench failure report](../../../evals/operations/strongbench/failure-report.md)
identifies receipt lookup, item parsing, and approval-boundary issues. Consider
these candidates before choosing an experiment:

| Observation | Candidate intervention | What could falsify it? |
| --- | --- | --- |
| Receipt lookup fails | Improve search or tool descriptions | Matched receipt cases do not improve, or incorrect retrieval increases |
| Item extraction fails | Validate structured extraction or add clarifying questions | Parsing improves but task completion or escalation cost worsens |
| Approval boundaries fail | Enforce permissions and explicit approval in the harness | A forbidden action still executes in an adversarial test |
| Inconsistent specialist behavior | Curate examples; evaluate a fine-tuned model only if justified | No held-out improvement over prompt and harness baselines |

These are hypotheses, not measured results. A stronger model may be one option,
but a permission boundary must be enforced independently of model compliance.
The best intervention is the one supported by evidence and feasible under the
risk, cost, latency, maintenance and data constraints.

## Run the Loop

1. Record baseline version, task IDs, grader and environment versions, relevant
   trace and state evidence, and cost and latency measurement method.
2. Select a single testable intervention and a competing explanation. Choose a
   primary metric, safety invariants, budget, and decision rule before running.
3. Run the same evaluation cases for baseline and candidate. Report paired
   results, critical slices, uncertainty, failed checks, cost and latency.
4. Use development data to iterate; protect the held-out cases for the final
   comparison. Promote confirmed failures to a versioned regression pack.
5. Decide to ship, restrict or delay. Specify how shadow testing, monitoring,
   human escalation and rollback will address evidence gaps. An offline pass
   does not prove production safety.
6. If data is the right next investment, use the preceding Level 4 lessons to
   create a documented, split and quality-checked dataset. If training is a
   candidate, compare it with non-training baselines in Level 5.

## Common Failure Modes

- Treating the most expensive model as the intervention without diagnosing the
  failure or measuring cost and latency.
- Improving an aggregate while degrading a rare safety-critical slice.
- Optimizing repeatedly on the held-out evaluation, or changing the grader with
  the candidate and attributing the score to the agent.
- Calling an offline gate a deployment decision without operational controls.
- Treating a synthetic example or a dataset card as proof of model improvement.

## Exercise

Use the failure report and the [intervention experiment](../../../evals/operations/strongbench/intervention-experiment.md).
Select one failure, propose two interventions, and specify a matched-task test
that could reject each hypothesis. The reference experiment reports 0/30 and
89/100 on different sets; do not calculate a causal effect from those rates.
Write a release decision and list what additional evidence would change it.
Compare your work with [Lab 5](../labs/lab-05-intervention-selection.md).

## Checkpoint

You can name the observed failure, intervention owner, runnable baseline,
paired comparison, safety constraints, measurement limitations and release
conditions, and explain when data or training would be justified.
