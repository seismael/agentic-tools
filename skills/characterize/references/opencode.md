# OpenCode adapter

Documentation checked 2026-10-04; runtime behavior not tested here. Recheck against the installed release; these pointers are not a frozen schema.

## Discover

Inspect local version/help, active launch options, project `opencode.json`/`opencode.jsonc`, `.opencode/`, and the user config directory; current TUI settings use separate `tui.json` files. Resolve XDG/custom paths and relevant environment overrides without printing their contents. Config layers merge: determine effective precedence across remote defaults, user/project/custom sources, runtime overrides, and managed controls. Preserve JSONC comments and permission ordering. [Configuration](https://opencode.ai/docs/config/)

Inspect existing agents, prompts, commands, skill paths, providers, plugins, and MCP definitions. Discover exact connected model IDs and supported variants through available native listing/help. Do not assume the host's subscription or model exists here. [Models](https://opencode.ai/docs/models/)

## Compile

| Intent | Native surface to verify |
| --- | --- |
| User-facing modes | `agent` definitions with `mode: primary`, or Markdown in `.opencode/agents/` / the active user `agents/` directory |
| Delegated specialist | Agent with `mode: subagent`; do not confuse it with the main user-facing mode |
| Model selection | Agent `model` using discovered `provider/model-id`; supported options/variants only |
| Task instructions | Agent prompt or referenced prompt file; short shared `AGENTS.md` conventions |
| Workflow shortcuts | Native command definitions, with verified agent/model binding |
| Tool boundaries | Agent/global `permission`, including shell, task delegation, custom/MCP tools |
| Reusable domain knowledge | Discovered native skill directories; load references when needed |

Primary agents support a main interactive profile with its own prompt, model, and permissions. Verify mode discovery and selection in the installed interface. Do not use an obsolete generic `mode` configuration block instead of current agent definitions. Built-in Plan currently asks for edits and shell commands; its name alone does not guarantee blocked writes. [Agents](https://opencode.ai/docs/agents/)

Use `permission` for current configurations rather than deprecated boolean `tools`, even where older examples still show it. Current permission patterns use the last matching rule; confirm installed behavior and preserve ordering. Restrict indirect writes through shell, task agents, MCPs, and hooks when promising read-only work. Do not replace existing deny rules with broad allows. [Permissions](https://opencode.ai/docs/permissions/)

## Apply and verify

Generate only selected modes. Names such as Diagnose/Architect/Plan/Build/Validate/Quick are candidate engineering choices, not universal requirements. Use separate domain stages for creators or analysts. Resolve name collisions without overwriting user-owned definitions.

Use native commands when they can express a workflow. A phrase such as “next” does not itself guarantee agent/model switching: confirm an available transition mechanism, or describe the necessary UI action and label the handoff convention accurately. Avoid plugins unless a required capability justifies them.

Validate syntax/schema for the installed version, effective merged values, agent/command discovery, exact selected model, and harmless permission probes. If local diagnostics are unavailable, mark runtime checks pending. Do not blindly execute a diagnostic that starts plugins or sends model requests.

Skill portability: verify discovery using [Agent skills](https://opencode.ai/docs/skills/). Current discovery includes `.opencode`, `.claude`, and `.agents` skill locations; inspect shared installs and name collisions before copying. Keep the full `characterize` folder together; do not paste its entire content into `AGENTS.md`. Check [Commands](https://opencode.ai/docs/commands/) only when emitting commands.
