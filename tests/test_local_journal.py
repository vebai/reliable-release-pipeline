"""Test that an unsuccessful promoted candidate is retained after rollback."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from scripts.journal_local import append_event, read_events

ROOT = Path(__file__).resolve().parents[1]
# The writer has a hyphenated filename because it is also a CLI entry point.
spec = importlib.util.spec_from_file_location('make_local_record', ROOT / 'scripts' / 'make-local-record.py')
# Import journal_local from scripts/ for the direct module import used by that CLI.
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)

GOOD = 'sha256:' + 'a' * 64
BAD = 'sha256:' + 'b' * 64


class LocalEvidenceTests(unittest.TestCase):
    def test_full_history_survives_rollback(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = root / '.lab' / 'state'
            evidence = root / '.lab' / 'evidence'
            state.mkdir(parents=True)
            (state / 'last-built').write_text(BAD + '\ncandidate-v2\n')
            (state / 'production.current').write_text(GOOD + '\ngood-v1\n')
            (state / 'production.verified').write_text(GOOD + '\ngood-v1\n')
            (state / 'production.previous-verified').write_text(GOOD + '\ngood-v1\n')
            journal = evidence / 'events.jsonl'
            for event, image, revision, status, note in [
                ('PROMOTE', GOOD, 'good-v1', 'DEPLOYED_UNVERIFIED', 'normal'),
                ('VERIFY', GOOD, 'good-v1', 'PASS', ''),
                ('PROMOTE', BAD, 'candidate-v2', 'DEPLOYED_UNVERIFIED', 'simulated-health-500'),
                ('VERIFY', BAD, 'candidate-v2', 'FAIL', 'http-check-failed'),
                ('RECOVER', GOOD, 'good-v1', 'STARTED', 'compatibility-acknowledged'),
                ('VERIFY', GOOD, 'good-v1', 'PASS', ''),
                ('RECOVER', GOOD, 'good-v1', 'VERIFIED', 'known-good-verified'),
            ]:
                append_event(journal, event, 'production', image, revision, status, note)
            (evidence / 'production-before-rollback.log').write_text('"GET /health HTTP/1.1" 500 -\n')
            record = writer.build_record(root)
            self.assertIn('`candidate-v2`', record)
            self.assertIn('FAIL; http-check-failed', record)
            self.assertIn('VERIFIED; known-good-verified', record)
            self.assertIn('observed HTTP 500 response lines: **1**', record)
            self.assertIn('Currently deployed: `' + GOOD + '` / `good-v1`', record)
            self.assertNotIn('Production approval: approved by protected reviewer', record)

    def test_pre_journal_snapshot_does_not_claim_missing_history(self):
        with tempfile.TemporaryDirectory() as temp:
            record = writer.build_record(Path(temp))
            self.assertIn('No machine-recorded event history exists', record)

    def test_invalid_journal_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'journal.jsonl'
            path.write_text('{not json}\n')
            with self.assertRaisesRegex(ValueError, 'line 1'):
                read_events(path)


if __name__ == '__main__':
    unittest.main()
