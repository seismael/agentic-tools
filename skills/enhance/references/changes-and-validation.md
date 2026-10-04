# Changes and validation

## Prepare a concrete change

Follow interaction-and-approval.md for proposal revision, preference questions, and authorization. Bind application to the approved decision set when approval is required; a declined or deferred dependency must not be activated indirectly. Existing authorization remains valid for its unchanged scope.

For each decision, record a stable ID, evidence references, expectation, scope, target surface, current configuration hash, exact proposed diff, expected effect, authorization basis, validation, and recovery reference. Keep raw configs/backups in private storage; display redacted diffs when they contain sensitive fields. A proposal can be useful without permission to apply it.

Use the governing native surface. Edit existing relevant content before creating new files. Preserve comments, ordering, ownership, encoding, newline conventions, unrelated settings, and precedence. Parse format-specific structures with appropriate tooling rather than unsafe blanket replacement. Do not write an invented file based on a guessed default.

Before each write, compare the current content with the inspected snapshot. If it drifted, re-read and merge the intended change without discarding the user's work. Use atomic replacement when supported. Several file replacements are not a single transaction: journal per-file before/after hashes and outcomes, then verify the resulting set. Use one integrator for shared files.

Keep application and review checkpoints independent. After interruption, inspect current hashes to determine which changes actually landed; do not blindly replay the whole bundle. Mark a decision applied only after checking the target state. A partially applied bundle remains partial until repaired or safely reverted. Never overwrite newer edits during rollback; apply a narrow inverse patch when possible, otherwise explain the conflict.

## Validate proportionately

1. **Static:** validate parsing/schema and supported keys, file locations, rule conflicts, and expected diff. Label this static-validated only.
2. **Loaded:** check effective configuration or native loading evidence. Use a fresh isolated session if required; do not disrupt the user's active work merely to obtain a smoke test.
3. **Behavior:** use a small relevant task or subsequent real session. Check the behavior implicated by the change, expected output, scope, handoff, and important retained exceptions. Simulation is useful but is not evidence of target enforcement.
4. **Outcome:** compare observed quality, user interventions, and total cost when telemetry is available. Record missing measurements and defer claims about improvement until observed.

For changes to permissions, tools, or delegation, explicitly verify the intended capability boundary, including indirect paths. Do not run destructive actions, send messages, or incur material unapproved cost merely to test a configuration. For prose-only changes, a structural check and relevant behavioral scenario can suffice; do not add a broad test project.

## Representative scenarios

Select only scenarios relevant to the change:

- A routine implementation task completes through required checks without repeated confirmation.
- A plan-only request remains analytical until implementation is authorized.
- Routine progress is concise, while an explicitly requested detailed audit stays detailed.
- A repository-specific convention applies in that project and does not contaminate another.
- An independent delegated task returns evidence and a compact result without duplicated investigation or overlapping edits.
- A real ambiguity produces a useful question; a routine discoverable fact produces investigation.
- A repeated invocation with unchanged evidence/configuration makes no duplicate edits.
- Preference questions offer useful choices and custom input; answers update the affected design without silently authorizing other changes.
- Approval of a package or subset leads to execution and verification without routine approval loops; deferred dependencies remain inactive.
- A required structured output passes both its actual schema and semantic acceptance checks; human-facing tasks remain appropriately readable.

Keep rejected/deferred decisions with a short reason. Reconsider only when new evidence changes their basis. When a new user edit supersedes an applied rule, retain the provenance without automatically restoring the old rule. Enhancement is evidence-led maintenance, not enforcement against the user.
