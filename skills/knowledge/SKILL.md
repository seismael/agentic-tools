---
name: knowledge
description: Maintain and query an indexed, token-efficient, Obsidian-compatible local Markdown wiki for any project. Stores intent, architectural topology, data/log paths, invariants, and decisions to eliminate redundant exploration and context drift across agent sessions.
---

# Knowledge Base (Local Markdown Wiki)

Maintain a living, token-efficient, Obsidian-compatible Map of Content (MOC) wiki for any repository. Enable autonomous agents to share verified structural facts, runtime evidence locations, domain invariants, accepted decisions, and executable capabilities without burning tokens on redundant exploration.

## Operating Contract

- **Zero-Daemon, Plaintext Markdown**: All knowledge is stored as human-readable, Git-versioned GitHub Flavored Markdown (GFM). No external databases, vector services, background daemons, or proprietary formats.
- **Obsidian & Dual-Syntax Compatibility**: Every internal reference uses dual-syntax links (standard markdown link alongside Obsidian `[[topic]]` wikilink) for seamless visual navigation in Obsidian and standard markdown viewers.
- **Strict Token-Economy & Leaf Bounds**:
  - The root Map of Content (`index.md`) is hard-capped at $\le 2\text{ KB}$ (~400 tokens).
  - Every individual topic leaf is hard-capped at $\le 3\text{ KB}$ (~600 tokens).
  - **Leaf-Only Traversal**: Agents MUST NEVER stream the full wiki into context. An agent loads `index.md` first, identifies the single relevant leaf, and fetches only that file.
- **Zero Conversational Chatter**: Wiki updates are strictly factual, dense, and structured (tables, bullet points, exact file paths). Never append conversational filler or narrative essays.
- **Path Isolation & Discovery**: Defaults to `<project_root>/docs/knowledge/` (version-controlled) or `.<project>/knowledge/` (runtime local). Respects project repository root immutability rules.

See [wiki protocol](references/wiki-protocol.md), [schema and structure](references/schema-and-structure.md), and [capability discovery](references/capability-discovery.md) for detailed contracts.

---

## 1. Core Wiki Structure

Every project wiki adheres to the standard 7-leaf Map of Content layout:

```
<knowledge_dir>/
├── index.md             # Root Map of Content (MOC): categorized links & 1-line briefs
├── architecture.md      # Tech stack, package manifests, runtime entry points, subsystems
├── data_topology.md     # Verified paths for configs, data lakes, logs, diagnostic reports
├── invariants.md        # Non-negotiable domain rules, safety limits, architectural axioms
├── decisions.md         # Chronological log of accepted user architectural decisions
├── known_defects.md     # Verified root-cause bugs, pitfalls, and traps to avoid
└── capabilities.md      # Executable-surface registry: CLI, engines, scripts, data, lanes
```

---

## 2. Cross-Skill Lifecycle Protocol

All agent skills (`audit`, `characterize`, `enhance`, `code`, `test`) interact with the knowledge base via a 2-step protocol:

### Step 1: Read-on-Boot (Targeted Orientation)
1. Check if `<knowledge_dir>/index.md` exists.
2. If present, load **only** `index.md` (< 400 tokens).
3. Identify the specific domain needed for the current task:
   - To locate configs or logs: read `data_topology.md`.
   - To check safety boundaries: read `invariants.md`.
   - To understand system layout: read `architecture.md`.
   - To avoid known bugs: read `known_defects.md`.
   - To find tools/commands/capabilities: read `capabilities.md`.
4. Proceed with task execution using verified paths and constraints, eliminating exploration scans (`ls`, `find`, `grep`).

### Step 2: Write-on-Completion (Knowledge Compounding)
When a skill finishes an investigation, execution, or decision cycle, it persists new verified facts:
- **Discovered Data/Log Path**: Append an exact row to `data_topology.md`.
- **Accepted Architectural Decision**: Append a dated record to `decisions.md` (including empirical metric delta and any realigned test fixtures).
- **Confirmed Root-Cause Defect**: Append a structured bug card to `known_defects.md` (detailing failure mechanics and anti-patterns to avoid).
- **New System Invariant**: Append the rule to `invariants.md`.
- **Discovered/Added Capability**: Append the surface to `capabilities.md` (run capability discovery when it predates a manifest/entry-point change).

---

## 3. Operations & Maintenance

### Bootstrapping a New Project (`init`)
1. Determine the knowledge directory (`docs/knowledge/` or `.<project>/knowledge/`).
2. Copy standard templates from `assets/templates/` into the target directory.
3. Perform an initial autonomous reconnaissance scan (manifests, source roots, docs) to populate initial high-level facts.
4. Run [capability discovery](references/capability-discovery.md) to populate `capabilities.md`.
5. Run `validate_knowledge.py` to certify structural integrity.

### Compacting Oversized Leaves (`prune`)
If any topic leaf grows beyond **$3\text{ KB}$**:
1. Remove stale or superseded observations.
2. Group related items into a sub-leaf (e.g., `data_topology_archive.md` or `subsystems/<subsystem>.md`).
3. Update `index.md` to reference the sub-leaf.

---

## 4. Verification

Run the bundled read-only validator from any directory:

```sh
python <skill_dir>/scripts/validate_knowledge.py <project_root>/docs/knowledge
```

The validator verifies:
- `index.md` exists and contains links to all existing markdown leaves.
- All internal markdown links and `[[wikilinks]]` resolve to real files.
- No page exceeds the $3\text{ KB}$ ceiling.
- Date and status formatting across records are compliant.
