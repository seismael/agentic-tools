"""Regression tests: python -m unittest discover -s scripts -p 'test_*.py'."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from validate_audit import HEADINGS, LIMIT, MAX_ERRORS, Validator, main


def finding(identity="F-001"):
    return {
        "id": identity, "title": "Preserve ordered retries",
        "kind": "defect", "severity": "high", "priority": "P1",
        "confidence": "confirmed", "status": "accepted", "plan_status": "ready",
        "decision": {"by": "user", "summary": "Plan the bounded retry fix.", "reference": "conversation:message-7"},
        "depends_on": [], "path": f"findings/{identity}.md",
        "evidence": [{"kind": "source", "reference": "src/queue.py:submit", "summary": "Retry bypasses sequence assignment."}],
    }


def packet(identity="F-001"):
    return f"# {identity}: Preserve ordered retries\n\n" + "\n\n".join(
        f"## {heading}\nConcrete {heading.lower()} detail for the local agent."
        for heading in HEADINGS
    ) + "\n"


class ValidateAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "audit"
        (self.root / "findings").mkdir(parents=True)
        for name in ("README.md", "CONTEXT.md"):
            (self.root / name).write_text("# Concrete audit context\n", encoding="utf-8")
        self.data = {
            "version": 1, "repository": "https://github.com/example/project",
            "baseline_commit": "a" * 40, "focus": "Queue correctness and recovery",
            "coverage": [{"id": "C-001", "domain": "Correctness", "status": "reviewed",
                          "basis": "Traced submit/retry behavior and consumers.",
                          "evidence": deepcopy(finding()["evidence"])}],
            "findings": [finding()],
        }
        self.write()

    def write(self):
        (self.root / "audit.json").write_text(json.dumps(self.data), encoding="utf-8")
        for item in self.data["findings"]:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                (self.root / "findings" / (item["id"] + ".md")).write_text(packet(item["id"]), encoding="utf-8")

    def errors(self):
        self.write()
        return Validator(self.root).validate()

    def assert_invalid(self, needle):
        self.assertTrue(any(needle in error for error in self.errors()), needle)

    def test_valid_bundle_is_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual([], Validator(self.root).validate())
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_empty_findings_and_pending_coverage_are_valid(self):
        self.data["findings"] = []
        self.data["coverage"][0].update(status="unreviewed", evidence=[], next_step="Inspect consumers.")
        self.assertEqual([], self.errors())

    def test_pin_and_version(self):
        for field, value, message in (("version", True, "version"), ("baseline_commit", "main", "baseline_commit"),
                                      ("baseline_commit", "a" * 39, "baseline_commit")):
            with self.subTest(field=field, value=value):
                old = self.data[field]
                self.data[field] = value
                self.assert_invalid(message)
                self.data[field] = old

    def test_repository_rejects_credentials_and_nonrepository_urls(self):
        for url in ("http://github.com/o/r", "https://user:secret@github.com/o/r", "https://github.com/o/r?token=x",
                    "https://github.com/o/r/tree/main", "https://github.com/o/..", "https://[broken/o/r"):
            with self.subTest(url=url):
                self.data["repository"] = url
                self.assert_invalid("repository")
        self.data["repository"] = "https://git.enterprise.example/org/repo"
        self.assertEqual([], self.errors())

    def test_required_files(self):
        for name in ("README.md", "CONTEXT.md", "findings/F-001.md", "audit.json"):
            with self.subTest(name=name):
                path = self.root / name
                saved = path.read_bytes()
                path.unlink()
                self.assertTrue(Validator(self.root).validate())
                path.write_bytes(saved)

    def test_duplicate_ids_and_packet_paths(self):
        self.data["findings"].append(deepcopy(self.data["findings"][0]))
        self.assert_invalid("duplicate finding id")
        self.data["findings"][1]["id"] = "F-002"
        self.assert_invalid("duplicate packet path")
        self.data["findings"][1]["path"] = "findings/f-001.md"
        self.assert_invalid("duplicate packet path")

    def test_safe_paths(self):
        for path in ("../outside.md", "/etc/passwd", "findings/../../outside.md", "C:\\outside.md",
                     "findings\\F-001.md", "findings/./F-001.md", "findings//F-001.md", "findings/x\x00.md"):
            with self.subTest(path=path):
                self.data["findings"][0]["path"] = path
                self.assert_invalid("path")

    def test_symlink_escape(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text(packet(), encoding="utf-8")
        link = self.root / "findings" / "escape.md"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.data["findings"][0]["path"] = "findings/escape.md"
        self.assert_invalid("escapes audit root")

    def test_manifest_symlink_escape(self):
        manifest = self.root / "audit.json"
        outside = Path(self.temp.name) / "outside.json"
        outside.write_bytes(manifest.read_bytes())
        manifest.unlink()
        try:
            manifest.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.assertTrue(any("escapes audit root" in e for e in Validator(self.root).validate()))

    def test_unknown_and_self_dependency(self):
        self.data["findings"][0]["depends_on"] = ["F-999"]
        self.assert_invalid("unknown dependency")
        self.data["findings"][0]["depends_on"] = ["F-001"]
        self.assert_invalid("cycle")

    def test_dependency_cycle_and_duplicates(self):
        second = finding("F-002")
        self.data["findings"].append(second)
        self.data["findings"][0]["depends_on"] = ["F-002"]
        second["depends_on"] = ["F-001"]
        self.assert_invalid("cycle")
        second["depends_on"] = []
        self.data["findings"][0]["depends_on"] = ["F-002", "F-002"]
        self.assert_invalid("duplicate dependency")

    def test_ready_dependency_and_done_dependency(self):
        second = finding("F-002")
        self.data["findings"].append(second)
        self.data["findings"][0]["depends_on"] = ["F-002"]
        self.assertEqual([], self.errors())
        second["plan_status"] = "done"
        self.assertEqual([], self.errors())

    def test_done_requires_completed_dependencies(self):
        self.data["findings"].append(finding("F-002"))
        self.data["findings"][0].update(plan_status="done", depends_on=["F-002"])
        self.assert_invalid("must be done")
        self.data["findings"][1]["plan_status"] = "done"
        self.assertEqual([], self.errors())

    def test_unresolved_dependency_blocks_ready(self):
        second = finding("F-002")
        self.data["findings"].append(second)
        self.data["findings"][0]["depends_on"] = ["F-002"]
        for status, plan in (("accepted", "draft"), ("accepted", "blocked"), ("deferred", "draft"),
                             ("rejected", "none"), ("undecided", "draft")):
            with self.subTest(status=status, plan=plan):
                second.update(status=status, plan_status=plan, revisit_trigger="Next milestone")
                self.assert_invalid("blocks readiness")

    def test_nonaccepted_cannot_be_ready_or_done(self):
        item = self.data["findings"][0]
        for status in ("undecided", "deferred", "rejected", "superseded"):
            for plan in ("ready", "done"):
                with self.subTest(status=status, plan=plan):
                    item.update(status=status, plan_status=plan)
                    self.assert_invalid("requires accepted")

    def test_hypothesis_cannot_be_ready(self):
        self.data["findings"][0]["confidence"] = "hypothesis"
        self.assert_invalid("confirmed/supported")

    def test_decision_attribution_is_required(self):
        self.data["findings"][0]["decision"]["reference"] = ""
        self.assert_invalid("reference")
        self.data["findings"][0].update(status="undecided", plan_status="draft", decision={"by": "", "summary": "", "reference": ""})
        self.assertEqual([], self.errors())

    def test_deferred_and_rejected_records(self):
        item = self.data["findings"][0]
        item.update(status="deferred", plan_status="draft")
        self.assert_invalid("revisit_trigger")
        item["revisit_trigger"] = "Revisit before the next release."
        self.assertEqual([], self.errors())
        item.update(status="rejected", plan_status="none")
        self.assertEqual([], self.errors())
        item["plan_status"] = "draft"
        self.assert_invalid("plan_status=none")

    def test_supersession_requires_known_acyclic_target(self):
        first = self.data["findings"][0]
        first.update(status="superseded", plan_status="none", superseded_by="F-002")
        self.assert_invalid("superseded_by")
        second = finding("F-002")
        self.data["findings"].append(second)
        self.assertEqual([], self.errors())
        second.update(status="superseded", plan_status="none", superseded_by="F-001")
        self.assert_invalid("cycle")

    def test_ready_requires_source_evidence(self):
        item = self.data["findings"][0]
        for entries in ([], [{"kind": "external", "reference": "https://example.org/paper", "summary": "Background"}],
                        [{"kind": "source", "reference": "", "summary": "Missing reference"}]):
            with self.subTest(entries=entries):
                item["evidence"] = entries
                self.assert_invalid("requires source evidence")

    def test_ready_manifest_evidence_cannot_be_template_placeholder(self):
        self.data["findings"][0]["evidence"][0]["reference"] = "REPLACE_SOURCE_REFERENCE"
        self.assert_invalid("ready manifest entry contains an unresolved placeholder")

    def test_headings_inside_code_fence_do_not_count(self):
        path = self.root / "findings" / "F-001.md"
        path.write_text("```markdown\n" + packet() + "```\n", encoding="utf-8")
        self.assertTrue(any("missing heading" in error for error in Validator(self.root).validate()))

    def test_packet_title_id_matches_manifest(self):
        (self.root / "findings" / "F-001.md").write_text(packet("F-002"), encoding="utf-8")
        self.assertTrue(any("packet title" in error for error in Validator(self.root).validate()))

    def test_empty_sections_and_ready_placeholders(self):
        path = self.root / "findings" / "F-001.md"
        path.write_text("\n".join("## " + heading for heading in HEADINGS), encoding="utf-8")
        self.assertTrue(any("empty" in error for error in Validator(self.root).validate()))
        for marker in ("TODO", "TBD", "REPLACE_ME", "REPLACE", "REPLACE_TITLE", "REPLACE_FULL_SHA",
                       "REPLACE_OR_NOT_GRANTED", "{{edit_target}}", "<insert steps>"):
            with self.subTest(marker=marker):
                path.write_text(packet() + marker, encoding="utf-8")
                self.assertTrue(any("placeholder" in error for error in Validator(self.root).validate()))

    def test_draft_allows_placeholders(self):
        self.data["findings"][0]["plan_status"] = "draft"
        self.write()
        (self.root / "findings" / "F-001.md").write_text(packet() + "TODO", encoding="utf-8")
        self.assertEqual([], Validator(self.root).validate())

    def test_coverage_states_and_duplicate_ids(self):
        entry = self.data["coverage"][0]
        entry.update(status="partial", next_step="")
        self.assert_invalid("next_step")
        entry.update(status="reviewed", evidence=[])
        self.assert_invalid("reviewed coverage requires evidence")
        entry.update(status="not_applicable", basis="No deployment artifacts exist in scope.")
        self.assertEqual([], self.errors())
        self.data["coverage"].append(deepcopy(entry))
        self.assert_invalid("duplicate coverage id")

    def test_malformed_shapes_do_not_raise(self):
        original = deepcopy(self.data)
        for field in ("kind", "severity", "priority", "confidence", "status", "plan_status", "id", "decision", "depends_on", "evidence", "path"):
            for value in (None, 1, [], {}):
                if field == "depends_on" and value == []:
                    continue
                with self.subTest(field=field, value=value):
                    self.data = deepcopy(original)
                    self.data["findings"][0][field] = value
                    self.assertTrue(self.errors())
        self.data = deepcopy(original)
        self.data["coverage"][0]["status"] = []
        self.assertTrue(self.errors())

    def test_json_errors_are_clean(self):
        for raw in ('{"version":1,"version":1}', '{"version": NaN}', '[1,2]', '{', '[' * 1100 + ']' * 1100):
            with self.subTest(raw=raw[:40]):
                (self.root / "audit.json").write_text(raw, encoding="utf-8")
                output = io.StringIO()
                with redirect_stderr(output):
                    self.assertEqual(1, main([str(self.root)]))
                self.assertNotIn("Traceback", output.getvalue())

    def test_invalid_encoding_and_file_size(self):
        path = self.root / "audit.json"
        path.write_bytes(b"\xff")
        self.assertTrue(Validator(self.root).validate())
        path.write_bytes(b" " * (LIMIT + 1))
        self.assertTrue(any("exceeds" in error for error in Validator(self.root).validate()))

    def test_errors_are_bounded_and_control_characters_escaped(self):
        self.data["findings"] = [{} for _ in range(100)]
        self.write()
        validator = Validator(self.root)
        self.assertEqual(MAX_ERRORS, len(validator.validate()))
        self.assertGreater(validator.omitted, 0)
        validator = Validator(self.root)
        validator.error("bad\x1b[31m\n" + "x" * 500)
        self.assertNotIn("\x1b", validator.errors[0])
        self.assertNotIn("\n", validator.errors[0])
        self.assertLessEqual(len(validator.errors[0]), 350)

    def test_cli_success_does_not_claim_semantic_verification(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, main([str(self.root)]))
        self.assertIn("remain unverified", output.getvalue())

    def test_nonascii_diagnostics_work_on_ascii_terminals(self):
        class AsciiOutput(io.StringIO):
            def write(self, value):
                value.encode("ascii")
                return super().write(value)

        self.data["findings"][0]["depends_on"] = ["F-\u05d0"]
        self.write()
        output = AsciiOutput()
        with redirect_stderr(output):
            self.assertEqual(1, main([str(self.root)]))
        self.assertIn("F-\\u05d0", output.getvalue())


if __name__ == "__main__":
    unittest.main()
