# Gemini CLI adapter

Documentation checked 2026-10-04; runtime behavior not tested here. Gemini CLI is distinct from the Gemini web app. Features and settings nesting depend on the installed release.

## Discover

Inspect version/help, user `~/.gemini/settings.json`, project `.gemini/settings.json`, configured system layers, `GEMINI.md` hierarchy, custom commands, skills, agents, extensions, MCPs, and policy rules. Check environment override presence without exposing values. Follow the installed schema's nesting and precedence rather than copying old flat settings. [Configuration](https://geminicli.com/docs/reference/configuration/)

Check the account route, selectable models, supported generation options, and CLI entitlement. A model connected in OpenCode or another host is not necessarily available in Gemini CLI.

## Compile

| Intent | Native surface to verify |
| --- | --- |
| Persistent context | Appropriate scoped `GEMINI.md` |
| Named workflow shortcut | `.gemini/commands/` TOML definitions or active user commands directory |
| On-demand expertise | `.gemini/skills/<name>/SKILL.md` or current supported user skill path |
| Isolated specialist | Supported `.gemini/agents/` definitions and native model/tool controls |
| Permissions | Native policy engine, approval behavior, and sandbox settings |
| Tools/integrations | Existing MCPs/extensions; add only when needed |

Custom commands define reusable prompts and may expose execution/interpolation features. Use only necessary features; do not introduce shell expansion into user-supplied text casually. A command is not automatically an independently enforced mode. [Custom commands](https://geminicli.com/docs/cli/custom-commands/)

Current docs describe subagents as enabled by default. Verify support locally before changing enablement; do not add an experimental flag speculatively. Agent definitions can use project or user `.gemini/agents/` paths. Omitted tool lists inherit parent tools, and current docs prohibit subagent-to-subagent calls. Verify effective permissions and delegation capabilities instead of inferring them from an agent's name. [Subagents](https://geminicli.com/docs/core/subagents/)

Use the policy engine for supported allow/ask/deny behavior, checking precedence, tool names, and rule locations. A prompt asking a specialist to stay read-only cannot replace enforceable policy. Avoid broad approval bypasses as an efficiency default. [Policy engine](https://geminicli.com/docs/reference/policy-engine/)

The checked policy docs mark workspace `.gemini/policies` as disabled/non-functional and point to user/admin policy locations. They also contain conflicting tier numbers and policy examples across pages. Resolve the actual rule syntax, supported scope, and precedence from the installed schema/parser before writing policies; do not silently substitute a broader scope. Report unresolved conflicts and leave enforcement unverified until an effective-policy check succeeds.

## Apply and verify

Choose domain-appropriate command/skill names. Native subagents may implement selected specialists; do not claim they create an OpenCode-equivalent main-mode selector. Verify supported model binding and switching for each chosen mechanism.

Validate JSON/TOML/frontmatter, loaded configuration and policy rules, skills/agents/commands discovery, model identity, and harmless permission probes. Check whether changed fields require a new session or reload. Mark unavailable runtime checks pending.

For portability, place the complete skill folder in a currently supported path and confirm its identity/source with native `/skills list`. Current docs give workspace skills precedence over user skills and `.agents/skills` precedence over `.gemini/skills` within each scope. Inspect existing shared installs before copying. Keep detailed references on demand. [Agent skills](https://geminicli.com/docs/cli/skills/)
