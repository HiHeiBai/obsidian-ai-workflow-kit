from __future__ import annotations

import argparse
import datetime as dt

from .config import language_target_path, localize_text_references
from .utils import validate_slug, vault_language, vault_root, write_file, yaml_string

def new_project(args: argparse.Namespace) -> int:
    validate_slug(args.slug)
    root = vault_root(args.vault)
    language = vault_language(root)
    project_dir = root / language_target_path(language, f"10-Projects/{args.slug}")
    if project_dir.exists() and any(project_dir.iterdir()):
        raise SystemExit(f"project directory already exists: {project_dir}")

    today = dt.date.today().isoformat()
    root_hint = args.root or "<your-project-path>"
    pillar = getattr(args, "pillar", None) or "general"
    bridge_name = f"BRIDGE-{args.slug}.md"
    files = {
        "README.md": f"""---
type: project-readme
status: active
project: {yaml_string(args.name)}
created: {today}
updated: {today}
---

# {args.name}

## Purpose

Describe what this project is for and why an AI agent may need to resume it.

## Start Here

- `{bridge_name}`
- `current-state.md`
- `decisions.md`

## Current Action

Read the primary action in `{bridge_name}`; update it there when the plan changes.
""",
        bridge_name: f"""---
type: project-bridge
record_format: compact-v1
status: active
project: {yaml_string(args.name)}
pillar: {yaml_string(pillar)}
project_entry: true
priority: p1
stage: discovery
local_root: {yaml_string(root_hint)}
kb_project: "10-Projects/{args.slug}/README.md"
startup_files:
  - "00-AI/START-HERE.md"
  - "10-Projects/{args.slug}/current-state.md"
  - "10-Projects/{args.slug}/decisions.md"
updated: {today}
created: {today}
last_verified:
next_action: Define the next concrete project action.
---

# Project Bridge | {args.name}

## One-line Purpose

Explain how this local project maps to the vault and why it matters.

## Startup Files

1. `00-AI/START-HERE.md`
2. This bridge card
3. `current-state.md`
4. `decisions.md`

## Current State

- Initial bridge created; the actual project state has not been verified.
- Keep at most 5 current facts, with source references. Replace changed facts.

## Effective Decisions

- No stable decisions recorded yet. Keep at most 5 still-effective decisions.

## Next Action

- Primary action: Define the next concrete project action.
- Dependencies: At most 2 required dependencies; remove this line if none.

## Blockers and Authorization Boundaries

- Record unresolved blockers, existing permissions, and prohibited actions. None recorded yet.

## Evidence and Lessons

- Link critical verification conclusions to project records; state what remains unverified.
- Put reusable lessons in `20-SharedAssets/01-user-assets/` and link them here.

## Write-back Rules

- Replace changed current facts and keep the primary action equal to `next_action`; no change means no write. Put detailed history in existing project records and link it here.
- Follow `00-AI/governance/write-back-rules.md` for budgets, evidence preservation, and conditional handoffs. Run `python3 00-AI/scripts/kb.py check-record <this-card.md>` after edits.

""",
        "current-state.md": f"""---
type: project-state
status: active
project: {yaml_string(args.name)}
created: {today}
updated: {today}
---

# Current State | {args.name}

- {today}: Project workspace created.
""",
        "decisions.md": f"""---
type: decisions
status: active
project: {yaml_string(args.name)}
created: {today}
updated: {today}
---

# Decisions | {args.name}

No stable decisions recorded yet.
""",
    }

    if args.dry_run:
        print(f"would create directory {project_dir}")
    else:
        project_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in files.items():
        content = localize_text_references(content, language)
        write_file(project_dir / filename, content, args.dry_run)
    return 0
