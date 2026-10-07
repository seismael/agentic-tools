"""Tests for tools/vendor_loop_runner.py (pinned vendoring + drift detection)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import vendor_loop_runner as vendor  # noqa: E402


class TestVendorLoopRunner(unittest.TestCase):
    def test_vendor_then_check_is_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(vendor.vendor(target), 0)
            self.assertTrue((target / "loop_runner" / "supervisor.py").is_file())
            self.assertTrue((target / vendor.MANIFEST).is_file())
            self.assertEqual(vendor.check(target), 0)

    def test_check_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            vendor.vendor(target)
            edited = target / "loop_runner" / "supervisor.py"
            edited.write_text(
                edited.read_text(encoding="utf-8") + "\n# hand edit\n", encoding="utf-8"
            )
            self.assertEqual(vendor.check(target), 1)

    def test_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            vendor.vendor(target)
            with self.assertRaises(ValueError):
                vendor.vendor(target)


if __name__ == "__main__":
    unittest.main()
