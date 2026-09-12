# Before / After Case

This example shows what the kit is meant to do with a small messy folder. It is not a promise of full automation. The user still decides what matters, and the AI must write back only after checking the relevant rules.

## Before

```text
~/Downloads/product-launch/
├── call-notes.txt
├── competitor-links.md
├── draft-positioning.md
├── onboarding-research.pdf
├── random-screenshot.png
└── todo-from-chat.md
```

The folder has useful material, but a new AI session does not know:

- which project this belongs to
- which file is current
- what is a source, a decision, or a task
- where a summary should be written
- what should be recalled next time

## First Intake

The user starts with an inventory instead of asking AI to read everything:

```bash
python3 90-系统/脚本/kb.py intake-folder ~/Downloads/product-launch \
  --title "Product Launch Materials" \
  --project product-launch
```

This creates:

```text
20-资料/02-folder-intakes/product-launch-materials.md
```

The intake card lists files, keeps originals in place, and tells AI to process a subset before promoting anything.

## AI Triage

After reading `00-入口/开始这里.md`, the AI should route the material like this:

| Input | Knowledge type | Write-back target |
|---|---|---|
| `call-notes.txt` | project state | `10-项目/product-launch/current-state.md` |
| `draft-positioning.md` | possible decision | `10-项目/product-launch/decisions.md` |
| `onboarding-research.pdf` | source evidence | `20-资料/01-示例/` |
| `todo-from-chat.md` | temporary task notes | project bridge next action or Inbox |
| repeated lesson from the work | reusable asset | `30-经验资产/06-本地经验/` |

## After

```text
10-项目/product-launch/
├── BRIDGE-product-launch.md
├── current-state.md
└── decisions.md

20-资料/
├── 01-samples/onboarding-research.md
└── 02-folder-intakes/product-launch-materials.md

90-系统/召回/任务上下文地图.md
30-经验资产/06-本地经验/<reusable-lesson>.md
```

Now a later AI session can start from the bridge card, read only the mapped context, and write updates back to the right place.

## What The Kit Does Not Do

- It does not decide your strategy for you.
- It does not read your whole computer.
- It does not keep itself useful if nobody updates project state, decisions, handoffs, or reusable lessons.
- It does not replace Obsidian. It gives Obsidian a workflow that AI can follow.
