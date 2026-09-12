import argparse
import contextlib
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kit" / "00-AI" / "scripts"))
from kb.records import check_record, record_findings


class CompactRecordTests(unittest.TestCase):
    def test_unicode_budget_excludes_metadata_but_catches_long_single_line(self):
        metadata = {"type": "project-bridge"}
        text = "---\ntype: project-bridge\nnote: " + "界" * 500 + "\n---\n" + "界" * 3000
        self.assertEqual(record_findings(metadata, text), ([], []))
        errors, _ = record_findings(metadata, text + "界")
        self.assertTrue(any("chars=3001/3000" in error for error in errors))

    def test_handoff_limit_and_visible_exception(self):
        metadata = {"type": "agent-handoff", "compact_exception": "Unresolved incident boundaries require a longer summary."}
        errors, warnings = record_findings(metadata, "x" * 1801)
        self.assertFalse(errors)
        self.assertTrue(any("exception requires review" in warning for warning in warnings))
        del metadata["compact_exception"]
        self.assertTrue(record_findings(metadata, "x" * 1801)[0])

    def test_line_limit_counts_nonblank_lines(self):
        self.assertFalse(record_findings({"type": "agent-handoff"}, "x\n\n" * 80)[0])
        self.assertTrue(record_findings({"type": "agent-handoff"}, "x\n\n" * 81)[0])

    def test_duplicate_actions_history_and_mirror_mismatch(self):
        errors, _ = record_findings({"type": "project-bridge", "next_action": "Review"}, "## 下次开工\n首要动作：Deploy\n## 当前下一步\nOther\n## 验证记录\nHistory")
        self.assertEqual(len(errors), 3)

    def test_code_example_is_not_an_action_section(self):
        errors, _ = record_findings({"type": "project-bridge", "next_action": "Review"}, "## Next action\nPrimary action: Review\n```md\n## Next action\nPrimary action: Other\n```\n")
        self.assertFalse(errors)

    def test_cli_rejects_bad_record_without_rewriting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bridge.md"
            path.write_text('---\ntype: project-bridge\nstatus: "active"\nnext_action: Review\n---\n## Next action\nPrimary action: Deploy\n')
            original = hashlib.sha256(path.read_bytes()).digest()
            with contextlib.redirect_stdout(io.StringIO()):
                result = check_record(argparse.Namespace(paths=[str(path)]))
            self.assertEqual(result, 1)
            self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), original)

    def test_compact_format_requires_action_and_bounds_dependencies(self):
        metadata = {"type": "project-bridge", "record_format": "compact-v1", "next_action": "Review"}
        self.assertTrue(record_findings(metadata, "## Current state\nUnchanged")[0])
        text = "## Next action\nPrimary action: Review\n- First dependency\n- Second dependency\n"
        self.assertFalse(record_findings(metadata, text)[0])
        self.assertTrue(record_findings(metadata, text + "- Third dependency\n")[0])

    def test_cli_handles_quoted_hash_and_rejects_yaml_log(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bridge.md"
            prefix = '---\ntype: project-bridge\nnext_action: "Review issue #123" # actual comment\n'
            body = '---\n## Next action\nPrimary action: Review issue #123\n'
            path.write_text(prefix + body)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check_record(argparse.Namespace(paths=[str(path)])), 0)
                path.write_text(prefix + 'notes: |\n  ' + 'x' * 4000 + '\n' + body)
                self.assertEqual(check_record(argparse.Namespace(paths=[str(path)])), 1)


if __name__ == "__main__":
    unittest.main()
