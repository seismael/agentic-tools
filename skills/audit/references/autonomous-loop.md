# Autonomous Optimization Loop: End-to-End Execution Protocol

A domain-agnostic, token-efficient, deterministic protocol for AI coding agents to autonomously diagnose, optimize, verify, and promote software, systems, and quantitative models.

---

## 1. Architectural Principles

Autonomous optimization must balance rapid iteration with rigorous system integrity. The loop is governed by 5 mandatory axioms:

1. **Information Density & Zero Conversational Chatter**: Agents communicate with maximum token frugality. Never emit conversational filler, polite preambles, or restatements of user requests. Output actionable findings, structured decision cards, and exact file/symbol links.
2. **Deterministic & Bounded Observability**: Never stream raw logs, massive time series, or full repository file trees into context. Delegate heavy metrics computation to host CLI tools and consume byte-bounded projections ($\le 2,500$ bytes per section).
3. **Pre-Evaluation Snapshot Gate**: Never evaluate candidates against a dirty or mutable working tree. Commit or stash candidate modifications before launching long-running evaluations to guarantee immutable run manifests and prevent artifact collisions (`RuntimeIdentityError`).
4. **Dual-Gate Verification**: Every candidate promotion requires satisfying two independent criteria:
   - **Primary Metric Improvement**: Measurable improvement in the target objective function (e.g. net profit, latency reduction, throughput, test coverage, memory footprint).
   - **Invariant Soundness**: Zero regressions in core system axioms (e.g. determinism, conservation laws, safety collars, path isolation, type checks).
5. **Continuous Knowledge Compounding**: Every verified finding, accepted decision, and disproven hypothesis is persisted to a local Markdown knowledge base (`docs/knowledge/` or `.<project>/knowledge/`) so subsequent agent sessions avoid repeating redundant work or hitting known traps.

---

## 2. The 5-Stage Autonomous Loop

```
[Stage 1: Reconnaissance] ──► [Stage 2: Gap Diagnosis] ──► [Stage 3: Candidate Formulation]
                                                                        │
[Stage 5: Upstream Push]  ◄── [Stage 4: Dual-Gate Verification] ◄───────┘
```

### Stage 1: Autonomous Reconnaissance & Invariant Mapping
1. **Boot from Knowledge Base**:
   - Check if `<project>/docs/knowledge/index.md` or `.<project>/knowledge/index.md` exists.
   - If present, read **only** `index.md` (< 400 tokens) to discover the project layout.
   - Load specific leaves relevant to the task:
     - `data_topology.md` to identify configuration, data, and log directories.
     - `invariants.md` to identify inviolable rules and safety limits.
     - `known_defects.md` to identify bugs, traps, and anti-patterns to avoid.
   - If absent, bootstrap the project wiki using the standard templates from `skills/knowledge/assets/templates/`.
2. **Pin the Baseline Ref**:
   - Confirm current git commit hash (`git rev-parse HEAD`) and verify a clean working tree (`git status`).
   - Run the project's narrow baseline test suite to confirm existing health before touching code.

### Stage 2: Empirical Gap Diagnosis & Causal Forensics
1. **Opportunity Gap Decomposition**:
   - Decompose the difference between current realization and the theoretical ceiling into distinct causal categories:
     - *Coverage/Elasticity Gap*: Missed entries or opportunities where signals failed to trigger.
     - *Execution Lockout Gap*: Opportunities missed because the system was locked in an existing suboptimal state.
     - *Filtering Drag*: Opportunities filtered out by overly conservative risk, sizing, or threshold rules.
2. **Empirical Distribution Inspection**:
   - Inspect empirical distributions (percentiles: p10, p25, p50, p75, p90) at missed opportunity points.
   - Identify where the current thresholds cut off high-quality opportunities or permit toxic churn.

### Stage 3: Surgical Candidate Formulation & Pre-Evaluation Snapshot
1. **Formulate a Minimal Candidate**:
   - Propose declarative, localized modifications targeting the verified root cause.
   - Avoid sprawling multi-file refactors when a localized threshold or logic tune achieves the outcome.
   - Apply edits surgically to source files.
2. **Pre-Evaluation Snapshot Gate (CRITICAL)**:
   - Evaluators that record run manifests or compute provenance hashes require an immutable git commit.
   - Execute:
     ```sh
     git add <modified_files>
     git commit -m "feat(<subsystem>): <candidate_brief_description>"
     ```
   - If running a dry-run test without a commit, use an isolated branch or worktree. Never run background evaluations against a dirty working tree.

### Stage 4: Dual-Gate Verification & Synthetic Fixture Realignment
1. **Execute Target Evaluation**:
   - Run the benchmark, evaluation suite, or backtest.
   - Extract primary metrics and calculate the empirical delta against the baseline.
2. **Run Component & Invariant Tests**:
   - Run unit and invariant tests:
     ```sh
     python -m pytest --tier unit
     ```
   - **Synthetic Fixture Realignment**: If tests fail solely because mock fixtures or unit tests hard-coded old nominal values (which were intentionally improved), update the test fixtures to match canonical behavior within the candidate commit (`git commit --amend` or follow-up fix).
   - If tests fail due to a genuine logic regression, revert or revise the candidate immediately.
3. **Dual-Gate Decision**:
   - Both Gates Passed: Candidate qualifies for adoption.
   - Gate Failed: Withdraw candidate, log root cause in `known_defects.md`, and revert to baseline commit.

### Stage 5: Compounding Knowledge Persistence & Atomic Publication
1. **Document Audit Finding**:
   - Write a structured finding file `docs/audit/findings/F-XXX.md` detailing:
     - Target issue and root cause.
     - Evidence and reproduction steps.
     - Before/after empirical metric realization.
     - Files modified and verification status.
   - Update `docs/audit/audit.json` with the new finding record.
2. **Persist Knowledge Base Entries**:
   - Append the accepted decision and metric delta to `docs/knowledge/decisions.md`.
   - Update `docs/knowledge/data_topology.md` if new runtime artifacts or report paths were generated.
3. **Atomic Upstream Publication**:
   - Stage all audit documents and knowledge updates:
     ```sh
     git add docs/audit/ docs/knowledge/
     git commit -m "docs(audit): register F-XXX and update decisions"
     git push origin <branch>
     ```

---

## 3. Cross-Platform Execution Patterns

The autonomous loop is fully host-agnostic and can be driven by any modern AI coding agent:

### A. Google Antigravity (CLI & IDE)
- **Invocation**: Invoke `/audit` to start an investigation, `/knowledge` to manage the wiki, or `/enhance` to optimize agent settings.
- **Tools**:
  - Run commands via `run_command` with synchronous timeouts or background tasks via `manage_task`.
  - Use `write_to_file` and `replace_file_content` for surgical code edits.
  - Present plans via artifacts (`ArtifactMetadata: {RequestFeedback: true}`).
- **Context Economy**: Strict zero-chatter; delegate analytics to CLI commands (`apex diagnostic gap`, `apex campaign batch-eval`).

### B. OpenCode
- **Invocation**: Place prompt instructions matching the audit contract in `.opencode/` or trigger via direct natural language instruction: `"Run the autonomous audit loop using skills/audit"`.
- **Tools**:
  - Use native terminal commands to inspect git status, run tests, and commit snapshots.
  - Ingest `docs/knowledge/index.md` first before exploring source trees.

### C. Claude Code
- **Invocation**: Use `/audit-project` or direct prompt reference to `skills/audit/SKILL.md`.
- **Tools**:
  - Execute commands via `Bash`.
  - Use file reading and editing tools for targeted edits.
  - Use git CLI to commit snapshots before executing evaluations.

### D. Codex CLI
- **Invocation**: Trigger via `$audit` or `$knowledge`.
- **Tools**:
  - Use terminal commands to run checks, evaluations, and git commits.
  - Adhere strictly to the pre-evaluation snapshot protocol.
