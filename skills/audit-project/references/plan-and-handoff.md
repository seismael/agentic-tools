# Plan quality and local-agent handoff

## Compact repository layout

Use one audit directory, default `docs/audit/`:

- `README.md`: audit status, ranked queue with links, execution order, coverage gaps, next decision, and the local-agent contract.
- `CONTEXT.md`: frozen source commit/ref, domain brief, goals and constraints, architecture/flows, verified commands/environment, source references, publication destination and limitations.
- `audit.json`: canonical IDs, classification, decision/readiness states, dependencies, evidence locators and coverage. Avoid repeating long prose here.
- `findings/F-001.md`: evidence, decision and the complete proportionate implementation packet for that finding. Use stable IDs, not priorities in filenames.

Link rather than duplicate: the manifest owns structured state; packets own detail; the index is a derived navigation/queue view. Verify they agree before committing. Do not create a separate file for every tiny task or copy an enormous plan into chat. Do not write repository-wide `AGENTS.md` or modify host configuration merely to make agents consume the audit.

Keep deferred packets concrete about the future objective and likely work, but avoid detailed invented code for an uncertain future architecture. Rejecting a finding needs a short disposition, not six empty pages. The artifact contract defines minimal required sections for all packets and the fuller ready gate.

## Implementation packet requirements

The following questions must have repository-specific answers for a ready packet. State a justified `not applicable` where a concern truly does not apply.

1. **Outcome:** What observable behavior must change, for whom, under which input/state conditions? What must remain compatible? Which success/failure boundary proves completion?
2. **Diagnosis:** What source at the baseline supports the finding, what exact path causes it, and which alternative explanations were checked? Which commands actually ran versus remain proposed?
3. **Decision:** What did the user accept, reject or defer, why, and with what constraints? Which implementation authority exists independently? What material options were rejected and why?
4. **Design:** Which existing structures are reused? Which paths/symbols change? Give exact interfaces, field shapes, invariants, algorithms/state transitions, error handling, resource lifetimes and integration points as relevant. Use small pseudocode only for non-obvious logic; do not prewrite the whole patch.
5. **Tasks:** Give stable IDs such as `F-001-T1`, sequential prerequisites, file ownership and exact transformations. Each task supplies input/precondition, changed files/symbols, instructions, acceptance result, check and expected outcome. Avoid “improve reliability”, “refactor appropriately” or “add tests” without specifying the behavior.
6. **Completeness:** Identify affected callers, config/schema, docs/examples, tests, generated artifacts and packaging. Name deprecated/duplicated paths to remove only when supported. Include data/backward compatibility only when it actually matters to this project.
7. **Verification:** Define meaningful regression cases, integration checks and domain-specific acceptance. Supply commands, working directory, prerequisites and expected result; use placeholders only in non-ready drafts. A command not executable in the audit environment is an implementer check, not a passed test.
8. **Deployment/recovery:** State rollout boundaries, monitoring and rollback or forward-recovery. For irreversible data changes, explain restoration constraints and explicitly flag necessary separate authorization. For doc-only changes, a reviewed file revert may be sufficient.
9. **Dependencies and stop conditions:** List prerequisite finding IDs and external blockers. Separate parallel work by disjoint ownership and stable contracts. Identify exactly what should stop implementation: conflicting source drift, unknown API behavior, missing required authority, inconsistent tests, failed safety invariant or unresolved product choice.

A large architectural change needs an explicit target model, preserved invariants, coherent phased cutover, interface ownership, compatibility strategy and exit checks. An unreleased project may use a clean replacement without migration; do not invent legacy support. An adopted system may require staged compatibility and data transition; do not erase it based on the auditor's aesthetic preference.

## Readiness review

Read the proposed packet as an implementer with no chat access. Ask whether any consequential design choice would still need rediscovery. Resolve it now from evidence or mark it blocked with an exact research/decision task. Review a complicated plan independently when the risk justifies it; pass the packet and raw evidence, not the intended verdict.

Check evidence-to-task traceability: every task contributes to an approved outcome, and every accepted outcome has a task and an observable check. Check realistic command syntax and paths against the pinned repository. Validate dependency order, ID/link consistency, status and absence of placeholders. The helper catches structural errors; human/model semantic review remains necessary.

“Ready” means ready for authorized implementation at the stated baseline. It does not mean implemented, executed, formally proven, universally optimal, or permission granted. The local agent still performs narrow source checks and verification because code, dependencies and external behavior can change.

## Executor protocol to include in the index

1. Read `audit.json`, `CONTEXT.md`, and the chosen accepted/ready packet plus direct prerequisites. Confirm current implementation authorization; do not treat `accepted` as blanket permission. Preserve existing authorization without routine reapproval.
2. Inspect current files/contracts and compare them with the frozen baseline and relevant evidence. Audit-document-only changes do not invalidate code evidence. If unrelated source changed, continue after targeted comparison; if relevant source/assumptions changed, mark the affected packet blocked, record the discrepancy and request/prepare reconciliation. Never blindly execute stale instructions.
3. Work in dependency order. A ready dependency may be planned first; a dependent task starts only after prerequisite implementation and checks actually complete. `ready` is not equivalent to `done`. Do not execute deferred, rejected, undecided, superseded or blocked packets.
4. Implement the specified behavior and necessary in-scope repairs, following native project conventions. Reuse approved mechanisms; avoid unrelated redesign. Delegate only independent tasks with disjoint file ownership and explicit integration ownership.
5. Run the specified checks and necessary project gates; report exact results and environmental limits. If an acceptance criterion fails, repair within scope. Stop for a material contradiction or changed decision rather than inventing a new architecture.
6. Record task completion, touched files, implementation commit(s), actual checks/outcomes, deviations and remaining limits in the packet; update structured plan state when authorized. Mark `done` only when all required acceptance criteria have supporting evidence. A source-code commit alone does not prove success.

No universal executor or orchestration service is required. Any capable authorized local agent can follow the repository files.
