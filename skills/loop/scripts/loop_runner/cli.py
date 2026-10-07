"""Generic command-line host for the loop runner.

An agnostic host can run ``python -m loop_runner <cmd> --profile <path>`` directly; a
project with its own CLI (e.g. Click) binds the same library functions instead. No
project-specific behaviour lives here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .issues import append_issue, read_issues, update_issue
from .profile import DEFAULT_PROFILE, Profile, ProfileError, load_profile
from .stream import STREAM_FILE, read_stream, render_event
from .supervisor import SupervisorBudget, request_stop, status, supervise


def _resolve(args: argparse.Namespace) -> tuple[Profile, Path]:
    root = (
        Path(args.project_root).resolve() if args.project_root else Path.cwd().resolve()
    )
    profile_path = Path(args.profile)
    if not profile_path.is_absolute():
        profile_path = root / profile_path
    return load_profile(profile_path), root


def _parse_budget(args: argparse.Namespace) -> SupervisorBudget:
    return SupervisorBudget(
        max_invocations=getattr(args, "max_steps", 0) or 0,
        max_hours=getattr(args, "max_hours", 0.0) or 0.0,
    )


def cmd_start(args: argparse.Namespace) -> int:
    profile, root = _resolve(args)
    result = supervise(
        profile,
        args.loop_id,
        agent=args.agent,
        goal=args.goal,
        budget=_parse_budget(args),
        opencode_bin=args.opencode_bin,
        project_root=root,
    )
    print(json.dumps(result, sort_keys=True))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    profile, root = _resolve(args)
    snapshot = status(profile, args.loop_id, project_root=root)
    print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0 if snapshot["running"] or snapshot["steps"] else 1


def cmd_stop(args: argparse.Namespace) -> int:
    profile, root = _resolve(args)
    path = request_stop(profile, args.loop_id, project_root=root)
    print(f"[loop] STOP written: {path}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    profile, root = _resolve(args)
    directory = profile.loop_dir(root, args.loop_id)
    print(
        json.dumps(
            status(profile, args.loop_id, project_root=root), indent=2, sort_keys=True
        )
    )
    stream = read_stream(directory / STREAM_FILE)
    print(f"stream events: {len(stream)}")
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    profile, root = _resolve(args)
    directory = profile.loop_dir(root, args.loop_id)
    for record in read_stream(directory / STREAM_FILE):
        print(render_event(record))
    return 0


def cmd_issue(args: argparse.Namespace) -> int:
    profile, root = _resolve(args)
    directory = profile.loop_dir(root, args.loop_id)
    directory.mkdir(parents=True, exist_ok=True)
    if args.list:
        for issue in read_issues(directory):
            print(json.dumps(issue, sort_keys=True))
        return 0
    if args.resolve:
        record = update_issue(
            directory, args.resolve, status=args.status, notes=args.notes
        )
        print(json.dumps(record, sort_keys=True))
        return 0
    record = append_issue(
        directory,
        {
            "title": args.title,
            "class": args.class_,
            "severity": args.severity,
            "status": args.status,
            "source": args.source,
            "evidence": args.evidence,
        },
    )
    print(json.dumps(record, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="loop_runner", description="Generic autonomous loop runner"
    )
    parser.add_argument(
        "--profile", default=DEFAULT_PROFILE, help="path to the project profile"
    )
    parser.add_argument(
        "--project-root", default=None, help="repository root (default: cwd)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="run the loop in the foreground")
    start.add_argument("loop_id")
    start.add_argument("--goal", default=None)
    start.add_argument("--agent", default="build")
    start.add_argument("--opencode-bin", default="opencode")
    start.add_argument("--max-steps", type=int, default=0)
    start.add_argument("--max-hours", type=float, default=0.0)
    start.set_defaults(func=cmd_start)

    run = sub.add_parser("run", help="alias of start")
    run.add_argument("loop_id")
    run.add_argument("--goal", default=None)
    run.add_argument("--agent", default="build")
    run.add_argument("--opencode-bin", default="opencode")
    run.add_argument("--max-steps", type=int, default=0)
    run.add_argument("--max-hours", type=float, default=0.0)
    run.set_defaults(func=cmd_start)

    status_cmd = sub.add_parser("status", help="print a status snapshot")
    status_cmd.add_argument("loop_id")
    status_cmd.set_defaults(func=cmd_status)

    stop = sub.add_parser("stop", help="write the operator STOP sentinel")
    stop.add_argument("loop_id")
    stop.set_defaults(func=cmd_stop)

    report = sub.add_parser("report", help="print the status snapshot and stream size")
    report.add_argument("loop_id")
    report.set_defaults(func=cmd_report)

    watch = sub.add_parser("watch", help="render the stream read-only")
    watch.add_argument("loop_id")
    watch.set_defaults(func=cmd_watch)

    issue = sub.add_parser("issue", help="record or resolve an issue")
    issue.add_argument("loop_id")
    issue.add_argument("--list", action="store_true")
    issue.add_argument("--resolve", default=None, help="issue_id to update")
    issue.add_argument("--title", default="")
    issue.add_argument("--class", dest="class_", default="harness")
    issue.add_argument("--severity", default="medium")
    issue.add_argument("--status", default="OPEN")
    issue.add_argument("--source", default="")
    issue.add_argument("--evidence", default="")
    issue.add_argument("--notes", default="")
    issue.set_defaults(func=cmd_issue)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ProfileError as error:
        print(f"profile error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


__all__ = ["build_parser", "main"]
