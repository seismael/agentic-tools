"""Coverage ledger: proof that every required front/sub-axis was examined.

Generalizes a project's one-off "soundness sweep" into the front taxonomy: the ledger is
the loop's breadth guarantee. Project-agnostic; the required surface comes from the
profile.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .profile import Profile

SCHEMA = "loop.coverage.v1"

UNEXPLORED = "UNEXPLORED"
EXPLORING = "EXPLORING"
COVERED_SOUND = "COVERED-SOUND"
COVERED_EXHAUSTED = "COVERED-EXHAUSTED"
DEFECT_OPEN = "DEFECT-OPEN"
BLOCKED_EXTERNAL = "BLOCKED-EXTERNAL"

TERMINAL = frozenset({COVERED_SOUND, COVERED_EXHAUSTED, BLOCKED_EXTERNAL})
ALL_STATUSES = frozenset(
    {
        UNEXPLORED,
        EXPLORING,
        COVERED_SOUND,
        COVERED_EXHAUSTED,
        DEFECT_OPEN,
        BLOCKED_EXTERNAL,
    }
)


@dataclass(frozen=True, slots=True)
class CoverageAssessment:
    """Admissibility of the coverage ledger."""

    complete: bool
    missing: tuple[str, ...] = ()
    blocking: tuple[str, ...] = ()
    verified: int = 0
    exhausted: int = 0
    total: int = 0
    open_defect: bool = False
    counts: dict[str, int] = field(default_factory=dict)


def _status(entry: Any) -> str:
    if not isinstance(entry, dict):
        return ""
    return str(entry.get("status", "")).strip().upper()


def _has_reason(entry: Any) -> bool:
    return isinstance(entry, dict) and bool(str(entry.get("reason", "")).strip())


def read_coverage(path: Path) -> dict[str, Any]:
    """Read the ledger; empty dict if absent or malformed."""
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def seed_coverage(profile: Profile, loop_id: str) -> dict[str, Any]:
    """Skeleton ledger with every required front/sub-axis ``UNEXPLORED``."""
    fronts: dict[str, Any] = {}
    for name, front in profile.required_fronts().items():
        if front.sub_axes:
            fronts[name] = {
                "status": UNEXPLORED,
                "sub_axes": {
                    axis: {"status": UNEXPLORED, "evidence": ""}
                    for axis in front.sub_axes
                },
            }
        else:
            fronts[name] = {"status": UNEXPLORED, "evidence": ""}
    return {
        "schema": SCHEMA,
        "loop_id": loop_id,
        "updated_at": "",
        "complete": False,
        "open_defect": False,
        "counts": {"verified_sound": 0, "covered_exhausted": 0, "open": 0},
        "fronts": fronts,
    }


def assess_coverage(profile: Profile, path: Path) -> CoverageAssessment:
    """Whether every required front/sub-axis has reached a terminal status."""
    payload = read_coverage(path)
    fronts = payload.get("fronts") if isinstance(payload.get("fronts"), dict) else {}
    missing: list[str] = []
    blocking: list[str] = []
    verified = exhausted = total = 0
    status_hist: Counter[str] = Counter()
    open_defect = False

    def classify(label: str, entry: Any) -> None:
        nonlocal verified, exhausted, open_defect
        status = _status(entry)
        status_hist[status or "MISSING"] += 1
        if status == COVERED_SOUND:
            verified += 1
        elif status == COVERED_EXHAUSTED:
            exhausted += 1
        elif status == BLOCKED_EXTERNAL and _has_reason(entry):
            pass
        elif status == DEFECT_OPEN:
            open_defect = True
            blocking.append(label)
        else:
            blocking.append(label)

    for name, front in profile.required_fronts().items():
        entry = fronts.get(name)
        if front.sub_axes:
            sub = entry.get("sub_axes") if isinstance(entry, dict) else None
            for axis in front.sub_axes:
                total += 1
                label = f"{name}.{axis}"
                if not isinstance(sub, dict) or axis not in sub:
                    missing.append(label)
                    status_hist["MISSING"] += 1
                    continue
                classify(label, sub[axis])
        else:
            total += 1
            if not isinstance(entry, dict):
                missing.append(name)
                status_hist["MISSING"] += 1
                continue
            classify(name, entry)

    complete = not missing and not blocking
    return CoverageAssessment(
        complete=complete,
        missing=tuple(missing),
        blocking=tuple(blocking),
        verified=verified,
        exhausted=exhausted,
        total=total,
        open_defect=open_defect,
        counts=dict(status_hist),
    )


__all__ = [
    "ALL_STATUSES",
    "BLOCKED_EXTERNAL",
    "COVERED_EXHAUSTED",
    "COVERED_SOUND",
    "CoverageAssessment",
    "DEFECT_OPEN",
    "EXPLORING",
    "SCHEMA",
    "TERMINAL",
    "UNEXPLORED",
    "assess_coverage",
    "read_coverage",
    "seed_coverage",
]
