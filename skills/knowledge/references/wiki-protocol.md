# Wiki Protocol: Map of Content (MOC) Architecture

## 1. Principles

1. **Token Frugality**: Plaintext markdown optimized for minimum prompt token footprint. Every token must convey a dense structural fact.
2. **Obsidian Compatibility**: Fully viewable and navigable inside Obsidian, VS Code Markdown Preview, or GitHub web interface.
3. **Decentralized Multi-Agent State**: Acts as the shared long-term memory for any collection of specialized autonomous agents (planners, auditors, refactorers, test runners).
4. **Deterministic Fact Compounding**: Knowledge learned in session $N$ directly informs session $N+1$, preventing repetitive regression loops.

---

## 2. File Naming and Linking Conventions

- **Filenames**: Lowercase with underscores (e.g., `data_topology.md`, `architecture.md`).
- **Dual-Syntax Links**: Every cross-reference should provide standard relative markdown syntax alongside Obsidian wikilinks:
  `[Architecture](architecture.md) / [[architecture]]`
- **Section Headers**: Standard markdown `#`, `##`, `###` headings to allow precise sub-section referencing.

---

## 3. Strict Byte Bounds & Splitting Rules

| Leaf Name | Target Token Count | Hard Byte Ceiling | Splitting Trigger |
| :--- | :--- | :--- | :--- |
| `index.md` | $\le 200\text{--}400$ tokens | **$2,048\text{ bytes}$** | $> 25$ top-level topic links |
| `architecture.md` | $\le 400\text{--}600$ tokens | **$3,072\text{ bytes}$** | $> 8$ primary subsystems |
| `data_topology.md` | $\le 400\text{--}600$ tokens | **$3,072\text{ bytes}$** | $> 20$ paths/directories |
| `invariants.md` | $\le 400\text{--}600$ tokens | **$3,072\text{ bytes}$** | $> 15$ mandatory rules |
| `decisions.md` | $\le 400\text{--}600$ tokens | **$3,072\text{ bytes}$** | $> 15$ logged decisions |
| `known_defects.md` | $\le 400\text{--}600$ tokens | **$3,072\text{ bytes}$** | $> 10$ documented bugs |

### Sub-leaf Splitting
When any leaf exceeds its byte ceiling:
1. Create a sub-folder corresponding to the topic (e.g., `subsystems/` or `archives/`).
2. Move granular leaf details into the sub-folder.
3. Retain a condensed summary table in the parent leaf linking to the sub-leaves.
4. Update `index.md` to reflect the expanded topology.

---

## 4. Interaction Rules for External Skills

- **Read Policy**:
  - Never load `*` or scan all markdown files.
  - Read `index.md` first.
  - Evaluate the user prompt to determine which 1 or 2 leaves are needed.
  - Read only the selected leaves.
- **Write Policy**:
  - Updates must be atomic.
  - Never rewrite a leaf from scratch unless performing a planned reorganization.
  - Append rows to existing markdown tables or list items to sections.
  - Validate formatting immediately using `validate_knowledge.py`.
