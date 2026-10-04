# Evidence and scope

## Compact finding

Use a stable finding ID and retain: source/session/revision/event references; project/task/mode; user expectation; observed behavior/outcome; explicit instruction or inference; support and counterevidence; diagnosed cause; intended scope; candidate native surface; disposition. Keep a short paraphrase, not a transcript. Link related findings to avoid counting the same incident twice.

Strength is a judgment, not a fabricated statistical probability:

- **Direct:** an explicit durable user instruction. Apply at its stated scope when compatible with current authorization.
- **Supported:** independent recurring corrections across comparable contexts, with no stronger counterevidence. Apply a narrow reversible improvement and observe its effect.
- **Tentative:** one ambiguous event, inferred silence, assistant self-report, or uncertain cause. Retain briefly as a hypothesis; do not create permanent policy.

Repeated failed attempts within one session are one cluster of evidence, not many independent preferences. Repeated copies/forks/imports of a conversation are also one source of support. Record changed or superseded preferences and stop treating their old evidence as active. Recent evidence wins only where scope, conditions, and meaning actually conflict; a recent one-off task does not erase a durable general preference.

## Purpose and ownership of scopes

| Scope or selector | Purpose |
|---|---|
| Private cross-tool preference profile | Describe portable user expectations; this is evidence for adaptation, not a universal configuration file or enforcement layer. |
| Tool/account/profile global defaults | Establish behavior appropriate for unrelated work in that target; preserve native defaults that already satisfy the need. |
| Shared workspace/project | Express requirements and conventions belonging to that work or team, independent of an individual machine. |
| Private project override | Express this user's or machine's project-specific needs when the target supports it; keep it out of shared project configuration. |
| Directory/component | Apply requirements only to the relevant subset of a project where supported. |
| Agent/mode/skill | Specialize a responsibility or workflow; this selector may intersect global and project scope rather than being above or below either. |
| Session/current task | Carry temporary constraints; do not persist them without evidence of a durable requirement. |
| Managed/vendor/generated configuration | Respect its owning policy or source; use authorized customization points rather than editing protected or regenerated content. |

Prefer the narrowest scope that faithfully expresses the purpose, not simply the smallest file. Before promoting a rule, ask whether it would be correct in an unrelated project, another domain, another user's workspace, and another target tool. A preference can be global for one tool while having no supported equivalent in another. Before adding a local override, check whether it needlessly duplicates a correct inherited default. Before removing one, check the reason for the exception.

Treat a client brand voice, research methodology, document template, dataset convention, deployment workflow, and repository test command as project/workflow requirements when the evidence limits them to that context. Their repeated appearance in one project is not proof that they should govern every task. Track outcomes using the domain's actual deliverables rather than assuming compilation/tests are universal validation.

## Routing table

| Evidence | Scope and action |
|---|---|
| “In every project, stop narrating each command.” | Global communication rule in each authorized target's active native surface. |
| “For this repository, run these two checks after changing the parser.” | Project instructions; preserve exact relevant conditions. |
| “Give this audit every detail.” | Current task/output requirement unless the user explicitly makes it durable. |
| “After I approve implementation, finish tests and fixes without asking again.” | Global or workflow autonomy rule as stated; maintain real permission boundaries. |
| “This monorepo needs a migration specialist.” | Project agent/skill when a recurring responsibility justifies it; do not install it globally by default. |
| Several unrelated workflows repeat the same reusable export procedure. | A selectively loaded skill may fit better than global prompt text. |
| A repeated tool error causes long retries. | Diagnose tool configuration, error handling, or native capability before changing writing style. |
| The current instruction already expresses the expectation. | Diagnose precedence, loading, applicability, routing, or adherence; avoid another duplicate rule. |

Promote inferred preferences globally only after independent evidence from more than one relevant context supports portability. Evidence observed in one project does not by itself establish that the requirement belongs to the project. With uncertain portability, retain a private tentative finding or supported bounded personal override; do not automatically write it into shared project policy. An explicit global instruction can establish global applicability even when only one project is visible. Changing a global permission affects future unrelated work, so evidence of annoyance alone does not authorize broad capability expansion.

## Conflict handling

Prefer a conditional rule when both expectations are valid: “Use brief progress updates; deliver detailed audits when requested.” Preserve project exceptions to global preferences only where native precedence allows them. Never use this skill to override managed policy. If two durable same-scope expectations conflict and context cannot resolve them, prepare the narrow options and ask one meaningful question; continue independent improvements.

When source evidence is edited, removed, or withdrawn, flag dependent findings for reassessment. Do not silently remove a user-approved improvement solely because retention deleted an old transcript. Preserve the minimal decision provenance and distinguish withdrawn preference from unavailable evidence.

Keep cross-tool profiles descriptive and private. Distribute only the minimum applicable instruction into each target, translated into supported native mechanisms. Avoid maintaining several independent copies of the same always-loaded rule within one tool.
