# Agentic Tools

Portable skills for making AI agents more effective, reliable, and economical through their native capabilities.

## Skills

| Skill | Purpose |
|---|---|
| [Loop](skills/loop/SKILL.md) | Execute single-goal autonomous continuous optimization loops endlessly across diagnosis, candidate testing, and git compounding. |
| [Audit](skills/audit/SKILL.md) | Audit local or remote repositories against user goals and domain risks, resolve findings, and produce verified implementation plans. |
| [Knowledge](skills/knowledge/SKILL.md) | Maintain an indexed, token-efficient, Obsidian-compatible local Markdown wiki to prevent context drift and eliminate redundant exploration scans. |
| [Characterize](skills/characterize/SKILL.md) | Translate goals, domains, workflows, and constraints into a minimal native setup; interview only where evidence leaves consequential choices unresolved. |
| [Enhance](skills/enhance/SKILL.md) | Learn from actual sessions, diagnose wasted effort, and improve native settings and workflows at the correct global, project, agent, or task scope. |

Use Loop to run autonomous, endless, goal-directed optimization cycles on any codebase. Use Audit to analyze domain risks and produce structured plans. Use Knowledge to preserve repository facts and decisions across sessions. See [Autonomous Optimization Guide](docs/guides/autonomous-loop.md) for cross-platform agent execution patterns.

Loop is generic and agnostic: a single project profile (`docs/knowledge/profile.yaml`) supplies the goal, fronts, pipeline, and boundaries; a coverage ledger proves every front/sub-axis was examined; the step contract is rendered from the profile (no domain text in the engine); and a bundled, drift-checked runner lets any host drive it non-stop.

All prioritize performance and cost effectiveness: useful completed work per input/output consumption, total cost, and elapsed time, while preserving required correctness and reliability. They support research, writing, analysis, design, operations, and engineering. Loop and Audit optimize the project itself; Characterize and Enhance improve the agent setup and its usage; Knowledge compounds verified project facts.

## Install a skill

Clone this repository or download its source. Copy the **whole** selected directory under `skills/` into one supported skill location. Do not copy only `SKILL.md`, and do not install duplicate copies into locations the same agent scans.

With Python 3.10 or newer, the optional installer works on Windows, macOS, and Linux and refuses to overwrite an existing destination:

```sh
git clone https://github.com/seismael/agentic-tools.git
cd agentic-tools
python tools/install_skill.py --skill characterize --to ~/.agents/skills/characterize --check
python tools/install_skill.py --skill characterize --to ~/.agents/skills/characterize
```

The shared installer accepts any bundled skill: replace `characterize` with `enhance`, `audit`, `knowledge`, or `loop` in both arguments. The example uses Codex's documented user skill directory. See [Installation](docs/INSTALLATION.md) for OpenCode, Claude Code, Gemini CLI, Antigravity CLI (`agy`), and Antigravity IDE. Python is optional for the instruction workflow; the installer and bundled helpers require it.

## Use it

Select the skill using your host's native control. In Codex CLI, use `$characterize`, `$enhance`, `$audit`, or `$knowledge`; in Claude Code and Antigravity CLI, use `/characterize`, `/enhance`, `/audit`, or `/knowledge`. In OpenCode or Gemini CLI, explicitly request the named skill in your prompt and verify discovery through the native skill interface.

Example requests:

> Use Characterize to tailor my agent's native setup to my work. Inspect the current setup, reuse what I have already told you, ask about consequential choices, and prepare minimal changes with clear scope and recovery.

> Use Enhance to review my accessible agent sessions. Prioritize input/output cost and performance, preserve necessary validation, and propose native improvements with global and project changes separated. Ask about meaningful choices before applying configuration changes.

> Continue Enhance from its saved review state. Review new and changed sessions, evaluate the previous improvements, and apply only the already-approved changes.

> Use Enhance for this project only. Investigate repeated research and reviewer work, propose clear role ownership and compact handoffs, and preserve our deliverable requirements.

> Use Audit Project on https://github.com/OWNER/PROJECT. Focus on whether its data-import pipeline reliably fulfills the product's goals, including architecture, correctness, performance, tests, and small inconsistencies. Trace the implementation and check domain assumptions. Discuss findings with me one at a time, recommend an approach, and record accepted, deferred, and rejected decisions. Commit the audit and detailed implementation plans under docs/audit/ using the repository's supported review workflow. Do not implement product changes.

The host agent performs the work with its existing model and authorized tools. These skills are not separate agent runtimes, universal history connectors, background services, or model subscriptions.

## Agent setup and improvement

1. Discover the actual target tool/version, relevant evidence, native settings, configuration precedence, and prior checkpoints.
2. Characterize resolves goals, representative tasks, and consequential setup choices. Enhance reviews sessions individually and incrementally, including reopened sessions and late imports.
3. Diagnose supported improvements across consumption/performance, reliability, consistency, structured inputs/outputs, autonomy, orchestration, context/tools, research/review, automation/workflows, and domain/project needs.
4. Propose concrete changes and tradeoffs. Resolve consequential choices with suggested options and a custom answer. Respect existing authorization; obtain scoped approval when needed.
5. Apply through supported native surfaces, verify proportionately, and save private coverage, decision, and recovery records.

A globally installed skill can still propose a project-only change. Shared team requirements, private project preferences, native global defaults, role-specific behavior, and temporary task constraints remain distinct. Storage location alone does not determine applicability.

## Project audits and implementation handoffs

Audit Project requires a GitHub repository URL and focus message. It records a frozen source baseline, establishes project goals and domain assumptions, and traces relevant execution paths before treating a suspicion as a finding. Its coverage record distinguishes reviewed, pending, unavailable, and inapplicable areas; a focused or unfinished review is not presented as exhaustive.

Each finding receives separate impact, priority, confidence, effort, and dependency information. The agent asks about one finding at a time, offers a recommended resolution with alternatives and custom feedback, and preserves accepted, deferred, or rejected decisions. Disproven findings can be withdrawn with counterevidence without inventing a user rejection. Accepting a plan does **not** authorize product implementation.

The default target-project directory is `docs/audit/`: `README.md` provides the handoff and next work, `CONTEXT.md` captures goals and constraints, `audit.json` carries structured state, and `findings/F-001.md`-style records contain evidence, decisions, ordered implementation steps, verification, and recovery. Accepted work must pass a readiness check before a local agent starts; unresolved design choices, changed source assumptions, or missing dependencies stay explicit. Deferred work remains concise and outside the ready queue. Rejected findings retain the user's rationale. Blocked plans name their blocker and next action; completed plans require recorded acceptance-check evidence. Expected prerequisite changes can be revalidated without another approval. Audit schema v2 records these states; v1 records require explicit revalidation before conversion.

Delivery follows the request: local files, local commits, or verified GitHub publication. The audit commits documentation through available, authorized GitHub or git mechanisms when requested. It pins source reads to a commit and preserves uncommitted workspace changes. Missing write access or protected-branch restrictions remain explicit publication blockers. Its bundled read-only validator checks artifact structure and consistency; it cannot establish that findings are true, designs are correct, or tests will pass. The skill package contains no target-project audit data.

## Status and limits

The packages follow the directory-based Agent Skills format. Installation locations are checked against official documentation; see [Compatibility](docs/COMPATIBILITY.md). Automated checks exercise the installer, metadata ledger, configuration change bundle, and audit artifact validator without calling models; see [Validation](docs/VALIDATION.md) for recorded results and pending checks. The Audit Project release also passed the four-job Windows/macOS/Linux CI matrix; see the linked validation evidence. Live target CLI checks remain pending. Representative instruction scenarios do not certify runtime enforcement, production readiness of a target project, or model behavior across all domains.

History access, permissions, native capabilities, and telemetry depend on the installed host/version. Missing evidence stays explicit. Measured savings require comparable real usage data; the skill does not guarantee a fixed saving or unlimited autonomous permissions.

## Privacy and maintenance

Keep session exports, review databases, user profiles, approval records, and configuration backups in private storage **outside this repository and outside shared project instructions**. Enhance's ledger stores supplied metadata. Characterize's optional helper stages and applies reviewed local file changes with drift checks and recovery records. Neither helper redacts secrets or validates native runtime semantics. See [Privacy and safety](docs/PRIVACY.md).

Audit Project deliberately writes reviewed findings and plans to the target repository. Its published artifacts must exclude credentials, private transcripts, exploit details unsuitable for public disclosure, and unrelated personal data. Keep sensitive evidence in an authorized private location and commit only safe references or summaries.

For development and regression checks:

```sh
python tools/check_release.py
python -B -m unittest discover -s skills/characterize/scripts -p 'test_*.py' -v
python -B -m unittest discover -s skills/enhance/scripts -p 'test_*.py' -v
python -B -m unittest discover -s skills/audit-project/scripts -p 'test_*.py' -v
python -B -m unittest discover -s tests -p 'test_*.py' -v
```

See [Validation](docs/VALIDATION.md) for reproducible behavior scenarios and [Contributing](CONTRIBUTING.md) for change requirements.

## License

[MIT](LICENSE), Copyright (c) 2026 seismael.
