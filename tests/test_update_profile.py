"""Users can ask for an update without knowing the vault's install flags."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'src/00-AI/scripts/kb.py'
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}


def snapshot(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in root.rglob('*') if p.is_file()}


class UpdateProfileTests(unittest.TestCase):
    def run_ok(self, command):
        result = subprocess.run(command, capture_output=True, text=True, env=ENV)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_unqualified_updates_keep_each_installed_profile(self):
        for language in ('en', 'zh-CN'):
            for mode in ('barebone', 'full', 'shared-core'):
                with self.subTest(language=language, mode=mode), tempfile.TemporaryDirectory() as tmp:
                    vault = Path(tmp) / 'vault'
                    if mode == 'shared-core':
                        policy = vault / '.obsidian-ai-workflow-kit/adoption-policy.json'
                        policy.parent.mkdir(parents=True)
                        policy.write_text(json.dumps({'mode': 'managed-core', 'allow_public_kit_writes': True,
                                                      'allowed_install_modes': ['shared-core']}))
                    self.run_ok([sys.executable, str(CLI), 'install-core', str(vault), '--mode', mode, '--language', language])
                    (vault / 'my-note.md').write_text('My own content\n')
                    before = snapshot(vault)
                    shell = ['bash', str(ROOT / 'install.sh'), '--source', str(ROOT), '--update', str(vault)]
                    self.run_ok(shell + ['--dry-run'])
                    self.assertEqual(snapshot(vault), before)
                    message = self.run_ok(shell)
                    self.assertEqual(snapshot(vault), before, 'Default update must not change profiles or introduce directories')
                    self.assertIn('--mode ' + mode if mode == 'shared-core' else '--mode "' + mode + '"', message)
                    if language == 'zh-CN':
                        self.assertIn('90-系统/脚本/kb.py', message)
                        self.assertFalse((vault / 'index.md').exists())
                        self.assertFalse((vault / '00-AI').exists())
                    self.run_ok([sys.executable, str(CLI), 'upgrade-core', str(vault)])
                    self.assertEqual(snapshot(vault), before)
                    if mode != 'shared-core':
                        self.run_ok(shell + ['--language', language])
                        self.run_ok(shell + ['--mode', mode])
                        self.assertEqual(snapshot(vault), before)

    def test_unknown_profile_does_not_guess_or_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / 'my-note.md').write_text('Keep this\n')
            before = snapshot(vault)
            result = subprocess.run(['bash', str(ROOT / 'install.sh'), '--source', str(ROOT), '--update', str(vault)],
                                    capture_output=True, text=True, env=ENV)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('cannot infer installed mode', result.stdout + result.stderr)
            self.assertEqual(snapshot(vault), before)
