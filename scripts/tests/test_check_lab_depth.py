import scripts.check_lab_depth as checker

COMPLETE = (
    "# Lab 1: Complete\n\n"
    "## Build\n\nText.\n\n"
    "## Checks\n\n```bash\npython3 -c 'print(1)'\n```\n\n"
    "## Reference\n\nCompare against [`artifact.md`](artifact.md).\n"
)


def _lab(tmp_path, name, text, *, with_artifact=True):
    lab = tmp_path / "levels" / "01-build" / "labs" / name
    lab.parent.mkdir(parents=True, exist_ok=True)
    lab.write_text(text, encoding="utf-8")
    if with_artifact:
        (lab.parent / "artifact.md").write_text("artifact\n", encoding="utf-8")
    return lab


def test_complete_lab_passes(tmp_path, monkeypatch):
    lab = _lab(tmp_path, "lab-01-complete.md", COMPLETE)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lab(lab)

    assert audit.valid is True
    assert audit.missing == []


def test_lab_without_checks_fails(tmp_path, monkeypatch):
    text = COMPLETE.replace("## Checks", "## Notes")
    lab = _lab(tmp_path, "lab-02-no-checks.md", text)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lab(lab)

    assert audit.valid is False
    assert "checks section" in audit.missing


def test_lab_without_reference_fails(tmp_path, monkeypatch):
    text = COMPLETE.split("## Reference")[0]
    lab = _lab(tmp_path, "lab-03-no-reference.md", text)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lab(lab)

    assert audit.valid is False
    assert "reference section" in audit.missing


def test_external_link_is_reading_not_a_reference_artifact(tmp_path, monkeypatch):
    text = COMPLETE.replace(
        "Compare against [`artifact.md`](artifact.md).",
        "Read [the paper](https://example.com/paper).",
    )
    lab = _lab(tmp_path, "lab-04-external-only.md", text)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lab(lab)

    assert audit.valid is False
    assert "a repository link in its reference section" in audit.missing


def test_reference_link_that_does_not_resolve_fails(tmp_path, monkeypatch):
    lab = _lab(tmp_path, "lab-05-dangling.md", COMPLETE, with_artifact=False)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lab(lab)

    assert audit.valid is False
    assert audit.broken_targets == ("artifact.md",)


def test_checks_in_another_section_do_not_count(tmp_path, monkeypatch):
    """A `Checks` heading must be the lab's own, not a stray mention."""
    text = COMPLETE.replace("## Checks", "### Checks")
    lab = _lab(tmp_path, "lab-06-subheading.md", text)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    assert checker.audit_lab(lab).valid is False


def test_pass_conditions_counts_as_a_checks_section(tmp_path, monkeypatch):
    text = COMPLETE.replace("## Checks", "## Pass Conditions")
    lab = _lab(tmp_path, "lab-07-pass-conditions.md", text)
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    assert checker.audit_lab(lab).valid is True


def test_every_committed_lab_satisfies_the_contract():
    """The regression this gate exists to prevent."""
    audits = [checker.audit_lab(path) for path in sorted(checker.ROOT.glob(checker.LAB_GLOB))]
    assert audits, "no labs found"
    failures = {str(audit.path.relative_to(checker.ROOT)): audit.missing for audit in audits if not audit.valid}
    assert not failures, failures
