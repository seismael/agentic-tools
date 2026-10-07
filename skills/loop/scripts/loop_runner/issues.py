"""Canonical issue ledger for the autonomous optimization loop.

Every well-defined finding is recorded here with reproducible evidence and an explicit
status, so the loop can *resolve* issues rather than merely recommend them. The loop may
only finalize when no *actionable* issue remains open and adopted work is committed and
pushed. Project-agnostic.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

ISSUES_FILE = "issues.jsonl"
ISSUES_SCHEMA = "loop.issue.v1"

# Lifecycle statuses.
OPEN = "OPEN"
IN_PROGRESS = "IN_PROGRESS"
FIXED = "FIXED"
REJECTED = "REJECTED"
BLOCKED_EXTERNAL = "BLOCKED-EXTERNAL"
OBSERVATION = "OBSERVATION"

ACTIONABLE_STATUSES = frozenset({OPEN, IN_PROGRESS})
CLOSED_STATUSES = frozenset({FIXED, REJECTED, BLOCKED_EXTERNAL})
ALL_STATUSES = ACTIONABLE_STATUSES | CLOSED_STATUSES | {OBSERVATION}

# Issue classes (what part of the system the finding concerns).
CLASS_BLOCKER = "blocker"
CLASS_HARNESS = "harness"
CLASS_CONFIG = "config"
CLASS_DATA = "data"
CLASS_TELEMETRY = "telemetry"
CLASS_TEST = "test"
CLASS_DOC = "doc"
CLASS_SIGNAL = "signal"
CLASS_OBSERVATION = "observation"
ALL_CLASSES = frozenset(
    {
        CLASS_BLOCKER,
        CLASS_HARNESS,
        CLASS_CONFIG,
        CLASS_DATA,
        CLASS_TELEMETRY,
        CLASS_TEST,
        CLASS_DOC,
        CLASS_SIGNAL,
        CLASS_OBSERVATION,
    }
)

SEVERITIES = ("critical", "high", "medium", "low", "info")
_SEVERITY_RANK = {name: rank for rank, name in enumerate(SEVERITIES)}


class IssueLedgerError(ValueError):
    """A malformed or inadmissible issue record."""


@dataclass(frozen=True, slots=True)
class IssueAssessment:
    """Admissibility of the actionable issue queue."""

    complete: bool
    actionable: tuple[dict[str, Any], ...] = ()
    counts: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DeliveryAssessment:
    """Whether adopted work is clean and pushed to ``origin/main``."""

    clean: bool
    pushed: bool
    head: str = ""
    origin_main: str = ""
    reason: str = ""

    @property
    def complete(self) -> bool:
        return self.clean and self.pushed


def _normalize_issue(issue: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and complete one issue record (raises on inadmissible input)."""
    title = str(issue.get("title") or "").strip()
    if not title:
        raise IssueLedgerError("issue requires a non-empty 'title'")
    issue_class = str(issue.get("class") or "").strip().lower()
    if issue_class not in ALL_CLASSES:
        raise IssueLedgerError(f"issue '{title}' has unknown class {issue_class!r}")
    severity = str(issue.get("severity") or "").strip().lower()
    if severity not in SEVERITIES:
        raise IssueLedgerError(f"issue '{title}' has unknown severity {severity!r}")
    status = str(issue.get("status") or "").strip().upper()
    if status not in ALL_STATUSES:
        raise IssueLedgerError(f"issue '{title}' has unknown status {status!r}")
    source = str(issue.get("source") or "").strip()
    if not source:
        raise IssueLedgerError(f"issue '{title}' requires a non-empty 'source'")

    evidence = issue.get("evidence") or ""
    if (
        status in ACTIONABLE_STATUSES
        and issue_class != CLASS_OBSERVATION
        and not evidence
    ):
        raise IssueLedgerError(
            f"actionable issue '{title}' requires non-empty 'evidence' (reproduction)"
        )

    issue_id = str(issue.get("issue_id") or "").strip()
    if not issue_id:
        digest = hashlib.sha256(f"{source}|{title}".encode("utf-8")).hexdigest()[:16]
        issue_id = f"{issue_class}-{digest}"

    record: dict[str, Any] = {
        "schema_marker": ISSUES_SCHEMA,
        "issue_id": issue_id,
        "title": title,
        "class": issue_class,
        "severity": severity,
        "status": status,
        "source": source,
        "evidence": evidence,
    }
    for key in (
        "found_at",
        "resolved_at",
        "commit",
        "pushed",
        "repro",
        "impact",
        "validation",
        "notes",
    ):
        if issue.get(key) not in (None, ""):
            record[key] = issue[key]
    return record


def read_issues(directory: Path) -> list[dict[str, Any]]:
    """Effective issue states (append-only ledger; later records override)."""
    path = directory / ISSUES_FILE
    if not path.is_file():
        return []
    by_id: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        issue_id = str(record.get("issue_id") or "")
        if not issue_id:
            continue
        if issue_id not in by_id:
            order.append(issue_id)
        by_id[issue_id] = {**by_id.get(issue_id, {}), **record}
    return [by_id[issue_id] for issue_id in order]


def append_issue(directory: Path, issue: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and append one issue record to the ledger."""
    record = _normalize_issue(issue)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ISSUES_FILE).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def normalize_issue(issue: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and complete one issue record without persisting it."""
    return _normalize_issue(issue)


def update_issue(directory: Path, issue_id: str, **changes: Any) -> dict[str, Any]:
    """Append an updated state for an existing issue (last record wins)."""
    current = {issue["issue_id"]: issue for issue in read_issues(directory)}
    if issue_id not in current:
        raise IssueLedgerError(f"unknown issue_id {issue_id!r}")
    merged = {**current[issue_id], **changes, "issue_id": issue_id}
    return append_issue(directory, merged)


def assess_open_issues(directory: Path) -> IssueAssessment:
    """Whether any actionable issue remains open (empty queue -> complete)."""
    issues = read_issues(directory)
    actionable = [
        issue
        for issue in issues
        if issue["status"] in ACTIONABLE_STATUSES
        and issue["class"] != CLASS_OBSERVATION
    ]
    actionable.sort(
        key=lambda issue: (
            _SEVERITY_RANK.get(str(issue.get("severity", "info")), len(SEVERITIES)),
            str(issue.get("found_at", "")),
        )
    )
    counts = Counter(str(issue["status"]) for issue in issues)
    return IssueAssessment(
        complete=not actionable, actionable=tuple(actionable), counts=dict(counts)
    )


def _default_git(args: Sequence[str], root: Path) -> str:
    completed = subprocess.run(  # noqa: S603 - fixed argv, dev tooling only
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else ""


def assess_delivery(
    repo_root: Path, *, branch: str = "origin/main", git: Any = None
) -> DeliveryAssessment:
    """Whether the working tree is clean and ``HEAD == <branch>``.

    ``git`` is injectable for tests: a callable taking a list of git arguments and
    returning stdout (empty string on failure).
    """
    run = git or (lambda args: _default_git(args, repo_root))
    status = run(["status", "--porcelain"])
    head = run(["rev-parse", "HEAD"])
    origin = run(["rev-parse", branch])
    clean = status == ""
    if not origin:
        return DeliveryAssessment(
            clean=clean, pushed=False, head=head, reason="no_origin"
        )
    pushed = bool(head) and head == origin
    if not clean:
        reason = "dirty_tree"
    elif not pushed:
        reason = "unpushed"
    else:
        reason = ""
    return DeliveryAssessment(
        clean=clean, pushed=pushed, head=head, origin_main=origin, reason=reason
    )


__all__ = [
    "ACTIONABLE_STATUSES",
    "ALL_CLASSES",
    "ALL_STATUSES",
    "BLOCKED_EXTERNAL",
    "CLASS_BLOCKER",
    "CLOSED_STATUSES",
    "DeliveryAssessment",
    "FIXED",
    "IssueAssessment",
    "IssueLedgerError",
    "ISSUES_FILE",
    "ISSUES_SCHEMA",
    "OBSERVATION",
    "OPEN",
    "REJECTED",
    "SEVERITIES",
    "append_issue",
    "assess_delivery",
    "assess_open_issues",
    "read_issues",
    "update_issue",
    "normalize_issue",
]
