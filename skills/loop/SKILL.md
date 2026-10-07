---
name: loop
description: Autonomous continuous optimization engine for software, quantitative trading, and systems engineering. Takes a single high-level goal and runs endless autonomous iterative cycles of diagnosis, candidate formulation, pre-evaluation snapshot, dual-gate verification, and knowledge compounding without stopping or asking intermediate questions.
---

# Loop (Autonomous Continuous Optimization Engine)

Execute endless, autonomous, goal-directed optimization cycles on any repository. The user
supplies only a single high-level objective (e.g. `/loop improve net profit across all
symbols` or `/loop reduce p99 latency under 5ms for the next 2 hours`). The agent derives
all operational details, discovers the data topology and execution commands, and iterates
continuously until the goal or time budget is satisfied.

The loop is **generic and agnostic**: the engine and its cognition are identical for every
project; a single declarative [project profile](references/project-profile.md) supplies
what to optimize, what to examine, how to run it, and when to stop. It explores the
project across **all fronts** — audit, discover, research, diagnose, debug, improve,
harden, performance, pipeline, knowledge, planning, orientation — deciding the next step
from accumulated evidence, never arbitrarily. See the [front taxonomy](references/front-taxonomy.md),
the [dispatch policy](references/dispatch-policy.md), the [coverage ledger](references/coverage-ledger.md),
the [pipeline contract](references/pipeline-contract.md), and the [runner contract](references/runner-contract.md).

## Operating Contract

- **Single-Sentence Autonomous Activation**: The user specifies only the objective and
  optional bounds. Never pause for intermediate instructions, ask where files are, or ask
  whether to run baselines. Derive all context autonomously.
- **Zero Conversational Chatter**: Output only concise progress summaries, verified
  quantitative deltas, and atomic git commit references.
- **Profile-Driven Boot**: Read the [project profile](references/project-profile.md)
  (`docs/knowledge/profile.yaml`); if absent, bootstrap the wiki and run the knowledge
  skill's capability-discovery protocol, then seed `docs/knowledge/index.md`,
  `capabilities.md`, and the profile itself. Load `capabilities.md` so tool selection is
  deliberate.
- **Coverage Guarantee**: Maintain the [coverage ledger](references/coverage-ledger.md):
  every required front/sub-axis must reach a terminal status (COVERED-SOUND,
  COVERED-EXHAUSTED, or BLOCKED-EXTERNAL with a reason). A metric may not be blamed while
  any required axis is unexamined.
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
- **Failure Recovery & Backoff**: If a candidate fails either gate, revert to the baseline
  commit, record the failure mode, and proceed to the next hypothesis.

---

## The Execution Cycle

```
1. Orient          -- profile + knowledge + capabilities; reproduce the baseline
2. Dispatch        -- choose the next front/move by the dispatch policy
3. Diagnose        -- run the pipeline; localize the dominant gap (no guessing)
4. Candidate       -- one bounded, falsifiable change; snapshot to git
5. Evaluate+Gate   -- pipeline run; objective + invariant gates
6. Compound        -- adopt (commit+push) or revert; update knowledge AND the coverage ledger
7. Repeat          -- immediately; stop only on completion, coverage-complete, or budget
```

Detailed lifecycle mechanics, including the front-driven loop and coverage semantics, are
in the [loop protocol](references/loop-protocol.md).
