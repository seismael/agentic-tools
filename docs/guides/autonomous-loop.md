# Guide: Running the Autonomous Optimization Loop Across AI Agent Hosts

This guide explains how to operate the generic, token-efficient, and deterministic **Autonomous Optimization Loop** across multiple AI coding agent environments including **Antigravity CLI/IDE**, **OpenCode**, **Claude Code**, and **Codex CLI**.

---

## 1. Overview of the Autonomous Loop

The Autonomous Optimization Loop is a structured, 5-stage engineering pipeline designed to allow AI agents to iteratively improve complex software repositories, systems, and quantitative models without human intervention at every intermediate step:

1. **Stage 1: Autonomous Reconnaissance & Invariant Mapping**
   - The agent reads `<project>/docs/knowledge/index.md` (< 400 tokens) to orient paths, configs, and constraints without running blind `find` or `ls` scans.
2. **Stage 2: Empirical Gap Diagnosis & Causal Forensics**
   - The agent decomposes opportunity gaps between current performance and theoretical potential using CLI diagnostics.
3. **Stage 3: Surgical Candidate Formulation & Pre-Evaluation Snapshot Gate**
   - The agent makes minimal, targeted code/config edits and commits them to Git prior to running evaluations, ensuring immutable evaluation artifacts and preventing `RuntimeIdentityError`.
4. **Stage 4: Dual-Gate Verification & Synthetic Fixture Realignment**
   - The candidate is tested for both primary metric gain and invariant preservation. Test fixtures asserting outdated nominal values are updated cleanly in the same commit.
5. **Stage 5: Compounding Knowledge Persistence & Atomic Publication**
   - The agent logs findings to `docs/audit/findings/`, records decisions in `docs/knowledge/decisions.md`, updates `known_defects.md`, and pushes commits upstream.

---

## 2. Environment-Specific Instructions

### A. Google Antigravity (CLI & IDE)

In Antigravity CLI (`agy`) or Antigravity IDE:

1. **Skill Installation**:
   Ensure `skills/audit` and `skills/knowledge` are linked or placed in `~/.gemini/antigravity-cli/skills/` or `.agents/skills/`.
2. **Initial Prompt**:
   ```
   Execute the autonomous optimization loop on this repository following skills/audit/references/autonomous-loop.md.
   1. Read docs/knowledge/index.md to orient paths and invariants.
   2. Diagnose current performance gaps against theoretical ceiling.
   3. Formulate minimal candidates, committing working tree before evaluating.
   4. Enforce dual-gate verification (metric improvement + zero invariant regressions).
   5. Record findings, update docs/knowledge/decisions.md, and push atomic commits when validated.
   ```
3. **Execution Features**:
   - The agent uses `run_command` for background tasks (`WaitMsBeforeAsync`).
   - The agent generates structured plans as artifacts (`ArtifactMetadata`).
   - The agent maintains absolute token frugality and zero conversational chatter.

---

### B. OpenCode

In OpenCode:

1. **Skill Configuration**:
   Place or symlink `agentic-tools/skills/` into your OpenCode skills directory (e.g. `~/.config/opencode/skills/` or repository root `.opencode/`).
2. **Initial Prompt**:
   ```
   Run the autonomous optimization loop for this project:
   - Refer to skills/audit/references/autonomous-loop.md for the 5-stage protocol.
   - Use docs/knowledge/ for repository facts, data topology, and invariants.
   - Always commit candidate changes before running background evaluations.
   - Verify both primary metric gain and invariant test passes.
   - Record findings in docs/audit/ and update decisions in docs/knowledge/.
   - Push verified improvements to origin/main.
   ```
3. **Tips for OpenCode**:
   - Remind the model to stay token-frugal and not output conversational pleasantries.
   - Ensure OpenCode's terminal permissions allow running git commits and tests.

---

### C. Claude Code

In Claude Code (`claude` CLI):

1. **Skill Configuration**:
   Copy or link `skills/audit` and `skills/knowledge` into `.claude/skills/` or reference them directly in `CLAUDE.md`.
2. **Initial Prompt**:
   ```
   Start the autonomous optimization cycle following skills/audit/references/autonomous-loop.md.
   Begin by checking docs/knowledge/index.md, run the baseline evaluation, and identify the top opportunity gap.
   Ensure every candidate is committed before running evaluations, tests pass, and knowledge leaves are updated.
   ```
3. **Tips for Claude Code**:
   - Instruct Claude Code to keep individual terminal outputs bounded (`head -n 50` or using structured JSON).
   - Use git commands cleanly without leaving uncommitted files.

---

### D. OpenAI Codex CLI

In OpenAI Codex CLI:

1. **Skill Configuration**:
   Install via `python tools/install_skill.py --skill audit --to ~/.codex/skills/audit`.
2. **Command / Prompt**:
   ```
   $audit Run the autonomous optimization loop following skills/audit/references/autonomous-loop.md.
   Focus on maximizing the target objective while strictly upholding project invariants.
   Commit working tree before each evaluation run and document all accepted findings.
   ```

---

## 3. Best Practices for Human Supervisors

- **Permissions**: Grant the agent terminal execution and git permissions so it can autonomously commit, evaluate, test, and push.
- **Knowledge Base as Source of Truth**: Encourage the agent to read and update `docs/knowledge/` leaves (`invariants.md`, `decisions.md`, `known_defects.md`). This guarantees that context survives session restarts and context truncations.
- **Pre-Evaluation Snapshots**: Ensure the agent always commits candidate code before running evaluations. Dirty worktrees cause evaluator provenance checks to fail.
- **Verification Gates**: Never accept candidates that fail invariant unit tests, even if they show short-term metric improvements.
