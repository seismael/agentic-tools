---
name: loop
description: Autonomous continuous optimization engine for software, quantitative trading, and systems engineering. Takes a single high-level goal and runs endless autonomous iterative cycles of diagnosis, candidate formulation, pre-evaluation snapshot, dual-gate verification, and knowledge compounding without stopping or asking intermediate questions. Runs entirely in-session, sequentially and self-managed, with no external process or plugin.
---

# Loop (Autonomous Continuous Optimization Engine)

Run an endless, autonomous, goal-directed optimization loop **inside this session**. The user
supplies a single high-level objective (e.g. `/loop improve net profit across all symbols`
or `/loop reduce p99 latency under 5ms`). The agent derives every operational detail, reads
the project's durable state, takes **one atomic step at a time**, records it, and continues
— sequentially and self-managed — until the goal is met, it is genuinely blocked, or the
user says stop.

The loop is **generic, agnostic, and portable**: it is this skill plus the project's state
files. Nothing external is installed or trusted. It explores the project across **all
fronts** — orient, discover, audit, diagnose, research, debug, improve, harden, performance,
pipeline, knowledge, plan — deciding the next step from accumulated evidence, never
arbitrarily. See the [in-session loop](references/in-session-loop.md),
[front taxonomy](references/front-taxonomy.md), [dispatch policy](references/dispatch-policy.md),
[coverage ledger](references/coverage-ledger.md), [pipeline contract](references/pipeline-contract.md),
and [project profile](references/project-profile.md).

## Operating Contract

- **Single-Sentence Autonomous Activation**: The user specifies only the objective. Never
  pause for intermediate instructions, ask where files are, or ask whether to run baselines.
  Derive all context autonomously.
- **Zero Conversational Chatter**: Output only concise progress summaries, verified
  quantitative deltas, and atomic git commit references. The journal holds the detail.
- **Profile-Driven Boot**: Read the [project profile](references/project-profile.md)
  (`docs/knowledge/profile.yaml`); if absent, bootstrap the wiki and run the knowledge
  skill's capability-discovery protocol, then seed `docs/knowledge/index.md`,
  `capabilities.md`, and the profile. Load `capabilities.md` so tool selection is deliberate.
- **Sequential and Continuous**: Perform one atomic step per iteration, persist it, and
  continue immediately. Never yield while actionable work remains — see
  [in-session loop](references/in-session-loop.md).
- **Coverage Guarantee**: Maintain the [coverage ledger](references/coverage-ledger.md):
  every required front/sub-axis must reach a terminal status. A metric may not be blamed
  while any required axis is unexamined.
- **Evidence-Based Dispatch**: Choose the next move with the [dispatch policy](references/dispatch-policy.md)
  — defect > uncovered front > largest diagnosed gap > structural candidate > parameter
  (last) > hygiene. Reason from data, code, wiki, and prior outcomes; never act without
  grounds.
- **Pipeline Only**: Execute the project's declared canonical [pipeline](references/pipeline-contract.md)
  stages. Never hand-roll analysis or produce numbers the pipeline cannot reproduce from a
  committed snapshot.
- **Pre-Evaluation Snapshot Protocol**: Before long-running evaluators/benchmarks/backtests,
  stage and commit candidate changes (`feat(candidate): ...`) for immutable, collision-free
  artifacts.
- **Dual-Gate Verification**: Every candidate promotion requires (1) **Primary Metric
  Improvement** — a measurable gain in the objective; and (2) **Invariant Soundness** —
  zero violations of the project's boundaries, axioms, or safety limits. Neither gate may
  be weakened to pass.
- **Continuous Knowledge Compounding**: For every accepted or rejected candidate, record
  the finding, append the decision, update `capabilities.md` with any new surface, and push
  upstream. Rejections and inert results are knowledge too.
- **Failure Recovery**: If a candidate fails either gate, revert to the baseline, record the
  failure mode, and proceed to the next hypothesis.
- **Delegation (director is the only writer)**: Delegate breadth and heavy analysis to
  subagents and consume only bounded summaries; the main session applies every change.

---

## The Execution Cycle

```
1. Orient          -- profile + knowledge + capabilities; ensure a current baseline
2. Dispatch        -- choose the next front/step by the dispatch policy
3. Diagnose        -- run the pipeline; localize the dominant gap (no guessing)
4. Candidate       -- one bounded, falsifiable change; snapshot to git
5. Evaluate+Gate   -- pipeline run; objective + invariant gates
6. Compound        -- adopt (commit+push) or revert; update knowledge AND the coverage ledger
7. Continue        -- immediately; stop only when the goal is met, blocked, or the user stops
```

Full lifecycle mechanics, including the sequential in-session loop and resume semantics, are
in the [loop protocol](references/loop-protocol.md).
