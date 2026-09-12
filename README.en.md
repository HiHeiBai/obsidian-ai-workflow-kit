# Obsidian AI Workflow Kit

Let an AI agent set up a local knowledge vault for your projects, sources, and lessons, so the next conversation can pick up where you left off.

## Copy this message to your AI

Use Codex, Claude Code, or Cursor with access to files on your computer:

```text
Please deploy this knowledge vault: https://github.com/HiHeiBai/obsidian-ai-workflow-kit . Read AI_DEPLOY.md at the repository root first, then carry out the deployment. Create the complete Chinese vault by default; if I have not specified a location, use the default folder defined in AI_DEPLOY.md inside my user Documents directory. Preserve existing content and do not overwrite an existing vault. Verify the result, report the actual vault path, and read its startup entry so this session is ready to use it.
```

The agent handles downloading, placing files, and checking the result. After deployment, open the folder it reports in Obsidian and start from the home page. If you prefer an English vault, say so in your message.

## What it helps with

- **Continue projects** with the current state and next action available to a new session.
- **Organize sources** into material you can find and use again.
- **Keep lessons** from problems you have solved for future work.

Your content stays in editable Markdown files on your computer. No Obsidian community plugins are required.

[Chinese homepage](README.md) · [Manual installation and updates](docs/manual-install.md) · [Changelog](CHANGELOG.md)

Code: [MIT](LICENSE). Original documentation and templates: [CC BY 4.0](docs/legal/content-license.md). Current version: `0.13.1`.
