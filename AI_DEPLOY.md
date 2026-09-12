# AI deployment guide

Use this guide when a user gives you this repository and asks you to deploy or start using it. Actually install the vault and verify it; a list of commands is not a completed deployment. For source development, follow [AGENTS.md](AGENTS.md) and the source instructions instead.

## 1. Choose the target and inspect it

- Honor the user's requested language and location. For a new vault, default to **Chinese, full**. If no location is supplied, use `AI知识库` inside the user's actual Documents directory (usually `~/Documents/AI知识库` on macOS/Linux). Resolve the real Documents location on Windows or systems with redirected folders. Report the resulting absolute path.
- The final target must be persistent storage, outside your temporary download, checkout, sandbox cache, or disposable session. Use a temporary location only for obtaining the source.
- Confirm your tools can write to the user's intended computer. A cloud agent's filesystem is not necessarily the user's filesystem. If you cannot deploy locally, state the limitation and the one action needed to continue; do not claim deployment succeeded.
- Inspect the chosen target before writing, including hidden files. Limit inspection to the target and relevant user-provided context; do not scan the whole computer.
- If the target does not exist or is empty, proceed with a new installation. Existing authorized location and language choices do not require another confirmation.
- If it contains a kit manifest, use the managed update path below. Current manifests are `90-系统/配置/kit-manifest.json` (Chinese) or `00-AI/config/kit-manifest.json` (English); older vaults may use `.obsidian-ai-workflow-kit/manifest.json`.
- If a nonempty target has no kit manifest, do not copy the starter over it or reorganize its contents. Inspect its entry and structure, then resolve whether the user wants integration or a separate vault. Ask only if the choice is not clear from their request. A protected adoption policy must be respected; use its established shared-core workflow, never bypass protection for a routine deployment.

## 2. Deploy

### New Chinese vault (default)

Download and extract the repository archive to a temporary directory:

`https://github.com/HiHeiBai/obsidian-ai-workflow-kit/archive/refs/heads/main.zip`

Use the available filesystem/download tools for the platform. Copy **the contents of `kit/`**, including its system configuration, into the chosen empty target. Do not copy the whole repository or nest an extra `kit/` directory inside the target. Do not put repository `src/`, tests, release notes, or development tooling into the user's vault. The delivered `kit/` already includes its managed update manifest and needs no build step.

The target root should contain only:

```text
首页.md
00-入口/
01-收件箱/
10-项目/
20-资料/
30-经验资产/
90-系统/
```

Do not recreate root `AGENTS.md` or `CLAUDE.md` by default. Explicitly reading the startup entry is sufficient for this session. Root automatic-discovery integrations are optional; enable them only if requested, merging with existing instructions rather than replacing them.

### New English vault (only if requested)

From the extracted source repository, with Python 3 and Bash available, run:

```bash
bash install.sh --language en --mode full --dry-run "/absolute/path/to/vault"
bash install.sh --language en --mode full "/absolute/path/to/vault"
```

Replace the path with the resolved user target. Review the preview before applying. On platforms without Bash, use the equivalent Python CLI:

```text
python src/00-AI/scripts/kb.py install-core "/absolute/path/to/vault" --language en --mode full --dry-run
python src/00-AI/scripts/kb.py install-core "/absolute/path/to/vault" --language en --mode full
```

Use the available Python 3 executable; do not assume the name `python` means Python 3.

### Existing managed vault

From the latest extracted repository, preview and then apply:

```bash
bash install.sh --update --dry-run "/absolute/path/to/vault"
bash install.sh --update "/absolute/path/to/vault"
```

Omit language and mode so the updater preserves the installed values from the manifest. The direct Python equivalent is `python3 src/00-AI/scripts/kb.py upgrade-core "/absolute/path/to/vault"`, with `--dry-run` for the preview. Do not add `--overwrite`. Preserve user edits and report any conflicts; do not silently resolve them by replacing content. An explicit language or mode change is a migration, not a routine update.

For a protected shared-core vault, read [the source sync policy](docs/release/source-sync-policy.md) and its local adoption policy before acting. Keep its existing home and startup entry.

## 3. Verify and start the current session

1. Verify the actual target exists and the copied/installed files are readable. For a new Chinese vault, check the seven root entries listed above and `90-系统/配置/kit-manifest.json`; the manifest should identify Chinese full mode. For an update, compare against the pre-update layout and report any unexpected language duplication or conflicts without deleting user files.
2. Read `首页.md` and `00-入口/开始这里.md` in the deployed Chinese vault. For English, read `index.md` and `00-AI/START-HERE.md`. Follow the entry's startup workflow using only the necessary context. For shared-core, use the vault's established entry.
3. When Python 3 is available, run the read-only health check against the **deployed target**, using the installed mode from its manifest:

```bash
python3 "/absolute/path/to/vault/90-系统/脚本/kb.py" health-check --vault "/absolute/path/to/vault" --mode full
```

For English, the CLI is `00-AI/scripts/kb.py`. Existing barebone or shared-core installations must use their recorded mode. Report failures accurately and fix deployment-caused problems before handing off. If Python is unavailable, perform the file/entry checks and explicitly say the automated health check was not run; Chinese file-copy deployment itself does not require Python.

4. If Obsidian is installed and your tools can open a local vault, open the target and its home page as part of setup. If this is unavailable, give only the minimal remaining UI step.

5. Do not create a sample project or task in the user's working vault just to test deployment. Do not claim Obsidian was opened or visually verified unless you actually did so.

## 4. Handoff

Keep the response short and concrete:

- The actual absolute vault folder and a clickable home-page path.
- What verification passed, and any remaining limitation or conflict.
- Whether you read the startup entry and the current session is ready.
- Tell the user to open that folder as an Obsidian vault if needed; do not claim this UI step is complete without evidence.
- Provide a ready-to-copy next-session prompt with the **real absolute path already filled in**, for example: “这个知识库位于：/actual/path/AI知识库。请先读取其中的 00-入口/开始这里.md，按开工流程接手。” Use the English entry path for an English vault.

No new repository clone, terminal commands, language flags, or install-mode decisions should be required of a user following the homepage prompt.
