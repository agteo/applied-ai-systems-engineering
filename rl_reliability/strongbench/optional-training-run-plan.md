# L7 RL Training and Case Study: Instructions and Reproducibility Requirements

**Status: full RL training environment and reference training run pending.** The
repo provides an offline simulator and rollout-analysis materials, not a
validated end-to-end RL training runtime or a trained policy. The hosted adapter
is unvalidated; see [validation notes](../../integrations/prime-intellect/VALIDATION.md).
Learners may supply their own compute, model, trainer and compatible environment.
The exact setup and training commands depend on those choices and are not a
repo-tested recipe.

The GPU-free literacy path remains complete without training: analyze a public
or otherwise authorized training record, or use the clearly illustrative scenario
in [Lab 6](../../levels/07-reinforcement-learning/labs/lab-06-training-validity.md).
The illustrative scenario is practice, not a real training case study.

## Option A: Analyze a real training case study

1. Choose an accessible, documented run. Record its source, date, permission to
   use artifacts, model, training method, environment and evaluation details.
   An external run may use a different domain; explain how that limits transfer.
2. Collect its configuration, reward definition, training curves or logs,
   checkpoint details, sampled trajectories and independent evaluation results
   where available. Label missing evidence as unavailable; never invent it.
3. Compare baseline and candidate on the same held-out task set where the source
   supports it. Inspect task-level changes, safety slices, verifier failures and
   reward hacking; consider whether the evaluation actually measures the claim.
4. Write a decision with supporting evidence, unknowns, reproducibility limits
   and a proposed follow-up. If the source lacks the artifacts needed to verify
   the conclusion, say that the result cannot be independently established.

## Option B: Run a bounded experiment in your own environment

1. Select a model, trainer and resettable environment with documented action,
   observation, reward and verifier interfaces. Record the toolchain, hardware,
   model/data terms and immutable versions. If adapting the provided simulator,
   validate your own integration; the supplied hosted adapter is not validated.
2. Test reset, episode isolation, reward and verifier behavior with known-good,
   known-bad and adversarial trajectories. Define sandbox and network boundaries
   and use scoped credentials; a simulator alone is not a security sandbox.
3. Split tasks and seeds into training, development and final held-out sets;
   include independent safety and adversarial cases. Freeze the evaluation
   version and establish a baseline before training. Distinct seeds alone do not
   prove that generated tasks or their underlying data are independent.
4. Predeclare maximum GPU-hours, spend, wall time and run count; resource and
   safety stop conditions; checkpoint and resume policy; and an adoption rule.
   A human must be able to stop an automated experiment within these limits.
5. Perform a smoke run in your own runtime to test rollout generation, reward,
   an update and checkpoint save/reload. Fix failures before the full run. A
   smoke run establishes mechanics, not learning.
6. Run the bounded experiment, retaining configurations, logs, worker errors and
   retries, sampled rollouts, checkpoints and actual usage. Select the candidate
   with development data, then compare it with the baseline on the frozen held-out
   tasks, verifier and safety cases. Report paired outcomes, slice counts,
   uncertainty, regressions and any verifier exploit. Reward gain alone does not
   establish improvement.

## Reproducibility requirements and submission

For either option, submit a case-study report and evidence manifest containing:

- Source and evidence-access status, code commit and local changes, model and
  tokenizer revisions, licenses, trainer/runtime versions, hardware and precision.
- Environment, tools, tasks, seeds, verifier and reward versions; split manifests
  and hashes; relevant permissions and sandbox or network configuration.
- Exact commands or a source's documented procedure, resolved configuration,
  budget, stop rules, checkpoint-selection rule and actual resource use when
  known. For external studies, mark unavailable fields explicitly.
- Baseline and candidate definitions; checkpoint and resume state where available;
  logs, curves, sampled trajectories, independent evaluation and safety findings.
  Explain missing artifacts and data or model access restrictions.
- A conclusion tied to evidence, including negative or inconclusive outcomes,
  uncertainty and a plan to test remaining hypotheses. A seed does not by itself
  guarantee identical training behavior across runtime or hardware changes.

Publish checkpoints, trajectories or data only when permitted. If access is
restricted, document the constraint and how an authorized reviewer can inspect
what is available. The learner-supplied runtime and any external case study are
not validated by this repository merely because this checklist is complete.
