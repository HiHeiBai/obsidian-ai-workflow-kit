---
type: entry
status: active
aliases: ["Start Here"]
language: en
---

# START HERE

Language: English

> Use this entry when the task needs vault routing. It tells the agent what to read, where to write, and what not to do.

## Startup Prompt

```text
You are the knowledge base maintenance agent. Read 00-AI/START-HERE.md in the current vault and follow its startup workflow.
```

If the agent did not start from the vault root, include the vault path:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read 00-AI/START-HERE.md in that directory, then follow its startup workflow.
```

## Start Working

Identify the objective, existing authorization and checkable outcome, then proceed. Ask only for material missing information. No fixed startup receipt is required. Known projects or files can be entered directly without traversing every route here.

## Startup Steps

> Execute directly by default. Do not create a task card when the current conversation can finish the work. Use `01-Inbox/tasks/` only for queued, cross-session, externally blocked, or explicitly coordinated work.

### 1. Identify The Task Type

| Task type | Read first |
|---|---|
| Document organization and classification suggestions | `index.md`, `00-AI/pipeline/README.md`, `00-AI/pipeline/local-material-intake.md` |
| Local material intake | `00-AI/pipeline/README.md`, `00-AI/pipeline/local-material-intake.md` |
| Project handoff | `10-Projects/<project>/BRIDGE-*.md` |
| External source processing | `00-AI/pipeline/README.md`, `00-AI/templates/TPL-source-analysis-card.md` |
| Lesson capture | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`, `00-AI/templates/TPL-question-knowledge-experience-asset-card.md` |
| Incident review | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`, `00-AI/templates/TPL-incident-experience-card.md` |
| Vault maintenance | `00-AI/governance/maintenance-loop.md`, `20-SharedAssets/02-modules/vault-health-checklist-v1.md` |
| Handoff writing | `00-AI/templates/TPL-agent-handoff-card.md` |
| Resume a local task | `01-Inbox/tasks/<task>.md` and the related project bridge card |

### 2. Load Only Necessary Context

- Read this entry or `index.md` when routing is needed. For known targets, enter the relevant project or file directly and reuse valid context.
- Read `00-AI/governance/README.md` only when governance rules are needed.
- Read `00-AI/recall/task-to-context-map.md` only when recall rules are needed.
- For project work, read only the relevant project bridge card.
- Do not scan the whole vault by default.
- When the user asks to organize documents, classify existing notes, or suggest where content should go, first inspect the user-provided scope. If no scope is provided, inspect only the vault's top-level folders, READMEs, index, and a small filename sample. Return organization suggestions directly. Do not create a mapping, recall rule, or new folder by default.

### Document Organization And Classification Suggestions

When asked for suggestions, return them first. When asked to organize or modify files, complete the authorized work. This is an optional response example:

```text
Current content read: <what the material appears to be>
Suggested classification:
- <material/folder> -> <suggested location>, reason: <one sentence>
Suggested first actions:
1. <smallest concrete action>
Not handling yet: <unclear items or items needing user confirmation>
```

### 3. Write Back To The Right Place

| Content | Write to |
|---|---|
| Temporary handoff | `01-Inbox/agent-handoffs/` |
| Queued, cross-session, or blocked task | `01-Inbox/tasks/` |
| External source analysis | `40-ExternalSources/01-samples/` or a relevant topic folder |
| Project state | The relevant project bridge card |
| Reusable lesson | `20-SharedAssets/01-user-assets/` |
| Incident lesson | Copy `00-AI/templates/TPL-incident-experience-card.md` into the relevant project or shared asset location |
| Recall rule | `00-AI/recall/` |
| Template | `00-AI/templates/` |

## Do Not

- Do not save secrets, tokens, cookies, verification codes, private keys, or account credentials.
- Do not treat raw chat logs as long-term memory.
- Analyze and cite external sources by default. Explicitly requested private collection may preserve originals and provenance when the user has the right to save them; do not publish them automatically.
- Do not use Inbox folders as permanent storage.
- Do not reorganize the vault without a clear task.
- When specialist review is useful, name the review perspective and acceptance criteria directly.

## Before Ending

- State what changed.
- State why it changed.
- State what was verified.
- Name the files when long-term memory was updated.
