import json
from pathlib import Path

from evals.runner import BENCHMARK_DIR, load_tasks
from evals.verifier_calibration import (
    DEFAULT_OUT,
    MUTATIONS,
    brier_score,
    build_bundle,
    confusion_at,
    expected_calibration_error,
    log_loss,
    mutate,
    predict,
    reliability_buckets,
    risk_coverage,
    select_threshold,
    split_role,
    write_bundle,
)

TASKS = load_tasks(BENCHMARK_DIR / "tasks.jsonl")


def _rows(label_probabilities):
    return [
        {
            "label": label,
            "probabilities": {"success": p, "failure": round(1.0 - p, 4)},
        }
        for label, p in label_probabilities
    ]


def test_confidence_always_matches_the_selected_value():
    """The invariant every lab consuming predictions.jsonl relies on."""
    rows = _committed_predictions()
    for row in rows:
        assert row["confidence"] == row["probabilities"][row["value"]]
        assert abs(sum(row["probabilities"].values()) - 1.0) < 1e-6


def test_predict_never_reads_the_oracle():
    trace = {"final_answer": {"next_action": "x", "confidence": "high"}, "steps": []}
    record = predict(trace, row_id="vc-test", label_role="verifier_eval")
    assert set(record["probabilities"]) == {"success", "failure"}
    assert "expected" not in json.dumps(record)


def test_brier_and_log_loss_reward_correct_probabilities():
    confident_right = _rows([("success", 0.99), ("failure", 0.01)])
    confident_wrong = _rows([("failure", 0.99), ("success", 0.01)])
    assert brier_score(confident_right) < brier_score(confident_wrong)
    assert log_loss(confident_right) < log_loss(confident_wrong)


def test_perfectly_calibrated_rows_have_near_zero_ece():
    # Ten rows at p=0.8, eight of which succeed.
    rows = _rows([("success", 0.8)] * 8 + [("failure", 0.8)] * 2)
    assert expected_calibration_error(rows) < 0.01


def test_overconfident_rows_have_large_ece():
    rows = _rows([("success", 0.95)] * 2 + [("failure", 0.95)] * 8)
    assert expected_calibration_error(rows) > 0.5


def test_reliability_buckets_cover_every_row():
    rows = _rows([("success", 0.05), ("success", 0.45), ("failure", 0.75), ("success", 1.0)])
    assert sum(bucket["count"] for bucket in reliability_buckets(rows)) == len(rows)


def test_confusion_counts_false_accepts_at_threshold():
    rows = _rows([("failure", 0.9), ("success", 0.9), ("failure", 0.1)])
    counts = confusion_at(rows, 0.5)
    assert counts == {"true_accept": 1, "false_accept": 1, "true_reject": 1, "false_reject": 0}


def test_risk_coverage_is_monotone_in_coverage():
    rows = _rows([("success", p / 10) for p in range(1, 11)])
    coverages = [point["coverage"] for point in risk_coverage(rows)]
    assert coverages == sorted(coverages, reverse=True)


def test_select_threshold_reports_the_constraint_it_satisfied():
    rows = _rows([("success", 0.9)] * 20 + [("failure", 0.1)] * 5)
    selection = select_threshold(rows, min_precision=0.98, max_false_accepts=0)
    assert selection["satisfied"] is True
    assert selection["constraint"]["min_precision"] == 0.98
    assert selection["threshold"] is not None


def test_select_threshold_refuses_rather_than_lowering_the_bar():
    rows = _rows([("success", 0.9)] * 10 + [("failure", 0.9)] * 10)
    selection = select_threshold(rows, min_precision=0.98, max_false_accepts=0)
    assert selection["satisfied"] is False
    assert "below the required" in selection["reason"]


def test_split_role_keeps_even_and_odd_tasks_apart():
    assert split_role("bench-002") == "threshold_selection"
    assert split_role("bench-003") == "verifier_eval"


def test_mutations_return_none_when_they_would_change_nothing():
    empty = {"final_answer": {"total_reimbursable": 0.0, "approvals_required": []}, "steps": []}
    for kind in MUTATIONS:
        assert mutate(empty, kind) is None


def test_adversarial_rows_are_never_built_from_held_out_tasks():
    rows = _committed_predictions()
    adversarial = [row for row in rows if row["label_role"] == "adversarial_eval"]
    assert adversarial
    assert all(split_role(row["task_id"]) == "threshold_selection" for row in adversarial)


def test_every_label_records_derived_provenance():
    for row in _committed_predictions():
        assert row["label_source"] == "derived-from-benchmark-oracle"
        assert row["reviewer"] is None


def test_adversarial_slice_exposes_more_false_accepts_than_the_dev_split():
    """The finding the bundle exists to make: polished answers pass."""
    metrics = json.loads((DEFAULT_OUT / "metrics.json").read_text(encoding="utf-8"))
    dev = metrics["slices"]["threshold_selection"]["at_threshold"]["false_accept"]
    adversarial = metrics["slices"]["adversarial_eval"]["at_threshold"]["false_accept"]
    assert adversarial > dev


def test_bundle_is_deterministic_and_regenerates_the_committed_report(tmp_path):
    bundle = build_bundle(TASKS)
    assert bundle["report"] == build_bundle(TASKS)["report"]
    write_bundle(bundle, Path(tmp_path))
    committed = (DEFAULT_OUT / "calibration-report.md").read_text(encoding="utf-8")
    assert (Path(tmp_path) / "calibration-report.md").read_text(encoding="utf-8") == committed


def _committed_predictions():
    path = DEFAULT_OUT / "predictions.jsonl"
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
