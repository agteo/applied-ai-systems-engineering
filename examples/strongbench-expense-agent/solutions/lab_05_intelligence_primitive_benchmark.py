#!/usr/bin/env python3
"""Reference solution: Lab 5, Intelligence Primitive Benchmark.

    python solutions/lab_05_intelligence_primitive_benchmark.py

One bounded decision — what shape of work this request needs — answered four
different ways, on the same versioned input, under the same decision contract.
The point is not that one candidate wins. It is that the winner is chosen from
a table instead of from a habit.

The label comes from `required_tools` in the committed benchmark, not from any
candidate's own output. Labelling with the scripted planner's behaviour would
score the scripted planner against itself. That is a derived label, not a human
judgment, and the report says so.

No third-party dependencies: the classifier is a bag-of-words nearest centroid
in about thirty lines, because "use a classifier" should not mean "install a
framework" before you know whether the classifier helps.
"""

from __future__ import annotations

import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strongbench_agent.agent import run_agent
from strongbench_agent.models import ScriptedModel

REPO_ROOT = Path(__file__).resolve().parents[3]
TASKS_PATH = REPO_ROOT / "evals" / "strongbench_benchmark" / "tasks.jsonl"

QUESTION_VERSION = "work-shape-v1"
INPUT_VERSION = "strongbench-benchmark-v1"

#: Every task needs `search_policy`, so routing on the first tool would be a
#: constant. The decision worth making is what the task needs *beyond* it.
PLANS = ["policy_only", "receipt", "calculate", "receipt_calculate", "approval"]

#: Missing a required approval is not worth one point. Track it separately.
SAFETY_PLAN = "approval"

#: Hand-written routing rules, in priority order. This is the baseline every
#: other candidate has to beat, and it costs nothing to run.
RULES = [
    (r"\bapprov|\bsubmit\b|\bon behalf\b|\bmanager\b", "approval"),
    (r"\breceipt\b|\brcpt-|\bexpense id\b", "receipt"),
    (r"\btotal\b|\bhow much\b|\bcalculat|\bclaim\b|\$|\busd\b", "calculate"),
]


def main() -> int:
    tasks = load_tasks()
    labelled = [(task, plan_label(task["required_tools"])) for task in tasks]

    # Even ids develop, odd ids are held out. Same split rule as the Level 2
    # calibration bundle, so the two artifacts can be read together.
    dev = [(task, label) for task, label in labelled if int(task["id"].split("-")[-1]) % 2 == 0]
    held = [(task, label) for task, label in labelled if int(task["id"].split("-")[-1]) % 2 == 1]

    centroids = fit_centroids(dev)
    candidates = {
        "rules": lambda task: rules_decision(task),
        "classifier": lambda task: centroid_decision(task, centroids),
        "structured_generative": lambda task: scripted_decision(task),
        "cascade": lambda task: cascade_decision(task, centroids),
    }

    print("Label source: required_tools in the committed benchmark (derived, not human)")
    print(f"Dev {len(dev)} tasks, held-out {len(held)} tasks, {len(PLANS)} classes")
    print(f"Held-out class counts: {dict(Counter(label for _, label in held))}\n")

    rows = []
    for name, decide in candidates.items():
        rows.append(evaluate(name, decide, held))

    rows.append(
        {
            "candidate": "hosted_decision_model",
            "accuracy": None,
            "coverage": None,
            "unsafe_errors": None,
            "p95_ms": None,
            "evidence": "not measured",
        }
    )

    print_table(rows)
    print_contract_example(candidates["cascade"], held[0][0])
    print_verdict(rows)
    return 0


# ---------------------------------------------------------------------------
# Candidates. Each returns the same decision record.
# ---------------------------------------------------------------------------


def decision(value: str | None, probabilities: dict[str, float] | None, model: str) -> dict:
    """The shared contract. `confidence` is derived, never carried separately."""
    record = {
        "value": value,
        "probabilities": probabilities,
        "confidence": probabilities[value] if probabilities and value else None,
        "model": model,
        "question_version": QUESTION_VERSION,
        "input_version": INPUT_VERSION,
    }
    return record


def rules_decision(task: dict) -> dict:
    prompt = task["prompt"].lower()
    for pattern, plan in RULES:
        if re.search(pattern, prompt):
            return decision(plan, None, "rules-v1")
    return decision("policy_only", None, "rules-v1")


def fit_centroids(dev: list[tuple[dict, str]]) -> dict[str, Counter]:
    """One bag-of-words centroid per class, with document-frequency weighting."""
    per_action: dict[str, Counter] = defaultdict(Counter)
    doc_freq: Counter = Counter()
    for task, label in dev:
        tokens = set(tokenize(task["prompt"]))
        per_action[label].update(tokens)
        doc_freq.update(tokens)
    total = max(len(dev), 1)
    centroids = {}
    for action, counts in per_action.items():
        weighted = Counter()
        for token, count in counts.items():
            idf = math.log(total / (1 + doc_freq[token])) + 1.0
            weighted[token] = count * idf
        centroids[action] = normalize(weighted)
    return centroids


def centroid_decision(task: dict, centroids: dict[str, Counter]) -> dict:
    vector = normalize(Counter(tokenize(task["prompt"])))
    scores = {action: cosine(vector, centroid) for action, centroid in centroids.items()}
    for plan in PLANS:
        scores.setdefault(plan, 0.0)
    probabilities = softmax(scores)
    value = max(probabilities, key=probabilities.get)
    return decision(value, probabilities, "nearest-centroid-v1")


def scripted_decision(task: dict) -> dict:
    """The structured-output generative candidate.

    Offline this is `ScriptedModel`, which produces the tool calls an LLM
    should produce. Swap `get_model("claude-sonnet-5")` in and the row becomes
    a measurement of a real model instead of its stand-in — the contract does
    not change, which is the whole point of the seam.

    It is scored on the tools it actually reached for, mapped through the same
    label function as every other candidate. No candidate defines its own
    ground truth.
    """
    outcome = run_agent(
        task["prompt"],
        model=ScriptedModel(employee_id=task["employee_id"]),
        task_id=task["id"],
    )
    tools = [
        step["tool_name"]
        for step in outcome.trace.to_dict().get("steps", [])
        if step.get("tool_name")
    ]
    return decision(plan_label(tools), None, "scripted-reference-v1")


def cascade_decision(task: dict, centroids: dict[str, Counter]) -> dict:
    """Rules first, classifier when the rules do not fire confidently."""
    prompt = task["prompt"].lower()
    for pattern, action in RULES:
        if re.search(pattern, prompt):
            return decision(action, None, "cascade-v1(rules)")
    classified = centroid_decision(task, centroids)
    if classified["confidence"] is not None and classified["confidence"] >= 0.35:
        return decision(classified["value"], classified["probabilities"], "cascade-v1(classifier)")
    return decision("policy_only", None, "cascade-v1(default)")


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


def evaluate(name: str, decide, held: list[tuple[dict, str]]) -> dict:
    latencies = []
    correct = 0
    answered = 0
    unsafe_errors = 0
    for task, label in held:
        start = time.perf_counter()
        record = decide(task)
        latencies.append((time.perf_counter() - start) * 1000)
        if record["value"] is None:
            continue
        answered += 1
        if record["value"] == label:
            correct += 1
        # The asymmetric error: the task required a human approval step and
        # this candidate did not route to one. Not worth one point.
        if label == SAFETY_PLAN and record["value"] != SAFETY_PLAN:
            unsafe_errors += 1
    latencies.sort()
    return {
        "candidate": name,
        "accuracy": round(correct / answered, 3) if answered else 0.0,
        "coverage": round(answered / len(held), 3) if held else 0.0,
        "unsafe_errors": unsafe_errors,
        "p95_ms": round(latencies[int(len(latencies) * 0.95) - 1], 3) if latencies else 0.0,
        "evidence": f"measured on {len(held)} held-out tasks",
    }


def print_table(rows: list[dict]) -> None:
    print("| Candidate | Accuracy | Coverage | Unsafe routes | p95 ms | Evidence |")
    print("| --- | ---: | ---: | ---: | ---: | --- |")
    for row in rows:
        fmt = lambda value: "-" if value is None else value  # noqa: E731
        print(
            f"| {row['candidate']} | {fmt(row['accuracy'])} | {fmt(row['coverage'])} | "
            f"{fmt(row['unsafe_errors'])} | {fmt(row['p95_ms'])} | {row['evidence']} |"
        )
    print()


def print_contract_example(decide, task: dict) -> None:
    print("--- One decision record ---")
    print(json.dumps(decide(task), indent=2, sort_keys=True))
    print()


def print_verdict(rows: list[dict]) -> None:
    measured = [row for row in rows if row["accuracy"] is not None]
    best = max(measured, key=lambda row: row["accuracy"])
    cheapest = min(measured, key=lambda row: row["p95_ms"])
    print("--- Verdict ---")
    print(f"Highest accuracy: {best['candidate']} at {best['accuracy']}")
    print(f"Lowest p95 latency: {cheapest['candidate']} at {cheapest['p95_ms']} ms")
    print()
    print("Read the table as a frontier, not a ranking. A candidate is only")
    print("rejected when something beats it on every column you care about.")
    print("The hosted row stays 'not measured' until someone measures it;")
    print("a vendor number is not evidence about this workload.")


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def load_tasks(path: Path = TASKS_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def plan_label(tools: list[str]) -> str:
    """Map a set of tools to the work shape. One function, every candidate."""
    required = set(tools)
    if "request_human_approval" in required:
        return "approval"
    if {"lookup_receipt", "calculate_reimbursement"} <= required:
        return "receipt_calculate"
    if "lookup_receipt" in required:
        return "receipt"
    if "calculate_reimbursement" in required:
        return "calculate"
    return "policy_only"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z0-9-]+", text.lower())


def normalize(counts: Counter) -> Counter:
    norm = math.sqrt(sum(value * value for value in counts.values())) or 1.0
    return Counter({token: value / norm for token, value in counts.items()})


def cosine(left: Counter, right: Counter) -> float:
    smaller, larger = (left, right) if len(left) < len(right) else (right, left)
    return sum(value * larger.get(token, 0.0) for token, value in smaller.items())


def softmax(scores: dict[str, float], temperature: float = 0.15) -> dict[str, float]:
    """Rounded to four places, and still summing to exactly one.

    Rounding each entry independently leaves a distribution that sums to
    0.9999, which fails the contract check this lab asks you to run. The
    residual goes on the largest entry, where it is least visible.
    """
    highest = max(scores.values())
    exponentiated = {key: math.exp((value - highest) / temperature) for key, value in scores.items()}
    total = sum(exponentiated.values()) or 1.0
    rounded = {key: round(value / total, 4) for key, value in exponentiated.items()}
    largest = max(rounded, key=rounded.get)
    rounded[largest] = round(rounded[largest] + (1.0 - sum(rounded.values())), 4)
    return rounded


if __name__ == "__main__":
    raise SystemExit(main())
