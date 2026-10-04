# Investigation, options, approval, and feedback

Use the target/host's native planning, question, approval, and execution mechanisms when available. Do not replace built-in agents or assume one product's Plan semantics exist elsewhere. Describe any instruction-only convention honestly. Distinguish the interaction used to customize the agent from the interaction the customized agent will use during ordinary work: collaborative setup can lead to autonomous execution.

## Phase and authority

Track `investigate → propose/refine → approved → apply → verify → feedback/complete`, allowing feedback to return only affected decisions to refinement. Treat these as workflow states, not new mandatory runtime modes.

Reuse explicit current instructions and previously recorded authorization. For audit, plan, or approval-first requests, investigate and prepare exact proposals without changing target behavior. If the request leaves customization authority unspecified, use proposal-first behavior. If the user already authorizes application or supplies a standing scoped authorization, apply within that scope without asking again. A request to update this skill authorizes the requested skill update, not every target configuration it can reach.

During planning, authorized reads, investigation, private progress records, and staged proposals may proceed. Do not activate hooks, alter live settings, run consequential target actions, or have a subagent apply changes while approval is pending. Native capability controls and instruction conventions differ; do not claim a read-only guarantee without checking indirect write paths.

## Ask questions that change the design

First investigate what can be discovered and reuse prior user answers. Ask only when a missing preference or unresolved tradeoff materially changes the proposal. Avoid a fixed questionnaire before doing useful work. Cover as needed:

- Quality and reliability requirements versus token/quota/latency priorities.
- Routine response length, detailed deliverables, and machine-consumed output contracts.
- Desired autonomy, mode transitions, meaningful decisions, and approval scope.
- Main-agent/helper responsibilities, model/effort tradeoffs, and allowed delegation overhead.
- Global defaults, shared project requirements, private exceptions, and follow-up evaluation.

For each preference question, provide three meaningful choices plus a custom response. Make a justified recommendation, explain the practical tradeoff briefly, and incorporate custom answers into the decision record. Use the native question interface when it supports this; otherwise present numbered choices with a fourth custom option. If the interface supplies its own free-text choice, do not add a duplicate. Batch one to three closely related questions; use follow-up questions only when answers expose a real new decision.

For example, an unresolved collaboration style can offer: recommended proposal-first with autonomous execution after approval; autonomous changes within a preapproved scope; or consultation at meaningful design milestones; plus a custom option. Do not ask this when the user has already chosen. Propose other options suited to the finding rather than reusing these choices for unrelated questions.

If an optional preference question receives no answer, continue with a stated, conservative assumption and complete the proposal. Silence is not approval to apply. Keep blocked decisions isolated so independent authorized work can continue. Avoid repeating an unanswered question unless it is genuinely indispensable.

## Present a concrete proposal before approval

Keep the package short and decision-ready, with details in staged artifacts when needed. For every suggestion, establish expected effectiveness and total overhead before requesting approval. Show a compact package containing:

- Evidence-backed problems and relevant assessment dimensions, with unknowns separated.
- Exact proposed changes or staged diffs, target tool/version and scope, and dependencies.
- Expected net performance and cost effects, including added input/output/context, orchestration, and recurring automation overhead; intended behavior, material tradeoffs, and measurable acceptance criteria.
- What stays inherited because native behavior already fits, where relevant to the decision.
- Validation and recovery plan; any unavailable target access or unverified native feature.

When target contents are unavailable, make the proposal as concrete as evidence permits, but never invent existing bytes or claim an exact applicable patch. Identify the local inspection needed to finalize it.

Offer feedback and scoped approval of the ready proposal. Use the host-supported authorization mechanism or a plain explicit approval question; do not use a preference-only question widget for permission. The user can approve the package, approve a clear subset, revise it, or defer it. A choice about preferred behavior does not automatically approve unrelated configuration edits. Record the approved proposal revision, decision IDs, target/scope, constraints, user modifications, and authorization basis.

## Execute, verify, and incorporate feedback

Apply the approved package through native surfaces, then validate and repair within scope. Do not request fresh approval for every tool call, file, check, or routine repair. Ask again only for an uncovered consequential action, materially broader change, actual authority/access barrier, or unresolved decision outside the approved bounds. Preserve prior approval for unchanged parts when feedback revises another part. Track dependencies so approving one component does not silently enable a deferred component.

Report what changed and what was actually verified. When a fresh acceptance judgment is useful, ask one focused question about the observed behavior, with meaningful suggested adjustments and custom input. Do not force a satisfaction questionnaire after every run. If runtime evidence is absent, state that the outcome remains unobserved and specify what the next relevant session should establish.

Incorporate feedback into the expectation profile and affected decisions. Update the proposal or authorized implementation without restarting discovery unnecessarily. Preserve rejected approaches and reasons so they are not repeatedly suggested. End when the accepted criteria are met or the remaining blocker is explicit. Do not schedule another review, install a watcher, or start another optimization cycle unless requested.
