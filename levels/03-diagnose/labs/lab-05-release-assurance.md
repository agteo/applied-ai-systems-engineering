# Lab 5: Release Assurance

An offline gate is useful evidence, not automatic authority to deploy. Decide
whether to ship, restrict, or delay a candidate when evidence is incomplete.

## Scenario

A candidate passes the aggregate regression gate and improves policy answers.
On the same tasks, an approval-boundary slice has few examples and one new
unsafe action. The production distribution and frequency of that action are
unknown. Treat this as a hypothetical scenario, not a claim about the reference
agent. The candidate is intended to prepare expense recommendations, not submit
real reimbursements.

## Tasks

1. Trace the unsafe action through observation → evidence → hypothesis →
   intervention → experiment → result. Distinguish the trace, the inferred
   cause, and evidence that would falsify the hypothesis. Consider a faulty
   grader as a competing explanation.
2. Decide whether to ship, restrict, or delay. State the authority and effects
   of the proposed deployment, critical thresholds, what is unknown, and which
   risk cannot be justified by an aggregate score. If you choose a restricted
   rollout, specify enforced boundaries rather than relying on the model.
3. Design a shadow test: production inputs are processed without external side
   effects, observations are compared with the existing workflow, and sensitive
   data is governed. Specify sampling, adjudication, duration or stopping rule,
   and what shadow mode cannot measure.
4. Specify deployment monitoring, an incident owner, escalation and rollback
   triggers, a rollback mechanism, and post-incident evidence retention. Explain
   how a confirmed failure becomes a regression case.

## Deliverables

A one-page release decision with the evidence chain, unknowns, release or
restriction conditions, shadow plan, monitors, incident process, rollback and
next experiment.

## Checks

- The decision addresses the unsafe action and the limited slice size; passing
  the aggregate gate alone is not sufficient justification.
- The shadow plan prevents side effects and names a comparison and stop rule.
- Every proposed trigger has an owner and a response, and the diagnosis
  distinguishes observed facts from hypotheses.

## Reference

Compare the [release recommendation](../../../evals/operations/strongbench/release-recommendation.md),
[annotated failures](../../../evals/operations/strongbench/annotated-failures.jsonl),
and [regression pack](../../../evals/operations/strongbench/regression-pack.jsonl).
The hypothetical incident and shadow rollout are not represented as real runs.
