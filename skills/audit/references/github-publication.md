# GitHub publication and recovery

## Access and destination

Use the repository URL already supplied. Resolve owner, repository and actual ref/default branch through available native tools; do not assume `main`. Read project instructions and preserve protected-branch requirements. Prefer an already connected GitHub API, plugin or authorized Git checkout. Browser use is a fallback governed by the host's own rules, not a reason to demand a second login when repository tools suffice.

Record source baseline separately from audit destination. Default to an audit branch such as `audit/<focus-slug>`; use direct publication only when requested or already authorized. Respect an existing chosen branch/directory. Do not create a public repository, fork, issue, PR, review comment or notification as a side effect without the relevant authorization. The audit request can authorize audit commits; repository creation and messages are separate actions.

Apply this publication procedure only when remote delivery is part of the request. For explicitly local files or local commits, verify those deliverables and report remote publication as not requested. When GitHub delivery is required but unavailable, record a delivery blocker while preserving completed review and decisions; do not pretend a local commit satisfies remote delivery.

Check visibility before publishing sensitive material. Audit source code without copying private source, credentials, personal data, private session history or raw logs into public artifacts. For a sensitive security finding, commit sanitized metadata and retain restricted details only through an authorized private surface. Do not make audit files a disclosure channel.

## Consistent commit unit

At each resolved finding, prepare the packet plus its manifest/index updates together. Review the exact diff and require only intended audit files. An initial coverage/evidence checkpoint may be committed with undecided findings, clearly non-executable. Never alter application code, CI or agent configuration merely to publish an audit.

When Git is available:

1. Inspect status, repository identity, destination and latest remote head; keep unrelated dirty files intact. Use an isolated checkout/worktree when appropriate.
2. Validate the prepared artifact set, inspect the diff and stage explicit audit paths rather than `git add .`.
3. Commit against the current destination parent and push without force. On concurrent updates, fetch and reconcile the audit-only change; reassess relevant source drift and repeat validation. Do not erase another author's work. Bound retries and preserve a checkpoint if conflicts need a decision.
4. Verify the remote branch contains the resulting commit and read back the changed files or compare their blobs/hashes.

When only GitHub APIs/tools are available:

1. Read the destination's current commit and tree through supported tools.
2. If exposed, construct a tree **based on the existing tree**, changing only intended audit entries; create one commit with the observed destination head as parent, then update the branch without force. Never create a replacement root tree from just audit files, which would drop unrelated project paths.
3. Recheck the branch and changed contents. A created blob/tree/commit not attached to the intended branch is not a published result. If a concurrent head moved, rebuild on the new parent after comparison rather than forcing the ref.
4. If only per-file writes are available, do not pretend they are transactional. Prefer a dedicated branch, write the packets first and index/manifest last, then read back the complete bundle. Record partial publication and retain non-ready state until the set is coherent. Use a supported atomic alternative when available.

Git operations can run project CI. Do not enable new workflows or bypass required gates. Report actual relevant remote checks separately from local artifact validation; absence of CI or inability to query it is not a passing result.

## Failures and receipts

If read access is missing, explain the repository/access blocker and request the smallest needed input or access. If write access alone is missing, continue the authorized audit and prepare concrete files; distinguish prepared work from publication and provide exact pending paths. Preserve user dispositions through retries.

Report commit URL, destination branch and verified changed paths. Store a publication receipt outside the commit being described, or use the tool response in chat; a commit cannot reliably embed its own final SHA. Do not fill a manifest with a fake self-referential commit. On interruption, inspect the remote first to distinguish published work from an orphaned commit or incomplete set before retrying.

Retain the frozen code baseline despite later audit-only commits. If product code changes during the review, compare affected evidence/dependencies and reconcile; do not silently stamp the latest SHA on old findings. A materially new audit can use a separate directory and baseline, linking superseded findings without deleting history.

Read remote source files at the pinned commit rather than a moving branch during a batch. Check pagination/truncation flags in tree/search results; incomplete listings keep coverage partial. A working-tree file with uncommitted edits must not be described as the pinned commit's contents. Source snapshot integrity is independent of whether publication succeeds.

## Official mechanisms

These sources explain the generic format and GitHub object/ref mechanics. Verify the live host's exposed operations before use; availability and authentication differ.

- [Agent Skills format and progressive loading](https://agentskills.io/specification)
- [GitHub Git references and non-forced updates](https://docs.github.com/en/rest/git/refs)
- [GitHub trees and base-tree construction](https://docs.github.com/en/rest/git/trees)
