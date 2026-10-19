# Lab 6: Training Infrastructure and Reward Validity

Analyze a training record and decide whether the policy should be adopted. The
required offline scenario below is illustrative: it is not a completed training
run. Replace it with a real, consented run when one is available.

## Scenario

| Evidence | Baseline | Candidate |
| --- | ---: | ---: |
| Mean training-verifier reward | 0.4 | 0.8 |
| Independent held-out task success | 42/100 | 41/100 |
| Observed unsafe actions on safety slice | 0/10 | 0/10 |

A sampled candidate trace cites a policy without retrieving it; the training
verifier checks the citation string but an independent process verifier checks
retrieval. The table does not provide paired outcomes, confidence intervals,
label agreement, or a representative safety sample.

## Tasks

1. Diagram workers, policy versions, environment and verifier, rollout store,
   trainer, checkpoint and independent evaluator. Record the versions and
   checkpoint state required to reproduce or resume a run. Include worker
   failure, retries, duplicate rollout handling, resource accounting and isolation.
2. Explain why reward went up without demonstrated task improvement. List the
   evidence in the scenario, alternative hypotheses, unknown paired counts and
   missing labels. Do not infer statistical significance from the aggregates.
3. Propose a verifier repair, an adversarial regression and a matched baseline
   versus candidate evaluation using the same new verifier and held-out tasks.
   Specify safety slices, sample limitations and a predeclared adoption rule.
4. Produce a ship, restrict or delay recommendation and a training budget,
   including GPU-hours, spend, wall time, checkpoint and stop rules. Specify what
   an experiment agent could propose or execute and how limits are enforced.
5. Optional: apply the rubric to a real training run. Include logs, curves,
   checkpoints, sampled rollouts, versions, independent evaluations and actual
   usage. Label every result as measured, illustrative or unavailable.

## Checks

- The hypothetical candidate is not credited with improved task success merely
  because reward rose. The safety slice does not establish zero risk.
- The verifier change is versioned and both policies are rescored using it;
  development and held-out tasks remain separate.
- The plan includes explicit budget and stopping authority; no fabricated run,
  checkpoint or utilization measurement appears in the report.

## Reference

Use the [experiment plan](../../../rl_reliability/strongbench/experiment-plan.md),
[reward-hacking review](../../../rl_reliability/strongbench/reward-hacking-review.md),
and [hosted training report template](../../../rl_reliability/strongbench/hosted-rl-report-template.md).
