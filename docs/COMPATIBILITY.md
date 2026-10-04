# Compatibility and evidence

Documentation checked: **2026-10-04**. This table applies to both Characterize and Enhance. These are documented installation targets, not a claim that every current or future version has passed a live integration test. In invocation examples, replace `<skill>` with `characterize` or `enhance`.

| Surface | Package/discovery evidence | Live runtime verification for this release |
|---|---|---|
| OpenCode | Official directory skills; use portable `name`/`description` frontmatter and a matching directory. | Not run in OpenCode. |
| Claude Code CLI | Official directory skills with supporting files and `/<skill>` invocation. | Not run in Claude Code. |
| Codex CLI | Official directory skills, `.agents/skills` discovery, `$<skill>` or `/skills`. | Not run in Codex CLI. |
| Gemini CLI | Official directory skills in `.gemini/skills` and `.agents/skills` aliases; `/skills list` exposes available skills. | Not run in Gemini CLI. |
| Antigravity CLI (`agy`) | Canonical official skills guide explicitly documents directory bundles, its CLI-specific global root, and slash-command registration. | Not run in agy. |
| Antigravity IDE | Same canonical format; different global root from the CLI. | Not run in the IDE. |
| Other Agent Skills hosts | Common-format candidate; verify host metadata, discovery, tools, and permissions. | Unverified. |

The development environment did not provide these local CLI executables. Automated tests passed locally as recorded in [Validation](VALIDATION.md); the updated remote CI matrix has not been observed. Helper tests and instruction scenarios do not substitute for testing a host's discovery, effective configuration, permissions, or model behavior.

## Portable contract

- Each `skills/<skill>/SKILL.md` contains standard `name` and `description` frontmatter matching its directory. Descriptions stay within the common 1,024-character limit.
- Relative references and Python scripts remain inside the skill directory. There are no fixed developer-machine paths, account-specific settings, API keys, or required external services.
- Optional `agents/openai.yaml` provides OpenAI UI metadata only. Other hosts do not need it; it is not a replacement for their native agent configuration.
- The instruction workflow uses the host's existing model and tools. Python 3.10+ and its standard library are needed only for the installer and optional helpers.
- Enhance discovers native histories at execution time. Its ledger consumes normalized metadata supplied by the agent; it is not a universal parser for all proprietary session formats.
- Characterize discovers target capabilities at execution time. Its file-change helper checks drift and supports recovery; it does not generate or validate a universal configuration schema.
- Instructions can guide behavior but cannot create unsupported runtime capabilities or bypass the host's permissions.

OpenCode V2 relaxes some metadata constraints compared with the unversioned documentation. This package retains the common strict format. Antigravity has older documentation for flat skill files; this release follows its canonical surface-specific directory guide. Check the actual installed version if documentation and discovery differ.

## Verification levels

1. **Format checked:** metadata, directory structure, and bundled references pass the release checker.
2. **Helper tested:** deterministic tests cover ledger correctness, staged file changes/recovery, and installation behavior.
3. **Scenario reviewed:** selected prompts exercise scope, decisions, cost reasoning, and authorization in a host agent.
4. **Runtime observed:** the exact target version discovers the skill and completes representative tasks. Record product/version, OS, date, evidence, and limits before marking this level.
5. **Outcome measured:** comparable real usage establishes cost/performance and quality effects. No savings percentage is asserted by this release.

## Official sources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [OpenCode V2 skills](https://opencode.ai/v2/docs/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex and ChatGPT skill authoring](https://learn.chatgpt.com/docs/build-skills)
- [Gemini CLI skills and discovery precedence](https://geminicli.com/docs/cli/skills/)
- [Antigravity skills by surface](https://antigravity.google/docs/skills/)

For a runtime test, follow [Validation](VALIDATION.md) using non-sensitive fixtures and existing connected models. Do not install or invoke additional paid services simply to claim compatibility.
