# Coverage Ledger: Proving Nothing Was Skipped

The ledger is the loop's breadth guarantee. It records, for every front and sub-axis
named in the [project profile](project-profile.md), the strongest status reached and the
evidence for it — so "we explored everything" is *verified*, not asserted, and an
abandoned direction is visible instead of silently dropped.

## Location and format

- Declared by the profile (`paths.coverage`); default `docs/knowledge/coverage.json`.
- One machine-readable JSON object; a human leaf may mirror it in the wiki. Keep the
  JSON authoritative.

```json
{
  "schema": "loop.coverage.v1",
  "loop_id": "<id>",
  "updated_at": "<ISO-8601>",
  "complete": false,
  "open_defect": false,
  "counts": {"verified_sound": 0, "covered_exhausted": 0, "open": 0},
  "fronts": {
    "debug": {
      "status": "IN_PROGRESS",
      "sub_axes": {
        "flow_event_ordering": {"status": "VERIFIED-SOUND", "evidence": "<artifact/command>"},
        "cost_fee_path": {"status": "DEFECT-FOUND", "evidence": "<issue id + repro>"}
      }
    }
  }
}
```

## Statuses (per sub-axis)

| Status | Meaning |
| :--- | :--- |
| `UNEXPLORED` | Not yet examined. Blocks completion. |
| `EXPLORING` | Examination in progress. |
| `COVERED-SOUND` | Examined; correct/sound as-is; evidence recorded. |
| `COVERED-EXHAUSTED` | Examined; the candidate frontier for this axis is empirically exhausted with evidence. |
| `DEFECT-OPEN` | A defect was found and is not yet resolved. Blocks completion. |
| `BLOCKED-EXTERNAL` | Cannot proceed for an external reason; a non-empty `reason` is required. |

A front's status is derived from its sub-axes (worst-wins), and may also carry
front-level evidence.

## Completion rule (generic)

The ledger is **complete** iff, for every required front/sub-axis, the status is a
terminal one — `COVERED-SOUND`, `COVERED-EXHAUSTED`, or `BLOCKED-EXTERNAL` with a
reason — and no `DEFECT-OPEN` or `UNEXPLORED` remains. A profile may declare a subset as
`required: false` (bounded out); those do not block. This mirrors, and generalizes, a
project's own soundness sweep: the sweep is simply the `debug` front's sub-axes.

## Why it matters

- Prevents "cost dominance / no edge" conclusions drawn while the machinery is
  unexamined.
- Makes the exploration surface auditable across sessions and agents.
- Lets a new session resume exactly where coverage stopped.
