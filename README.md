# Obsidian AI Workflow Kit

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Obsidian AI Workflow Kit routes a new AI session through startup instructions, project context, required files, and structured write-back.">
</p>

[Chinese](README.zh-CN.md) | English

[![CI](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/actions/workflows/ci.yml)

Make your local Obsidian vault readable, writable, and maintainable by AI agents.

## Give every new AI session a reliable starting point

Claude Code, Cursor, Codex, and ChatGPT should not need to rediscover what a project is, where its decisions live, or what changed last time. This kit provides a local-first Obsidian structure with one startup entry, project bridge cards, write-back rules, source triage, recall maps, and maintenance checks.

It is a file-system-level workflow, not an app, community plugin, cloud memory service, or RAG stack. Humans can edit every part; any AI agent with file access can follow it. Instead of searching the entire vault, the agent routes to the small set of files the current task needs. Optional dashboards use Obsidian's built-in Bases core plugin.

<p align="center">
  <img src="./assets/readme/session-route.svg" width="100%" alt="A new AI session enters through START-HERE, opens project state and required context, then writes back a durable handoff for the next session.">
</p>

## Start fast

### New or existing vault

Install the minimal layer into an empty folder or your existing vault. Open the **installation target folder** in Obsidian, then open `index.md` for the human-facing home page. The GitHub repository contains development resources; the installer builds your working vault from them.

The installer writes English paths and starter text by default. Use `--language zh-CN` for Chinese paths and starter text.

Preview:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --dry-run "/path/to/your-vault"
```

Install:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
```

Chinese paths and starter text:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN "/path/to/your-vault"
```

Check:

```bash
python3 "/path/to/your-vault/00-AI/scripts/kb.py" health-check --vault "/path/to/your-vault" --mode barebone
```

For Chinese install paths, see [README.zh-CN.md](README.zh-CN.md).

Then send this to your AI agent:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read 00-AI/START-HERE.md in that directory, then follow its startup workflow.
```

Use full mode when you want the complete starter vault, including pipeline, recall system, docs, examples, and templates:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode full "/path/to/your-vault"
```

The installer skips existing files by default. Pass `--overwrite` only when you intentionally want to replace files.

Update later:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update "/path/to/your-vault"
```

Updates use a local manifest to replace only managed kit files that you have not edited.

The downloadable `v0.9.1` archives remain historical snapshots. Starting with `v0.10.0`, ongoing maintenance uses repository source plus the managed installer, and the project no longer builds custom customer ZIP packages.

### Keep an established working vault in sync

Use `shared-core` when the vault already has its own entry, projects, Inbox, archives, and private context. This mode manages only reusable system files and excludes working content.

From a local clone of this repository, preview and then apply:

```bash
python3 kit/00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN --dry-run
python3 kit/00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN
```

The target vault must explicitly allow only `shared-core` in `.obsidian-ai-workflow-kit/adoption-policy.json`. See [Source Sync Policy](docs/release/source-sync-policy.md).

### See the handoff in 30 seconds

Install a separate demo vault to try the workflow before using your own notes:

1. Follow [30-Second Demo](docs/30-second-demo.md) to install full mode into a new test folder.
2. In Obsidian, choose **Open folder as vault** and select that installation target.
3. Open `index.md`, then send the demo prompt to your AI agent.

After setup, the read-only demo shows current state, the latest decision, and the next action from a filled project bridge card. No Obsidian community plugins are required.

## What gets installed

| Need | Included layer |
|---|---|
| AI needs a clear start point | `00-AI/START-HERE.md` |
| Project context is scattered | project bridge cards in `10-Projects/` |
| AI writes too freely | governance rules in `00-AI/governance/` |
| Local materials need sorting | knowledge pipeline in `00-AI/pipeline/` |
| Useful lessons are hard to recall | task maps and recall fields in `00-AI/recall/` |
| Handwritten indexes go stale | optional project, task, and source Bases in `00-AI/bases/` |
| Metadata silently drops pages from views | typed status, `project_entry`, and Base-field health checks |
| The vault slowly gets messy | read-only link, metadata, and maintenance checks |

The default mode includes the core workflow and templates. Full mode adds dashboards, examples, and selected user guides. Its guides live under `00-AI/help/` and examples under `00-AI/examples/`; development plans and release checklists stay in the source repository.

## How the routing works

![Obsidian AI Workflow Kit architecture](docs/images/architecture-flow.png)

Daily use stays small:

```text
User task
  -> 00-AI/START-HERE.md
  -> relevant project bridge card or task map
  -> execute directly when the current conversation can finish
  -> create 01-Inbox/tasks/ card only for queued, cross-session, or blocked work
  -> required context only
  -> structured write-back
  -> reusable lessons promoted for future recall
```

The agent should not scan your whole vault by default. It should read the startup entry, open the mapped context, do the task, and write results back to the right place. When specialist review is useful, name the perspective in the task or acceptance criteria.

## Choose an install scope

The default install is the minimal starter template. Advanced users can pass `--mode full` or the restricted `--mode shared-core` profile.

| Mode | Best for | What it installs |
|---|---|---|
| `barebone` | First step inside an existing vault | startup entry, core workflow folders, governance, project registry, templates, `00-AI/scripts/kb.py` |
| `full` | New complete starter vault | core workflow plus templates, scripts, Bases views, user guides in `00-AI/help/`, and examples in `00-AI/examples/` |
| `shared-core` | Keep an established working vault aligned | reusable rules, pipeline, recall, templates, Bases, scripts, and standards; no entry, projects, Inbox, archives, or root files |

Security-sensitive users can skip the remote `curl` form and run the installer from a local clone:

```bash
bash install.sh --dry-run "/path/to/your-vault"
bash install.sh "/path/to/your-vault"
bash install.sh --language zh-CN "/path/to/your-vault"
```

## Is this for you?

Good fit:

- You already use Obsidian for project notes, sources, or decisions.
- You use AI agents often enough that context handoff is painful.
- You want local-first memory that remains human editable.
- You are willing to keep project state and handoffs current.

Not a good fit:

- You want a graphical Obsidian plugin.
- You want a cloud memory service or managed RAG backend.
- You want AI to scan your whole computer automatically.
- You want automatic bulk rewriting of an existing vault.

## Learn more

- [30-Second Demo](docs/30-second-demo.md)
- [10-Minute First Run](docs/10-minute-first-run.md)
- [Before / After Case](docs/before-after-case.md)
- [Automation Starter](docs/automation.md)
- [Migration Guide](docs/migration.md)
- [Concepts](docs/concepts.md)
- [Templates](docs/templates.md)
- [Scripts](kit/00-AI/scripts/README.md)
- [v0.9.1 Release Notes](docs/release/v0.9.1-release-notes.md)

## Your installed vault

English installations have this working layout:

```text
index.md                   start here as a person
00-AI/                     AI entry, rules, recall, templates, and scripts
  START-HERE.md            start here as an AI agent
  help/                    user guides (full mode)
  examples/                reference examples (full mode)
01-Inbox/                  temporary material and pending work
10-Projects/               project notes and bridge cards
20-SharedAssets/           reusable methods and lessons
40-ExternalSources/        source analysis cards
```

Root-level `AGENTS.md` and `CLAUDE.md` point agents to the startup entry. `LICENSE` and `VERSION` retain package information, and a hidden `.obsidian-ai-workflow-kit/` directory records managed files for updates.

Chinese installations use localized folder and home-page names. See [the Chinese guide](README.zh-CN.md).

## Source repository

For contributors, the GitHub checkout is organized separately:

```text
kit/                       installable vault templates and runtime scripts
  00-AI/                   rules, templates, language variants, and CLI
  01-Inbox/                Inbox starter files
  10-Projects/             project starter files
  20-SharedAssets/          reusable asset starter files
  40-ExternalSources/      source starter files
  index.md                 installed home-page source
  AGENTS.md / CLAUDE.md    installed agent-entry sources
docs/                      documentation and contributor records
examples/                  source examples selected by full installation
assets/                    repository presentation assets
tests/                     development tests
install.sh                 installer entry point
```

Run `bash install.sh "/path/to/your-vault"` from this checkout, then open the target folder in Obsidian. Installing full mode does not copy repository READMEs, the installer, changelog, or top-level development directories into your vault.

## Maturity

This is a `0.x` beta starter kit. It is ready for controlled trials, small vaults, and feedback. It does not promise compatibility with every existing Obsidian vault layout.

This is a workflow kit, not an automation platform. If project state, decisions, handoffs, and reusable lessons are not maintained, the vault will slowly become ordinary folders again.

[Task handoff and lesson reuse walkthrough](examples/ai-handoff-demo/walkthrough.md)

## License

- Code, scripts, and executable snippets: [MIT](LICENSE).
- Original written content, templates, examples, and documentation: [CC BY 4.0](docs/legal/content-license.md).
- Third-party content is not covered by this repository license.

## Version

Current version: `0.12.0`. See [CHANGELOG.md](CHANGELOG.md).
