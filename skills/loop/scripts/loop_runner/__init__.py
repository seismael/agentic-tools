"""Generic, project-agnostic autonomous-loop runner.

A host supplies a project profile (``profile.yaml``/``profile.json``); every loop
behaviour — dispatch, coverage, gates, journal, issue ledger — is identical for every
project. See ``skills/loop/references/runner-contract.md``.
"""

from __future__ import annotations

from .coverage import CoverageAssessment, assess_coverage, seed_coverage
from .invocation import build_invocation
from .issues import (
    DeliveryAssessment,
    IssueAssessment,
    append_issue,
    assess_delivery,
    assess_open_issues,
    read_issues,
    update_issue,
)
from .profile import (
    DEFAULT_PROFILE,
    Front,
    Profile,
    ProfileError,
    Stage,
    load_profile,
    validate_profile,
)
from .stream import STREAM_FILE, normalize_agent_event, read_stream, render_event
from .supervisor import SupervisorBudget, request_stop, status, supervise

__all__ = [
    "CoverageAssessment",
    "DEFAULT_PROFILE",
    "DeliveryAssessment",
    "Front",
    "IssueAssessment",
    "Profile",
    "ProfileError",
    "STREAM_FILE",
    "Stage",
    "SupervisorBudget",
    "append_issue",
    "assess_coverage",
    "assess_delivery",
    "assess_open_issues",
    "build_invocation",
    "load_profile",
    "normalize_agent_event",
    "read_issues",
    "read_stream",
    "render_event",
    "request_stop",
    "seed_coverage",
    "status",
    "supervise",
    "update_issue",
    "validate_profile",
]
