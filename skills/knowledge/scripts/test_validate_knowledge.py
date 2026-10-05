"""Unit tests for validate_knowledge.py."""

from pathlib import Path
import tempfile
import unittest

from validate_knowledge import (
    MAX_INDEX_BYTES,
    MAX_LEAF_BYTES,
    extract_links,
    validate_knowledge_base,
)


class TestValidateKnowledge(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kb_dir = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_extract_links(self) -> None:
        text = (
            "See [Architecture](architecture.md) and [[data_topology]] for details. "
            "Also check [[invariants|System Invariants]] and external [Docs](https://example.com)."
        )
        links = extract_links(text)
        self.assertIn("architecture.md", links)
        self.assertIn("data_topology.md", links)
        self.assertIn("invariants.md", links)
        self.assertNotIn("https://example.com", links)

    def test_valid_knowledge_base(self) -> None:
        (self.kb_dir / "index.md").write_text(
            "# MOC\n- [Arch](architecture.md)\n- [[data_topology]]", encoding="utf-8"
        )
        (self.kb_dir / "architecture.md").write_text(
            "# Architecture\n[[index]]", encoding="utf-8"
        )
        (self.kb_dir / "data_topology.md").write_text(
            "# Data Topology\n[[index]]", encoding="utf-8"
        )

        errors = validate_knowledge_base(self.kb_dir)
        self.assertEqual(errors, [])

    def test_missing_index(self) -> None:
        (self.kb_dir / "architecture.md").write_text("# Architecture", encoding="utf-8")
        errors = validate_knowledge_base(self.kb_dir)
        self.assertTrue(any("Missing index.md" in e for e in errors))

    def test_index_size_limit(self) -> None:
        large_content = "# MOC\n" + ("x" * (MAX_INDEX_BYTES + 10))
        (self.kb_dir / "index.md").write_text(large_content, encoding="utf-8")
        errors = validate_knowledge_base(self.kb_dir)
        self.assertTrue(any("index.md exceeds byte ceiling" in e for e in errors))

    def test_leaf_size_limit(self) -> None:
        (self.kb_dir / "index.md").write_text("# MOC\n- [[leaf]]", encoding="utf-8")
        large_leaf = "# Leaf\n" + ("y" * (MAX_LEAF_BYTES + 10))
        (self.kb_dir / "leaf.md").write_text(large_leaf, encoding="utf-8")
        errors = validate_knowledge_base(self.kb_dir)
        self.assertTrue(any("leaf.md exceeds leaf byte ceiling" in e for e in errors))

    def test_broken_link(self) -> None:
        (self.kb_dir / "index.md").write_text("# MOC\n- [[missing_leaf]]", encoding="utf-8")
        errors = validate_knowledge_base(self.kb_dir)
        self.assertTrue(any("Broken link" in e and "missing_leaf.md" in e for e in errors))

    def test_orphan_leaf(self) -> None:
        (self.kb_dir / "index.md").write_text("# MOC\n", encoding="utf-8")
        (self.kb_dir / "orphan.md").write_text("# Orphan", encoding="utf-8")
        errors = validate_knowledge_base(self.kb_dir)
        self.assertTrue(any("Orphan leaf: 'orphan.md'" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
