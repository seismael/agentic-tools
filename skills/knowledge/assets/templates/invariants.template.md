# System Invariants & Non-Negotiable Rules

[[index|← Back to MOC]]

## 1. Architectural Axioms
- **[INV-01] Determinism**: Systems must produce identical state transitions given identical inputs.
- **[INV-02] Time Isolation**: Core logic must not consult system wall-clocks directly; state advances monotonically upon discrete events.
- **[INV-03] Single-Writer Mutability**: State mutation is strictly restricted to designated single-threaded sequencers.

## 2. Mandatory Risk & Safety Bounds
- **Pre-Execution Gating**: All actions must be validated by pre-flight checks before dispatching to execution boundaries.
- **Circuit Breakers**: Immediate halt on threshold breach or balance divergence.

## 3. Directory & Path Isolation
- **Root Immutability**: No ad-hoc scripts, test dumps, or scratch files may be created in the repository root.
- **Test Isolation**: All test artifacts must resolve through isolated temporary directories (`tmp_path`).
