# Model Improvement

## Focus

Model Improvement teaches which intelligence component should change and when
better deterministic code, prompting, retrieval, tooling, a specialised
decision model, workflow design, or a frontier API is the better intervention.

This track includes post-training, but it should not treat training as the default answer.

## Core Skills

- data sufficiency assessment
- training/test split discipline
- contamination checks
- SFT data preparation
- preference data design
- LoRA and QLoRA experiments
- DPO concept planning
- model comparison
- classifier and decision-model comparison
- calibration and selective prediction
- confidence-gated cascades
- local versus hosted model tradeoffs
- cost, latency, privacy, and governance analysis

## Reference Stack

The preferred stack should stay open-source-first where possible:

```text
Python
Hugging Face datasets and transformers
PEFT
TRL where appropriate
local or low-cost hosted compute
```

Commercial APIs and hosted training should be comparison points, not required for the core learning path.

Hosted Type 1 systems such as Jev are optional candidates, not curriculum
dependencies. Compare them with rules, embedding or encoder classifiers,
structured-output generative models, and local alternatives on the same
versioned decision contract.

## Portfolio Evidence

A learner completing this track should have:

- a model improvement decision memo
- a curated training dataset
- a dataset card
- a training config if training is run
- a model comparison report
- benchmark evidence showing whether the intervention helped

Reference artifacts:

- Phase 5A bundle: [`model_improvement/strongbench/`](../model_improvement/strongbench/)
- assessment anchor:
  [`examples/reference-artifacts/model-improvement-decision/`](../examples/reference-artifacts/model-improvement-decision/)
- portfolio example:
  [`examples/portfolio/model-improvement.md`](../examples/portfolio/model-improvement.md)
