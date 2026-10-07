"""Unit + fixture tests for the generic loop runner (no project dependencies)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from loop_runner import (  # noqa: E402
    Profile,
    ProfileError,
    SupervisorBudget,
    append_issue,
    assess_coverage,
    assess_open_issues,
    build_invocation,
    load_profile,
    normalize_agent_event,
    read_stream,
    render_event,
    request_stop,
    seed_coverage,
    status,
    supervise,
    validate_profile,
)
from loop_runner.coverage import (  # noqa: E402
    COVERED_EXHAUSTED,
    COVERED_SOUND,
    DEFECT_OPEN,
)
from loop_runner.issues import DeliveryAssessment, assess_delivery  # noqa: E402


def _profile_data() -> dict:
    return {
        "schema": "loop.profile.v1",
        "project": "fixture",
        "goal": "maximize the fixture metric",
        "metric": "score",
        "modes": ["eval"],
        "paths": {"loop": ".fixture/loop", "coverage": "docs/knowledge/coverage.json"},
        "boundaries": ["deterministic", "no-lookahead"],
        "fronts": {
            "debug": {"required": True, "sub_axes": ["axis_a", "axis_b"]},
            "improve": {"required": True},
            "audit": {"required": False},
        },
        "pipeline": [
            {
                "id": "evaluate",
                "kind": "evaluate",
                "command": "fixture eval",
                "artifact": "out.json",
            }
        ],
        "gates": {"objective": "delta>0", "invariants": "fixture test"},
        "completion": {
            "rule": "coverage",
            "require_coverage": True,
            "require_delivery": True,
        },
    }


def _write_profile(root: Path, data: dict | None = None) -> Profile:
    path = root / "docs" / "knowledge" / "profile.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data or _profile_data()), encoding="utf-8")
    return load_profile(path)


def _terminal_coverage(profile: Profile, loop_id: str = "L1") -> dict:
    payload = seed_coverage(profile, loop_id)
    for front in payload["fronts"].values():
        if "sub_axes" in front:
            for axis in front["sub_axes"].values():
                axis["status"] = COVERED_SOUND
        else:
            front["status"] = COVERED_SOUND
    return payload


class ProfileTests(unittest.TestCase):
    def test_load_valid_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profile = _write_profile(Path(tmp))
            self.assertEqual(profile.project, "fixture")
            self.assertEqual(set(profile.required_fronts()), {"debug", "improve"})
            self.assertEqual(profile.fronts["debug"].sub_axes, ("axis_a", "axis_b"))
            self.assertEqual(len(profile.pipeline), 1)

    def test_validate_reports_errors(self) -> None:
        errors = validate_profile({"schema": "wrong", "fronts": {}, "paths": {}})
        joined = "; ".join(errors)
        for expected in (
            "schema must be",
            "project must be",
            "goal must be",
            "metric must be",
            "modes must be",
            "boundaries must be",
            "paths.loop",
            "fronts must be",
            "completion must be",
        ):
            self.assertIn(expected, joined)

    def test_load_missing_profile_raises(self) -> None:
        with self.assertRaises(ProfileError):
            load_profile(Path(tempfile.gettempdir()) / "does-not-exist-profile.json")


class CoverageTests(unittest.TestCase):
    def test_seed_is_unexplored_and_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            path = profile.coverage_file(root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(seed_coverage(profile, "L1")), encoding="utf-8")
            assessment = assess_coverage(profile, path)
            self.assertFalse(assessment.complete)
            self.assertTrue(assessment.blocking or assessment.missing)

    def test_all_terminal_is_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            path = profile.coverage_file(root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(_terminal_coverage(profile)), encoding="utf-8")
            assessment = assess_coverage(profile, path)
            self.assertTrue(assessment.complete)
            self.assertEqual(assessment.verified, 3)  # axis_a, axis_b, improve
            self.assertFalse(assessment.open_defect)

    def test_defect_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            payload = _terminal_coverage(profile)
            payload["fronts"]["debug"]["sub_axes"]["axis_a"]["status"] = DEFECT_OPEN
            path = profile.coverage_file(root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload), encoding="utf-8")
            assessment = assess_coverage(profile, path)
            self.assertFalse(assessment.complete)
            self.assertTrue(assessment.open_defect)
            self.assertIn("debug.axis_a", assessment.blocking)

    def test_exhausted_is_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            payload = _terminal_coverage(profile)
            payload["fronts"]["debug"]["sub_axes"]["axis_b"]["status"] = (
                COVERED_EXHAUSTED
            )
            path = profile.coverage_file(root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload), encoding="utf-8")
            assessment = assess_coverage(profile, path)
            self.assertTrue(assessment.complete)
            self.assertEqual(assessment.exhausted, 1)


class IssueTests(unittest.TestCase):
    def test_append_and_assess(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            append_issue(
                directory,
                {
                    "title": "boom",
                    "class": "test",
                    "severity": "high",
                    "status": "OPEN",
                    "source": "fixture",
                    "evidence": "repro cmd",
                },
            )
            assessment = assess_open_issues(directory)
            self.assertFalse(assessment.complete)
            self.assertEqual(assessment.actionable[0]["title"], "boom")

    def test_actionable_requires_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(Exception):
                append_issue(
                    Path(tmp),
                    {
                        "title": "x",
                        "class": "test",
                        "severity": "low",
                        "status": "OPEN",
                        "source": "s",
                    },
                )

    def test_delivery_with_injected_git(self) -> None:
        clean = lambda args: "" if args[0] == "status" else "a" * 40  # noqa: E731
        self.assertTrue(assess_delivery(Path("."), git=clean).complete)
        dirty = lambda args: " M file" if args[0] == "status" else "a" * 40  # noqa: E731
        self.assertFalse(assess_delivery(Path("."), git=dirty).complete)


class InvocationTests(unittest.TestCase):
    def test_invocation_is_profile_driven_and_agnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profile = _write_profile(Path(tmp))
        command = build_invocation(profile, "L1", goal="raise score")
        message = command[-1]
        self.assertEqual(command[:4], ["opencode", "run", "--agent", "build"])
        self.assertIn("raise score", message)
        self.assertIn("debug, improve", message)
        self.assertIn("deterministic, no-lookahead", message)
        self.assertIn("coverage.json", message)
        for forbidden in ("apex", "PAPER", "LIVE", "holdout"):
            self.assertNotIn(forbidden, message.lower().replace("autonomous", ""))


class StreamTests(unittest.TestCase):
    def test_normalize_tool_use(self) -> None:
        line = json.dumps(
            {
                "type": "tool_use",
                "part": {
                    "tool": "bash",
                    "state": {
                        "status": "completed",
                        "input": {"command": "ls -la"},
                        "output": "ok",
                    },
                },
            }
        )
        record = normalize_agent_event(line)
        self.assertEqual(record["kind"], "agent.tool")
        self.assertEqual(record["tool"], "bash")
        self.assertIn("ls -la", render_event(record))

    def test_read_stream_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "stream.jsonl"
            path.write_text(
                '{"kind": "step", "entry": {"step": 1, "axis": "a"}}\n',
                encoding="utf-8",
            )
            records = read_stream(path)
            self.assertEqual(len(records), 1)
            self.assertIn("step 1", render_event(records[0]))


class SupervisorTests(unittest.TestCase):
    def test_stop_sentinel_halts_without_invoking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            directory = profile.loop_dir(root, "L1")
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "STOP").write_text("", encoding="utf-8")
            called: list = []
            result = supervise(
                profile,
                "L1",
                project_root=root,
                runner=lambda cmd: called.append(cmd) or 0,
                emit=lambda _: None,
            )
            self.assertEqual(result["stopped_reason"], "stop_sentinel")
            self.assertEqual(called, [])

    def test_budget_bound(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            result = supervise(
                profile,
                "L1",
                project_root=root,
                budget=SupervisorBudget(max_invocations=2),
                runner=lambda cmd: 0,
                emit=lambda _: None,
            )
            self.assertEqual(result["stopped_reason"], "max_invocations")
            self.assertEqual(result["invocations"], 2)

    def test_finalize_refused_then_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)

            def runner(command):
                directory = profile.loop_dir(root, "L1")
                (directory / "finalize.json").write_text(
                    "{}", encoding="utf-8"
                )  # premature
                return 0

            result = supervise(
                profile,
                "L1",
                project_root=root,
                budget=SupervisorBudget(max_finalize_rejections=1),
                runner=runner,
                emit=lambda _: None,
                delivery=lambda: DeliveryAssessment(
                    clean=True, pushed=True, head="a", origin_main="a"
                ),
            )
            self.assertEqual(result["stopped_reason"], "fail_closed_finalize")

    def test_completes_when_all_gates_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)

            def runner(command):
                directory = profile.loop_dir(root, "L1")
                coverage = profile.coverage_file(root)
                coverage.parent.mkdir(parents=True, exist_ok=True)
                coverage.write_text(
                    json.dumps(_terminal_coverage(profile)), encoding="utf-8"
                )
                (directory / "journal.jsonl").write_text(
                    json.dumps({"step": 1, "axis": "debug.axis_a"}) + "\n",
                    encoding="utf-8",
                )
                (directory / "finalize.json").write_text("{}", encoding="utf-8")
                return 0

            result = supervise(
                profile,
                "L1",
                project_root=root,
                budget=SupervisorBudget(max_invocations=5),
                runner=runner,
                emit=lambda _: None,
                delivery=lambda: DeliveryAssessment(
                    clean=True, pushed=True, head="a", origin_main="a"
                ),
            )
            self.assertEqual(result["stopped_reason"], "completed")

    def test_status_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = _write_profile(root)
            request_stop(profile, "L1", project_root=root)
            snapshot = status(profile, "L1", project_root=root)
            self.assertEqual(snapshot["loop_id"], "L1")
            self.assertTrue(snapshot["stop_sentinel"])


if __name__ == "__main__":
    unittest.main()
