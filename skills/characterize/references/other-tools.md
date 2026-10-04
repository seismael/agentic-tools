# Other targets and portability

## Capability-driven adapter

For Codex, an editor agent, another CLI, a local application, or an unfamiliar tool, first identify the exact product/interface and installed version. Do not infer configuration support from a shared model provider or a similar product name.

Build an adapter record from local help, installed schemas, product-owned source, and current official documentation. Confirm the actual effective value; a value in a file can be overridden or ignored. Where documentation conflicts with installed behavior, keep the feature unverified until the installed schema/parser or harmless native probe resolves it:

1. Supported config/instruction/skill/profile locations, discovery, precedence, and management ownership.
2. Actual mechanisms for persistent context, invoked workflows, primary profiles, subagents, models/options, tools/MCPs, permissions/sandbox/trust, hooks/extensions, context/compaction, and usage export. Include UI/language/accessibility, telemetry, updates, and sharing where exposed and relevant.
3. Exact setting key/type/location and evidence for each proposed feature.
4. Native validation, reload/discovery procedures, and representative permission probes.
5. Unsupported requirements, documented alternatives, and remaining unknowns.

Do not emit plausible-looking keys. Translate intent into supported mechanisms or clearly label the limitation. If a tool only supports project instructions, deliver that supported subset and state which model/tool/permission controls remain unavailable. Changes to program source or new plugins are a separate proposed implementation when required, not an invisible configuration step.

## Scope and ownership

| Layer or selector | Intended meaning |
|---|---|
| Private cross-tool profile | User goals and preferences, translated per target; not a universal runtime config |
| Tool/user defaults | Durable behavior suitable across unrelated work in that target |
| Shared project/workspace | Team or work-product requirements, independent of personal machine preferences |
| Private project override | Individual or machine-specific needs, only where the target supports this layer |
| Directory/component | Requirements limited to part of the project |
| Role, mode, skill | Responsibility-specific behavior; intersects rather than replaces project/global scope |
| Session/task | Temporary constraints; keep temporary unless the user makes them durable |
| Managed/generated | Policy or source owned elsewhere; customize only through supported authorized surfaces |

Use the narrowest layer that expresses the meaning faithfully. A global brevity preference can coexist with a detailed project audit requirement. A client's voice, project build command, or dataset convention must not become universal policy. Installing a skill globally changes discovery, not the scope of all its actions. Shared `.agents` directories may be discovered by multiple hosts; inspect that effect before installing duplicates or editing shared instructions.

Preserve native inheritance where correct. Diagnose ineffective existing rules before adding duplicates. Resolve conflicts using actual precedence and ownership; ask only if two consequential same-scope preferences remain incompatible. Do not infer permission to edit shared policy from a private preference.

## Additional native discovery maps

Official documentation checked 2026-10-04; these pointers do not certify the user's installed version.

- **Codex CLI/IDE:** Inspect native config, trusted project layers, selected profiles, instructions, and custom agents separately. Current docs describe `~/.codex/config.toml`, project `.codex/config.toml`, profile files, and `.codex/agents/` TOML definitions. Managed requirements differ from editable defaults; inherited runtime permission overrides can constrain spawned agents. ChatGPT Work's hosted surfaces are separate from local CLI settings. Start with [config](https://learn.chatgpt.com/docs/config-file/config-basic), [instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), and [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents); emit exact fields only after installed-version confirmation.
- **Antigravity:** Identify CLI (`agy`), IDE, or 2.0 before adapting. They differ in settings, global skill roots, rules, and agent support. Current CLI settings use `~/.gemini/antigravity-cli/settings.json`; do not transplant Gemini CLI settings because both use `.gemini`. Check [CLI settings](https://antigravity.google/docs/cli/using/), [skills](https://antigravity.google/docs/skills/), [rules](https://antigravity.google/docs/rules/), and [agents](https://antigravity.google/docs/subagents/). Treat rule text as guidance and verify [permissions](https://antigravity.google/docs/permissions/) independently.
- **Other CLIs, editors, hosted apps, and API agents:** Apply the same discovery record to supported files, UI, API settings, or application-owned schemas. Without configuration access, deliver only the supported proposal or instruction subset. Never infer local filesystem control from a conversational interface.

## Installation on another host

This skill uses portable Markdown frontmatter (`name`, `description`) and relative references. It requires an LLM-capable host that can read skills and, for application, access the target filesystem and permitted editing tools. The bundled helper uses only Python 3.10+'s standard library; it is optional when native editing can satisfy the change protocol.

Determine the target's currently supported skill directory before copying. Preserve `SKILL.md`, `references/`, and `scripts/` together under a folder named `characterize`, subject to the host's naming rules. `agents/openai.yaml` is optional host UI metadata; it is not configuration for the target being characterized. Use only documented per-host metadata when creating an adapter copy.

If a host has no native skill discovery, a user can explicitly ask it to read `characterize/SKILL.md` and follow the references, but this is manual instruction loading. Do not call that native installation. If it cannot edit local files, produce a staged proposal and the exact local continuation steps.

Do not silently install this skill into every detected agent. Characterizing one target does not authorize altering all agents on the machine. For an explicitly requested multi-target setup, map one shared user profile into separate native implementations and validate independently.

## Scope limits

Support is extensible through discovery, not a claim that every application exposes every control. Paid entitlements, provider availability, closed-source runtime internals, managed restrictions, and inaccessible machines cannot be fixed by instruction text. Complete the supported work and report precise gaps instead of building an unauthorized proxy or changing credentials.
