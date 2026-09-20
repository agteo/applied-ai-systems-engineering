# Lab 5: RL Against a Flawed Verifier

## Objective

Demonstrate that improving reward can mean exploiting a verifier rather than
improving the intended behavior, then repair the measurement system.

This lab may use search, best-of-N selection, scripted adversarial policies, or
a real RL run. A training run is not required; the verifier exploit is.

## Setup

Start with a deliberately incomplete learned verifier or reward component. For
example, let it judge whether an answer appears to explain an approval decision
without checking whether the cited evidence was retrieved.

Freeze before optimization:

- a human-reviewed verifier evaluation set
- a named adversarial slice
- deterministic safety and state checks
- the policy benchmark and rejection gate

## Attack

Create or optimize a policy that raises the learned verifier's score while
violating the intended behavior. Preserve the complete trajectory and every
reward component.

Distinguish these hypotheses:

```text
H1: the policy improved the underlying task behavior
H2: the policy learned features that please the verifier
H3: both changed
```

Use deterministic outcomes and independent human or stronger-verifier review
to decide which hypothesis the evidence supports.

## Repair

Strengthen the system with at least three of:

- a deterministic veto
- a process verifier separate from the outcome verifier
- hard negatives derived from the exploit
- a confidence threshold and abstention path
- disagreement sampling for stronger-model or human review
- a verifier ensemble
- a held-out distribution-shift slice

Re-evaluate the repaired verifier on the frozen sets before optimizing against
it again. Adding the exploit cases to training and testing on the same cases is
not evidence of repair.

## Deliverable

Submit:

1. The original verifier contract and known blind spot.
2. The exploiting policy or trajectory set.
3. Before/after reward components and true outcome checks.
4. Human-reviewed false-accept and false-reject analysis.
5. The repaired verifier stack.
6. Results on the frozen adversarial set.
7. A statement of the remaining exploitable assumption.

## Rejection Rule

Reject the trained or selected policy if reward rises while deterministic task
success, independent review, or a protected safety slice regresses. A better
score from the verifier being optimized is not independent evidence.

