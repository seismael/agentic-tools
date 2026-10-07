# Loop Protocol: Autonomous Continuous Optimization Engine

Detailed operational mechanics for executing goal-directed, endless autonomous optimization loops across any codebase.

---

## 1. Goal Deconstruction & Target Formulation

When receiving a single-sentence goal (e.g. `/loop improve net profit across all symbols` or `/loop reduce latency below 10ms for 2 hours`):

1. **Extract Target Objective**: Identify the primary scalar or vector metric to optimize (e.g., Net PnL, Profit Factor, Latency, Throughput, Error Rate).
2. **Extract Operational Constraints**: Identify any time budget, stop criteria, or safety bounds. If no time budget is given, iterate continuously until major opportunity gaps are exhausted or no further positive candidate can be validated.
3. **Resolve Repository Context**: Never ask the user where directories or files are located. Read `docs/knowledge/index.md` first, then `docs/knowledge/capabilities.md` to select tools deliberately.

---

## 2. Autonomous Iteration Pipeline

### Step 1: Baseline Verification
- Check current git commit hash (`git rev-parse HEAD`) and working tree status (`git status`).
- Check `docs/knowledge/decisions.md` to establish current champion baseline metrics.
- Check `docs/knowledge/capabilities.md` for the CLI/engine/verification surfaces that produce those metrics.
- If no recent evaluation artifact exists, run the baseline evaluation headless once to establish ground truth.

### Step 2: Gap Diagnosis & Hypothesis Formulation
- Inspect the diagnostic output of the latest run (decision funnels, error counts, latency breakdowns, trade logs) using byte-bounded queries ($\le 2,500$ bytes).
- Identify the single largest component contributing to performance drag (e.g., false breakouts, trailing stop slippage, lockouts, CPU bottlenecks).
- Formulate a falsifiable hypothesis and design the minimal localized code or configuration modification.

### Step 3: Pre-Evaluation Snapshot Gate
- Apply the surgical change to source code or configuration.
- Stage and commit the change to Git:
  ```sh
  git add <touched_files>
  git commit -m "feat(candidate): test hypothesis for gap <gap_id>"
  ```
- *Strict Rule*: Never launch evaluations against an uncommitted worktree.

### Step 4: Headless Execution & Dual-Gate Verification
- Launch the target evaluation or benchmark in the background.
- Upon completion, evaluate the two verification gates:
  - **Gate A (Objective Metric)**: Is the metric strictly superior to the baseline?
  - **Gate B (Invariant Soundness)**: Did all core invariant tests and conservation laws pass?

### Step 5: Decision & Compounding
- **If Both Gates Pass**:
  1. Write structured finding in `docs/audit/findings/F-XXX.md`.
  2. Update `docs/audit/audit.json`.
  3. Append the accepted decision to `docs/knowledge/decisions.md`; append any newly discovered command, engine, or data surface to `docs/knowledge/capabilities.md`.
  4. Push the commit upstream: `git push origin <branch>`.
  5. The new candidate becomes the new active baseline.
- **If Either Gate Fails**:
  1. Revert the commit immediately (`git reset --hard HEAD~1`).
  2. Record the failure mode and anti-pattern in `docs/knowledge/known_defects.md`.
  3. Formulate the next alternative hypothesis.

### Step 6: Endless Recurrence
- Without pausing or outputting conversational filler, immediately proceed to Step 2 to target the next opportunity gap.
