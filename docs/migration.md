# Migration Guide

Use this kit gradually. Do not rebuild an existing Obsidian vault.

## Upgrading to v0.13: a quieter vault root

Fresh full and barebone vaults contain only the home page and functional directories at the root. Start AI work by copying the prompt from the home page. `AGENTS.md` and `CLAUDE.md` are now optional templates under `00-AI/integrations/` (`90-系统/接入/` in Chinese). Copy the matching template to the vault root only when you want automatic discovery; if a root instruction file already exists, merge the startup instruction instead of overwriting it. Templates in the system directory do not provide root-level automatic discovery by default.

`LICENSE` and `VERSION` move to `00-AI/about/` (`90-系统/关于/`). Full and barebone update manifests move to `00-AI/config/kit-manifest.json` (`90-系统/配置/kit-manifest.json`). The updater reads the previous root manifest so existing managed installations can upgrade.

Preview with `--update --dry-run`, retaining your existing language and mode. Upgrades remove the old managed root files only when they still match their recorded content. Modified root instructions and other user-owned files are preserved and may remain visible; review them before moving or deleting anything yourself. Shared-core keeps its existing scope and retains a legacy root manifest when one is already present.

## Upgrading to v0.12: source and vault layout

The GitHub repository keeps maintained templates in `src/`; `kit/` is a complete Chinese vault ready to open after downloading the ZIP. Run the installer from the repository root; the installed CLI keeps its existing path. Re-run `install.sh --update` from the new repository (or use the remote installer), retaining your existing mode and language, and preview with `--dry-run` first.

A new full installation has one home page and working directories. User guides and examples are inside the system directory: `00-AI/help` and `00-AI/examples` in English, or `90-系统/使用指南` and `90-系统/示例` in Chinese. Repository READMEs, installer, changelog, release checklists, and development plans are no longer installed. Version 0.12 retained root agent pointers, license, and version; version 0.13 moves them into the system directory as described above.

Managed upgrades remove retired kit files only when they still match their recorded hashes. Modified old guides/examples and untracked user notes stay in place and are reported for review; this can leave old directories present. Review those documents before moving them yourself. Empty retired directories are removed. The updater does not rewrite private note links to moved documents, so review links from your own notes if they referenced the old `docs/` or `examples/` paths. Shared-core installations keep their ownership boundary and do not adopt the new homepage or user directories.

## Upgrading From v0.8 To v0.9

The v0.9 upgrade has two separate steps so kit files and user-owned notes are never treated the same.

First preview and upgrade managed kit files. Keep the same language and mode as the existing install:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode full --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode full "/path/to/your-vault"
```

Use `--mode barebone` for a barebone installation. The updater creates new kit files and updates only managed files that still match their previous checksum. Modified and unmanaged files are skipped.

Then preview the metadata migration:

```bash
python3 00-AI/scripts/kb.py migrate-v0.9 --vault "/path/to/your-vault" --dry-run
```

It reports legacy dispatch-card moves, task status mappings, exact folder-reference updates, and project bridge cards that can safely receive `project_entry: true`. The old dispatch directory is removed only after every real file has moved and the directory is empty.

Apply only after the preview is correct:

```bash
python3 00-AI/scripts/kb.py migrate-v0.9 --vault "/path/to/your-vault"
python3 00-AI/scripts/kb.py health-check --vault "/path/to/your-vault"
```

The migration stops before writing when a task destination already exists or a project has multiple current bridge cards. Resolve that ambiguity manually; do not use `--overwrite` as a migration shortcut. Legacy `owner_role` and `owner_agent` values are left in user-owned cards as historical data, but new templates no longer create them.

## If You Are Starting Fresh

1. Download the repository ZIP and open its `kit/` folder in Obsidian for the ready-to-use Chinese vault, or install an English vault with `install.sh --lang en`.
2. Open the home page (`首页.md` in Chinese or `index.md` in English).
3. Copy its AI startup prompt into your agent session.
4. Create your first real project bridge card. The following commands use English installation paths:

```bash
python3 00-AI/scripts/kb.py new-project my-project --name "My Project" --root "/path/to/project"
```

5. Fill only three files first:

- `10-Projects/my-project/BRIDGE-my-project.md`
- `10-Projects/my-project/current-state.md`
- `10-Projects/my-project/decisions.md`

## If You Already Have a Vault

1. Copy only these files and folders into your existing vault:

- `00-AI/START-HERE.md`
- `00-AI/AGENTS.md`
- `00-AI/governance/`
- `00-AI/pipeline/`
- `00-AI/recall/`
- `10-Projects/`
- `20-SharedAssets/`
- `40-ExternalSources/`
- `00-AI/templates/`
- `00-AI/scripts/`

2. Do not move all existing notes.
3. Pick one active project.
4. Create one bridge card for that project.
5. Link existing notes from the bridge card instead of reorganizing them.

## If You Used Older Codex-Specific Names

Version `0.6.0` changed the public default naming from Codex-specific names to agent-neutral names.

Preview the rename first:

```bash
python3 00-AI/scripts/kb.py migrate-codex-names --vault "/path/to/your-vault" --dry-run
```

Apply it:

```bash
python3 00-AI/scripts/kb.py migrate-codex-names --vault "/path/to/your-vault"
```

This command renames legacy files such as `CODEX-BRIDGE-my-project.md` to `BRIDGE-my-project.md`, renames old Chinese/Codex-specific template filenames to English filenames, and updates Markdown references.

## If You Used The Older Scattered AI Layout

Version `0.7.0` moved AI-facing files into one top-level `00-AI/` directory.

Preview the layout migration first:

```bash
python3 00-AI/scripts/kb.py migrate-ai-layout --vault "/path/to/your-vault" --dry-run
```

Apply it:

```bash
python3 00-AI/scripts/kb.py migrate-ai-layout --vault "/path/to/your-vault"
```

This command moves legacy paths such as `START-HERE.md`, `AGENTS.md`, `00-Agent-Governance/`, `02-Knowledge-Pipeline/`, `03-Recall-System/`, `90-Templates/`, and `scripts/` into `00-AI/`, then updates Markdown references.

After migration, run:

```bash
python3 00-AI/scripts/kb.py health-check --vault "/path/to/your-vault"
python3 00-AI/scripts/kb.py stale-check --vault "/path/to/your-vault"
```

## Keeping The Kit Updated

New full and barebone installs write a small manifest at `00-AI/config/kit-manifest.json` (`90-系统/配置/kit-manifest.json` in Chinese). Future updates use it to distinguish kit-managed files from user-edited files. Existing legacy manifests are recognized during upgrades; shared-core retains a legacy root manifest when present.

Preview an update first:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone --dry-run "/path/to/your-vault"
```

Apply it:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone "/path/to/your-vault"
```

Update behavior:

- New kit files are created.
- Unmodified managed files are updated.
- User-edited files are skipped.
- Existing files without manifest history are treated as user-owned.
- New full-mode Base files are created without requiring Dataview or a community plugin.

If you need to compare a skipped file with the new kit version:

```bash
python3 00-AI/scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone --conflict-copy
```

## If You Want AI To Organize Existing Local Materials

1. Pick one folder, not your whole computer.
2. Ask AI to read `00-AI/pipeline/local-material-intake.md`.
3. Let AI classify the folder into:

- project memory
- external source analysis
- reusable lessons
- temporary Inbox items

4. Move or summarize only the high-value material.
5. Add recall entries only after the material becomes useful for future tasks.

## First Project Bridge Card

A useful first bridge card should answer:

- What project is this?
- Where is the local project folder?
- What is the current state?
- What decisions are stable?
- What should the next AI session read first?
- Where should the result be written back?

## What Not To Migrate

- Full chat history.
- Temporary scratch notes.
- Old web clips without source value.
- Private credentials or account data.
- Every note in your vault.

## Good First Acceptance Check

After migration, give an AI agent this instruction:

```text
You are the knowledge base maintenance agent. Read 00-AI/START-HERE.md in the current vault and follow its startup workflow.
```

The agent should identify one project bridge card, read only the needed project files, and say where it will write results back.
