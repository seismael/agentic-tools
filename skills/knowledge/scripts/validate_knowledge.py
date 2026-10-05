#!/usr/bin/env python3
"""Deterministic validator for project knowledge bases (Obsidian/Markdown wikis).

Usage:
    python validate_knowledge.py <path_to_knowledge_dir>

Checks:
    - index.md exists and acts as Map of Content (MOC).
    - File size limits: index.md <= 2,048 bytes; other leaves <= 3,072 bytes.
    - Link integrity: all [target](path.md) and [[wikilinks]] resolve to existing files.
    - Orphan check: all markdown files in the directory must be linked from index.md.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys

MAX_INDEX_BYTES = 2048
MAX_LEAF_BYTES = 3072

MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)(?:#[^)]+)?\)")
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


class KnowledgeValidationError(ValueError):
    """Validation failure in knowledge base structure."""


def extract_links(content: str) -> set[str]:
    """Extract referenced filenames from both markdown and wikilinks."""
    targets = set()
    for _, md_path in MD_LINK_PATTERN.findall(content):
        # Ignore external URLs
        if not (md_path.startswith("http://") or md_path.startswith("https://")):
            targets.add(Path(md_path).name)

    for wiki_target in WIKI_LINK_PATTERN.findall(content):
        name = wiki_target.strip()
        if not name.endswith(".md"):
            name = f"{name}.md"
        targets.add(name)

    return targets


def validate_knowledge_base(directory: Path | str) -> list[str]:
    """Validate a knowledge base directory. Returns list of errors (empty if valid)."""
    kb_dir = Path(directory).resolve()
    errors: list[str] = []

    if not kb_dir.is_dir():
        return [f"Directory not found: {kb_dir}"]

    index_path = kb_dir / "index.md"
    if not index_path.is_file():
        return [f"Missing index.md (Map of Content) in {kb_dir}"]

    all_md_files = {p.name: p for p in kb_dir.glob("*.md")}
    
    # Check size limits
    index_size = index_path.stat().st_size
    if index_size > MAX_INDEX_BYTES:
        errors.append(
            f"index.md exceeds byte ceiling: {index_size} bytes (limit {MAX_INDEX_BYTES} bytes)"
        )

    for name, path in all_md_files.items():
        if name == "index.md":
            continue
        size = path.stat().st_size
        if size > MAX_LEAF_BYTES:
            errors.append(
                f"{name} exceeds leaf byte ceiling: {size} bytes (limit {MAX_LEAF_BYTES} bytes)"
            )

    # Check index links to all leaves
    index_content = index_path.read_text(encoding="utf-8")
    index_targets = extract_links(index_content)

    for name in all_md_files:
        if name != "index.md" and name not in index_targets:
            errors.append(f"Orphan leaf: '{name}' is not indexed in index.md")

    # Check bidirectional link integrity across all leaves
    for name, path in all_md_files.items():
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"File {name} is not valid UTF-8")
            continue

        targets = extract_links(content)
        for target in targets:
            if target not in all_md_files:
                errors.append(f"Broken link in {name}: target '{target}' does not exist")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Project Knowledge Base.")
    parser.add_argument("directory", help="Path to knowledge directory")
    args = parser.parse_args()

    errors = validate_knowledge_base(args.directory)
    if errors:
        print("KNOWLEDGE BASE VALIDATION FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - ERROR: {err}", file=sys.stderr)
        return 1

    print("VALID: Knowledge base adheres to token-efficient MOC structure and link integrity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
