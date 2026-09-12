# Scripts

These scripts are optional. The vault works without them.

For everyday commands below, run from the installed vault root. To install or upgrade a vault, use the repository root and `python3 src/00-AI/scripts/kb.py`, or the one-line installer. The repository source layout is separate from the installed vault layout.

## One-line Install

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --mode barebone "/path/to/your-vault"
```

The remote installer downloads the current repository archive and delegates to `install-core`.

Language:

- `en` is the default.
- `zh-CN` writes Chinese starter text to language-aware kit files.

Modes:

- `barebone` is the default and installs the smallest usable layer: startup entry, governance, project registry, focused templates, and `90-系统/脚本/kb.py`.
- `full` installs the complete workflow kit, examples, documentation, and the built-in Obsidian Bases views.

## Update Existing Install

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone "/path/to/your-vault"
```

`--update` upgrades managed kit files from the latest GitHub version. It uses `.obsidian-ai-workflow-kit/manifest.json` to tell whether a file is still the original kit file or has been changed by the user.

Default behavior:

- Creates new kit files that were added after your install.
- Updates kit files that are still unmodified.
- Skips files that were edited by the user.
- Skips existing files that were never recorded in the manifest.
- Refuses to write into vaults protected by `.obsidian-ai-workflow-kit/adoption-policy.json`.

Use `--conflict-copy` with `upgrade-core` when you want new versions written beside conflicted files for manual comparison:

```bash
python3 src/00-AI/scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone --conflict-copy
```

## Local Adapter Protection

A vault can consume this kit as an architecture reference without becoming a managed kit install. Add this file to the vault:

```json
{
  "mode": "local-adapter",
  "allow_public_kit_writes": false
}
```

Path:

```text
.obsidian-ai-workflow-kit/adoption-policy.json
```

When this policy exists, `install-core` and `upgrade-core` refuse to write kit files into the vault. `--dry-run` still works for review. Only use `--allow-protected-adapter-write` after an explicit manual decision.

## Health Check

```bash
python3 90-系统/脚本/kb.py health-check
python3 90-系统/脚本/kb.py health-check --mode barebone
```

Checks:

- Core files and directories exist.
- Legacy private-vault concepts are not present.
- Markdown relative links point to existing files.
- Obsidian Wikilinks resolve to exactly one target.
- Typed `status` values match their page type.
- Project entries, local tasks, and external source cards contain every field used by Bases.
- Full-mode Base files preserve their required filters and views.
- Public Markdown does not contain private-looking `/Users/<name>/` paths.
- The English README does not contain visible Chinese text in English full mode.

Use `--mode barebone` when checking a minimal install.

## Check A Bridge Or Handoff

```bash
python3 90-系统/脚本/kb.py check-record "10-项目/my-project/BRIDGE-my-project.md"
```

Read-only: checks body size (3000 Unicode characters / 120 nonblank lines for bridges, 1800 / 80 for handoffs), duplicate action/log sections, and the `next_action` mirror. Counts exclude opening YAML frontmatter. Detailed history belongs in project records; never cut unresolved blockers, authorization boundaries, or evidence to fit. A short `compact_exception` reason remains a visible review warning. The command exits with 1 for structural errors and does not rewrite the file. Full/barebone health checks include this check; shared-core checks keep their managed-files-only boundary.

## Stale Check

```bash
python3 90-系统/脚本/kb.py stale-check --vault "/path/to/your-vault"
python3 90-系统/脚本/kb.py stale-check --vault "/path/to/your-vault" --max-age-days 7 --inbox-threshold 10 --fail-on-findings
```

Reports project bridge cards with old or missing `updated` dates and Inbox folders that exceed the file threshold. Use `--fail-on-findings` for hooks or CI jobs that should stop when review items exist.

Stale concept patterns are loaded from:

```text
90-系统/配置/过时概念.txt
```

To override them in your own vault, create:

```text
.obsidian-ai-workflow-kit/stale-patterns.txt
```

The override file replaces the kit defaults.

## Migrate Legacy Codex Names

```bash
python3 90-系统/脚本/kb.py migrate-codex-names --vault "/path/to/your-vault" --dry-run
python3 90-系统/脚本/kb.py migrate-codex-names --vault "/path/to/your-vault"
```

Renames older Codex-specific files to the current agent-neutral names and updates Markdown references.

Examples:

- `CODEX-BRIDGE-my-project.md` -> `BRIDGE-my-project.md`
- `TPL-Codex项目桥接卡.md` -> `TPL-project-bridge-card.md`
- `Codex项目经验资产化机制-v1.md` -> `项目经验沉淀机制-v1.md`

## Migrate Legacy AI Layout

```bash
python3 90-系统/脚本/kb.py migrate-ai-layout --vault "/path/to/your-vault" --dry-run
python3 90-系统/脚本/kb.py migrate-ai-layout --vault "/path/to/your-vault"
```

Moves older scattered AI system files into `90-系统/` and updates Markdown references.

Examples:

- `START-HERE.md` -> `00-入口/开始这里.md`
- `00-Agent-Governance/` -> `90-系统/规则/`
- `02-Knowledge-Pipeline/` -> `20-资料/处理流程/`
- `03-Recall-System/` -> `90-系统/召回/`
- `90-Templates/` -> `90-系统/模板/`
- `scripts/` -> `90-系统/脚本/`

## Migrate v0.8 To v0.9

Preview first:

```bash
python3 90-系统/脚本/kb.py migrate-v0.9 --vault "/path/to/your-vault" --dry-run
```

Apply only after reviewing the preview:

```bash
python3 90-系统/脚本/kb.py migrate-v0.9 --vault "/path/to/your-vault"
```

This migration:

- moves legacy `01-收件箱/派工卡/` files to `01-收件箱/任务/`;
- removes the legacy dispatch directory only after every real file has moved and the directory is empty;
- maps legacy task and page status values to the v0.9 typed status domains;
- changes `type: task_card` to `type: local-task`;
- updates exact task-folder references;
- adds `pillar: general` and `project_entry: true` when a project has exactly one unambiguous current bridge card.

It performs a preflight before writing. If a destination task file already exists or a project has multiple current bridge cards, it stops without making changes.

## Install Core

```bash
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault" --dry-run
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault"
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault" --mode barebone --dry-run
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault" --mode barebone
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault" --language zh-CN --mode barebone
bash install.sh --dry-run "/path/to/your-vault"
bash install.sh "/path/to/your-vault"
bash install.sh --mode barebone --dry-run "/path/to/your-vault"
bash install.sh --mode barebone "/path/to/your-vault"
bash install.sh --language zh-CN --mode barebone "/path/to/your-vault"
```

Copies the core kit into an existing Obsidian vault.

Default behavior:

- Creates missing files and directories.
- Skips existing files.
- Does not overwrite unless `--overwrite` is passed.
- Records managed kit files in `.obsidian-ai-workflow-kit/manifest.json` so future updates can be safer.
- Refuses to install into this kit repository or into a child directory of it.

## Upgrade Core

```bash
python3 src/00-AI/scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone --dry-run
python3 src/00-AI/scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone
```

Use this when a vault already has the kit and you want to follow newer GitHub versions without replacing user-owned notes. It only updates files that are managed by the kit and still match the last installed checksum.

## New Project

```bash
python3 90-系统/脚本/kb.py new-project my-project --name "My Project" --root "/path/to/project"
python3 90-系统/脚本/kb.py new-project my-project --name "My Project" --pillar "product" --root "/path/to/project"
```

Creates:

- `10-项目/my-project/README.md`
- `10-项目/my-project/BRIDGE-my-project.md`
- `10-项目/my-project/current-state.md`
- `10-项目/my-project/decisions.md`

## Intake Source

```bash
python3 90-系统/脚本/kb.py intake-source "/path/to/source.md" --title "Source Title" --project my-project
```

Creates a source analysis card under `20-资料/01-示例/`.

Use this when a local file or URL should enter the knowledge pipeline before AI decides whether to promote it into a project update, shared asset, or recall map entry. For folders, use `intake-folder`.

## Intake Folder

```bash
python3 90-系统/脚本/kb.py intake-folder "/path/to/materials" --title "Materials Intake" --project my-project
```

Creates a folder inventory card under `20-资料/02-folder-intakes/`.

Default behavior:

- Does not move or edit original files.
- Skips hidden files and common tool folders.
- Lists at most 200 files unless `--max-files` is passed.
- Supports `--extensions md,pdf,txt` for a narrower inventory.

## Audit Vault

```bash
python3 90-系统/脚本/kb.py audit-vault
python3 90-系统/脚本/kb.py audit-vault --write-report
```

Checks core entry points, stale concepts, Markdown links, Inbox files, and project directories without bridge cards. `--write-report` writes a report under `30-经验资产/05-audit-reports/`.
