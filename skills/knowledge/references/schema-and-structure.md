# Schema and Content Structure of Core Leaves

## 1. `index.md` (Map of Content)
Must contain:
- `# Project Knowledge Base`
- A 2-line high-level project summary (problem domain, primary language/runtime).
- A markdown table listing each leaf:
  - `Topic`: Relative link to target markdown leaf alongside Obsidian wikilink (e.g. `[[topic_leaf]]`).
  - `Focus`: 1-line description of what facts live here.
  - `Last Updated`: ISO date (`YYYY-MM-DD`).

---

## 2. `architecture.md`
Must contain:
- `# Architecture & System Topology`
- **Tech Stack & Manifests**: Primary languages, build files, runtime versions.
- **Entry Points**: Main executables, CLI commands, web service entry points.
- **Subsystem Boundaries**: Table of major components, their directory roots, and their responsibilities.

---

## 3. `data_topology.md`
Must contain:
- `# Data Topology & File Locations`
- **Configuration Paths**: Exact files configuring environments, runners, and risk gates.
- **Runtime State & Artifacts**: Exact directories where runs, logs, telemetry, and caches are persisted.
- **Historical / Source Data**: Data lakes, mock fixtures, external database targets.
- Table format:
  `| Category | Path | Lifecycle / Mutability | Notes |`

---

## 4. `invariants.md`
Must contain:
- `# System Invariants & Non-Negotiable Rules`
- **Axioms**: Core architectural rules that cannot be violated (e.g., single-writer mutation, determinism).
- **Safety Boundaries**: Pre-execution gates, budget ceilings, circuit breakers.
- **Testing & Isolation Rules**: Directory isolation, temporary file hygiene, path immutability.

---

## 5. `decisions.md`
Must contain:
- `# Architectural Decision Log`
- Chronological list or table of user-approved architectural decisions:
  `| Decision ID | Date | Topic | Option Selected | Rationale / Reference |`

---

## 6. `known_defects.md`
Must contain:
- `# Known Defects & Architectural Anti-Patterns`
- Documented traps, confirmed defects, and anti-patterns:
  - `Defect ID / Title`
  - `Root Cause`: Dense causal summary.
  - `Symptom`: What breaks if this occurs.
  - `Resolution / Rule`: What pattern must be used instead.
