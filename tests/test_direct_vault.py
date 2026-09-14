"""The GitHub-visible kit must work after copying it away from the repository."""
import io
import tarfile
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
            self.assertEqual({p.name for p in vault.iterdir()}, {'00-入口', '01-收件箱', '10-项目', '20-资料', '30-经验资产', '90-系统', '首页.md'})
            self.assertTrue((vault / '90-系统/关于/LICENSE').is_file())
            self.assertTrue((vault / '90-系统/接入/AGENTS.md').is_file())
            self.assertFalse((vault / '00-AI').exists())
            metadata = json.loads((vault / '90-系统/配置/kit-manifest.json').read_text())
            self.assertEqual((metadata['language'], metadata['mode']), ('zh-CN', 'full'))
            cli = vault / '90-系统/脚本/kb.py'
            for arguments in [('health-check', '--vault', str(vault)),
                              ('new-project', 'direct-demo', '--name', '直接打开项目', '--vault', str(vault))]:
                result = subprocess.run([sys.executable, '-B', str(cli), *arguments], cwd=tmp,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((vault / '10-项目/direct-demo/BRIDGE-direct-demo.md').is_file())

    def test_upgrade_previous_direct_download_removes_root_clutter(self):
        archive = subprocess.run(['git', 'archive', 'aefd67b:kit'], cwd=ROOT, capture_output=True)
        if archive.returncode:
            self.skipTest('Previous direct-download fixture not available')
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
                bundle.extractall(vault)
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'src/00-AI/scripts/kb.py'),
                                     'upgrade-core', str(vault), '--mode', 'full', '--language', 'zh-CN'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual({p.name for p in vault.iterdir()},
                             {'首页.md', '00-入口', '01-收件箱', '10-项目', '20-资料', '30-经验资产', '90-系统'})
            # Unmodified managed instructions migrate to the current template,
            # which may change between releases; custom-file preservation is
            # covered separately by the upgrade tests.
            self.assertEqual((vault / '90-系统/接入/AGENTS.md').read_bytes(),
                             (ROOT / 'kit/90-系统/接入/AGENTS.md').read_bytes())
            result = subprocess.run([sys.executable, '-B', str(vault / '90-系统/脚本/kb.py'),
                                     'health-check', '--vault', str(vault)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_duplicate_manifests_abort_before_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            shutil.copytree(ROOT / 'kit', vault)
            legacy = vault / '.obsidian-ai-workflow-kit/manifest.json'
            legacy.parent.mkdir()
            legacy.write_text('{"files": {}, "language": "zh-CN", "mode": "full"}')
            before = {str(p.relative_to(vault)): p.read_bytes() for p in vault.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'src/00-AI/scripts/kb.py'),
                                     'upgrade-core', str(vault), '--mode', 'full', '--language', 'zh-CN'],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('multiple kit manifests', result.stdout + result.stderr)
            self.assertEqual(before, {str(p.relative_to(vault)): p.read_bytes() for p in vault.rglob('*') if p.is_file()})
