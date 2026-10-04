# Incremental review state

## Storage and identities

Use a private durable location appropriate to the host, outside the skill package, shared repositories, and automatically loaded instructions. Record its location in the existing private user/tool record or an authorized lightweight locator; do not inject the full ledger into prompts. In hosted environments, save/restore the record with the available durable file mechanism. Without persistence, report that resumability is unavailable rather than pretending a scratch file will survive.

Use one source ID per tool/account/profile history, one stable session ID within that source, and one content revision per snapshot. Project identity is separate. A date is useful display metadata, not the review cursor. Use a fingerprint covering the stable project identity (including null), relevant session content, and any reliable native revision marker. Reclassification to another project must change the fingerprint even if message text is unchanged; otherwise old scope conclusions could be reused. Exclude volatile export metadata when hashing. Preserve provenance to avoid counting forked/copied messages as independent evidence.

The helper below handles normalized metadata and review/decision bookkeeping. It does not discover native histories, redact secrets, read transcripts, infer expectations, apply configuration, or prove semantic completeness. The agent remains responsible for accurate coverage and privacy. If Python is unavailable, use a supported store with the same semantics rather than installing dependencies automatically.

## CLI

Run the bundled script using its resolved installed path. Pass an absolute private database path; replace the illustrative paths below with actual locations. Create the private database parent directory first. Input JSON files must contain only compact nonsecret metadata. Keep one discovery owner per source/run and serialize its inventory updates: opaque fingerprints have no ordering, so an older manifest must not overwrite a newer snapshot. The helper serializes database writes but cannot establish source freshness.

```bash
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite inventory --manifest /private/enhance/inventory.json
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite pending --source opencode:profile-a --limit 25 --offset 0
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite record --source opencode:profile-a --session s1 --revision hash-v1 --status partial --cursor event-40 --note 'Reviewed through event 40; later messages remain.'
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite record --source opencode:profile-a --session s1 --revision hash-v1 --status reviewed --cursor event-78 --note 'Full revision assessed; findings saved.'
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite decision --file /private/enhance/decision.json
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite decisions --limit 25 --offset 0
python3 scripts/review_ledger.py --db /private/enhance/review.sqlite show --summary
```

Inventory shape:

```json
{
  "source": "opencode:profile-a",
  "sessions": [
    {"id": "s1", "revision": "hash-v1", "locator": "native-session:s1", "project": "project-a"},
    {"id": "s2", "revision": "hash-v4", "locator": "native-session:s2", "project": null}
  ]
}
```

Build and register an inventory snapshot before recording reviews. A manifest may represent a page or a batch; absent rows must not be interpreted as deletions. Track whether enumeration covered the entire source separately. Keep blocked or absent sources visible until resolved. Use `show --summary` for counts. When paging `pending` with `--limit`/`--offset`, collect the complete worklist before recording reviews, with inventory and review coverage unchanged throughout enumeration. Marking a row reviewed removes it from `pending`, so advancing an offset after reviews can skip sessions even when the inventory is stable. Page `decisions` only while decision membership is stable. If the relevant membership changes during either enumeration, restart paging and deduplicate identities. Redirect unbounded diagnostic output to a private file rather than dumping it into context. CLI JSON output escapes non-ASCII characters for portability; JSON parsing restores the original text.

Decision shape:

```json
{
  "id": "concise-routine-updates:profile-a",
  "scope": "global:opencode:profile-a",
  "evidence": [{"source": "opencode:profile-a", "session": "s1", "revision": "hash-v1", "locator": "events:20-24"}],
  "status": "proposed",
  "rationale": "User explicitly requested concise routine updates across projects; retain detailed requested deliverables.",
  "target": "verified-native-instruction-surface",
  "before_hash": "sha256-before",
  "after_hash": "sha256-proposed-after",
  "verification": "Pending native loading and representative task."
}
```

Decision statuses are `proposed`, `applied`, `verified`, `rejected`, `deferred`, `reverted`, and `failed`. Use `verified` only when the intended level is stated explicitly in `verification`; static validation alone must not imply observed behavioral success. Keep per-file application journals, assessment-dimension findings, user answers/custom choices, and approval/feedback records in private companion records when needed. The helper decision schema is intentionally small; do not add unsupported fields to it. The same decision ID replaces its current record: submit the complete object on updates and keep decision transition history in the companion journal if recovery requires it. Do not overload the ledger with raw transcripts.

## Review semantics

- Unchanged, fully reviewed revisions can be skipped. Unchanged partial/blocked revisions remain pending and retain their boundary.
- New sessions enter pending even if their dates predate the last run. Newly changed revisions enter pending without erasing prior reviewed coverage.
- `latest_status`, `cursor`, and `note` describe only the current revision. `prior_checkpoint_revision`, `prior_checkpoint_status`, `prior_checkpoint_cursor`, and `prior_checkpoint_note` expose the most recently saved checkpoint from a different revision, including partial or blocked progress; they are null when none exists. These fields do not certify current coverage. `last_reviewed_revision` and `last_reviewed_cursor` continue to identify the most recently saved fully reviewed revision.
- The script rejects a record for a revision that is no longer current. Reinspect the new snapshot instead of asserting coverage for stale data.
- A partial cursor certifies only a contiguous assessed prefix in that exact revision. Reuse across revisions only after verifying the old prefix is identical; then record a new partial boundary explicitly. Whole-session review is a safe fallback when that cannot be established.
- Save findings before marking reviewed. If a crash occurs between those operations, a repeat review should deduplicate by evidence reference/finding ID. An applied change is recorded independently so replay does not duplicate it.
- A blocked read does not count as reviewed. A title-only listing, search hit, truncated export, or summarized memory is partial evidence. If history is retained only partly, record that limitation rather than claiming full-session coverage.
- Several decisions can arise from one reviewed session, and one decision can depend on several sessions. No-change, rejected, and deferred outcomes still count as reviewed if semantic review was complete.

Keep a compact companion run record: run ID/time, requested scope, workflow phase, interaction preference, proposal revision, approved/deferred decision IDs and authorization bounds, target versions, source enumeration completeness, counts/backlog/gaps, state location, reviewed revision boundary, most recent successfully applied change/run, current config hashes, and measurement availability. A single “last enhanced session” may be displayed for convenience but must not replace per-session coverage.

When new content arrives during review, record only the captured revision, refresh discovery, and assess the new revision as needed. For continuously active sessions, checkpoint a clearly identified snapshot and report later content pending. Do not claim a moving session was permanently completed.

## Retention and recovery

Retain minimal evidence and decision provenance, not private source text. Respect deletion/retention requests. Treat disappearance from a listing as unknown until confirmed, not automatic erasure or review completion. Archive old bulky run reports when appropriate, but retain deduplication and last-reviewed state. Do not erase deferred findings to make the backlog look complete.

The SQLite helper uses transactions for its own state. It does not make configuration edits transactional. Back up/copy a database only through a consistent SQLite backup or after all helper processes have exited. Use supported host storage rules for durable copies, and never label an unpersisted checkpoint saved.
