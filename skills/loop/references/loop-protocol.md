# Loop Protocol: Autonomous Continuous Optimization Engine

Detailed operational mechanics for executing goal-directed, endless autonomous
optimization loops across any codebase. The engine is generic; the
[project profile](../assets/templates/profile.template.yaml) supplies every project
specific.

---

## 1. Goal Deconstruction & Target Formulation

From the profile (or a supplied goal):

1. **Target Objective** — the scalar/vector `metric` to optimize (read from the profile).
2. **Operational Constraints** — `modes`, `boundaries`, time/budget, stop criteria.
3. **Repository Context** — never ask the user for paths. Read `docs/knowledge/index.md`,
   then `capabilities.md`, then the profile. If the profile is absent, bootstrap it.

---

## 2. The Front-Driven Pipeline

The loop is not a single linear pass; it is a dispatcher over **fronts** (see the
[front taxonomy](front-taxonomy.md)).

### Step 1: Orient
- Confirm `git rev-parse HEAD` / `git status`; read the profile and the coverage ledger.
- If no recent baseline artifact exists, run the profile's `evaluate` stage once to
  reproduce ground truth. Record it in the `orient` front.

### Step 2: Dispatch
- Apply the [dispatch policy](dispatch-policy.md): pick the front and sub-axis that most
  advances the goal. Update `next_moves.json` with ranked candidates + kill-criteria.

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
- **Pass**: write the finding, append the decision, update `capabilities.md`, push, and
  mark the coverage sub-axis `COVERED-SOUND`/adopted. The candidate becomes the baseline.
- **Fail**: revert, record the failure mode (an *inert* result is recorded, never adopted),
  and mark the axis `COVERED-EXHAUSTED` if the frontier is proven exhausted.
- Always update the [coverage ledger](coverage-ledger.md) for the axis just examined.

### Step 7: Endless Recurrence
- Proceed immediately to Step 2. Stop only when: the goal `target` is met **and** coverage
  is complete; coverage is complete with the frontier exhausted; the operator writes
  `STOP`; or a budget fires. A `finalize.json` is accepted only under those conditions.

---

## 3. Completion

The loop may conclude only when **all** hold:

1. The [coverage ledger](coverage-ledger.md) is complete (every required axis terminal; no
   open defect).
2. The issue queue has no open actionable item.
3. Delivery is clean: working tree clean and `HEAD == origin/main` (everything adopted is
   committed and pushed).

Otherwise the finalize is refused and the loop continues. Repeated refusal, repeated
invocation errors, or a stalled journal fail closed for operator attention.

## 4. Boundaries

This is development tooling. It obeys `profile.modes` and `profile.boundaries`, never
performs a production action, and never weakens determinism, safety, or correctness.
