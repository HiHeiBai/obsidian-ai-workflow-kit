# 30-Second Demo

For the ready-to-open Chinese demo, [download the GitHub ZIP](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/archive/refs/heads/main.zip), extract it, and open the `kit/` subfolder in Obsidian. Follow the [Chinese demo guide](30-second-demo.zh-CN.md) for its entry paths and prompt. No installation is needed.

For an English demo, use the installation steps below, then ask an AI agent to summarize a project in about 30 seconds. Open the installation target folder in Obsidian.

## Set up the demo vault

From a downloaded or cloned repository, run:

```bash
bash install.sh --mode full "$HOME/obsidian-ai-workflow-demo"
```

Or install directly:

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode full "$HOME/obsidian-ai-workflow-demo"
```

Choose a new folder for this demo. In Obsidian, select **Open folder as vault**, open `~/obsidian-ai-workflow-demo`, and open `首页.md`.

## Try the read-only handoff

Send this to an AI agent that can read local files, replacing the placeholder with the absolute path to your installed demo vault:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <path-to-installed-demo-vault>. First read 00-入口/开始这里.md, then use the read-only demo in 90-系统/示例/filled-example. Tell me the current project state, the latest decision, and the next action. Do not edit files or create a task card.
```

## Expected result

The agent should read:

- `00-入口/开始这里.md`
- `首页.md`
- `90-系统/示例/filled-example/BRIDGE-launch-notes.md`
- `90-系统/示例/filled-example/current-state.md`
- `90-系统/示例/filled-example/decisions.md`

It should answer with the demo project's current state, latest decision, next action, and where real work would be written back. User guides and examples are under `90-系统/`; the repository's development documents stay outside this working vault.
