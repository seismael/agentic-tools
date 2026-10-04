#!/usr/bin/env python3
"""Read-only structural checks for an Audit Project bundle; Python 3.10+."""

import argparse
from collections import deque
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit


LIMIT = 2 * 1024 * 1024
MAX_ERRORS = 40
HEADINGS = (
    "Finding", "Evidence", "Decision", "Implementation plan", "Validation",
    "Risks and rollback",
)
ENUMS = {
    "kind": {"defect", "risk", "opportunity", "alignment", "question"},
    "severity": {"critical", "high", "medium", "low", "info"},
    "priority": {"P0", "P1", "P2", "P3"},
    "confidence": {"confirmed", "supported", "hypothesis"},
    "status": {"undecided", "accepted", "deferred", "rejected", "superseded"},
    "plan_status": {"none", "draft", "ready", "blocked", "done"},
}
PLACEHOLDER = re.compile(
    r"(?i:\b(?:TODO|TBD)\b|\{\{[^\n}]+\}\}|<\s*(?:insert|fill|replace)\b)"
    r"|\bREPLACE(?:_[A-Z0-9]+)*\b",
)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def relative_path(value):
    if not nonempty(value) or any(c in value for c in ("\\", ":", "\x00")):
        return False
    parts = value.split("/")
    return not PurePosixPath(value).is_absolute() and all(p not in {"", ".", ".."} for p in parts)


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def invalid_constant(_value):
    raise ValueError("non-finite JSON number")


def sections(text):
    """Only real level-two Markdown headings count, never fenced examples."""
    result, current, fence = {}, None, None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            if current is not None:
                result[current].append(line)
            continue
        if fence is None and line.startswith("## "):
            current = line[3:].strip().rstrip("#").strip()
            result.setdefault(current, [])
        elif current is not None:
            result[current].append(line)
    return result


class Validator:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.errors = []
        self.omitted = 0

    def error(self, message):
        # Findings originate in untrusted repositories; keep terminal output bounded.
        message = "".join(c if c.isprintable() else "?" for c in message)
        message = message.encode("ascii", "backslashreplace").decode("ascii")[:350]
        if len(self.errors) < MAX_ERRORS:
            self.errors.append(message)
        else:
            self.omitted += 1

    def read(self, value):
        if not relative_path(value):
            self.error("artifact path must be a safe relative POSIX path")
            return None
        try:
            path = (self.root / value).resolve()
            if not path.is_relative_to(self.root):
                self.error(f"{value}: path escapes audit root")
                return None
            if not path.is_file():
                self.error(f"{value}: missing regular file")
                return None
            with path.open("rb") as handle:
                data = handle.read(LIMIT + 1)
            if len(data) > LIMIT:
                self.error(f"{value}: exceeds {LIMIT} byte limit")
                return None
            return data.decode("utf-8")
        except (OSError, UnicodeError, ValueError, RuntimeError):
            self.error(f"{value}: unreadable UTF-8 file or invalid path")
            return None

    def text_fields(self, obj, fields, label):
        for field in fields:
            if not nonempty(obj.get(field)):
                self.error(f"{label}: {field} must be a nonempty string")

    def evidence(self, items, label):
        if not isinstance(items, list):
            self.error(f"{label}: evidence must be an array")
            return False
        has_source = False
        for item in items:
            if not isinstance(item, dict):
                self.error(f"{label}: evidence entry must be an object")
                continue
            kind = item.get("kind")
            if not isinstance(kind, str) or kind not in {"source", "test", "observation", "external"}:
                self.error(f"{label}: invalid evidence kind")
            self.text_fields(item, ("reference", "summary"), label + " evidence")
            if kind == "source" and nonempty(item.get("reference")) and nonempty(item.get("summary")):
                has_source = True
        return has_source

    def coverage(self, items):
        if not isinstance(items, list) or not items:
            self.error("coverage must be a nonempty array")
            return
        ids = set()
        for i, item in enumerate(items):
            label = f"coverage[{i}]"
            if not isinstance(item, dict):
                self.error(f"{label}: must be an object")
                continue
            self.text_fields(item, ("id", "domain", "basis"), label)
            identity = item.get("id")
            if isinstance(identity, str):
                if identity in ids:
                    self.error(f"{label}: duplicate coverage id")
                ids.add(identity)
            status = item.get("status")
            if not isinstance(status, str) or status not in {"reviewed", "partial", "unreviewed", "not_applicable", "blocked"}:
                self.error(f"{label}: invalid status")
            self.evidence(item.get("evidence"), label)
            if status in ("partial", "unreviewed", "blocked"):
                self.text_fields(item, ("next_step",), label)
            if status == "reviewed" and not item.get("evidence"):
                self.error(f"{label}: reviewed coverage requires evidence")

    def packet(self, finding, label, ready):
        path = finding.get("path")
        if not relative_path(path) or not path.startswith("findings/") or not path.endswith(".md"):
            self.error(f"{label}: path must be a Markdown file inside findings/")
            return
        content = self.read(path)
        if content is None:
            return
        title = re.search(r"^#\s+(F-[0-9]{3,})\b", content, re.MULTILINE)
        if not title or title.group(1) != finding.get("id"):
            self.error(f"{label}: packet title must start '# {finding.get('id')}: ...'")
        blocks = sections(content)
        for heading in HEADINGS:
            if heading not in blocks:
                self.error(f"{label}: packet missing heading '## {heading}'")
            elif ready and not any(line.strip() and not line.lstrip().startswith("#") for line in blocks[heading]):
                self.error(f"{label}: ready packet has empty '{heading}' section")
        if ready and PLACEHOLDER.search(content):
            self.error(f"{label}: ready packet contains an unresolved placeholder")

    def finding(self, finding, label):
        self.text_fields(finding, ("id", "title"), label)
        identity = finding.get("id")
        if not isinstance(identity, str) or not re.fullmatch(r"F-[0-9]{3,}", identity):
            self.error(f"{label}: id must match F-001 format")
        for field, choices in ENUMS.items():
            if not isinstance(finding.get(field), str) or finding[field] not in choices:
                self.error(f"{label}: invalid {field}")
        status, plan = finding.get("status"), finding.get("plan_status")
        decision = finding.get("decision")
        if not isinstance(decision, dict):
            self.error(f"{label}: decision must be an object")
        elif status == "undecided":
            if any(not isinstance(decision.get(field), str) for field in ("by", "summary", "reference")):
                self.error(f"{label}: undecided decision fields must be strings (empty allowed)")
        else:
            self.text_fields(decision, ("by", "summary", "reference"), label + " decision")
        if status in ("rejected", "superseded") and plan != "none":
            self.error(f"{label}: rejected/superseded findings must have plan_status=none")
        if status == "deferred":
            self.text_fields(finding, ("revisit_trigger",), label)
        if status == "superseded":
            self.text_fields(finding, ("superseded_by",), label)
        dependencies = finding.get("depends_on")
        if not isinstance(dependencies, list) or any(not isinstance(d, str) for d in dependencies):
            self.error(f"{label}: depends_on must be an array of finding IDs")
        elif len(dependencies) != len(set(dependencies)):
            self.error(f"{label}: duplicate dependency")
        ready = plan in ("ready", "done")
        has_source = self.evidence(finding.get("evidence"), label)
        if ready:
            if status != "accepted" or finding.get("confidence") not in ("confirmed", "supported"):
                self.error(f"{label}: ready/done requires accepted status and confirmed/supported confidence")
            if not has_source:
                self.error(f"{label}: ready/done requires source evidence")
            if PLACEHOLDER.search(json.dumps(finding, ensure_ascii=False)):
                self.error(f"{label}: ready manifest entry contains an unresolved placeholder")
        self.packet(finding, label, ready)

    def graph(self, findings):
        edges = {identity: [] for identity in findings}
        for identity, finding in findings.items():
            dependencies = finding.get("depends_on")
            if not isinstance(dependencies, list):
                continue
            for dep in dependencies:
                if not isinstance(dep, str):
                    continue
                if dep not in findings:
                    self.error(f"{identity}: unknown dependency {dep}")
                    continue
                edges[identity].append(dep)
                target = findings[dep]
                if finding.get("plan_status") in ("ready", "done") and (
                    target.get("status") != "accepted" or target.get("plan_status") not in ("ready", "done")
                ):
                    self.error(f"{identity}: dependency {dep} blocks readiness")
                if finding.get("plan_status") == "done" and target.get("plan_status") != "done":
                    self.error(f"{identity}: dependency {dep} must be done before completion")
            if finding.get("status") == "superseded":
                target = finding.get("superseded_by")
                if not isinstance(target, str) or target not in findings or target == identity:
                    self.error(f"{identity}: superseded_by must name another finding")
                else:
                    edges[identity].append(target)
        indegree = {identity: 0 for identity in edges}
        for targets in edges.values():
            for target in targets:
                indegree[target] += 1
        queue = deque(identity for identity, degree in indegree.items() if degree == 0)
        count = 0
        while queue:
            count += 1
            for target in edges[queue.popleft()]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
        if count != len(edges):
            self.error("findings contain a dependency or supersession cycle")

    def validate(self):
        raw = self.read("audit.json")
        if raw is None:
            return self.errors
        try:
            data = json.loads(raw, object_pairs_hook=object_pairs, parse_constant=invalid_constant)
        except (ValueError, RecursionError):
            self.error("audit.json: invalid JSON, duplicate keys, or excessive nesting")
            return self.errors
        if not isinstance(data, dict):
            self.error("audit.json: root must be an object")
            return self.errors
        if type(data.get("version")) is not int or data["version"] != 1:
            self.error("version must be integer 1")
        repository = data.get("repository")
        try:
            url = urlsplit(repository) if isinstance(repository, str) else None
            valid_url = bool(url and url.scheme == "https" and url.hostname and not url.username
                             and not url.password and not url.query and not url.fragment
                             and len(url.path.strip("/").split("/")) == 2
                             and relative_path(url.path.strip("/"))
                             and (url.port is None or 0 < url.port < 65536))
        except ValueError:
            valid_url = False
        if not valid_url:
            self.error("repository must be an HTTPS GitHub repository URL (public or enterprise)")
        commit = data.get("baseline_commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
            self.error("baseline_commit must be a full 40-character Git commit SHA")
        self.text_fields(data, ("focus",), "audit")
        for path in ("README.md", "CONTEXT.md"):
            value = self.read(path)
            if value is not None and not value.strip():
                self.error(f"{path}: must not be empty")
        self.coverage(data.get("coverage"))
        items = data.get("findings")
        if not isinstance(items, list):
            self.error("findings must be an array")
            return self.errors
        findings, paths = {}, set()
        for i, finding in enumerate(items):
            label = f"findings[{i}]"
            if not isinstance(finding, dict):
                self.error(f"{label}: must be an object")
                continue
            self.finding(finding, label)
            identity, path = finding.get("id"), finding.get("path")
            if isinstance(identity, str):
                if identity in findings:
                    self.error(f"{label}: duplicate finding id")
                findings[identity] = finding
            if isinstance(path, str):
                if path.casefold() in paths:
                    self.error(f"{label}: duplicate packet path (case-insensitive)")
                paths.add(path.casefold())
        self.graph(findings)
        return self.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="audit directory containing audit.json")
    args = parser.parse_args(argv)
    try:
        validator = Validator(args.root)
        errors = validator.validate()
    except (OSError, ValueError, RuntimeError, RecursionError):
        print("INVALID: unreadable audit root or malformed input", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        if validator.omitted:
            print(f"... {validator.omitted} additional errors omitted", file=sys.stderr)
        return 1
    print("VALID: artifact structure checked; evidence, decisions, and implementation remain unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
