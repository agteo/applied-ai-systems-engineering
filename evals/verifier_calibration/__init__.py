"""Verifier calibration bundle.

    python3 -m evals.verifier_calibration

Level 2 asks whether an agent is good. This module asks the next question:
whether the *verifier* that judges the agent can be trusted to act on its own
confidence.

The trusted label here is the deterministic grader, which sees `expected.*`.
The verifier being measured is `trace-support-verifier-v1`, a cheap proxy that
sees only the trace — the situation you are in during production, where no
oracle exists. Its weights are hand-set, not fitted. It is deliberately naive
so that the calibration report has something real to find.

Nothing here is human-labelled. Every label is derived from the committed
benchmark oracle, and every row records that provenance.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AGENT_ROOT = ROOT / "examples" / "strongbench-expense-agent"
if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from evals.runner import BENCHMARK_DIR, load_tasks, run_benchmark  # noqa: E402
from evals.strongbench_benchmark.graders.deterministic import grade_task  # noqa: E402

DEFAULT_TASKS = BENCHMARK_DIR / "tasks.jsonl"
DEFAULT_OUT = ROOT / "evals" / "verifier_calibration" / "strongbench"

QUESTION_ID = "trace-support-v1"
VERIFIER_VERSION = "trace-support-verifier-v1"
INPUT_VERSION = "strongbench-benchmark-v1"
LABEL_SOURCE = "derived-from-benchmark-oracle"

#: Hand-set logistic weights. These were chosen to encode a plausible naive
#: prior — "more tool use and a citation means the answer is probably right" —
#: not fitted to the labels. The report exists to show where that prior fails.
WEIGHTS = {
    "bias": -2.2,
    "distinct_tools": 1.1,
    "has_citation": 1.6,
    "has_next_action": 0.5,
    "self_reported_high": 0.4,
    "tool_errors": -1.4,
    "missing_information": -0.35,
}

#: Confidence bands for the reliability table.
BUCKET_EDGES = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)

#: Adversarial mutations. Each keeps the answer looking polished while breaking
#: something the deterministic grader checks.
MUTATIONS = ("inflate_total", "drop_approvals", "drop_missing_information", "strip_citations")


# ---------------------------------------------------------------------------
# The verifier under test
# ---------------------------------------------------------------------------


def extract_features(trace: dict[str, Any]) -> dict[str, float]:
    """Features the verifier may look at. Trace only — never `expected`."""
    answer = trace.get("final_answer") or {}
    steps = trace.get("steps") or []
    tools = [step.get("tool_name") for step in steps if step.get("tool_name")]
    errors = sum(
        1
        for step in steps
        if isinstance(step.get("observation"), dict) and step["observation"].get("error")
    )
    return {
        "distinct_tools": float(len(set(tools))),
        "has_citation": 1.0 if _cited_sources(answer) else 0.0,
        "has_next_action": 1.0 if answer.get("next_action") else 0.0,
        "self_reported_high": 1.0 if answer.get("confidence") == "high" else 0.0,
        "tool_errors": float(errors),
        "missing_information": float(len(answer.get("missing_information") or [])),
    }


def predict(trace: dict[str, Any], *, row_id: str, label_role: str) -> dict[str, Any]:
    """Return one decision record.

    Invariant, relied on by every lab that consumes this file:
    `confidence == probabilities[value]`. Confidence is derived from the
    distribution, never carried alongside it, so the two cannot drift.
    """
    features = extract_features(trace)
    logit = WEIGHTS["bias"] + sum(WEIGHTS[name] * value for name, value in features.items())
    p_success = 1.0 / (1.0 + math.exp(-logit))
    # Round once, then derive the complement from the rounded value, so the
    # distribution sums to exactly one rather than to 0.9999.
    success = round(p_success, 4)
    probabilities = {"success": success, "failure": round(1.0 - success, 4)}
    value = "success" if probabilities["success"] >= probabilities["failure"] else "failure"
    return {
        "id": row_id,
        "question_id": QUESTION_ID,
        "value": value,
        "probabilities": probabilities,
        "confidence": probabilities[value],
        "model": VERIFIER_VERSION,
        "input_version": INPUT_VERSION,
        "label_role": label_role,
        "features": features,
    }


def oracle_label(task: dict[str, Any], trace: dict[str, Any]) -> str:
    """The trusted label: the deterministic grader, which may see `expected`."""
    return "success" if grade_task(task, trace)["passed"] else "failure"


def _cited_sources(answer: dict[str, Any]) -> set[str]:
    cited = set(answer.get("cited_policy_source_ids") or [])
    for group in ("reimbursable_items", "non_reimbursable_items"):
        for line in answer.get(group, []) or []:
            cited.update(line.get("policy_source_ids") or [])
    return cited


# ---------------------------------------------------------------------------
# Dataset construction
# ---------------------------------------------------------------------------


def split_role(task_id: str) -> str:
    """Even benchmark ids develop the threshold, odd ids are held out."""
    return "threshold_selection" if int(task_id.split("-")[-1]) % 2 == 0 else "verifier_eval"


def mutate(trace: dict[str, Any], kind: str) -> dict[str, Any] | None:
    """Return a polished-but-wrong variant, or None when it would be a no-op.

    A mutation that changes nothing the grader checks is not an adversarial
    case, and counting it as one would inflate the slice.
    """
    mutated = json.loads(json.dumps(trace))
    answer = mutated.get("final_answer") or {}
    if kind == "inflate_total":
        total = float(answer.get("total_reimbursable") or 0.0)
        if total <= 0.0:
            return None
        answer["total_reimbursable"] = round(total * 1.5 + 5.0, 2)
    elif kind == "drop_approvals":
        if not answer.get("approvals_required"):
            return None
        answer["approvals_required"] = []
    elif kind == "drop_missing_information":
        if not answer.get("missing_information"):
            return None
        answer["missing_information"] = []
    elif kind == "strip_citations":
        if not _cited_sources(answer):
            return None
        answer["cited_policy_source_ids"] = []
        for group in ("reimbursable_items", "non_reimbursable_items"):
            for line in answer.get(group, []) or []:
                line["policy_source_ids"] = []
    else:
        raise ValueError(f"unknown mutation {kind!r}")
    mutated["final_answer"] = answer
    return mutated


def build_rows(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build every labelled prediction row, deterministically."""
    rows: list[dict[str, Any]] = []
    scripted = run_benchmark(tasks, "scripted", include_traces=True)
    by_id = {task["id"]: task for task in tasks}

    for result in scripted:
        task = by_id[result["task_id"]]
        trace = result["trace"]
        role = split_role(task["id"])
        rows.append(
            _row(
                row_id=f"vc-{task['id']}",
                task_id=task["id"],
                source_run="scripted-current",
                label_role=role,
                trace=trace,
                task=task,
                note="Unmodified scripted reference trajectory.",
            )
        )

    # Adversarial cases are derived only from threshold-selection tasks, so the
    # held-out split never sees a task the adversarial slice was built from.
    for result in scripted:
        task = by_id[result["task_id"]]
        if split_role(task["id"]) != "threshold_selection":
            continue
        for kind in MUTATIONS:
            mutated = mutate(result["trace"], kind)
            if mutated is None:
                continue
            rows.append(
                _row(
                    row_id=f"vc-{task['id']}-{kind}",
                    task_id=task["id"],
                    source_run=f"adversarial:{kind}",
                    label_role="adversarial_eval",
                    trace=mutated,
                    task=task,
                    note=f"Polished answer with {kind.replace('_', ' ')} applied.",
                )
            )

    weak_results = _weak_rows(tasks)
    rows.extend(weak_results)
    return rows


def _row(
    *,
    row_id: str,
    task_id: str,
    source_run: str,
    label_role: str,
    trace: dict[str, Any],
    task: dict[str, Any],
    note: str,
) -> dict[str, Any]:
    record = predict(trace, row_id=row_id, label_role=label_role)
    record.update(
        {
            "task_id": task_id,
            "source_run": source_run,
            "label": oracle_label(task, trace),
            "label_source": LABEL_SOURCE,
            "reviewer": None,
            "note": note,
        }
    )
    return record


def _weak_rows(tasks: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    """A small slice of the Level 3 weak baseline.

    Its answers are identical by construction, so twenty rows carry the same
    information as a hundred. They are kept as their own slice rather than
    mixed into the held-out set, where they would make the verifier look good
    for free.
    """
    from evals.operations import run_weak_baseline

    rows = []
    results = run_weak_baseline(tasks[:limit])
    by_id = {task["id"]: task for task in tasks}
    for result in results:
        task = by_id[result["task_id"]]
        rows.append(
            _row(
                row_id=f"vc-{task['id']}-weak",
                task_id=task["id"],
                source_run="weak-no-tool",
                label_role="weak_baseline",
                trace=result["trace"],
                task=task,
                note="No tool calls, no citations, self-reported confidence high.",
            )
        )
    return rows


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def _p_success(row: dict[str, Any]) -> float:
    return float(row["probabilities"]["success"])


def _is_success(row: dict[str, Any]) -> bool:
    return row["label"] == "success"


def brier_score(rows: list[dict[str, Any]]) -> float:
    """Mean squared error of the predicted success probability."""
    if not rows:
        return 0.0
    total = sum((_p_success(row) - (1.0 if _is_success(row) else 0.0)) ** 2 for row in rows)
    return round(total / len(rows), 4)


def log_loss(rows: list[dict[str, Any]], epsilon: float = 1e-9) -> float:
    if not rows:
        return 0.0
    total = 0.0
    for row in rows:
        p = min(max(_p_success(row), epsilon), 1.0 - epsilon)
        total -= math.log(p) if _is_success(row) else math.log(1.0 - p)
    return round(total / len(rows), 4)


def reliability_buckets(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Mean predicted probability against observed success rate, per band."""
    buckets = []
    for low, high in zip(BUCKET_EDGES, BUCKET_EDGES[1:]):
        in_band = [
            row
            for row in rows
            if low <= _p_success(row) < high or (high == 1.0 and _p_success(row) == 1.0)
        ]
        if not in_band:
            buckets.append({"band": f"{low:.1f}-{high:.1f}", "count": 0})
            continue
        mean_p = sum(_p_success(row) for row in in_band) / len(in_band)
        observed = sum(1 for row in in_band if _is_success(row)) / len(in_band)
        buckets.append(
            {
                "band": f"{low:.1f}-{high:.1f}",
                "count": len(in_band),
                "mean_confidence": round(mean_p, 4),
                "observed_success_rate": round(observed, 4),
                "gap": round(mean_p - observed, 4),
            }
        )
    return buckets


def expected_calibration_error(rows: list[dict[str, Any]]) -> float:
    """Count-weighted mean absolute gap between confidence and accuracy."""
    if not rows:
        return 0.0
    total = 0.0
    for bucket in reliability_buckets(rows):
        if bucket["count"]:
            total += bucket["count"] * abs(bucket["gap"])
    return round(total / len(rows), 4)


def confusion_at(rows: list[dict[str, Any]], threshold: float) -> dict[str, int]:
    """Accept when p(success) >= threshold. False accept is the costly error."""
    counts = {"true_accept": 0, "false_accept": 0, "true_reject": 0, "false_reject": 0}
    for row in rows:
        accepted = _p_success(row) >= threshold
        if accepted and _is_success(row):
            counts["true_accept"] += 1
        elif accepted:
            counts["false_accept"] += 1
        elif _is_success(row):
            counts["false_reject"] += 1
        else:
            counts["true_reject"] += 1
    return counts


def risk_coverage(rows: list[dict[str, Any]], thresholds: list[float] | None = None) -> list[dict[str, Any]]:
    """How precision and coverage move as the accept threshold rises."""
    points = []
    for threshold in thresholds or [round(0.05 * step, 2) for step in range(1, 20)]:
        counts = confusion_at(rows, threshold)
        accepted = counts["true_accept"] + counts["false_accept"]
        points.append(
            {
                "threshold": threshold,
                "coverage": round(accepted / len(rows), 4) if rows else 0.0,
                "precision": round(counts["true_accept"] / accepted, 4) if accepted else None,
                "false_accepts": counts["false_accept"],
                "false_rejects": counts["false_reject"],
            }
        )
    return points


def select_threshold(
    rows: list[dict[str, Any]],
    *,
    min_precision: float = 0.98,
    max_false_accepts: int = 0,
) -> dict[str, Any]:
    """Maximise coverage subject to a precision floor and a false-accept cap.

    Returns the constraint alongside the answer, because a threshold without
    the constraint it satisfies is not an operating policy.
    """
    constraint = {
        "min_precision": min_precision,
        "max_false_accepts": max_false_accepts,
        "selected_on": "threshold_selection",
    }
    curve = risk_coverage(rows)
    scored = [point for point in curve if point["precision"] is not None]
    feasible = [
        point
        for point in scored
        if point["precision"] >= min_precision and point["false_accepts"] <= max_false_accepts
    ]
    if feasible:
        best = max(feasible, key=lambda point: (point["coverage"], -point["threshold"]))
        return {"constraint": constraint, "satisfied": True, **best}

    # No operating point clears the bar. Report the best available one anyway so
    # the slice tables are readable, but do not call it an operating policy: the
    # verdict is that this verifier cannot be automated, not that the bar moves.
    if not scored:
        return {"constraint": constraint, "satisfied": False, "threshold": None, "reason": "no scored thresholds"}
    best_effort = max(
        scored,
        key=lambda point: (
            point["precision"],
            -point["false_accepts"],
            point["coverage"],
            point["threshold"],
        ),
    )
    return {
        "constraint": constraint,
        "satisfied": False,
        "reason": (
            f"best achievable precision is {best_effort['precision']} at threshold "
            f"{best_effort['threshold']}, below the required {min_precision}"
        ),
        "best_effort": True,
        **best_effort,
    }


def evaluate_slice(rows: list[dict[str, Any]], threshold: float | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "count": len(rows),
        "positives": sum(1 for row in rows if _is_success(row)),
        "negatives": sum(1 for row in rows if not _is_success(row)),
        "brier_score": brier_score(rows),
        "log_loss": log_loss(rows),
        "expected_calibration_error": expected_calibration_error(rows),
        "reliability": reliability_buckets(rows),
    }
    if threshold is not None:
        counts = confusion_at(rows, threshold)
        accepted = counts["true_accept"] + counts["false_accept"]
        summary["at_threshold"] = {
            "threshold": threshold,
            **counts,
            "coverage": round(accepted / len(rows), 4) if rows else 0.0,
            "precision": round(counts["true_accept"] / accepted, 4) if accepted else None,
        }
    return summary


# ---------------------------------------------------------------------------
# Bundle
# ---------------------------------------------------------------------------


def build_bundle(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    rows = build_rows(tasks)
    by_role: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_role.setdefault(row["label_role"], []).append(row)

    selection = select_threshold(by_role.get("threshold_selection", []))
    threshold = selection.get("threshold")

    metrics = {
        "verifier": VERIFIER_VERSION,
        "question_id": QUESTION_ID,
        "input_version": INPUT_VERSION,
        "label_source": LABEL_SOURCE,
        "row_count": len(rows),
        "operating_policy": selection,
        "slices": {role: evaluate_slice(slice_rows, threshold) for role, slice_rows in sorted(by_role.items())},
    }
    return {"rows": rows, "metrics": metrics, "report": render_report(metrics)}


def write_bundle(bundle: dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "predictions.jsonl", "w", encoding="utf-8") as handle:
        for row in bundle["rows"]:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    (out / "metrics.json").write_text(
        json.dumps(bundle["metrics"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out / "calibration-report.md").write_text(bundle["report"], encoding="utf-8")


def render_report(metrics: dict[str, Any]) -> str:
    policy = metrics["operating_policy"]
    threshold = policy.get("threshold")
    lines = [
        "# Verifier Calibration Report",
        "",
        f"- Verifier: `{metrics['verifier']}`",
        f"- Question: `{metrics['question_id']}`",
        f"- Rows: {metrics['row_count']}",
        f"- Label source: `{metrics['label_source']}`",
        "",
        "The trusted label is the deterministic grader. The verifier sees only the",
        "trace, which is the information available in production. Accuracy alone",
        "cannot tell you whether its confidence is safe to act on.",
        "",
        "## Operating Policy",
        "",
        "```text",
        f"Maximize coverage subject to precision >= {policy['constraint']['min_precision']}",
        f"and at most {policy['constraint']['max_false_accepts']} false accepts,",
        f"selected on the {policy['constraint']['selected_on']} split.",
        "```",
        "",
    ]
    if not policy.get("satisfied"):
        lines += [
            f"**No threshold satisfies the constraint.** {policy.get('reason', '')}".rstrip() + ".",
            "",
            "That is a result, not a bug. Precision does not improve as the threshold",
            "rises, because the failures this verifier misses are the ones it is most",
            "confident about. The next move is a stronger verifier, not a lower bar.",
            "",
        ]
        if threshold is not None:
            lines += [
                f"The tables below use the best achievable point (threshold **{threshold}**, "
                f"coverage {policy['coverage']}, precision {policy['precision']}) so the error",
                "counts are visible. It is a reference point, not an approved operating policy.",
                "",
            ]
    else:
        lines += [
            f"Selected threshold: **{threshold}** "
            f"(coverage {policy['coverage']}, precision {policy['precision']}, "
            f"{policy['false_accepts']} false accepts, {policy['false_rejects']} false rejects).",
            "",
        ]

    lines += ["## Slices", "", "| Slice | n | +/- | Brier | Log loss | ECE | FA | FR |", "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |"]
    for role, summary in metrics["slices"].items():
        at = summary.get("at_threshold") or {}
        lines.append(
            f"| `{role}` | {summary['count']} | {summary['positives']}/{summary['negatives']} | "
            f"{summary['brier_score']} | {summary['log_loss']} | {summary['expected_calibration_error']} | "
            f"{at.get('false_accept', '-')} | {at.get('false_reject', '-')} |"
        )
    lines += ["", "FA = false accepts, FR = false rejects, both at the selected threshold.", ""]

    for role, summary in metrics["slices"].items():
        lines += [f"## Reliability: `{role}`", "", "| Band | n | Mean confidence | Observed | Gap |", "| --- | ---: | ---: | ---: | ---: |"]
        for bucket in summary["reliability"]:
            if not bucket["count"]:
                continue
            lines.append(
                f"| {bucket['band']} | {bucket['count']} | {bucket['mean_confidence']} | "
                f"{bucket['observed_success_rate']} | {bucket['gap']:+.4f} |"
            )
        lines.append("")

    lines += [
        "## What This Set Cannot Tell You",
        "",
        "Every label here is derived from the committed benchmark oracle, so no row",
        "carries reviewer disagreement. Genuine ambiguity — the cases that most",
        "deserve human adjudication — is absent by construction. The splits are also",
        "small: fifty rows per scripted split. Treat the numbers as a worked",
        "mechanism, and re-measure on your own labelled traces before trusting any",
        "threshold in production.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Build the StrongBench verifier calibration bundle.")
    parser.add_argument("--tasks", default=str(DEFAULT_TASKS))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args(argv)

    bundle = build_bundle(load_tasks(args.tasks))
    write_bundle(bundle, Path(args.out))
    print(bundle["report"].rstrip())
    return 0
