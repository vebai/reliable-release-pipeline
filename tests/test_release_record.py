import tempfile
import unittest
from pathlib import Path
from scripts.record_evidence import append_phase, write_new


class EvidenceTests(unittest.TestCase):
    def test_record_identity_and_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "record.md"
            digest = "sha256:" + ("a" * 64)
            image = "ghcr.io/example/shop-api@" + digest
            write_new(out, "testsha123", image, "https://github.com/example/run/123")
            append_phase(out, "staging", "PASS", image, "staging")
            text = out.read_text()
            self.assertIn("testsha123", text)
            self.assertIn(image, text)
            self.assertIn("STAGING — PASS", text)
            self.assertIn("Security/coverage gates:** Not implemented", text)

    def test_cannot_rewrite_evidence_with_different_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "record.md"
            image1 = "ghcr.io/example/shop-api@sha256:" + ("a" * 64)
            image2 = "ghcr.io/example/shop-api@sha256:" + ("b" * 64)
            write_new(out, "source123", image1, "run-url")
            with self.assertRaises(ValueError):
                append_phase(out, "staging", "PASS", image2, "staging")
            self.assertNotIn("STAGING — PASS", out.read_text())

    def test_reject_incomplete_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                write_new(Path(tmp) / "bad.md", "sha", "ghcr.io/x/app@sha256:deadbeef", "run")

    def test_reject_non_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                write_new(Path(tmp) / "bad.md", "sha", "ghcr.io/x/app:latest", "run")


if __name__ == "__main__":
    unittest.main()
