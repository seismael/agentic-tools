# One-finding decision loop

Discuss the highest-value substantiated finding first, unless a prerequisite or the user's focus dictates another order. Preserve new findings in the queue. Do not ask the user to solve a diagnosis the auditor can resolve from available evidence.

Use a compact decision card:

- **F-001 — title**. Severity / priority / confidence, and affected outcome.
- **Evidence:** one or two precise source references and the causal failure or opportunity; state material uncertainty.
- **Recommendation:** the concrete, professional approach. It must logically and realistically solve the root cause without 'cheating' or removing mandatory constraints. Detail the expected benefit, important cost/risk, and why it beats the credible alternatives.
- **Alternatives:** normally one or two viable technical choices, each with its tradeoff. Avoid filler choices or obvious straw men.
- **Decision:** accept recommended or named alternative, defer with reason/trigger, reject with reason, or reply with a question/custom change.

When presenting a finding, DO NOT just ask for a generic "Approve, Reject, or Defer" response in plain text. Instead, use native interactive UI tools (such as the `ask_question` tool) to present concrete, deeply investigated remediation options as selectable checkboxes (e.g., "Option A: Migrate to zero-fee tier", "Option B: Widen RSI entry threshold"). 

Always ensure a write-in option is available (or rely on the tool's default 'other' text box) so the user can submit a custom reply or tailored message instead of just clicking an option. Presenting distinct, well-researched architectural choices is mandatory. Ask one finding at a time. A further explanation or request to compare options leaves the disposition undecided.

Persist provenance as the user's statement/message locator, chosen option, scope, rationale and relevant conditions. Do not fabricate a message ID; a concise attributable quotation/description is sufficient when stable IDs are unavailable. Do not paste the whole conversation. A previous clear decision satisfies this loop; do not force a redundant interview.

If the user clearly rejects or defers without explaining why, record that no further rationale was supplied; do not demand one just to fill a template. For a deferral without a trigger, use the next explicit request to reconsider as its conservative trigger unless a material dependency warrants a focused question. Do not invent a deadline or automatic approval.

## Dispositions

| State | Required response |
|---|---|
| Undecided | Retain evidence and recommendation; ask or resume the outstanding decision. No ready implementation packet. |
| Accepted | Complete the agreed design and task breakdown; check readiness and publish the packet. Planning acceptance alone does not authorize implementation. |
| Deferred | Retain a proportionate future plan, reason, prerequisite/revisit trigger and priority. Do not place it in the executable queue. Revalidate before future promotion. |
| Rejected | Record rationale and evidence compactly, with no executable plan. Stop revisiting unless material evidence or goals change. |
| Withdrawn | Record the auditor's correction and disconfirming evidence; retain the ID with no executable plan. Do not invent user rejection or require approval to correct a false claim. |
| Superseded | Preserve the old ID and decision history; link its replacement, explain the merge/change, and remove it from execution. Do not silently reuse IDs. |

If a reply is ambiguous (for example “interesting” or “what about another design?”), keep the finding undecided. If the question UI yields no answer, preserve the checkpoint; continue only authorized independent investigation, never mark acceptance. If the user explicitly delegates all decisions or requests grouped minor decisions, record that scope and follow it rather than enforcing unnecessary prompts.

User feedback can change a finding, not just select it. Correct mistaken evidence, lower confidence, split distinct root causes, or withdraw a disproven recommendation. Use `withdrawn` only for a refuted claim, not to bypass a user decision about a real risk or to dismiss a valid issue that is merely fixed. Preserve previous decisions when correcting an already accepted record; explain the correction briefly and reconcile dependent plans. Use `superseded` only when a real replacement exists.

Before advancing, update the packet, manifest and index together and complete the agreed delivery checkpoint. A failed required write does not erase the user's decision or require approving it again. Retain prepared work and exact pending paths, state the blocker once, and report delivery separately from completed review/decisions. Do not describe unrequested remote publication as a blocker for local-only work.

Do not equate rejecting a proposal with resolving the underlying technical risk. Report accepted risk or known unfixed defects accurately. Reopen only when new evidence, changed source, elapsed trigger or changed goals materially warrants another decision.
