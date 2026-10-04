# Contributing

Keep each skill self-contained under `skills/<name>/`. Repository documentation, release tooling, and CI stay outside the installed skill directory. Avoid adding mandatory dependencies or an orchestration service for work a native agent can already perform.

Characterize establishes setup from user goals and current capabilities; Enhance improves it from actual session evidence. Keep each independently usable and exchange compact private records only when appropriate. The shared installer must continue to accept either complete skill bundle.

For changes to either skill:

1. Describe the observed failure or user need and the smallest supported change.
2. Explain the expected input/output, total-cost, latency, and maintenance effect. Preserve required correctness and reliability.
3. Keep global, shared-project, private-project, role, and task scope distinct; respect native permissions and explicit authorization.
4. Use current official documentation for host-specific behavior and update the checked date. Label runtime support according to evidence.
5. Run the release checker and relevant tests from [Validation](docs/VALIDATION.md), including Characterize's change-bundle suite for file-change/recovery behavior. Add a meaningful regression for a deterministic bug; do not create redundant test suites for wording changes.
6. Use synthetic or redacted fixtures and keep all runtime state out of the repository.

Do not promise universal host compatibility, exact savings, or runtime enforcement from instructions alone. Avoid copying host-specific configuration keys into the generic skill. Prefer on-demand references over expanding always-loaded descriptions or instructions.

If a host/version changes discovery or metadata behavior, include its exact version and official source, plus a minimal reproducible installation example. Separate documented support from observed live execution in the compatibility table.
