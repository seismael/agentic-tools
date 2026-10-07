# Capability Discovery: Inventorying a Project's Executable Surface

Deterministic protocol that discovers what a project can *do* — its command-line
surfaces, engines/subsystems, scripts/tools, data sources, and verification lanes — and
records them in the knowledge base so autonomous loops select tools deliberately instead
of rediscovering them (or missing them) every session.

## When to run

- On knowledge-base `init`, after topology and invariants are seeded.
- On boot, when `capabilities.md` is absent, or its `Last Updated` predates a manifest,
  entry-point, or top-level surface change.
- When the loop cannot locate the tool needed for the next move (the `loop` skill's tool
  admission test requires proving existing tools cannot answer the question first).

## Protocol (deterministic, read-only, token-bounded)

1. **Boot** — read `docs/knowledge/index.md`; load `capabilities.md` if present and
   fresh. Stop if it already answers the question.
2. **Manifests and entry points** — read the build/manifest files to find declared
   commands, console entry points, binaries, and build/lint/test scripts. Cross-reference
   `data_topology.md` and `architecture.md`.
3. **CLI surface** — for each primary entry point, run `<cli> --help`, then
   `<cli> <group> --help` for each top-level group (bounded depth; prefer introspection
   over reading source). Record every command with a one-line purpose and a minimal
   example.
4. **Engines and subsystems** — map top-level source roots to responsibilities and their
   public entry points; record reusable libraries (engines, optimizers, clients).
5. **Scripts and task runners** — enumerate declared script directories and task runners;
   record purpose and invocation.
6. **Data sources and artifacts** — record input data roots, formats, and regenerable
   artifact locations (cross-link `data_topology.md`; do not duplicate it).
7. **Verification lanes** — record the exact test/lint/type/format commands and the scope
   each covers.
8. **Record** — write or update `capabilities.md` (see schema), add it to `index.md`, and
   run the bundled validator.
9. **Refresh** — re-run when a manifest, entry point, or top-level surface changes; update
   `Last Updated`.

## Rules

- **Read-only**: never execute mutating commands during discovery; `--help`/`--version`
  only.
- **Deterministic ordering**: sort capabilities by name; stable rows so diffs are
  meaningful.
- **Bounded output**: cap every section and the whole leaf (see the wiki byte ceilings);
  split into `capabilities/<topic>.md` sub-leaves when it overflows.
- **No raw dumps**: no logs, help-text dumps, or directory listings — one line per
  capability.
- **Honest**: mark `UNKNOWN` where introspection is unavailable; never invent a
  capability.
- **Project-local**: record only this project's surfaces; never encode another project's.
