"""The GitHub-visible kit must work after copying it away from the repository."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DirectVaultTests(unittest.TestCase):
    def test_shipped_kit_matches_installer(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/build_kit.py'), '--check'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_downloaded_folder_is_independently_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / '我的知识库'
            shutil.copytree(ROOT / 'kit', vault, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            self.assertEqual({p.name for p in vault.iterdir() if p.is_dir() and not p.name.startswith('.')},
                             {'00-入口', '01-收件箱', '10-项目', '20-资料', '30-经验资产', '90-系统'})
            self.assertTrue((vault / '首页.md').is_file())
            self.assertFalse((vault / '00-AI').exists())
            metadata = json.loads((vault / '.obsidian-ai-workflow-kit/manifest.json').read_text())
            self.assertEqual((metadata['language'], metadata['mode']), ('zh-CN', 'full'))
            cli = vault / '90-系统/脚本/kb.py'
            for arguments in [('health-check', '--vault', str(vault)),
                              ('new-project', 'direct-demo', '--name', '直接打开项目', '--vault', str(vault))]:
                result = subprocess.run([sys.executable, '-B', str(cli), *arguments], cwd=tmp,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((vault / '10-项目/direct-demo/BRIDGE-direct-demo.md').is_file())
