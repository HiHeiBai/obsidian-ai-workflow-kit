"""Exercise the shipped CLI and managed upgrades across the v0.12 layout boundary."""
import hashlib
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "src/00-AI/scripts/kb.py"
LEGACY_REF = "6c6e351"
LAYOUTS = {
    "en": {
        "home": "index.md",
        "dirs": {"00-AI", "01-Inbox", "10-Projects", "20-SharedAssets", "40-ExternalSources"},
        "cli": "00-AI/scripts/kb.py",
        "help": "00-AI/help",
        "examples": "00-AI/examples",
        "projects": "10-Projects",
    },
    "zh-CN": {
        "home": "首页.md",
        "dirs": {"00-入口", "01-收件箱", "10-项目", "20-资料", "30-经验资产", "90-系统"},
        "cli": "90-系统/脚本/kb.py",
        "help": "90-系统/使用指南",
        "examples": "90-系统/示例",
        "projects": "10-项目",
    },
}


class InstalledLayoutTests(unittest.TestCase):
    def run_cli(self, cli, *args, cwd):
        result = subprocess.run(
            [sys.executable, "-B", str(cli), *map(str, args)], cwd=cwd,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def snapshot(self, root):
        return {
            p.relative_to(root).as_posix(): (
                hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns
            )
            for p in root.rglob("*") if p.is_file()
        }

    def assert_home_links(self, vault, home):
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", home.read_text(encoding="utf-8"))
        local = [link for link in links if not urlsplit(link).scheme and not link.startswith("#")]
        self.assertTrue(local, "The installed home page must offer clickable local navigation")
        for link in local:
            destination = (home.parent / unquote(urlsplit(link).path)).resolve()
            self.assertTrue(destination.is_relative_to(vault.resolve()), link)
            self.assertTrue(destination.exists(), f"Broken home link: {home}: {link}")

    def test_source_commands_survive_chinese_localization(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("layout_config", ROOT / "src/00-AI/scripts/kb/config.py")
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        text = "python3 src/00-AI/scripts/kb.py upgrade-core; docs/release/source-sync-policy.md"
        self.assertEqual(config.localize_text_references(text, "zh-CN"), text)

    def test_clean_install_matrix_and_isolated_runtime(self):
        for language, layout in LAYOUTS.items():
            for mode in ("barebone", "full"):
                with self.subTest(language=language, mode=mode), tempfile.TemporaryDirectory() as tmp:
                    outside = Path(tmp)
                    vault = outside / "vault"
                    args = ("install-core", vault, "--language", language, "--mode", mode)
                    self.run_cli(CLI, *args, "--dry-run", cwd=outside)
                    self.assertFalse(vault.exists(), "Fresh dry run must not create the target")
                    self.run_cli(CLI, *args, cwd=outside)
                    visible = {p.name for p in vault.iterdir() if not p.name.startswith(".")}
                    self.assertEqual(
                        visible,
                        layout["dirs"] | {layout["home"], "AGENTS.md", "CLAUDE.md", "LICENSE", "VERSION"},
                    )
                    self.assert_home_links(vault, vault / layout["home"])
                    help_dir, examples = vault / layout["help"], vault / layout["examples"]
                    if mode == "full":
                        self.assertTrue((help_dir / "30-second-demo.md").is_file())
                        self.assertTrue((examples / "filled-example/BRIDGE-launch-notes.md").is_file())
                        self.assertFalse((help_dir / "release").exists())
                        self.assertFalse((help_dir / "superpowers").exists())
                        demo = (help_dir / "30-second-demo.md").read_text(encoding="utf-8")
                        demo_paths = [
                            path for path in re.findall(r"`([^`\n]+)`", demo)
                            if path.endswith(("BRIDGE-launch-notes.md", "current-state.md", "decisions.md"))
                        ]
                        self.assertEqual(len(demo_paths), 3)
                        for path in demo_paths:
                            self.assertTrue((vault / path).is_file(), f"Broken demo instruction: {path}")
                        self.assertNotIn("00-AI/00-AI/", demo)
                        self.assertNotIn("90-系统/90-系统/", demo)
                    else:
                        self.assertFalse(help_dir.exists())
                        self.assertFalse(examples.exists())
                    installed_cli = vault / layout["cli"]
                    self.run_cli(installed_cli, "health-check", "--vault", vault, "--mode", mode, cwd=outside)
                    self.run_cli(
                        installed_cli, "new-project", "layout-demo", "--vault", vault,
                        "--name", "Layout Demo", "--root", outside / "project", cwd=outside,
                    )
                    self.assertTrue(list((vault / layout["projects"]).glob("**/BRIDGE-layout-demo.md")))
                    before = self.snapshot(vault)
                    self.run_cli(CLI, "upgrade-core", vault, "--language", language, "--mode", mode, "--dry-run", cwd=outside)
                    self.assertEqual(self.snapshot(vault), before)
                    self.run_cli(CLI, "upgrade-core", vault, "--language", language, "--mode", mode, cwd=outside)
                    self.assertEqual(self.snapshot(vault), before, "A current install must not be rewritten")

    def test_legacy_full_upgrade_preserves_user_content(self):
        available = subprocess.run(
            ["git", "cat-file", "-e", f"{LEGACY_REF}^{{commit}}"], cwd=ROOT,
            capture_output=True, timeout=10,
        )
        if available.returncode:
            self.skipTest(f"Legacy fixture commit {LEGACY_REF} unavailable in this checkout")
        archive = subprocess.run(
            ["git", "archive", LEGACY_REF], cwd=ROOT, capture_output=True,
            check=True, timeout=15,
        ).stdout
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp)
            legacy = outside / "legacy-source"
            legacy.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive)) as source:
                source.extractall(legacy)
            self.assertEqual((legacy / "VERSION").read_text().strip(), "0.11.1")
            for language, layout in LAYOUTS.items():
                with self.subTest(language=language):
                    vault = outside / language
                    self.run_cli(
                        legacy / "00-AI/scripts/kb.py", "install-core", vault,
                        "--language", language, "--mode", "full", cwd=outside,
                    )
                    preserved = {
                        "docs/30-second-demo.md": "# My customized guide\n",
                        "examples/filled-example/current-state.md": "# My customized example\n",
                        "docs/private-note.md": "# Private, unmanaged note\n",
                        "my-notes/idea.md": "# My own idea\n",
                    }
                    for relative, content in preserved.items():
                        path = vault / relative
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(content, encoding="utf-8")
                    before = self.snapshot(vault)
                    args = ("upgrade-core", vault, "--language", language, "--mode", "full")
                    preview = self.run_cli(CLI, *args, "--dry-run", cwd=outside)
                    self.assertIn("would remove retired", preview)
                    self.assertEqual(self.snapshot(vault), before)
                    self.run_cli(CLI, *args, cwd=outside)
                    for relative, content in preserved.items():
                        self.assertEqual((vault / relative).read_text(encoding="utf-8"), content)
                    for retired in ("README.md", "README.zh-CN.md", "CHANGELOG.md", "install.sh", "docs/release/release-checklist.md"):
                        self.assertFalse((vault / retired).exists(), retired)
                    self.assertTrue((vault / layout["help"] / "30-second-demo.md").is_file())
                    self.assertTrue((vault / layout["examples"] / "filled-example/current-state.md").is_file())
                    self.assert_home_links(vault, vault / layout["home"])
                    after = self.snapshot(vault)
                    self.run_cli(CLI, *args, cwd=outside)
                    self.assertEqual(self.snapshot(vault), after, "Repeated migration must not rewrite files")
                    self.run_cli(vault / layout["cli"], "health-check", "--vault", vault, "--mode", "full", cwd=outside)


if __name__ == "__main__":
    unittest.main()
