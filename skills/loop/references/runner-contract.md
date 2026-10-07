# Runner Contract: Hosting the Loop

The loop cognition (this skill's references) is executed by a **host runner**: a small
program that spawns one fresh agent session per step, journals progress, enforces the
gates, and stops on completion, exhaustion, or budget. The reference implementation lives
in [`scripts/loop_runner/`](../scripts/loop_runner/) and is project-agnostic — a host
supplies only a [profile](project-profile.md) and its paths.

## Responsibilities

1. **Seed the goal once.** Write `goal.json` (idempotent; never overwrite on resume) and
   inject the objective + profile path into each step's prompt.
2. **Spawn one bounded step.** A fresh session per invocation keeps context bounded;
   continuity comes from the on-disk journal, not a growing conversation.
3. **Journal everything.** `state.json` (status), `journal.jsonl` (one per step),
   `stream.jsonl` (normalized events), `issues.jsonl`, `coverage.json`.
4. **Enforce gates.** A `finalize.json` is accepted only when coverage is complete, no
   actionable issue is open, and delivery is clean (tree clean, `HEAD == origin/main`).
   Otherwise it is refused (renamed) and the loop continues.
5. **Stop cleanly.** On `STOP` sentinel (operator-only), completion, or a budget
   (`max_steps` / `max_hours`); fail closed after repeated invocation errors or a stalled
   journal.
6. **Never cross boundaries.** The runner obeys `profile.boundaries` and `profile.modes`;
   it is development tooling and never performs a production action.

## Reference library API (`skills/loop/scripts/loop_runner/`)

| Module | Provides |
| :--- | :--- |
| `profile` | `load_profile(path)`, `validate_profile(dict)` |
| `coverage` | `assess_coverage(profile, directory)` |
| `issues` | `read_issues`, `append_issue`, `assess_open_issues`, `assess_delivery` |
| `stream` | `normalize_agent_event`, event-kind constants, `STREAM_FILE` |
| `invocation` | `build_invocation(profile, loop_id, goal, agent, bin)` |
| `supervisor` | `supervise(profile, loop_id, ...)`, `status`, `request_stop` |
| `cli` | `main(host)` — `start/watch/stop/status/report/run/issue` |

A host constructs a small `Host` (profile path, project root, CLI entry) and calls
`cli.main(host)`. No domain logic lives in the runner; if a behaviour depends on the
project, it is a profile field.

## Events (`stream.jsonl`)

`supervise.start|end|refused|error|stop`, `step`, `coverage`, `issues`, and normalized
`agent.*` events mapped from the agent's JSON output. Producers and consumers import the
same constants (`stream`) to prevent drift; the host's `watch` is a read-only consumer.
