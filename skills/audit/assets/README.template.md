# Project audit and implementation queue

AUDIT_TODO: Focus, frozen source baseline, review coverage, decision completion, plan readiness and delivery state (local files, local commits or GitHub as agreed). Link CONTEXT.md for the domain/architecture brief; audit.json is the canonical state ledger. This audit does not certify an absence of defects.

## Findings and execution order

AUDIT_TODO: A compact table of ID/title/link, severity/priority/confidence, user disposition, plan state, prerequisites and next action. Derive it from audit.json; keep deferred/rejected work visible outside the executable queue. No ready tasks is a valid result.

## Next decision or review step

AUDIT_TODO: The next single user decision, blocked check, or unreviewed scope. Do not mark a partial audit complete. Already resolved decisions do not need another approval.

## Local-agent execution contract

1. Read audit.json, CONTEXT.md, the selected accepted/ready finding packet and its direct prerequisites. Check your current implementation authorization; acceptance of a plan alone is not permission to change product code. Reuse approval that already covers the work.
2. Compare current files/contracts, callers/tests/configuration and prerequisite completion with the pinned evidence. Preserve unrelated edits. Audit-only changes do not invalidate source; expected prerequisite changes can be compatible. Record compatible revalidation with its checked commit and evidence, then continue within authority. For unresolved contradictions, record block_reason and next_action and reconcile before implementing; preserve original evidence anchors.
3. Execute in dependency order. A ready prerequisite still needs implementation and successful checks before dependent work starts. Do not execute deferred, rejected, withdrawn, undecided, superseded or blocked packets.
4. Follow each task's exact outcome, paths, scope and checks using native project conventions. Complete in-scope repairs autonomously within existing authority. Parallelize only disjoint work with explicit integration ownership. Do not redesign unrelated components.
5. Stop for a material contradiction, missing authority, failed invariant or unresolved product choice. Record the precise blocker and needed decision; do not guess or silently omit a requirement.
6. Run specified acceptance checks and relevant project gates. Record commands/results, implementation commits, changed files, deviations and limits once in the packet. Add completion evidence and final check results to the manifest; mark done only when criteria and dependencies are satisfied. An unavailable check is blocked, not passed or not applicable.

Load only the needed packets and evidence. The audit records supply the design; targeted source inspection and implementation validation remain necessary.
