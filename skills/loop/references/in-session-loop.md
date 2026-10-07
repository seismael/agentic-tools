# In-Session Loop: the Self-Contained Autonomous Engine

The loop is **not a process, a daemon, a plugin, or a CLI**. It is a way of working that the
agent performs **inside its own session**: a single, sequential, continuous, self-managed
loop that reads durable state from the project, takes **one atomic step at a time**, records
the step, and immediately continues. The agent *is* the engine. This makes it generic (any
project), agnostic (any domain), and fully portable (a skill plus files — nothing to install,
nothing outside the repository to trust).

## The loop (sequential, one atomic step per iteration)

```
repeat
  1. Read state     goal.json + coverage.json + journal tail + knowledge + capabilities
  2. Dispatch       choose the single next step (dispatch policy); record next_moves
  3. Act            do exactly that one step; delegate breadth to subagents
  4. Verify         run the step's gate (invariants always; objective for economic changes)
  5. Persist        append the journal record; update coverage.json / goal.json / issues.jsonl
  6. Continue       go to 1 immediately
until the goal target is met with coverage complete, or an actionable issue blocks progress,
      or the user says stop
```

- **Continue immediately.** Do not end the turn while actionable work remains. Only yield to
  the user when the goal is met, you are genuinely blocked (state why in `goal.json`), or the
  user tells you to stop.
- **One step at a time.** No batching unrelated work; each iteration is a coherent unit with
  its own evidence and gate, so progress is auditable and resumable.
- **The user can steer at any time.** A message is a live directive: fold it into the next
  move. It never abandons the goal unless the user says so.

## Durable state: the loop's memory and process

State lives in files inside the project (paths from the profile), so the loop survives
compaction and a resumed session continues exactly where it stopped.

| File | Purpose | Shape |
| :--- | :--- | :--- |
| `goal.json` | Objective, status, sub-goals | `{goal, status: ACTIVE\|DONE\|STOPPED\|BLOCKED, sub_goals: [{id, statement, status}], updated_at}` |
| `coverage.json` | Breadth proof (fronts) | see [coverage ledger](coverage-ledger.md) |
| `journal.jsonl` | One record per step | `{step, front, axis, action, evidence, outcome, ts}` |
| `issues.jsonl` | Findings ledger | see [dispatch policy](dispatch-policy.md) |

`goal.json`, `journal.jsonl`, and `issues.jsonl` live under the profile's `paths.loop`;
`coverage.json` lives under the profile's `paths.coverage` (default in the knowledge base).

**Compaction is expected and harmless.** If the conversation is summarized, re-read these
files and the knowledge base; they — not the transcript — are the truth. A brand-new session
resumes by reading them and running the loop from step 1.

## Delegation: the director is the only writer

Keep the session small by delegating heavy or high-output work to subagents and consuming
only their **bounded** summaries.

- **Delegate:** multi-file exploration, deep source synthesis, independent verification,
  anything whose raw output would flood context.
- **Never delegate a write.** The main session applies every change; subagents are
  read-only analysts. This keeps one writer, one deterministic history.
- **Bounded projections only.** Each subagent returns a compact summary (findings + exact
  `path:line` evidence), not file dumps. Recompute nothing in the main session that a
  subagent already computed.

## Token economy

- Read the smallest sufficient slice; never read the same file twice; prefer `grep` with
  context over whole-file reads.
- Journal records are one line each — terse by design.
- Prefer the project's canonical pipeline commands (which return bounded artifacts) over
  hand-rolled analysis.
- On a large context, write a compact handoff into the state files and continue.

## Portability

The entire engine is **this skill plus the project's state and knowledge files**. Any
tool-calling agent host runs it identically; the only host-specific detail is how the user
invokes the loop ("use the loop skill with goal: …"), which every host does natively. There
is no external component to install, version, or trust.
