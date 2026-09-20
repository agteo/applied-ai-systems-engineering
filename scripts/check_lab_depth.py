"""Check Workstream E lab-contract markers.

ROADMAP declares the lab contract: every lab links a reference artifact and
states a check the learner can run or a rubric they can apply. That claim was
made in prose and went stale the first time a lab was added without either,
because nothing enforced it.

The mechanical gate checks two things:

- a reference section that links something committed to this repository
- a checks section

Whether the check is a *good* check still needs human review. This only ensures
there is one.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB_GLOB = "levels/*/labs/lab-[0-9][0-9]-*.md"

CHECK_HEADINGS = {
    "## Checks",
    "## Check",
    "## Pass Conditions",
}

REFERENCE_HEADINGS = {
    "## Reference",
    "## Reference Solution",
    "## Reference Artifact",
}

#: A reference section has to point at something in this repo. An external URL
#: is reading, not an artifact the learner can diff against.
REPO_LINK = re.compile(r"\]\((?!https?://)([^)]+)\)")


@dataclass(frozen=True)
class LabAudit:
    path: Path
    has_checks: bool
    has_reference: bool
    reference_targets: tuple[str, ...]
    broken_targets: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return self.has_checks and self.has_reference and bool(self.reference_targets) and not self.broken_targets

    @property
    def missing(self) -> list[str]:
        missing = []
        if not self.has_checks:
            missing.append("checks section")
        if not self.has_reference:
            missing.append("reference section")
        elif not self.reference_targets:
            missing.append("a repository link in its reference section")
        if self.broken_targets:
            missing.append(f"existing reference targets ({', '.join(self.broken_targets)})")
        return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check lab-contract markers.")
    parser.parse_args(argv)

    lab_paths = sorted(ROOT.glob(LAB_GLOB))
    audits = [audit_lab(path) for path in lab_paths]
    print_report(audits)
    return 1 if any(not audit.valid for audit in audits) else 0


def audit_lab(path: Path) -> LabAudit:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = {line.strip() for line in lines if line.startswith("## ")}

    reference_body = section_body(lines, REFERENCE_HEADINGS)
    targets = tuple(
        target.split("#", 1)[0]
        for target in REPO_LINK.findall(reference_body)
        if target.split("#", 1)[0]
    )
    broken = tuple(
        target for target in targets if not (path.parent / target).resolve().exists()
    )
    return LabAudit(
        path=path,
        has_checks=bool(CHECK_HEADINGS & headings),
        has_reference=bool(REFERENCE_HEADINGS & headings),
        reference_targets=targets,
        broken_targets=broken,
    )


def section_body(lines: list[str], headings: set[str]) -> str:
    """Everything under the first matching heading, up to the next one."""
    collected: list[str] = []
    capturing = False
    for line in lines:
        if line.strip() in headings:
            capturing = True
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            collected.append(line)
    return "\n".join(collected)


def print_report(audits: list[LabAudit]) -> None:
    missing_checks = sum(not audit.has_checks for audit in audits)
    missing_reference = sum(not audit.has_reference for audit in audits)
    broken = sum(bool(audit.broken_targets) for audit in audits)
    print("# Lab Depth Audit")
    print()
    print(f"- labs: {len(audits)}")
    print(f"- complete: {sum(audit.valid for audit in audits)}")
    print(f"- missing checks section: {missing_checks}")
    print(f"- missing reference section: {missing_reference}")
    print(f"- reference links that do not resolve: {broken}")
    print()
    for audit in audits:
        if audit.valid:
            continue
        relative = audit.path.relative_to(ROOT)
        print(f"FAIL {relative}: missing {', '.join(audit.missing)}.")


if __name__ == "__main__":
    raise SystemExit(main())
