# Intelligence and Verification Architecture

## Purpose

Applied AI systems should not ask one large generative model to perform every
kind of computation. Planning, writing, routing, scoring, extraction,
verification, and control have different requirements. The durable engineering
skill is choosing the cheapest adequately reliable primitive for each job and
measuring how those primitives behave together.

This course calls the non-generative half of that set **constrained decision
models**: systems that answer one predefined question with a value, score, or
distribution over a fixed set, rather than with open-ended text. The category
includes classical and neural classifiers, embedding models, rerankers, reward
models, and safety classifiers, alongside hosted products that expose the same
shape. It is named for what the component does, not for any vendor's framing of
it; current examples are indexed in
[references.md](references.md) and will date faster than the category will.

The core curriculum must remain runnable offline. Hosted decision systems are
optional comparison candidates, just like hosted generative models.

## Two Interlocking Loops

```text
POLICY LOOP                            VERIFICATION LOOP

Agent / model -> environment -> outcome
      ^                         |
      |                         v
      |                 deterministic checks
      |                 decision models
      |                 reasoning judges
      |                 human review
      |                         |
      +------ data / reward ----+
```

The policy loop chooses and executes actions. The verification loop measures
whether the actions and outcomes were correct, safe, efficient, and supported
by evidence. Neither loop is trustworthy merely because its output is typed or
fluent.

## Choose the Intelligence Primitive

Before choosing a model, ask: **what kind of computation is this?**

| Job | Default primitive |
| --- | --- |
| Exact calculation or invariant | deterministic code |
| Database or record lookup | query or tool |
| Semantic routing | classifier or decision model |
| Candidate ranking | reranker |
| Extraction into a known schema | extractor or constrained model |
| Complex synthesis or planning | autoregressive reasoning model |
| Objective success checking | deterministic verifier |
| Narrow semantic judgment | classifier or decision model |
| Ambiguous, evidence-heavy judgment | reasoning or agentic verifier |
| High-consequence unresolved case | human or subject-matter expert |

This table is a starting hypothesis, not a law. Benchmark competing primitives
on representative data before adoption.

## Decision Systems and Verifiers Are Different Roles

A **decision system** maps state and a predefined question to a constrained
answer, score, ranking, or probability distribution. It may route work, select
a tool, or recommend escalation.

A **verifier** judges a claim, action, trajectory, or outcome against evidence
and a success criterion. The same underlying classifier may implement both
roles, but the system contract and evaluation question are different.

A provider-neutral decision record should preserve:

```json
{
  "question_id": "approval-routing-v3",
  "value": "escalate",
  "probabilities": {
    "continue": 0.08,
    "escalate": 0.89,
    "stop": 0.03
  },
  "confidence": 0.89,
  "model": "provider/model-version",
  "input_version": "finance-state-v2",
  "created_at": "2026-09-19T00:00:00Z"
}
```

Typed output prevents schema drift; it does not make the selected answer true.
Probability fields are operational only after calibration on representative,
held-out data.

## Verifier Cascade

Use the least expensive tier that can answer the question reliably:

```text
Tier 0  Ground truth: tests, schemas, database state, permissions, calculations
Tier 1  Narrow judgment: classifiers, rerankers, constrained decision models
Tier 2  Deliberative verification: reasoning model, rubric, evidence, tools
Tier 3  Human adjudication: SME review and new gold labels
```

This is a routing policy, not a mandatory serial pipeline. A Tier 0 safety
failure can veto immediately. A calibrated Tier 1 result can accept, reject, or
escalate. Tier 2 should be reserved for cases whose ambiguity justifies its
cost. Tier 3 resolves consequential uncertainty and supplies data for improving
the earlier tiers.

Each verifier must declare:

- the question it answers and evidence it may inspect
- its output schema and whether it can veto, advise, or contribute reward
- the dataset and metrics used to evaluate it
- its confidence threshold and escalation behavior
- its version, provenance, and known failure modes

## Calibration Is a Control Property

Accuracy measures how often a decision is right. Calibration measures whether
confidence predicts how often it is right. A system that acts automatically at
high confidence depends on both.

Learners should evaluate decision systems with:

- class-specific precision, recall, and error costs
- Brier score or log loss
- reliability diagrams and calibration error
- selective accuracy and risk-coverage curves
- automation coverage at a required precision or safety level
- abstention and escalation rates
- latency, cost, schema validity, and repeatability

Thresholds must be chosen on development data and reported before final
held-out evaluation. Choosing a threshold on the test set leaks the answer.

## Eval the Verifier

Verifier output is another probabilistic system, not ground truth. The complete
quality loop is:

```text
evaluate the policy
        -> evaluate verifier agreement against trusted labels
        -> test whether the policy can exploit the verifier
        -> evaluate the combined system under distribution shift
```

False accepts can corrupt benchmark results and training data. False rejects
can suppress valid strategies. Process judgments and outcome judgments should
be recorded separately so a successful outcome does not erase a reckless
trajectory, and an environmental blocker is not blamed on the policy.

## Curriculum Thread

| Level | Decision and verifier emphasis |
| --- | --- |
| 1 Build | choose the intelligence primitive; separate routing, generation, tools, and checks |
| 2 Evaluate | classifiers, calibration, thresholds, abstention, and verifier evaluation |
| 3 Diagnose | false accepts/rejects, miscalibration, schema errors, shift, and rubric failures |
| 4 Data | labels, hard negatives, disagreements, calibration sets, and provenance |
| 5 Improve | compare rules, specialised models, generative models, and cascades |
| 6 Environments | implement tiered verifier stacks and preserve component outputs |
| 7 RL | study dense verifier rewards, verifier hacking, and uncertainty-aware training |

## Cumulative Practicums

1. **Intelligence Primitive Benchmark:** implement one routing task with rules,
   a classifier, a hosted constrained decision model where available, a structured-output
   generative model, and a cascade. Compare the Pareto frontier rather than
   declaring a universal winner.
2. **Calibrated Verifier:** label agent trajectories, measure calibration, and
   choose an operating threshold that maximizes coverage subject to a precision
   or safety constraint.
3. **RL Against a Flawed Verifier:** expose a policy to an incomplete reward,
   identify the exploit, strengthen the verifier stack, and verify on a frozen
   adversarial set that the exploit did not merely move.

