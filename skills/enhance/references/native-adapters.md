# Native discovery and portability

Use one common review method and a separate discovered adapter for each target. This skill is a workflow, not a universal history connector or a guaranteed runtime controller.

## Adapter record

Record only nonsecret metadata:

- Product, executable/UI, observed version, OS, profile/account identity, observation date.
- History listing/read/export mechanisms, pagination, retention limits, session/event IDs, revision reliability, parent/fork provenance, accessible sources, and content gaps.
- Global, project, directory, mode, and session configuration locations; active versus merely existing files; precedence and merge/replace behavior; managed or generated surfaces.
- Supported instructions, skills, agent roles, delegation, models/effort, compaction, permissions, tools, plugins/hooks, validators, reload behavior, and usage telemetry.
- Evidence supporting each proposed key or mechanism; classify native enforcement separately from instruction conventions.

Use metadata and installed help/schema before broad file reads. Consult current official documentation to resolve uncertain version-sensitive behavior. Cache this record; recheck affected capabilities when a version/configuration/source changes. Do not query every manual on every run.

## Configuration semantics, not filenames

For each affected setting or instruction, build a compact record:

`purpose | owner | storage surface/type | applicability/activation | persistence | declared value | effective value | inherited source | merge/override rule | constraints | affected contexts | verification`

Derive these fields from observed native behavior, schema/help, user intent, and applicable policy. Distinguish a missing value (inherit a default) from an explicitly empty or disabled value. Do not invent override semantics: lists may replace or append, permission rules may use specificity or ordered evaluation, and organization policy may constrain all lower scopes. An instruction is a behavioral request, not a typed runtime switch. A globally stored skill can activate only in one project; storage location does not establish applicability. Prefer removing a redundant override when inheritance restores the desired native behavior. Record why deliberate overrides remain and recheck them after relevant upgrades so old enhancements do not unnecessarily freeze obsolete defaults.

Resolve representative execution contexts, including profile/account, workspace/directory, agent/mode, environment, command-line arguments, and session overrides where supported. Record the winning source and resolution chain for each affected context, then verify the intended winning source after changes. Map the tool's actual precedence and selectors; do not impose a universal global → project → agent ladder. Explain which contexts a change affects and which inheritance relationship produces that result. A desired project outcome does not justify changing a global-only setting without evaluating the consequences for other work. When a required scope is unsupported, retain a scoped instruction if sufficient, propose a native alternative, or mark the capability unsupported.

| Surface family | What to discover before changing it |
|---|---|
| Structured settings, including UI/API-backed settings | Supported fields/types, defaults, active profile, merge rules, validators, and reload needs. |
| Instructions and memory | Actual loading, hierarchy, conditional applicability, retention, and behavioral limits. |
| Skills, commands, templates, and workflows | Selection triggers, scope, ownership, input/output contract, and context-loading cost. |
| Agents, modes, and delegation | Native role semantics, routing, capabilities, model inheritance, and handoff behavior. |
| Tools, MCPs, plugins, and hooks | Availability, relevance, trust/ownership, activation, conditional effects, permissions, and runtime overhead. |
| Models, context, retries, concurrency, and execution | Connected capabilities, units and limits, billing implications, defaults, and task-specific tradeoffs. |
| Output, interface, localization, telemetry, and privacy | User intent, supported scope, operational effect, and applicable policy. |

Classify relevant surfaces as `change`, `keep`, `not-applicable`, or `unresolved`, with a brief reason. Cover configuration broadly without changing everything or reauditing unrelated settings every run. Leave credentials, account identity, billing routes, managed controls, and unrelated product/application code outside scope unless separately authorized. When a configuration is generated, edit its authorized source through the owning mechanism rather than an output that will be overwritten.

## Target-specific discovery questions

| Target | Questions to resolve locally |
|---|---|
| OpenCode | Which native session listing/export/storage interfaces does this version expose? Which global/project settings and instructions actually load? How do primary agents, subagents, commands, skills, permissions, model options, and tool restrictions interact? |
| Claude Code | Which sessions belong to the selected profile/project? Which user/project/local instructions and managed settings load, and in what order? Which native subagent, skill, permission, and hook mechanisms are available? |
| Gemini CLI | Which saved sessions and resume/export interfaces exist? Which settings and instruction files load at user, workspace, or directory scope? Which extension, skill, delegation, and approval features are actually supported? |
| Antigravity CLI (`agy`) or IDE | Which surface and version is being enhanced? Which skill roots, session access, native settings, and invocation mechanisms apply to that surface? Keep CLI and IDE profiles distinct. |
| Codex or ChatGPT | Is this a local CLI, IDE, or hosted surface? What history and persistence are actually exposed? Which instructions, skills, agent controls, or user settings are editable here? A remote host does not imply desktop access. |
| Other tools | Discover equivalent native interfaces; use instruction-only improvements if appropriate, and explicitly leave unsupported controls pending. |

Names such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and tool settings files are examples to verify, not a universal path or precedence contract. Do not create every example file. Do not install an extension just to simulate an unsupported native feature without authorization.

## History acquisition

Prefer supported list/read/export APIs or CLI commands. For an existing local database, use a supported read-only query/export or consistent snapshot; never mutate its live schema or infer that copying a live database file captures pending WAL content. For JSONL/file histories, parse records locally and preserve role/event boundaries. Do not truncate arbitrary bytes and claim the session is complete.

When a tool has no reliable revision marker, derive a fingerprint from stable normalized relevant event content, or use metadata as a hint and recheck ambiguous sessions. A timestamp is not a content identity. Include stable project identity in the ledger revision fingerprint so a project reclassification triggers a new scope review. Detect missing fields, truncated records, edits, imports, and forks. Do not send raw histories to an unrelated service.

Choose stable private identifiers. A working-directory path alone is insufficient when projects move; a remote URL alone is insufficient when repositories/forks or accounts differ. Preserve explicit project identity mappings, distinguish unrelated copies, and associate worktrees only when verified. Store no credential-bearing URLs.

## Collaboration with other skills

Use Enhance for evidence-led improvement of an existing setup. If the user instead needs a new domain/workflow designed through interviews, use an available characterization skill for unresolved design decisions and reuse its existing profile. Do not force that interview onto a straightforward enhancement run. Use available native skill-editing workflows when changing personal skills; do not fork or overwrite vendor-provided skills automatically.
