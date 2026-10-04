# Behavior, delegation, and efficiency

Choose only patterns supported by observed needs. These are candidate designs, not a template to append wholesale.

## Communication and autonomy

Make communication informative and actionable with minimal repetition. For a meaningful update, state the result/change, supporting evidence when needed, and the next action or decision. For a blocker, state the concrete missing condition and the smallest action that resolves it. Keep plans focused on outcomes, dependencies, acceptance criteria, and genuine gates rather than a narration of every tool call. Compress repetition, not substance. Prefer outcome-first answers with material changes, relevant verification, and a real blocker or next decision. Avoid repeating a plan in every update, narrating routine tool calls, printing enormous tool responses, and asking whether to do the work already requested. Preserve useful progress visibility on long tasks and the detail explicitly requested for designs, audits, education, or research.

Within authorized capabilities, carry a task through implementation, relevant checks, and repairs. Infer routine implementation choices from local evidence. Ask for input when an unresolved choice materially changes the result and cannot responsibly be inferred; ask for permission only when actual authority requires it. Do not convert “fewer questions” into “guess every important decision.”

Where the user has staged workflows, keep their transitions: analytical work can investigate and refine without silently starting implementation; approved implementation includes its validation and repairs. Native modes, tool policy, and prompt conventions have different enforcement strength. Do not claim a prompt enforces a read-only boundary while an available shell or delegated helper can still write.

## Agents that earn their overhead

Evaluate the expected net input/output, cost, and latency effect before adding coordination. Prefer native roles and existing skills. A useful new role has a repeated responsibility, a concrete output, and a routing trigger. Do not add a permanent agent for every task or turn a generic quality request into a multi-agent organization.

For each delegated task, use a compact contract:

`goal | required evidence/files | owned scope | allowed effects | constraints | done criteria | return format`

Return `result | supporting evidence | changed files (if any) | validation | blocker`, with paths or references instead of duplicated full artifacts. Send enough task context for accuracy, not the whole conversation by default. The integrator owns shared edits and resolves contradictions. Independent work may run in parallel; dependent work must wait for its inputs. Prevent circular parent/child calls, overlapping writes, recursive self-enhancement, and repeated delegation of an already completed investigation. Retry or escalate only to resolve a concrete gap.

Do not let a helper expand the parent's authority. Verify effective capabilities through native controls where available. If the target cannot call agents or enforce routing, label the design instruction-only or unsupported; do not fabricate runtime features.

## Cost and quality

Use available telemetry; distinguish measured, estimated, and unavailable values. Track comparable task type/model/tool version/context and include:

- Input, output, reasoning, cached/uncached tokens when exposed; child-agent usage and retries. Avoid double-counting child usage already aggregated by the host.
- Paid cost or quota consumption only when the tool exposes them or a verified pricing/account model supports calculation; token count alone does not determine subscription quota use.
- End-to-end latency, task completion, regressions, manual corrections, unnecessary questions, and repeated work.
- Standing instruction size and loaded skill/context size. Character counts are a proxy, not exact tokens.

Prefer targeted retrieval, local filtering, resumable review, native compaction, and compact evidence. Avoid large new always-loaded instruction blocks: estimate persistent context cost against the actual recurring issue fixed. Use the least expensive verified model/effort that meets the task's acceptance criteria; do not hardcode fashionable model names or promise a cheaper model has equivalent reliability. Changing providers, billing routes, or subscriptions is not implied by a writing-style enhancement.

Use a small matched comparison or the next relevant real sessions to evaluate an applied change. Tiny samples support observations, not a percentage-saving guarantee or causal proof. Report unmeasured improvements as intended effects. If existing behavior works and no new evidence appears, stop without another tuning pass.
