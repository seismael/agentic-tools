# Adaptive interview

## Question protocol

Select the next question by its effect on a concrete design decision. Ask goals before implementation details. Interpret free text fully; combinations and entirely new domains are valid.

Reuse available answers before asking. Each consequential question has one focused prompt in the user's language, preferably three relevant alternatives with a short practical consequence, and a custom answer. Use two alternatives when a third would be artificial. Recommend an option only when evidence supports it. When a widget adds custom automatically, do not duplicate it; otherwise include a numbered custom choice. Allow a number or description. Ask independent dimensions separately instead of creating an artificial either/or choice. Approval is a separate plain question, not a preference option.

Example when inspection and the user's request do not establish a target:

Which local agent should we characterize first?
1. OpenCode — configurable profiles across supported providers.
2. Claude Code — specialize its local workflow and available models.
3. Gemini CLI — specialize its local workflow and available models.
4. Custom — another tool, an editor integration, or several tools; describe it.

When the target is known, resolve the highest-impact remaining design choice. Do not ask for a domain label if supplied tasks already establish the relevant work. Do not ask a question merely to demonstrate this format.

## Coverage ledger

Each dimension ends as `answered`, `observed`, `inferred-with-confidence`, `not-applicable`, or `explicitly-deferred`. Consequential inferences about permissions, spending, or audience need confirmation. Do not ask every row verbatim.

| Dimension | Establish | Example branching |
| --- | --- | --- |
| Target/scope | Product, interface, project/personal/team scope | One target; shared intent across targets; separate profiles |
| Domain/role | Profession, specialization, collaborators | Engineer; creator; researcher; custom |
| Recurring work | Jobs, inputs, outputs, representative examples | Create; improve; investigate |
| Success/failure | Good result and expensive failure | Correctness; audience fit; reproducibility |
| Environment | OS, shell, layout, installed tools, constraints | Local files; connected apps; constrained workspace |
| Standards | Domain practices that affect decisions | Existing standards; propose standards; hybrid |
| Interaction | Questions, explanations, progress, expertise | Consultative; concise autonomous; teaching |
| Workflow | Stages, shortcuts, review points, iteration | Discuss then execute; execute a brief; collaborative stages |
| Authority | Design, implementation, publication, spending | Per-deliverable review; approved scope; custom boundaries |
| Models | Existing connections, available IDs, account route | Current connection; several existing routes; inspect access |
| Resources | Quality floor, latency, quota, API budget | Quality within cap; balanced throughput; low latency |
| Data/tools | Required sources/MCPs, sensitive material, offline needs | Selected sources; workspace scope; custom scope |
| Actions | Edits, shell, network, external writes, deletion | Read/advise; approved local work; scoped external workflow |
| Context | Durable conventions, knowledge, session handoffs | Project; domain; client-specific sources |
| Output | Format, language, tone, audience, citations, paths | Artifacts; concise decisions; structured technical output |
| Verification | Acceptance checks, reviewer, example tasks | Existing checks; tailored rubric; both |
| Maintenance | Ownership, portability, updates, drift, team sharing | On demand; review updates; requested scheduled checks |

Inspect before asking users to transcribe technical facts. Request representative tasks using the same three-plus-custom format: alternatives can be task archetypes and custom can accept an actual example. Use spontaneously supplied examples directly.

## Domain branches

These are probes, not preset identities. Dig into subdomains when answers change the design. Do not fabricate domain requirements.

| Domain | Follow-up decisions | Candidate stages | Acceptance evidence |
| --- | --- | --- | --- |
| Software engineering | Stack, architecture, greenfield/maintenance, tests, release authority, failure impact | Diagnose, Architect, Plan, Build, Validate; optional Quick | Relevant tests, reviewable changes, reproduction, maintained behavior |
| Content/editorial | Audience, channel, voice samples, sources, originality, brand/client boundaries, publishing | Brief, Research, Outline, Draft, Edit, Verify, Deliver | Brief coverage, factual checks, voice/format rubric, editorial approval |
| Research/analysis | Question type, evidence, provenance, uncertainty, reproducibility, decision | Frame, Collect, Analyze, Challenge, Report | Traceable sources, calculations, uncertainty |
| Operations/support | Systems, incidents, runbooks, change windows, customer data, escalation | Triage, Diagnose, Propose, Execute, Verify | Scoped commands, recovery checks, incident notes |
| Design/product | Audience, constraints, design system, assets, usability, handoff | Discover, Explore, Design, Critique, Test, Handoff | User needs, consistency, usability, usable artifacts |
| Custom/mixed | Actual jobs, unique artifacts, standards, exceptions | Derive verbs from the user's process | User-defined observable criteria |

Do not install all candidate stages automatically. A typo fix, headline variation, or simple lookup can use a shortcut with relevant checks. For mixed work, avoid applying one client's voice or permissions to another profile.

## Depth and stopping

Work in short rounds. Once a coherent design emerges, summarize only material decisions and resolve remaining tradeoffs. Do not read every reference, ask every row, or create a profile for every listed domain. Resolve contradictions such as offline-only data with remote-only models; scoped autonomy with publication review is a valid boundary, not a contradiction.

Stop when consequential choices are settled and the workflow has observable success criteria. If the user requests defaults, propose them with reasons and proceed under actual authorization. Keep analytical design open to feedback until approval to advance; after approval, do not repeatedly gate implementation substeps.
