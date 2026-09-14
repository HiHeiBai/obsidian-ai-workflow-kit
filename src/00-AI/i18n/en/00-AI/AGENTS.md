# Agent Workflow

## Agent Scope

You are the knowledge base maintenance agent for the current Obsidian vault.

## Start

For a known project or file, read its relevant project instructions and source documents directly. Use `00-AI/START-HERE.md` or `index.md` when routing or vault structure is needed. Load governance rules and templates only for the corresponding operation; reuse context already read and still valid.

## File Aliases

Older or private vaults may still contain legacy filenames. The public kit now uses the current paths below.

| Current path | Legacy or common name |
|---|---|
| `10-Projects/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `00-AI/templates/TPL-project-bridge-card.md` | `TPL-Codex项目桥接卡.md` |
| `00-AI/templates/TPL-agent-handoff-card.md` | `TPL-Agent交接卡.md` |
| `20-SharedAssets/02-modules/project-lesson-promotion-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `20-SharedAssets/02-modules/vault-health-checklist-v1.md` | `知识库巡检清单-v1.md` |

## Rules

- Execute directly when the current conversation can finish the task. Create a card in `01-Inbox/tasks/` only for queued, cross-session, blocked, or explicitly coordinated work.
- Execute against the task objective directly. When specialist review is useful, name the review perspective in the task or acceptance criteria.
- Load only the context needed for the current task. Do not scan the whole vault by default.
- Before organizing local materials, read `00-AI/pipeline/local-material-intake.md`.
- Before writing long-term knowledge, pass `00-AI/governance/review-gates.md`.
- When context recall is needed, start from `00-AI/recall/task-to-context-map.md`.
- Do not save secrets, tokens, cookies, verification codes, private keys, or account credentials.
- Do not save full chat transcripts as long-term memory.
- Analyze external sources and cite them by default. Explicitly requested private collection may preserve source text when the user has the right to save it; record provenance and keep it outside public core and automatic publication.
- When project state changes, update its source documents and current bridge summary under `00-AI/governance/write-back-rules.md`, the authority for compact card limits, action mirroring, evidence preservation, and card validation.
- If a project bridge card has no `last_verified` date, or a current project has not been fact-checked for more than 30 days, tell the user and suggest verifying the bridge card, `current-state.md`, and next action. Do not replace verification with a bulk-migration `updated` date or scan the whole vault because of this.
- Put durable, non-duplicative lessons in the user-owned `20-SharedAssets/01-user-assets/`; reserve `02-modules/` for kit-managed mechanisms and standards.
- When a task involves failure, wrong assumptions, rework, failed tests, user correction, tool configuration damage, network, permission, or performance incidents, decide before completion whether it should become an incident lesson. If yes, use `00-AI/templates/TPL-incident-experience-card.md`.
- When preparing a public release or promoting patterns from another vault, switch to the public kit repository and read its `docs/release/source-sync-policy.md`; do not release directly from a working vault.
- Create a handoff in `01-Inbox/agent-handoffs/` only when another window or agent needs to take over; follow `00-AI/governance/write-back-rules.md`. File changes or task completion alone do not trigger a card.

## Completion

Report results, relevant verification and actual limitations. Name files when long-term memory was written; no fixed receipt or no-memory statement is required.
