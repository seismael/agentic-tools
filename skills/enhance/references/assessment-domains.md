# Assessment domains and acceptance criteria

Assess the setup end to end across the dimensions below. Treat performance, token consumption, and cost effectiveness as the primary optimization dimension, subject to correctness, required completeness, reliability, and the user's explicit priorities. “Best setup” means the best supported fit for this user's work and constraints, not a universal configuration or the greatest number of features.

Use one semantic pass over each session to extract evidence for several dimensions. Do not reread the full history separately for each domain or create a council of agents to fill a checklist. Maintain a compact assessment matrix:

`dimension | evidence/baseline | diagnosed issue | desired outcome | proposed mechanism/scope | tradeoff | validation | disposition`

Classify each dimension `change`, `keep`, `unknown`, or `not-applicable`, with a reason. Unknown is not healthy and not a reason to invent changes. An initial review covers all relevant dimensions at useful depth; subsequent reviews refresh affected dimensions and verify previous changes. Read related references only as needed.

## Efficiency-first decision rule

Apply this rule to every recommendation, including changes whose main benefit is reliability, consistency, research quality, or autonomy. Record a compact assessment of:

`useful outcome | input/output and total usage effect | latency/throughput effect | one-time and recurring overhead | simpler native alternative | quality constraints | evidence/uncertainty | validation`

Prefer the smallest supported change that improves verified useful work per cost/time. Include setup, additional instructions, helper context, checks, retries, runtime activity, and maintenance in the cost of the suggestion itself. Separate one-time enhancement cost from recurring savings. A quality fix may justify more tokens when needed to satisfy a requirement or reduce failures/rework; state that tradeoff rather than claiming all metrics improve. If the net benefit is uncertain, prefer a bounded observation or experiment over a permanent speculative layer. Do not remove necessary verification or choose a weak model solely for a lower token count.

Measure useful task completion, latency, throughput, and resource use where relevant. More tool calls can still be cheaper and more reliable than more model generation; fewer tokens do not necessarily mean lower price, quota usage, or elapsed time. Prioritize high-impact observed waste over marginal formatting tweaks. Do not invent numerical savings, efficiency scores, or a universal weighted optimum when data is unavailable.

## 1. Token consumption, cost, quota, and latency

Attribute available usage to source session, task type, phase, model/effort, parent/helper, input/output/reasoning/cache class, tool payloads, retries, and rework. Use existing telemetry and local aggregation; do not send full histories to another model just to count them. Deduplicate usage already rolled up by the host. Separate tokens, monetary charges, subscription quota, and latency; verify the accounting model before converting between them.

Investigate the largest supported recurring contributors first: expensive verbose outputs, repeated narration, broad reads, repeated history loading, redundant standing rules, always-loaded skills, tool/schema payloads, duplicate investigations, unnecessary delegation, failed retry loops, unsuitable model effort, or poor context retention. Short final answers do not prove low total consumption. Cache discounts or native compaction benefits must be observed or labeled estimates; preserve critical context and acceptance criteria.

Rank candidates by evidence strength, expected recurring impact, implementation/validation cost, and regression risk. Consider the cost of the enhancement run itself. Prefer reuse of telemetry, deterministic filtering, bounded outputs, and incremental review. Never claim a percentage saving without a stated comparable baseline. Treat output reduction as a candidate saving while preserving required explanations, artifacts, and useful progress visibility.

## 2. Reliability and correctness

Inspect incomplete tasks, inaccurate claims, unsupported assumptions, repeated errors, unchecked tool results, recovery failures, lost progress, and rework. Diagnose the actual cause: unsupported capability, stale evidence, bad routing, insufficient context, configuration conflict, or a task/model limitation. Define appropriate evidence and success criteria for the user's domain.

Use bounded retries with a changed hypothesis, resumable checkpoints, checks tied to concrete risks, and clear handling of failure. Verify a completed outcome rather than equating a successful command with success. Preserve necessary tests, source checks, or review when optimizing cost. Avoid endless repair loops and repeated broad validations once the relevant criteria pass.

## 3. Consistency and configuration coherence

Inspect conflicting global/project rules, duplicated prompts, stale overrides, inconsistent mode transitions, forgotten preferences, and differences across agents. Determine the governing rule and effective value for each affected context. Preserve intentional task/project exceptions. Consolidate duplicated sources only where ownership and native precedence permit it; do not erase useful specialization.

Record a stable decision once and reuse it. Recheck relevant overrides after product updates and user feedback. Require repeat runs with unchanged evidence/configuration to make no duplicate changes.

## 4. Structured inputs, outputs, and artifacts

Define the minimum useful task input contract: objective, relevant context/references, constraints, authorized effects, desired deliverable, and acceptance criteria. Infer these from the request and accessible environment where possible; do not force users to fill a form for every task. Ask only for consequential missing information.

Distinguish human-facing prose from machine-consumed data. Use clear sections, tables, or files when useful to humans; use the consumer's actual schema, types, required fields, and version when producing structured data. Prefer native structured-output support when verified; otherwise validate parsing and contract compliance with an explicit repair path. Do not impose JSON on all responses or promise schema enforcement through prompting alone. Check semantic completeness as well as syntax. Apply a project's output contract locally unless it is explicitly shared.

## 5. Autonomy, questions, approval, and user control

Assess unnecessary questions, ignored decisions, premature implementation, abandoned tasks, unclear authority, and excessive narration. Separate meaningful design choices and configuration approval from ordinary execution. Once a concrete change is authorized, finish implementation, relevant verification, and in-scope repairs without repeated permission requests.

Honor the user's preferred collaborative or autonomous style and native mode boundaries. Preserve meaningful questions where their answer changes the result. Use the proposal-and-feedback workflow in interaction-and-approval.md; do not infer authorization from silence, a suggested option, or historical assistant statements.

## 6. Native agents, subagents, and orchestration

Map the actual primary roles, native modes, skills, helpers, delegation mechanisms, context visibility, permissions, and model inheritance. Evaluate task fit, ownership, routing, handoff clarity, duplicate work, coordination overhead, and result integration. Prefer existing native capabilities over a new orchestration layer.

For each role, specify responsibility, trigger, required input, owned scope, allowed effects, completion criteria, result contract, and who verifies/integrates its result. Use a narrow project role for project needs; share a role globally only when its responsibility is portable. Parallelize independent work when it pays for its overhead; keep dependent work ordered and one integrator for shared changes. Avoid circular calls, uncontrolled fan-out, and helpers redoing the parent's whole analysis. Adapt behavior to the target's real agent semantics rather than copying another tool's agent files.

## 7. Context, memory, tools, and operational flow

Assess retrieval relevance, context loss, checkpoint quality, long-session continuity, tool availability, repeated payloads, hook behavior, permissions, and environment-specific friction. Prefer native discovery, compaction, persistence, and tool activation when suitable. Load the minimum sufficient context at the right time and retain evidence links rather than duplicated artifacts.

Check the complete path from user request through planning, execution/delegation, validation, deliverable, and resumption. Fix the handoff or configuration responsible for the break rather than adding general prose. Keep unavailable capabilities and access limits explicit. Preserve existing privacy and security boundaries while reducing unnecessary friction.

## 8. Research and review

Assess whether research resolves the actual question with sufficient credible evidence and whether review finds material defects without becoming a repeated broad audit. Examine repeated searches/reads, irrelevant sources, premature conclusions, stale evidence, unsupported citations, excessive report length, and independent reviewers duplicating the same work.

Define the question, needed evidence, uncertainty to resolve, and stopping criteria. Reuse valid retrieved evidence, prefer authoritative sources where appropriate, investigate conflicting claims, and deepen only where the decision requires it. Keep research notes compact and separate from the final actionable conclusions. Bound a review by the actual changed scope, acceptance criteria, and unresolved risks. Report a finding with evidence, consequence, recommendation, and a relevant verification step; avoid cosmetic checklists or another reviewer without an expected quality/cost benefit.

## 9. Workflows, gates, and automation

Assess request intake, planning, execution, handoffs, validation, delivery, feedback, and resumption as one workflow. Identify abandoned stages, unnecessary transitions, repeated approvals, missing ownership, unbounded retries, and gates that add no decision value. For each necessary gate, define the condition, required evidence or user decision, owner, and next action. Routine already-authorized operations are not new approval gates.

Where automation already exists or is requested, evaluate native hooks, triggers, schedules, and event workflows for actual fit, frequency, idempotence, retries, concurrency, duplicate execution, failure handling, cancellation, observability, and cost. Prefer low-overhead native or deterministic handling for mechanical work; use model calls only when judgment is needed. Explain ongoing token/runtime costs and side effects before proposing activation. Do not equate more automation with a better setup, activate an unapproved workflow, or add a background optimizer by default. Keep automation scope aligned with its intended projects and permissions.

## 10. Domain and project fitness

Evaluate actual work products: for example, runnable changes in engineering, traceable findings in research, brand-appropriate writing, valid data transformations, usable design artifacts, or correctly completed operational tasks. Respect shared project conventions, private project preferences, language, audience, output schema, environment, and local acceptance criteria. Do not assume engineering checks or one user's project constraints apply everywhere.

## Synthesis and stopping

Explain tradeoffs between dimensions: a smaller prompt can lose critical constraints; a cheaper model can create costly rework; another helper can increase latency and input tokens; structured output can help a machine consumer while hindering a human. Prefer candidates that satisfy the user's minimum quality/reliability needs and improve total effort or cost. Keep hypotheses separate from measurements.

Build a coherent proposal from supported changes, grouped by scope and dependency. Use a small matched comparison or the next relevant real sessions to assess results. Stop when approved acceptance criteria pass; keep remaining experiments explicit and optional. Feedback should reopen affected decisions, not restart a full audit or an indefinite tuning loop.
