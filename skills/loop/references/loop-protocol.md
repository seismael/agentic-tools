# Loop Protocol: Autonomous Continuous Optimization Engine

Detailed operational mechanics for executing a goal-directed, endless, autonomous
optimization loop **in-session**. The engine is generic and portable; the
[project profile](../assets/templates/profile.template.yaml) supplies every project
specific. The loop itself is defined in the [in-session loop](in-session-loop.md).

---

## 1. Goal Deconstruction & Target Formulation

From the profile (or a supplied goal):

1. **Target Objective** — the scalar/vector `metric` to optimize (read from the profile).
2. **Operational Constraints** — `modes`, `boundaries`, stop criteria.
3. **Repository Context** — never ask the user for paths. Read `docs/knowledge/index.md`,
   then `capabilities.md`, then the profile. If the profile is absent, bootstrap it.

Write the objective and its sub-goals to `goal.json` under the profile's `paths.loop`.

---

## 2. The Front-Driven, Sequential Loop

The loop is a dispatcher over **fronts** (see the [front taxonomy](front-taxonomy.md)),
executed one atomic step at a time, continuously, inside the session.

### Step 1: Orient
- Confirm the repository state (branch, clean/dirty) and read the profile, `goal.json`, the
  [coverage ledger](coverage-ledger.md), and the journal tail.
- If no recent baseline artifact exists, run the profile's `evaluate` stage once to
  reproduce ground truth. Record it in the `orient` front.

### Step 2: Dispatch
- Apply the [dispatch policy](dispatch-policy.md): pick the single step that most advances
  the goal. Update the ranked next moves (in `goal.json` or a sibling file).

### Step 3: Diagnose (for value fronts)
- Run the relevant pipeline `diagnose` stage; consume only byte-bounded projections
  (≤ 2,500 bytes per artifact). Localize the single largest component of drag/opportunity.

### Step 4: Candidate & Snapshot
- Make the minimal localized change (or, for `debug`, the minimal fix + regression test).
- Commit the snapshot: `feat(candidate): test hypothesis for <gap_id>`.
- Never evaluate an uncommitted worktree.

### Step 5: Evaluate & Dual-Gate
- Launch the pipeline `evaluate`/`experiment` stages headless.
- **Gate A (Objective)**: the metric is strictly superior (per the profile).
- **Gate B (Invariants)**: every boundary/axiom/limit test passes.

### Step 6: Decide & Compound
- **Pass**: write the finding, append the decision, update `capabilities.md`, push, and mark
  the coverage sub-axis adopted.
- **Fail**: revert, record the failure mode (an *inert* result is recorded, never adopted),
  and mark the axis `COVERED-EXHAUSTED` if the frontier is proven exhausted.
- Always update the [coverage ledger](coverage-ledger.md) and append a `journal.jsonl`
  record for the step just taken.

### Step 7: Continue (Endless Recurrence)
- Persist the step, then **immediately** go to Step 2. Do not stop between steps.
- Stop only when: the goal `target` is met **and** coverage is complete; an actionable issue
  leaves you genuinely blocked (record `status: BLOCKED` with the reason); or the user says
  stop.

---

## 3. Completion

The loop may conclude only when **all** hold:

1. The [coverage ledger](coverage-ledger.md) is complete (every required axis terminal; no
   open defect).
2. The issue ledger has no open actionable item.
3. The goal `target` is met (or the frontier is provably exhausted with evidence).

On completion, set `goal.json` `status: DONE`, summarize the verified deltas, and yield.

## 4. Boundaries

This is development tooling. It obeys `profile.modes` and `profile.boundaries`, never
performs a production action, and never weakens determinism, safety, or correctness.
