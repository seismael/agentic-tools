---
name: loop
description: Autonomous continuous optimization engine for software, quantitative trading, and systems engineering. Takes a single high-level goal and runs endless autonomous iterative cycles of diagnosis, candidate formulation, pre-evaluation snapshot, dual-gate verification, and knowledge compounding without stopping or asking intermediate questions.
---

# Loop (Autonomous Continuous Optimization Engine)

Execute endless, autonomous, goal-directed optimization cycles on any repository. The user supplies only a single high-level objective (e.g. `/loop improve net profit across all symbols` or `/loop reduce p99 latency under 5ms for the next 2 hours`). The agent derives all operational details, discovers data topologies and execution commands, and iterates continuously until the goal or time budget is satisfied.

## Operating Contract

- **Single-Sentence Autonomous Activation**: The user only specifies the target objective and optional bounds (e.g., time limit, target metric). Never pause, prompt for intermediate instructions, ask where files are located, or ask whether to run baselines. Derive all context autonomously.
- **Zero Conversational Chatter**: Never emit conversational filler, status monologues, or polite preambles. Output only concise progress summaries, verified quantitative deltas, and atomic git commit references.
- **Automatic Knowledge Booting**: Always boot from `<project>/docs/knowledge/index.md` (or `.<project>/knowledge/index.md`) if present (< 400 tokens) to orient paths, configs, invariants, and prior decisions. If absent, bootstrap it autonomously from standard templates.
- **Pre-Evaluation Snapshot Protocol**: Before launching long-running evaluators, benchmarks, or backtests, always stage and commit candidate changes to Git (`feat(candidate): ...`) to ensure immutable run manifests and prevent artifact collisions.
- **Dual-Gate Verification**: Every candidate promotion requires:
  1. *Primary Metric Improvement*: Measurable positive gain in the target objective function.
  2. *Invariant Soundness*: Zero violations of project axioms, safety boundaries, or non-negotiable invariants.
- **Continuous Knowledge Compounding**: For every accepted candidate, record the finding in `docs/audit/findings/`, append the decision to `docs/knowledge/decisions.md`, and push to upstream Git.
- **Failure Recovery & Backoff**: If a candidate fails either gate, immediately revert to the baseline commit, record the failure mode in `docs/knowledge/known_defects.md`, and proceed to the next hypothesis.

---

## The Execution Cycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Autonomous Orientation (Read docs/knowledge/index.md)    │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Gap Diagnosis (Analyze funnels, profilers, benchmarks)   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Surgical Candidate Formulation & Git Commit Snapshot     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Headless Evaluation & Dual-Gate Verification             │
│    - Pass: Record finding, update decisions, push to Git    │
│    - Fail: Revert to baseline commit, log defect to wiki    │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Repeat Immediately on Next Primary Gap                   │
└─────────────────────────────────────────────────────────────┘
```

See [loop protocol](references/loop-protocol.md) for detailed lifecycle mechanics.
