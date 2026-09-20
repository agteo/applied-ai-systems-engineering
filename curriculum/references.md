# References and Tooling Anchors

The curriculum should be pressure-tested against prior work. Learners should know when they are following established patterns, adapting them, or intentionally building something smaller for pedagogy.

This page is the index. Each reference is also assigned to the lesson where it does real work, because a repo-level reading list is a list nobody reads at the moment it would have helped.

| Reference | Read it during |
| --- | --- |
| Inspect | [Level 2, Lesson 1: Why evals matter](../levels/02-evaluate/lessons/01-why-evals-matter.md) and [Lesson 4: Rubrics and LLM judges](../levels/02-evaluate/lessons/04-rubrics-and-llm-judges.md) |
| OpenAI Evals | [Level 2, Lesson 1: Why evals matter](../levels/02-evaluate/lessons/01-why-evals-matter.md) |
| SWE-bench | [Level 2, Lesson 3: Deterministic graders](../levels/02-evaluate/lessons/03-deterministic-graders.md) |
| WebArena-Verified | [Level 2, Lesson 3: Deterministic graders](../levels/02-evaluate/lessons/03-deterministic-graders.md) |
| tau2-bench | [Level 3, Lesson 2: Failure taxonomies](../levels/03-diagnose/lessons/02-failure-taxonomies.md) and [Level 6, Lesson 1: Environment thinking](../levels/06-environments/lessons/01-environment-thinking.md) |
| WebArena | [Level 6, Lesson 1: Environment thinking](../levels/06-environments/lessons/01-environment-thinking.md) |
| TRL and PEFT | [Level 5, Lesson 4: LoRA and QLoRA](../levels/05-post-training/lessons/04-lora-and-qlora.md) and [Level 7, Lesson 5: PPO and GRPO](../levels/07-reinforcement-learning/lessons/05-ppo-and-grpo.md) |
| ML prerequisite courses | [Level 5, Lesson 2: ML foundations](../levels/05-post-training/lessons/02-ml-foundations.md) |
| Universal Verifier | [Level 6, Lesson 5: Rewards and success checks](../levels/06-environments/lessons/05-rewards-and-success-checks.md) |
| RLCR | [Level 2, Lesson 5: Metrics and confidence](../levels/02-evaluate/lessons/05-metrics-and-confidence.md) |
| AgentV-RL | [Level 7, Lesson 2: Rewards and reward hacking](../levels/07-reinforcement-learning/lessons/02-rewards-and-reward-hacking.md) |

## Evaluation Frameworks

- [Inspect](https://inspect.aisi.org.uk/?lang=en-US): an open-source framework for large language model evaluations with datasets, agents, tools, scorers, sandboxing, and agent evaluation support.
- [OpenAI Evals](https://github.com/openai/evals): a framework and benchmark registry for evaluating LLMs and LLM systems, including custom evals.

## Agent And Environment Benchmarks

- [tau2-bench](https://github.com/sierra-research/tau2-bench): a benchmark for tool-agent-user interaction in real-world domains, with policies, tools, tasks, and evaluation criteria.
- [SWE-bench](https://github.com/princeton-nlp/SWE-bench): a benchmark for evaluating LLMs on real software issues using reproducible Docker-based evaluation.
- [WebArena](https://github.com/web-arena-x/webarena): a self-hostable web environment for evaluating autonomous agents on realistic web tasks.
- [WebArena-Verified](https://servicenow.github.io/webarena-verified/): a verified release emphasizing audited tasks, deterministic scoring, and offline evaluation from traces.

## Post-Training Tooling

- [TRL](https://huggingface.co/docs/trl/en/index): a Hugging Face library for training transformer language models with methods such as SFT, DPO, GRPO, reward modeling, and related post-training workflows.
- [PEFT](https://huggingface.co/docs/peft/en/index): parameter-efficient fine-tuning methods, including the LoRA implementation Track 5B uses.

## Decision And Verifier Systems

The course calls this category **constrained decision models** and teaches it
provider-neutrally. Hosted products in the category are optional comparison
candidates, and their launch materials date quickly: treat any speed, cost, or
comparative performance figure as a vendor claim until it is reproduced on the
course benchmark. No lesson depends on one being available.

- [Microsoft Research: The Art of Building Verifiers for Computer Use Agents](https://www.microsoft.com/en-us/research/articles/the-art-of-building-verifiers-for-computer-use-agents/): evidence for specific rubric design, separating process and outcome, and evaluating verifier quality against human labels.
- [RLCR: Beyond Binary Rewards](https://openreview.net/pdf?id=ASQ649zdHm): calibration-aware reinforcement learning using a proper scoring rule, relevant to confidence-aware reward design. Note that it trains for calibration, which is a different intervention from selecting a threshold after the fact.
- [AgentV-RL](https://arxiv.org/abs/2604.16004): an example of multi-turn, tool-augmented verification for tasks too complex for a narrow classifier.

## ML Prerequisites

Track 5B requires a real training run, and Level 5's ML foundations lesson is a prerequisite gate rather than a course. Complete one of these first:

- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1): the closest fit to this curriculum's library stack.
- [fast.ai Practical Deep Learning for Coders](https://course.fast.ai/): best if you have never trained a model.
- [Karpathy, Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html): best for making backpropagation concrete.

## How These Influence The Course

This repo should not ask learners to reinvent prior art blindly.

The StrongBench curriculum intentionally starts smaller than these systems, but it should borrow their discipline:

- explicit task schemas
- reproducible environments
- deterministic scoring where possible
- clear grader limitations
- task quality review
- trace capture
- benchmark versioning
- cost-aware evaluation
- held-out test sets
- model comparisons on the same benchmark
