"""Non-stop supervisor for the autonomous optimization loop (offline dev tooling).

The loop is driven by an external agent process (``--agent``, default ``build``), which
reads its journal, performs one atomic step, and exits. This module re-invokes that agent
one step at a time so the loop survives context exhaustion and runs unattended until it
*completes*, an operator writes the ``STOP`` sentinel, or a declared budget/watchdog
fires. Each invocation is a fresh session, so no single context grows without bound.

The supervisor is the sole producer of ``stream.jsonl``; the host's ``watch``/``report``
are read-only consumers. Project-agnostic: everything domain-specific comes from the
:class:`~loop_runner.profile.Profile`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

from .coverage import assess_coverage
from .invocation import build_invocation
from .issues import DeliveryAssessment, assess_delivery, assess_open_issues
from .profile import Profile
from .stream import (
    COVERAGE,
    ISSUES,
    STEP,
    STREAM_FILE,
    SUPERVISE_END,
    SUPERVISE_ERROR,
    SUPERVISE_REFUSED,
    SUPERVISE_START,
    SUPERVISE_STOP,
    normalize_agent_event,
)

STOP_SENTINEL = "STOP"
FINALIZE_FILE = "finalize.json"
GOAL_FILE = "goal.json"
PID_FILE = "supervisor.pid"
JOURNAL_FILE = "journal.jsonl"


@dataclass(frozen=True, slots=True)
class SupervisorBudget:
    """Stop conditions for the supervisor. Zero means unbounded/disabled."""

    max_invocations: int = 0
    max_hours: float = 0.0
    max_consecutive_failures: int = 3
    max_finalize_rejections: int = 3
    max_stalled_invocations: int = 3


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def _seed_goal(directory: Path, goal: str) -> None:
    """Persist the operator's one-time objective; idempotent on resume."""
    path = directory / GOAL_FILE
    if path.is_file():
        return
    payload = {"goal": goal, "status": "ACTIVE", "sub_goals": []}
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _resolve_binary(binary: str) -> str:
    """Resolve the executable (``.cmd`` shim on Windows) on PATH."""
    return shutil.which(binary) or binary


def _read_journal(directory: Path) -> list[dict[str, Any]]:
    """Parsed journal entries; one per appended step."""
    path = directory / JOURNAL_FILE
    if not path.is_file():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            parsed = {"raw": line}
        entries.append(parsed if isinstance(parsed, dict) else {"raw": line})
    return entries


def _existing_invocation_count(directory: Path) -> int:
    """Completed invocations on disk, so a resume never overwrites their logs."""
    return sum(1 for path in directory.glob("invocation-*.log") if path.is_file())


def _run_child(
    argv: Sequence[str], *, invocation: int, log_file: Path, stream_path: Path, cwd: str
) -> int:
    """Spawn one agent session, teeing stdout to the log and normalized stream."""
    with (
        log_file.open("w", encoding="utf-8") as log,
        stream_path.open("a", encoding="utf-8") as stream,
    ):
        process = subprocess.Popen(  # noqa: S603 - fixed argv, dev tooling only
            list(argv),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        stdout = process.stdout
        if stdout is not None:
            for line in stdout:
                log.write(line)
                record = normalize_agent_event(line)
                if record is not None:
                    record["invocation"] = invocation
                    stream.write(json.dumps(record, sort_keys=True) + "\n")
                    stream.flush()
        process.wait()
        return int(process.returncode)


def supervise(
    profile: Profile,
    loop_id: str,
    *,
    agent: str = "build",
    goal: str | None = None,
    budget: SupervisorBudget | None = None,
    opencode_bin: str = "opencode",
    project_root: Path | str | None = None,
    runner: Callable[[Sequence[str]], int] | None = None,
    emit: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    delivery: Callable[[], DeliveryAssessment] | None = None,
) -> dict[str, object]:
    """Run the loop non-stop until completion, STOP, or a budget/watchdog bound.

    ``runner``, ``sleep``, ``clock`` and ``delivery`` are injectable so the control flow is
    unit-testable without invoking the agent or reading real git state.
    """
    budget = budget or SupervisorBudget()
    root = Path(project_root).resolve() if project_root else Path.cwd().resolve()
    directory = profile.loop_dir(root, loop_id)
    directory.mkdir(parents=True, exist_ok=True)
    if goal:
        _seed_goal(directory, goal)
    coverage_path = profile.coverage_file(root)
    stop_path = directory / STOP_SENTINEL
    finalize_path = directory / FINALIZE_FILE
    log_path = directory / "supervisor.jsonl"
    stream_path = directory / STREAM_FILE
    pid_path = directory / PID_FILE
    delivery_check = delivery or (lambda: assess_delivery(root))

    started = clock()
    invocations = _existing_invocation_count(directory)
    failures_in_a_row = 0
    stalled_in_a_row = 0
    rejections = 0
    reason = "budget"
    entries = _read_journal(directory)
    last_progress = len(entries)
    pid_path.write_text(str(os.getpid()), encoding="utf-8")

    def stream_event(kind: str, **fields: Any) -> None:
        _append_jsonl(stream_path, {"kind": kind, **fields})

    try:
        while True:
            if stop_path.exists():
                reason = "stop_sentinel"
                break
            if finalize_path.exists():
                coverage = assess_coverage(profile, coverage_path)
                issues = assess_open_issues(directory)
                delivered = delivery_check()
                blockers: list[str] = []
                if not coverage.complete:
                    blockers.append("coverage_incomplete")
                if not issues.complete:
                    blockers.append("open_issues")
                if not delivered.complete:
                    blockers.append(f"delivery_{delivered.reason or 'incomplete'}")
                if not blockers:
                    reason = "completed"
                    break
                rejections += 1
                open_issues = [
                    {
                        k: issue[k]
                        for k in ("issue_id", "title", "class", "severity", "status")
                    }
                    for issue in issues.actionable
                ]
                _append_jsonl(
                    log_path,
                    {
                        "event": "finalize_refused",
                        "invocation": invocations,
                        "blockers": blockers,
                        "missing": list(coverage.missing),
                        "blocking": list(coverage.blocking),
                        "open_issues": open_issues,
                        "delivery": {
                            "clean": delivered.clean,
                            "pushed": delivered.pushed,
                            "head": delivered.head,
                            "origin_main": delivered.origin_main,
                            "reason": delivered.reason,
                        },
                        "rejections": rejections,
                    },
                )
                stream_event(
                    SUPERVISE_REFUSED,
                    invocation=invocations,
                    blockers=blockers,
                    missing=list(coverage.missing),
                    blocking=list(coverage.blocking),
                    open_issues=open_issues,
                    delivery_reason=delivered.reason,
                    rejections=rejections,
                )
                emit(
                    f"[supervise] refusing finalize: blockers={blockers} "
                    f"(missing={coverage.missing} blocking={coverage.blocking} "
                    f"open_issues={len(open_issues)} delivery={delivered.reason or 'ok'})"
                )
                rejected = directory / f"finalize.rejected-{rejections}.json"
                try:
                    finalize_path.replace(rejected)
                except OSError:
                    pass
                if (
                    budget.max_finalize_rejections
                    and rejections >= budget.max_finalize_rejections
                ):
                    reason = "fail_closed_finalize"
                    break
            if budget.max_invocations and invocations >= budget.max_invocations:
                reason = "max_invocations"
                break
            if budget.max_hours and (clock() - started) >= budget.max_hours * 3600.0:
                reason = "max_hours"
                break

            invocations += 1
            command = build_invocation(
                profile, loop_id, goal=goal, agent=agent, opencode_bin=opencode_bin
            )
            emit(f"[supervise] invocation {invocations}: agent={agent} loop={loop_id}")
            stream_event(SUPERVISE_START, invocation=invocations, agent=agent)
            invocation_started = clock()
            if runner is None:
                log_file = directory / f"invocation-{invocations}.log"
                exit_code = _run_child(
                    [_resolve_binary(opencode_bin), *command[1:]],
                    invocation=invocations,
                    log_file=log_file,
                    stream_path=stream_path,
                    cwd=str(root),
                )
            else:
                exit_code = runner(command)
            elapsed = round(clock() - invocation_started, 1)
            _append_jsonl(
                log_path,
                {
                    "event": "invocation",
                    "invocation": invocations,
                    "exit_code": exit_code,
                    "elapsed_s": elapsed,
                },
            )
            entries = _read_journal(directory)
            progress = len(entries)
            for entry in entries[last_progress:progress]:
                stream_event(STEP, entry=entry)
            stalled_in_a_row = 0 if progress != last_progress else stalled_in_a_row + 1
            last_progress = progress

            stream_event(
                SUPERVISE_END,
                invocation=invocations,
                exit_code=exit_code,
                elapsed_s=elapsed,
            )

            coverage = assess_coverage(profile, coverage_path)
            stream_event(
                COVERAGE,
                verified=coverage.verified,
                exhausted=coverage.exhausted,
                total=coverage.total,
                complete=coverage.complete,
                missing=list(coverage.missing),
                blocking=list(coverage.blocking),
            )

            issues_assessment = assess_open_issues(directory)
            stream_event(
                ISSUES,
                complete=issues_assessment.complete,
                counts=issues_assessment.counts,
                actionable=[
                    {
                        k: issue[k]
                        for k in ("issue_id", "title", "class", "severity", "status")
                    }
                    for issue in issues_assessment.actionable
                ],
            )

            if exit_code != 0:
                failures_in_a_row += 1
                backoff = min(30.0, float(2**failures_in_a_row))
                stream_event(
                    SUPERVISE_ERROR,
                    invocation=invocations,
                    exit_code=exit_code,
                    backoff_s=backoff,
                )
                emit(f"[supervise] invocation {invocations} failed rc={exit_code}")
                if failures_in_a_row >= budget.max_consecutive_failures:
                    reason = "fail_closed"
                    break
                sleep(backoff)
            else:
                failures_in_a_row = 0
                if (
                    budget.max_stalled_invocations
                    and stalled_in_a_row >= budget.max_stalled_invocations
                ):
                    reason = "fail_closed_stalled"
                    break
    finally:
        _append_jsonl(
            log_path, {"event": "stop", "reason": reason, "invocations": invocations}
        )
        stream_event(SUPERVISE_STOP, reason=reason, invocations=invocations)
        try:
            pid_path.unlink()
        except OSError:
            pass
        emit(f"[supervise] stopped: {reason} after {invocations} invocations")
    return {"loop_id": loop_id, "invocations": invocations, "stopped_reason": reason}


def read_pid(directory: Path) -> int | None:
    path = directory / PID_FILE
    if not path.is_file():
        return None
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def request_stop(
    profile: Profile, loop_id: str, *, project_root: Path | str | None = None
) -> Path:
    """Write the STOP sentinel (operator-only hard stop)."""
    root = Path(project_root).resolve() if project_root else Path.cwd().resolve()
    directory = profile.loop_dir(root, loop_id)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / STOP_SENTINEL
    path.write_text("operator stop\n", encoding="utf-8")
    return path


def status(
    profile: Profile, loop_id: str, *, project_root: Path | str | None = None
) -> dict[str, Any]:
    """Compact status snapshot for a loop."""
    root = Path(project_root).resolve() if project_root else Path.cwd().resolve()
    directory = profile.loop_dir(root, loop_id)
    entries = _read_journal(directory)
    steps = [entry for entry in entries if not entry.get("raw")]
    coverage = assess_coverage(profile, profile.coverage_file(root))
    issues = assess_open_issues(directory)
    pid = read_pid(directory)
    return {
        "loop_id": loop_id,
        "running": bool(pid),
        "pid": pid,
        "steps": len(steps),
        "invocations": _existing_invocation_count(directory),
        "finalized": (directory / FINALIZE_FILE).is_file(),
        "stop_sentinel": (directory / STOP_SENTINEL).is_file(),
        "coverage_complete": coverage.complete,
        "coverage": {
            "verified": coverage.verified,
            "exhausted": coverage.exhausted,
            "total": coverage.total,
        },
        "open_issues": len(issues.actionable),
        "directory": str(directory),
    }


__all__ = [
    "FINALIZE_FILE",
    "GOAL_FILE",
    "JOURNAL_FILE",
    "PID_FILE",
    "STOP_SENTINEL",
    "SupervisorBudget",
    "read_pid",
    "request_stop",
    "status",
    "supervise",
]
