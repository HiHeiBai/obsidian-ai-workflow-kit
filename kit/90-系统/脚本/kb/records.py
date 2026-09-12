"""Read-only checks for compact, current-state bridge and handoff cards."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


RECORD_LIMITS = {
    "project-bridge": (3000, 120),
    "codex-project-bridge": (3000, 120),
    "agent-handoff": (1800, 80),
    "handoff": (1800, 80),
}
NEXT_HEADINGS = {
    "下一步", "下次开工", "当前下一步", "next action", "next actions",
    "next startup", "next steps", "下一步（next action）", "下一步 (next action)",
}
LOG_HEADINGS = {"状态时间线", "决策时间线", "验证记录", "validation log", "test log"}


def record_body(text: str) -> str:
    text = text.replace("\r\n", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end >= 0:
            body = text[end + 4:]
            return body[1:] if body.startswith("\n") else body
    return text


def record_findings(metadata: dict[str, str], text: str) -> tuple[list[str], list[str]]:
    """Return actionable errors and visible exceptions; never rewrite a record."""
    kind = metadata.get("type", "")
    if kind not in RECORD_LIMITS:
        return [], []
    body = record_body(text)
    errors: list[str] = []
    warnings: list[str] = []
    chars, lines = len(body), sum(bool(line.strip()) for line in body.splitlines())
    max_chars, max_lines = RECORD_LIMITS[kind]
    for key, value in metadata.items():
        if len(str(value)) > 600:
            errors.append(f"metadata field too long: {key}; do not move body prose into YAML")
    normalized = text.replace("\r\n", "\n")
    if normalized.startswith("---\n") and "\n---" in normalized[4:]:
        front = normalized[4:normalized.find("\n---", 4)]
        if len(front) > 2000:
            errors.append("frontmatter exceeds 2000 characters; keep only short routing fields")
        fields = list(re.finditer(r"^([^\s:]+):[^\n]*", front, re.M))
        for index, field in enumerate(fields):
            end = fields[index + 1].start() if index + 1 < len(fields) else len(front)
            if len(front[field.start():end]) > 600:
                errors.append(f"raw metadata field too long: {field.group(1)}; multiline values count too")
    if chars > max_chars or lines > max_lines:
        message = f"record budget exceeded: chars={chars}/{max_chars}, nonblank_lines={lines}/{max_lines}; move detailed history to a linked record, preserve current blockers and boundaries"
        exception = metadata.get("compact_exception", "").strip()
        if exception:
            warnings.append(f"{message}; exception requires review: {exception}")
        else:
            errors.append(message)

    # Code examples do not create real sections, but still count toward the budget.
    prose = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", body, flags=re.M | re.S)
    headings = [m.group(1).strip().casefold() for m in re.finditer(r"^#{2,6}\s+(.+?)\s*#*\s*$", prose, re.M)]
    sections = list(re.finditer(r"^#{2,6}\s+([^\n]+)$", prose, re.M))
    for position, section in enumerate(sections):
        name = section.group(1).strip().casefold()
        if name not in {"当前状态", "当前摘要", "current state", "有效决策", "有效决策与操作边界", "effective decisions", "最近决策", "recent decisions"}:
            continue
        end = sections[position + 1].start() if position + 1 < len(sections) else len(prose)
        points = re.findall(r"^(?:[-*] |\d+[.)] )", prose[section.end():end], re.M)
        if len(points) > 5:
            errors.append(f"too many current-summary points in {name}: {len(points)}/5")
    next_sections = [h for h in headings if h in NEXT_HEADINGS]
    strict = metadata.get("record_format") == "compact-v1"
    if strict and not next_sections:
        errors.append("compact-v1 requires one next-action section")
    if len(next_sections) > 1:
        errors.append("multiple next-action sections: " + ", ".join(next_sections))
    if kind in {"project-bridge", "codex-project-bridge"}:
        logs = [h for h in headings if any(h == name or h.startswith(name + "（") or h.startswith(name + " (") for name in LOG_HEADINGS)]
        if logs:
            errors.append("bridge contains history/log sections: " + ", ".join(logs))

    actions = re.findall(r"^\s*(?:[-*]\s*)?(?:首要动作|Primary action)[:：]\s*(.+)$", prose, flags=re.M | re.I)
    if strict and not actions:
        errors.append("compact-v1 requires one labeled primary action")
    if len(actions) > 1:
        errors.append("multiple primary actions; keep one action and at most two dependencies")
    if actions and metadata.get("next_action", "").strip() != actions[0].strip():
        errors.append("next_action does not match the body's primary action")
    if strict:
        dependencies = 0
        for position, section in enumerate(sections):
            name = section.group(1).strip().casefold()
            if name not in NEXT_HEADINGS and name not in {"dependencies", "必要依赖", "依赖"}:
                continue
            end = sections[position + 1].start() if position + 1 < len(sections) else len(prose)
            for item in re.findall(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$", prose[section.end():end], re.M):
                if re.match(r"(?:首要动作|Primary action)[:：]", item, re.I):
                    continue
                if re.fullmatch(r"(?:dependencies|必要依赖|依赖)[:：]?", item, re.I):
                    continue
                dependencies += 1
        if dependencies > 2:
            errors.append(f"too many dependencies in next-action sections: {dependencies}/2")
    return errors, warnings


def check_record(args: argparse.Namespace) -> int:
    # Imported here to keep this module reusable by the vault health checker.
    from .health import read_frontmatter

    failed = False
    for filename in args.paths:
        path = Path(filename).expanduser()
        if not path.is_file():
            print(f"ERROR {path}: file not found")
            failed = True
            continue
        metadata, text = read_frontmatter(path)
        if metadata.get("type") not in RECORD_LIMITS:
            print(f"ERROR {path}: expected a project bridge or handoff record")
            failed = True
            continue
        errors, warnings = record_findings(metadata, text)
        for finding in errors:
            print(f"ERROR {path}: {finding}")
        for finding in warnings:
            print(f"WARN {path}: {finding}")
        if not errors and not warnings:
            print(f"PASS {path}")
        failed = failed or bool(errors)
    return int(failed)
