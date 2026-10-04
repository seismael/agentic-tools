# One-finding decision loop

Discuss the highest-value substantiated finding first, unless a prerequisite or the user's focus dictates another order. Preserve new findings in the queue. Do not ask the user to solve a diagnosis the auditor can resolve from available evidence.

Use a compact decision card:

- **F-001 — title**. Severity / priority / confidence, and affected outcome.
- **Evidence:** one or two precise source references and the causal failure or opportunity; state material uncertainty.
- **Recommendation:** the concrete approach, expected benefit, important cost/risk, and why it beats the credible alternatives.
- **Alternatives:** normally one or two viable technical choices, each with its tradeoff. Avoid filler choices or obvious straw men.
- **Decision:** accept recommended or named alternative, defer with reason/trigger, reject with reason, or reply with a question/custom change.

When a native question tool limits options, use recommended approach, defer, and reject, with custom text for alternatives, questions and modifications; explain the technical alternative in the card. When no suitable tool exists, use a plain concise question. Ask one finding at a time. A further explanation or request to compare options leaves the disposition undecided.

Persist provenance as the user's statement/message locator, chosen option, scope, rationale and relevant conditions. Do not fabricate a message ID; a concise attributable quotation/description is sufficient when stable IDs are unavailable. Do not paste the whole conversation. A previous clear decision satisfies this loop; do not force a redundant interview.

If the user clearly rejects or defers without explaining why, record that no further rationale was supplied; do not demand one just to fill a template. For a deferral without a trigger, use the next explicit request to reconsider as its conservative trigger unless a material dependency warrants a focused question. Do not invent a deadline or automatic approval.

## Dispositions

| State | Required response |
|---|---|
| Undecided | Retain evidence and recommendation; ask or resume the outstanding decision. No ready implementation packet. |
| Accepted | Complete the agreed design and task breakdown; check readiness and publish the packet. Planning acceptance alone does not authorize implementation. |
| Deferred | Retain a proportionate future plan, reason, prerequisite/revisit trigger and priority. Do not place it in the executable queue. Revalidate before future promotion. |
| Rejected | Record rationale and evidence compactly, with no executable plan. Stop revisiting unless material evidence or goals change. |
| Superseded | Preserve the old ID and decision history; link its replacement, explain the merge/change, and remove it from execution. Do not silently reuse IDs. |

If a reply is ambiguous (for example “interesting” or “what about another design?”), keep the finding undecided. If the question UI yields no answer, preserve the checkpoint; continue only authorized independent investigation, never mark acceptance. If the user explicitly delegates all decisions or requests grouped minor decisions, record that scope and follow it rather than enforcing unnecessary prompts.

User feedback can change a finding, not just select it. Correct mistaken evidence, lower confidence, split distinct root causes, or withdraw a disproven recommendation. If withdrawal requires no user decision because there is no longer a valid finding, preserve the explanation as a coverage note and mark any previously registered record superseded only when a real replacement exists; otherwise obtain/record the user's rejection rather than falsifying a disposition.

Before advancing, update the packet, manifest and index together and publish when authorized. On a write blocker, retain local prepared work and exact pending paths, state the blocker, and keep that finding's publication pending. A publication failure does not erase the user's decision or require approving it again. Never call a run complete while required audit records remain unpublished.

Do not equate rejecting a proposal with resolving the underlying technical risk. Report accepted risk or known unfixed defects accurately. Reopen only when new evidence, changed source, elapsed trigger or changed goals materially warrants another decision.
