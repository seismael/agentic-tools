# Project Profile: The Agnostic Seam

Everything project-specific lives in one declarative file, `docs/knowledge/profile.yaml`.
The loop engine and its cognition are identical for every repository; the profile tells
them *what to optimize, what to examine, how to run it, and when to stop*. This is what
makes the loop generically and agnostically reusable without touching engine code.

A ready-to-edit copy is at [profile.template.yaml](../assets/templates/profile.template.yaml).
Shape and semantics:

```yaml
schema: loop.profile.v1
project: <name>
goal: "<one-sentence objective the loop optimizes>"
metric: "<the objective scalar/vector and how to read it>"
target: "<the success predicate, if any>"        # optional; enables goal-completion
modes: [eval]                                     # allowed run modes; never a forbidden one
paths:
  loop: .<project>/reports/research/loop         # journal root
  coverage: docs/knowledge/coverage.json
  knowledge: docs/knowledge
boundaries:                                       # the fixed safety envelope
  - "<invariant the loop must never weaken>"
fronts:                                           # coverage surface (see front-taxonomy)
  debug:
    required: true
    sub_axes: [a, b, ...]
  improve:
    required: true
    sub_axes: [entry, exit, risk, cost, ...]
pipeline:                                         # see pipeline-contract
  - {id: evaluate, kind: evaluate, command: "<cli>", artifact: "<path>"}
gates:                                            # see below
  objective: "<how a candidate improves the goal>"
  invariants: "<the test/lint commands that must stay green>"
completion:
  rule: "<goal met | coverage complete | budget>"
  require_coverage: true
  require_delivery: true                          # clean tree, HEAD == origin
```

## Field semantics

- **`goal` / `metric` / `target`** — the loop optimizes `metric`; if `target` is present
  the host may declare `completed` when it is met *and* coverage is complete.
- **`modes`** — the allowed run modes. The engine must refuse anything outside them; a
  profile never lists a forbidden mode.
- **`boundaries`** — the fixed envelope (determinism, safety, correctness). The loop may
  explore any direction *inside* it; it never weakens an item here.
- **`fronts`** — the coverage surface. `required: false` bounds a front out of the
  completion gate with a reason. Sub-axis names are the project's own.
- **`pipeline` / `gates`** — how work is executed and verified (see
  [pipeline-contract.md](pipeline-contract.md)).
- **`completion`** — when the loop may stop: goal met, coverage complete, or budget.

## Rules

- **One seam.** No project detail belongs in the engine. If the engine needs a new knob,
  add it to the profile schema, not to engine code.
- **Honest.** Every command must be real and runnable; never invent a capability (fall
  back to `discover`).
- **Validated.** The knowledge validator checks the profile's shape and that every front
  sub-axis and pipeline id is non-empty and unique.
