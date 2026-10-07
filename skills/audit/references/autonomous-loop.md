# Autonomous Optimization Loop (audit reference)

The autonomous, non-stop optimization loop is defined **once**, in the bundled `loop`
skill (`skills/loop/SKILL.md` and `skills/loop/references/loop-protocol.md`). That
definition is authoritative for every host and domain.

This reference is retained only for the audit-specific obligations the loop inherits:

- **Stage 5 artifacts**: write audit records under the agreed audit directory
  (`docs/audit/` by default) — a `findings/F-XXX.md` record and the `audit.json` index —
  and synchronize the knowledge base (`decisions.md`, `known_defects.md`,
  `data_topology.md`, `capabilities.md`).
- **Pre-evaluation snapshot, dual-gate verification, and knowledge compounding** follow
  the `loop` skill, which in turn uses the `knowledge` skill's capability-discovery and
  compounding protocol.

Do not restate the loop's stages here. Load `skills/loop/SKILL.md` and
`skills/loop/references/loop-protocol.md` for the protocol itself.
