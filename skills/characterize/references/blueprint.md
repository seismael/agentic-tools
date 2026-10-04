# Record and blueprint

Use a compact JSON or Markdown record outside always-loaded context. This is a skill-owned design format, **not a target agent configuration schema**. The sections below are a field inventory, not mandatory headings or tables. For a small change, use one brief record covering decisions/authority, targets/diff, checks/limits, and recovery/next action. Add detail only where another operator needs it to apply, verify, or resume safely. Reuse helper manifests for hashes and file metadata; do not narrate them again. Count generated records and artifacts in output cost.

| Section | Content |
| --- | --- |
| Identity | Record version, profile ID, owner, targets, workspace scope, dates |
| Needs | Domain/subdomain, jobs, examples, constraints, selected and custom answers |
| Coverage | Dimension status, unresolved blockers, deferral reasons |
| Observations | Version, platform, paths/hashes, effective precedence, capability evidence |
| Models | Exact provider/ID, access evidence, supported options, route, limits, billing unknowns |
| Design | Workflow, mode contracts, conventions, permission matrix, tools/context |
| Surfaces | Relevant discovered categories: change/keep/not-applicable/unresolved with reason |
| Change set | Paths, keys/sections, before/after hashes, scope, rationale, dependencies |
| Authorization | Actual user authorization, scope, proposal/digest reference, pending decisions |
| Validation | Static/runtime/behavior evidence, tasks, thresholds, observed usage |
| Recovery | Bundle location, recovery procedure, subsequent drift |
| Maintenance | Recheck triggers, ownership, rejected alternatives, resume summary |

Separate `stated`, `observed`, and `recommended`. Record path/help command/official URL, date, and installed-version relevance for non-obvious emitted features. Latest docs alone do not prove support in an older installation.

## Durable state

Use record version `1` for this format and a stable private profile ID. Per target, record phase `discovered`, `proposed`, `approved`, `applied`, `verified`, `blocked`, or `rolled-back`; keep separate evidence for each verification level. A verified stage does not imply that unrun levels passed. Retain the last applied hashes, proposal digest/reference, authorization scope, changed requirements, and one next action. Write a checkpoint after a material decision or change, not after every read.

On resume, compare the recorded target identity/version/scope and current state before reusing approvals or conclusions. Reuse authorization only while its meaning and scope still match. If the record schema is unknown, preserve it and request a supported migration rather than rewriting it silently. When evidence is absent, label the gap; a missing record does not authorize repeating external effects.

Reconcile user feedback by marking affected decisions superseded and updating dependent proposals. Keep rejected options with short reasons to avoid suggesting them repeatedly. Retain source references and minimal paraphrases rather than transcripts, secrets, or full private configs. Use native private durable storage with its normal access controls; a project-local ignored file is not automatically private or excluded from agent context.

## Capability matrix

Record `need → actual mechanism → emitted location/key → evidence → enforcement → fallback`.

- `native`: verified runtime feature.
- `instruction-only`: LLM convention without enforcement.
- `extension-required`: documented extension mechanism with proposed dependencies/effects.
- `unsupported`: no supported implementation in the target.
- `unverified`: missing evidence or access; do not enable speculatively.

Separate claims within one feature: Research can be a native subagent, source-checking can be an instruction convention, and read restrictions can be runtime policy. Different targets need different mechanisms to express the same intent.

## Mode contract

Define purpose, invocation, entry/exit criteria, required inputs, and smallest useful output. Identify the native mechanism, exact verified model or inheritance, supported effort, escalation trigger, and fallback. Specify tools, data scope, allowed/confirm/prohibited effects, enforcement limits, user decisions, authorized follow-through, and stopping conditions.

Handoff only goal, scope, constraints, decisions, changed artifacts, verification, unresolved risks, next action, and existing authorization. Create a mode only if its focus, tools, model, authority, or interaction differs usefully.

Name one owner for each mutable artifact and one integrator for parallel work. Assign bounded, independent tasks; require helpers to return findings/results with evidence and material limits. The parent validates relevant results before integration. Limit delegation depth/concurrency using verified native controls where available; an instruction-only bound is not a runtime limit. On a failed helper, change the approach or checkpoint the unresolved work instead of launching an unbounded replacement loop.

## Input, output, and gates

Infer the minimum task brief from context: goal, relevant sources, constraints, authorized effects, deliverable, and acceptance. Ask only for missing facts that materially affect execution. Do not require a form for every task.

For human deliverables, define audience, useful detail, format, and next action. For machine consumers, use their actual schema/version, field meanings, and parse/semantic checks; repair once within scope and escalate unresolved contract ambiguity. Prompted JSON is not guaranteed schema enforcement. Keep client/project-specific output formats scoped to their consumer.

Each necessary gate has a condition, owner, evidence or decision, and next action. Research stops when the deciding uncertainty is resolved; review stops when material scoped risks are addressed; execution continues through approved verification and repair. Existing authorization is carried forward, not re-requested by every role. Irrecoverable blockers produce a resumable record and precise user action.

## Transitions

Define “next”, “continue”, “revise”, and “apply” within current state. Interpret approval against the latest concrete proposal. Do not let “next” silently approve publication, spending, or other consequential external effects.

For consultative engineering, Diagnose/Architect/Plan investigate and iterate with feedback. Implementation approval covers in-scope Build, Validate, and repair. A failed check returns to implementation when the repair remains within scope; changed scope or consequential effects require a new decision.

Natural-language transitions are instruction conventions unless a verified mechanism executes them. If agent/model switching requires UI/CLI action, show the actual action. Do not pretend an ordinary prompt changed the runtime model or add an LLM router to hide a manual switch.

## Acceptance

Select observable checks: correctness, source accuracy, brief adherence, voice/audience, format, safe scope, completeness, time/usage. Establish the quality floor before resource optimization. Use a typical task and an ambiguous or high-consequence case where feasible. Expand only for a concrete failure or required gate; pending checks are not passes.
