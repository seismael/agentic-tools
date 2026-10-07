"""Build the exact agent invocation for one loop step (profile-driven, no domain text).

The step contract is rendered entirely from the project profile: the goal, the required
fronts, the boundaries, the allowed modes, and the completion rule. This is what keeps
the runner project-agnostic.
"""

from __future__ import annotations

from typing import Sequence

from .profile import Profile


def _join(items: Sequence[str], empty: str = "none") -> str:
    return ", ".join(items) if items else empty


def build_invocation(
    profile: Profile,
    loop_id: str,
    *,
    goal: str | None = None,
    agent: str = "build",
    opencode_bin: str = "opencode",
) -> list[str]:
    """Build the agent command for one iteration of ``loop_id``."""
    objective_text = (goal or profile.goal).strip()
    fronts = _join(tuple(profile.required_fronts()))
    boundaries = _join(profile.boundaries)
    modes = _join(profile.modes)
    loop_rel = "/".join(part for part in (profile.loop_root, loop_id) if part)
    coverage_rel = profile.coverage_path

    objective = (
        f"Objective: {objective_text}. "
        f"Persisted at {loop_rel}/goal.json; you own goal-setting: decompose it into "
        "measurable sub-goals, keep goal.json current (sub_goals + status), and re-rank "
        "next_moves.json every step. Keep the coverage ledger current at "
        f"{coverage_rel}. "
    )
    message = (
        objective
        + f"Operate the autonomous optimization loop '{loop_id}'. Resume from the journal at "
        f"{loop_rel}/ (state.json, journal.jsonl, issues.jsonl, next_moves.json, goal.json, "
        f"{coverage_rel}). Perform exactly ONE atomic step and journal it. "
        "Choose the next move with the dispatch policy: an open defect outranks an "
        "uncovered front, which outranks the largest diagnosed gap, which outranks a "
        "structural candidate; a parameter change is last. Always decide from data, code, "
        "the knowledge base and prior outcomes - never act without grounds and never run a "
        "groundless sweep. "
        f"Every required front/sub-axis must reach a terminal coverage status: {fronts}. "
        "Use only the declared pipeline stages; never hand-roll analysis. "
        "Maintain the canonical issues.jsonl ledger: record every well-defined finding with "
        "reproducible evidence (exact command + artifact), then RESOLVE it - there is no "
        "RECOMMEND status. Confirm from the data (no speculation), implement one bounded fix "
        "with a regression test, validate it (the profile's invariant lanes, and the objective "
        "gate for economic changes), independently verify, then ADOPT: commit AND git push. If "
        "disproven, mark REJECTED with counter-evidence. Do NOT write the STOP file "
        "(operator-only). "
        "To finish the loop, write finalize.json ONLY after (1) the coverage ledger is complete "
        "(every required front/sub-axis terminal, no open defect), (2) issues.jsonl has no open "
        "actionable issue, and (3) the working tree is clean and HEAD == origin/main. Otherwise "
        "the finalize is refused and the loop continues. "
        f"Never weaken these boundaries: {boundaries}. Allowed run modes: {modes}. "
        "Never produce numbers the pipeline cannot reproduce from a committed snapshot."
    )
    return [
        opencode_bin,
        "run",
        "--agent",
        agent,
        "--auto",
        "--format",
        "json",
        message,
    ]


__all__ = ["build_invocation"]
