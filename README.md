# Agentic Tools

Portable skills for making AI agents more effective, reliable, and economical through their native capabilities.

## Skills

| Skill | Purpose |
|---|---|
| [Characterize](skills/characterize/SKILL.md) | Translate goals, domains, workflows, and constraints into a minimal native setup; interview only where evidence leaves consequential choices unresolved. |
| [Enhance](skills/enhance/SKILL.md) | Learn from actual sessions, diagnose wasted effort, and improve native settings and workflows at the correct global, project, agent, or task scope. |

Use Characterize to establish or revise a setup from current needs. Use Enhance to improve it from actual session evidence. Each works independently; when useful, carry forward a compact private profile and approved scope.

Both prioritize performance and cost effectiveness: useful completed work per input/output consumption, total cost, and elapsed time, while preserving required correctness and reliability. They support research, writing, analysis, design, operations, and engineering.

## Install a skill

Clone this repository or download its source. Copy the **whole** `skills/characterize/` or `skills/enhance/` directory into one supported skill location. Do not copy only `SKILL.md`, and do not install duplicate copies into locations the same agent scans.

With Python 3.10 or newer, the optional installer works on Windows, macOS, and Linux and refuses to overwrite an existing destination:

```sh
git clone https://github.com/seismael/agentic-tools.git
cd agentic-tools
python tools/install_skill.py --skill characterize --to ~/.agents/skills/characterize --check
python tools/install_skill.py --skill characterize --to ~/.agents/skills/characterize
```

The shared installer accepts either skill: replace `characterize` with `enhance` in both arguments to install Enhance. The example uses Codex's documented user skill directory. See [Installation](docs/INSTALLATION.md) for OpenCode, Claude Code, Gemini CLI, Antigravity CLI (`agy`), and Antigravity IDE. Python is optional for the instruction workflow; the installer and bundled helpers require it.

## Use it

Select the skill using your host's native control. In Codex CLI, use `$characterize` or `$enhance`; in Claude Code and Antigravity CLI, use `/characterize` or `/enhance`. In OpenCode or Gemini CLI, explicitly request the named skill in your prompt and verify discovery through the native skill interface.

Example requests:

> Use Characterize to tailor my agent's native setup to my work. Inspect the current setup, reuse what I have already told you, ask about consequential choices, and prepare minimal changes with clear scope and recovery.

> Use Enhance to review my accessible agent sessions. Prioritize input/output cost and performance, preserve necessary validation, and propose native improvements with global and project changes separated. Ask about meaningful choices before applying configuration changes.

> Continue Enhance from its saved review state. Review new and changed sessions, evaluate the previous improvements, and apply only the already-approved changes.

> Use Enhance for this project only. Investigate repeated research and reviewer work, propose clear role ownership and compact handoffs, and preserve our deliverable requirements.

The host agent performs the work with its existing model and authorized tools. These skills are not separate agent runtimes, universal history connectors, background services, or model subscriptions.

## What happens

1. Discover the actual target tool/version, relevant evidence, native settings, configuration precedence, and prior checkpoints.
2. Characterize resolves goals, representative tasks, and consequential setup choices. Enhance reviews sessions individually and incrementally, including reopened sessions and late imports.
3. Diagnose supported improvements across consumption/performance, reliability, consistency, structured inputs/outputs, autonomy, orchestration, context/tools, research/review, automation/workflows, and domain/project needs.
4. Propose concrete changes and tradeoffs. Resolve consequential choices with suggested options and a custom answer. Respect existing authorization; obtain scoped approval when needed.
5. Apply through supported native surfaces, verify proportionately, and save private coverage, decision, and recovery records.

A globally installed skill can still propose a project-only change. Shared team requirements, private project preferences, native global defaults, role-specific behavior, and temporary task constraints remain distinct. Storage location alone does not determine applicability.

## Status and limits

The packages follow the directory-based Agent Skills format. Installation locations are checked against official documentation; see [Compatibility](docs/COMPATIBILITY.md). Local automated checks exercise the installer, metadata ledger, and configuration change bundle without calling models; see [Validation](docs/VALIDATION.md) for results. Live target CLI checks and the updated remote CI matrix remain pending. Representative instruction scenarios do not certify runtime enforcement or model behavior.

History access, permissions, native capabilities, and telemetry depend on the installed host/version. Missing evidence stays explicit. Measured savings require comparable real usage data; the skill does not guarantee a fixed saving or unlimited autonomous permissions.

## Privacy and maintenance

Keep session exports, review databases, user profiles, approval records, and configuration backups in private storage **outside this repository and outside shared project instructions**. Enhance's ledger stores supplied metadata. Characterize's optional helper stages and applies reviewed local file changes with drift checks and recovery records. Neither helper redacts secrets or validates native runtime semantics. See [Privacy and safety](docs/PRIVACY.md).

For development and regression checks:

```sh
python tools/check_release.py
python -B -m unittest discover -s skills/characterize/scripts -p 'test_*.py' -v
python -B -m unittest discover -s skills/enhance/scripts -p 'test_*.py' -v
python -B -m unittest discover -s tests -p 'test_*.py' -v
```

See [Validation](docs/VALIDATION.md) for reproducible behavior scenarios and [Contributing](CONTRIBUTING.md) for change requirements.

## License

[MIT](LICENSE), Copyright (c) 2026 seismael.
