from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path

from .config import DEFAULT_LANGUAGE, MANIFEST_DIR, MANIFEST_FILE, validate_language, find_manifest_path

def vault_root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def vault_language(root: Path) -> str:
    path = find_manifest_path(root)
    if not path.exists():
        return DEFAULT_LANGUAGE
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_LANGUAGE
    if not isinstance(manifest, dict):
        return DEFAULT_LANGUAGE
    try:
        return validate_language(manifest.get("language"))
    except SystemExit:
        return DEFAULT_LANGUAGE


def iter_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        if ".git" not in path.parts:
            if (root / "src/00-AI").is_dir() and path.relative_to(root).parts[0] == "kit":
                continue
            yield path


def has_chinese(text: str) -> bool:
    return re.search(r"[\u4e00-\u9fff]", text) is not None


def validate_slug(slug: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise SystemExit("slug must use lowercase letters, numbers, and hyphens")


def make_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "source"


def yaml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def escape_table(value: str) -> str:
    return value.replace("|", "\\|")


def format_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} B"
        size = size / 1024
    return f"{size} B"


def parse_extensions(value: str | None) -> set[str] | None:
    if not value:
        return None
    extensions = set()
    for item in value.split(","):
        ext = item.strip().lower()
        if not ext:
            continue
        extensions.add(ext if ext.startswith(".") else f".{ext}")
    return extensions or None


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"would create {path}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"created {path}")


def repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if find_manifest_path(parent).exists():
            return parent
        if (parent / "VERSION").exists() and (parent / "README.md").exists():
            return parent
    return current.parents[2]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_frontmatter_value(path: Path, key: str) -> str | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        if line.startswith(f"{key}:"):
            return frontmatter_scalar(line.split(":", 1)[1])
    return None


def frontmatter_scalar(value: str) -> str:
    """Read simple YAML scalars without treating a quoted # as a comment."""
    value = value.strip()
    if not value or value.startswith("#"):
        return ""
    if value[0] in {"'", '"'}:
        quote = value[0]
        index = 1
        while index < len(value):
            if quote == '"' and value[index] == "\\":
                index += 2
                continue
            if value[index] == quote:
                if quote == "'" and value[index:index + 2] == "''":
                    index += 2
                    continue
                literal = value[:index + 1]
                if quote == "'":
                    return literal[1:-1].replace("''", "'")
                try:
                    return json.loads(literal)
                except json.JSONDecodeError:
                    return literal[1:-1]
            index += 1
        return value
    return re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
