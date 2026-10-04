# Claude Code adapter

Documentation checked 2026-10-04; runtime behavior not tested here. Verify installed version and interface; Claude's web app is not Claude Code's local filesystem.

## Discover

Inspect version/help, `~/.claude/settings.json`, project `.claude/settings.json`, applicable `.claude/settings.local.json`, instruction files, agents, skills, MCPs, hooks, and managed policy. Resolve actual paths: local settings placement can depend on version, repository/worktree, platform, and ownership. Strict JSON settings cannot accept JSONC comments. Preserve unrelated keys and verify per-key precedence and list merging. A manually created local settings file may need an explicit ignore entry, included in the proposal. [Settings and precedence](https://code.claude.com/docs/en/settings)

Check the target's supported model selection and account route. Do not assume arbitrary OpenAI/Gemini model IDs work in this runtime or that a connected model in another app is available here. Only emit verified model aliases/IDs and effort settings. [Model configuration](https://code.claude.com/docs/en/model-config)

## Compile

| Intent | Native surface to verify |
| --- | --- |
| Durable conventions | Scoped `CLAUDE.md` instructions, with appropriate hierarchy |
| Reusable domain workflow | `.claude/skills/<name>/SKILL.md` or active user skill directory |
| Named specialist | `.claude/agents/<name>.md` or user agent definition |
| Main-session specialist | Verified `--agent <name>` launch option or `agent` setting |
| Specialist behavior | Supported frontmatter for tools, model, permissions, skills, and effort |
| Action boundaries | Native settings permission rules and available sandbox controls |
| Deterministic event action | A documented hook only when needed and reviewed |

Subagents are a native delegation mechanism with version-dependent configuration fields. Current docs say parent `bypassPermissions`, `acceptEdits`, or `auto` can override a subagent's `permissionMode`; plugin agents ignore `permissionMode`, `hooks`, and `mcpServers`. Verify effective tool access and inherited permissions before promising restrictions. [Subagents](https://code.claude.com/docs/en/sub-agents)

Use skills/commands for an invoked workflow and subagents for actual isolated specialist work. Check current skill frontmatter and discovery rules. Keep heavyweight references on demand rather than preloading every domain guide. [Skills](https://code.claude.com/docs/en/skills)

## Apply and verify

Current docs support main-session selection through `claude --agent <name>` or the `agent` setting. Verify the installed behavior and active agent; this does not establish in-session mode switching. Model changes and permission changes require real native mechanisms.

Map approve-once local work onto supported settings within user scope. Do not default to `bypassPermissions` or broad shell allowances merely to reduce interruptions. Read-only analysis must account for shell, delegation, MCPs, hooks, and parent policy. Record unavoidable native confirmation behavior. [Permissions](https://code.claude.com/docs/en/permissions)

Validate strict JSON/frontmatter, actual loaded settings sources, agent/skill discovery, selected model, and non-destructive policy tests. Use current native status/diagnostics and respect reload semantics; do not claim every setting hot-reloads. Do not overwrite credentials, managed rules, or the user's entire instruction file.

To carry this skill into Claude Code, use a supported native skill directory and preserve the complete folder. Keep the common `name`/`description` frontmatter portable; any Claude-specific flags belong in a verified adapter copy.
