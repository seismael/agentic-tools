# Project audit and implementation queue

REPLACE: Focus, frozen source baseline, current coverage, unresolved decisions and publication state. Link CONTEXT.md for the domain/architecture brief; audit.json is the canonical state ledger. This audit does not certify an absence of defects.

## Findings and execution order

REPLACE: A compact table of ID/title/link, severity/priority/confidence, user disposition, plan state, prerequisites and next action. Derive it from audit.json; keep deferred/rejected work visible outside the executable queue. No ready tasks is a valid result.

## Next decision or review step

REPLACE: The next single user decision, blocked check, or unreviewed scope. Do not mark a partial audit complete. Already resolved decisions do not need another approval.

## Local-agent execution contract

1. Read audit.json, CONTEXT.md, the selected accepted/ready finding packet and its direct prerequisites. Check your current implementation authorization; acceptance of a plan alone is not permission to change product code. Reuse approval that already covers the work.
2. Inspect current source and compare relevant files/contracts with the pinned evidence. Audit-only commits do not invalidate source. Preserve unrelated edits. If relevant behavior or assumptions changed, mark the affected plan blocked and reconcile before implementing.
3. Execute in dependency order. A ready prerequisite still needs implementation and successful checks before dependent work starts. Do not execute deferred, rejected, undecided, superseded or blocked packets.
4. Follow each task's exact outcome, paths, scope and checks using native project conventions. Complete in-scope repairs autonomously within existing authority. Parallelize only disjoint work with explicit integration ownership. Do not redesign unrelated components.
5. Stop for a material contradiction, missing authority, failed invariant or unresolved product choice. Record the precise blocker and needed decision; do not guess or silently omit a requirement.
6. Run specified acceptance checks and relevant project gates. Record actual commands/results, implementation commits, changed files, deviations and remaining limitations in the packet. Mark done only when required acceptance evidence exists; never equate an untested commit with completion.

Load only the needed packets and evidence. The audit records supply the design; targeted source inspection and implementation validation remain necessary.
