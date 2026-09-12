#!/usr/bin/env python3
"""Build/check the ready-to-open Chinese vault from the maintained installer."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = '90-系统/配置/kit-manifest.json'
LEGACY_MANIFEST = '.obsidian-ai-workflow-kit/manifest.json'


def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.name != '.DS_Store'}


def comparable(mapping):
    result = dict(mapping)
    if MANIFEST in result:
        manifest = json.loads(result[MANIFEST])
        manifest.pop('updated_at', None)
        result[MANIFEST] = json.dumps(manifest, sort_keys=True).encode()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare without writing')
    args = parser.parse_args()
    target = ROOT / 'kit'
    with tempfile.TemporaryDirectory(prefix='kb-build-') as tmp:
        generated = Path(tmp) / 'vault'
        subprocess.run([sys.executable, '-B', str(ROOT / 'src/00-AI/scripts/kb.py'),
                        'install-core', str(generated), '--language', 'zh-CN', '--mode', 'full'],
                       check=True, stdout=subprocess.DEVNULL)
        wanted, current = files(generated), files(target)
        if comparable(wanted) == comparable(current):
            print('PASS kit/ matches the Chinese full installation')
            return 0
        different = sorted(p for p in wanted.keys() | current.keys()
                           if comparable(wanted).get(p) != comparable(current).get(p))
        if args.check:
            print('FAIL kit/ differs from installer output; run python3 scripts/build_kit.py')
            print('\n'.join(different))
            return 1
        # Refuse to overwrite work someone has added to or edited in a copied kit.
        old = json.loads(current.get(MANIFEST, current.get(LEGACY_MANIFEST, b'{"files":{}}'))).get('files', {})
        unsafe = [p for p, data in current.items() if p not in {MANIFEST, LEGACY_MANIFEST} and p in different
                  and hashlib.sha256(data).hexdigest() != old.get(p, {}).get('sha256')]
        if unsafe:
            raise SystemExit('Refusing to replace user-modified/unmanaged files:\n' + '\n'.join(unsafe))
        for name in different:
            path = target / name
            if name in wanted:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(wanted[name])
            else:
                path.unlink()
                parent = path.parent
                while parent != target:
                    try:
                        parent.rmdir()
                    except OSError:
                        break
                    parent = parent.parent
        print(f'Built kit/: {len(different)} changed files; open kit/ in Obsidian')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
