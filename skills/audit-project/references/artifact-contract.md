# Audit artifact contract

Use this contract when creating or checking the handoff. Version 1 is a small
manifest plus Markdown packets, independent of the programming language or agent.

- [Files](#files)
- [Manifest](#manifest)
- [State constraints](#state-constraints)
- [Packet headings](#packet-headings)
- [Validation and its limits](#validation-and-its-limits)

## Files

```text
docs/audit/
  audit.json
  README.md
  CONTEXT.md
  findings/F-001.md
```

The audit root may be another agreed repository directory. `README.md` is the
queue and local-agent entry point; `CONTEXT.md` records project goals, constraints,
baseline, architecture, evidence limitations, and coverage interpretation.
`audit.json` is the authoritative index of finding identities, states, and
dependencies. Keep its summaries consistent with packets. Do not infer permission
to implement from the existence of a plan or from `accepted`/`ready` status.

## Manifest

| Field | Required value |
|---|---|
| `version` | Integer `1` |
| `repository` | HTTPS repository URL, public GitHub or enterprise, without credentials/query/fragment |
| `baseline_commit` | Full 40-character Git commit SHA actually reviewed |
| `focus` | Nonempty user focus and scope description |
| `coverage` | Nonempty list of coverage objects below |
| `findings` | List of finding objects; empty is valid when no findings are established |

Freeze the baseline for this audit. New source revisions require impact review
before applying a packet; record an explicit rebasing/revalidation decision or
create a separate audit. Publication receipts belong in the conversation or
external receipt: a manifest cannot contain the hash of its own committing change.

Every coverage object has `id`, `domain`, `status`, `basis`, and `evidence`.
IDs are unique. Status is `reviewed`, `partial`, `unreviewed`, `not_applicable`, or
`blocked`. `basis` explains what was actually inspected or why it was not.
Partial, unreviewed, and blocked areas require a nonempty `next_step`.
Reviewed areas require at least one evidence entry; applicability decisions need
a reason, not an invented source. Do not mark an entire area reviewed merely
because a representative file was read.

Every finding object has these fields:

| Field | Values and meaning |
|---|---|
| `id` | Stable `F-001` format; three or more digits; never recycle IDs |
| `title` | Specific, nonempty problem or opportunity |
| `kind` | `defect`, `risk`, `opportunity`, `alignment`, `question` |
| `severity` | Consequence: `critical`, `high`, `medium`, `low`, `info` |
| `priority` | Agreed scheduling: `P0`, `P1`, `P2`, `P3`; distinct from consequence |
| `confidence` | `confirmed`, `supported`, `hypothesis` |
| `status` | User disposition: `undecided`, `accepted`, `deferred`, `rejected`, `superseded` |
| `decision` | Object with strings `by`, `summary`, `reference`; references an actual decision |
| `plan_status` | `none`, `draft`, `ready`, `blocked`, `done` |
| `depends_on` | List of prerequisite finding IDs; no duplicates, unknown IDs, or cycles |
| `path` | Unique Markdown path under `findings/`, relative to audit root |
| `evidence` | List of evidence entries below; source evidence required for ready/done |

Additional domain-specific fields are permitted. Put value, reach, recurrence,
effort, change risk, and uncertainty in the packet, adding manifest fields only
when they help scheduling. Avoid unsupported numerical scoring.

Evidence entries contain `kind` (`source`, `test`, `observation`, `external`),
`reference`, and `summary`, all nonempty strings. A source reference is a precise
repository path plus symbol or line range, interpreted at `baseline_commit`, or a
permalink containing that commit. A test reference points to the command/result
record; an external reference points to the primary source and relevant section.
Explain what each item supports. The validator checks their presence and shape,
not whether the referenced evidence is true, current, sufficient, or accessible.

## State constraints

- `undecided`: decision fields may be empty; plan may be none/draft/blocked.
  Drafting a recommended option does not make it accepted.
- Other dispositions require nonempty decision attribution, summary, and reference.
  Only record a user decision or explicit delegated decision rule actually given.
- `deferred`: require `revisit_trigger`; allow none/draft/blocked, never ready/done.
- `rejected`: plan must be none; retain reason and evidence for traceability.
- `superseded`: plan must be none; require `superseded_by` naming another finding.
  Supersession links must also be acyclic.
- `ready` and `done`: require accepted disposition, confirmed/supported confidence,
  source evidence, and complete packet sections without unresolved placeholders.
  Every dependency must itself be accepted with a ready or done plan.
- `done` additionally requires all dependencies to be done, and actual implementation and verification evidence
  recorded by the executing agent. Structural validation cannot establish this.

Acceptance authorizes the agreed planning disposition. Execution requires separate
user authorization in the actual implementing session; existing applicable
authorization should be respected, not repeatedly requested.

## Packet headings

Start each packet with a title such as `# F-001: Preserve ordered retries`, matching
its manifest ID. Every packet includes these exact level-two headings, even when a rejected or
deferred packet needs only a short explanation:

```markdown
## Finding
## Evidence
## Decision
## Implementation plan
## Validation
## Risks and rollback
```

For ready/done packets, each section must contain meaningful content. Resolve
`TODO`, `TBD`, uppercase `REPLACE`/`REPLACE_*`, `{{template slots}}`, and `<insert ...>` markers.
Ready/done manifest entries are also checked for these markers. The check is
deliberately conservative and may flag quoted source containing
these tokens; cite the source location instead of copying an ambiguous marker.
Keep alternatives, rejected/deferred reasons, and separate execution authorization
in Decision. Put ordered tasks, exact edit targets, contracts/invariants,
dependencies, acceptance checks, and stop conditions in Implementation plan.
For a field that truly does not apply, explain why; do not pad small changes.

## Validation and its limits

Run `python /path/to/audit-project/scripts/validate_audit.py docs/audit`.
Exit 0 means structurally valid; exit 1 means invalid. Output is bounded to forty
diagnostics plus an omitted count. Input files must be UTF-8 and at most 2 MiB each.
Paths use forward slashes, stay within the audit root after symlink resolution,
and contain no traversal or absolute components. Duplicate IDs, packet paths
(case-insensitive), JSON keys, malformed enums, and graph cycles fail validation.

The helper reads only, does not run repository commands, fetch URLs, edit files,
validate Git objects, approve decisions, or verify semantics. A valid bundle is
not proof of audit completeness, source correctness, implementation safety, or
user authorization. Review those separately. Validate a stable local checkout;
this checker is not a sandbox for a concurrently malicious filesystem.
