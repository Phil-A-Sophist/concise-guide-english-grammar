#!/usr/bin/env python3
"""
Remove italics from language examples in PreTeXt source files - Version 2.

Enhanced script that handles more complex patterns including:
1. Multiple italicized items in table cells
2. Word examples in prose (the word <em>X</em>)
3. Lists of examples separated by commas

Preserves italics for:
- Section/test labels (e.g., "Test 1: Plural formation")
- Emphasis within sentences (e.g., "look like" where look is emphasized)
- Form/function questions
"""

import re
from pathlib import Path

SOURCE_DIR = Path(__file__).parent.parent / "pretext" / "source"


def remove_em_in_cells_multi(content: str) -> tuple[str, int]:
    """Remove <em> tags from table cells, handling multiple examples."""
    # Pattern: cell content with one or more <em>word</em> patterns
    def replace_cell(match):
        cell_content = match.group(1)
        # Remove all <em></em> tags within the cell
        cleaned = re.sub(r'<em>([^<]+)</em>', r'\1', cell_content)
        return f'<cell>{cleaned}</cell>'

    pattern = r'<cell>((?:[^<]*<em>[^<]+</em>[^<]*)+)</cell>'
    new_content, count = re.subn(pattern, replace_cell, content)
    return new_content, count


def remove_em_word_examples(content: str) -> tuple[str, int]:
    """Remove <em> from 'the word X' patterns."""
    # "the word <em>X</em>" or "words like <em>X</em>"
    patterns = [
        (r'the word <em>([^<]+)</em>', r'the word \1'),
        (r'the words <em>([^<]+)</em>', r'the words \1'),
        (r'words like <em>([^<]+)</em>', r'words like \1'),
        (r'word <em>([^<]+)</em> (is|are|can|names|means)', r'word \1 \2'),
    ]

    total_count = 0
    for pattern, replacement in patterns:
        content, count = re.subn(pattern, replacement, content)
        total_count += count

    return content, total_count


def remove_em_in_parentheses(content: str) -> tuple[str, int]:
    """Remove <em> from examples in parentheses like (the <em>destruction</em>)."""
    # Patterns like (the <em>word</em>) or (<em>word</em>)
    def replace_paren(match):
        paren_content = match.group(1)
        cleaned = re.sub(r'<em>([^<]+)</em>', r'\1', paren_content)
        return f'({cleaned})'

    pattern = r'\(([^)]*<em>[^<]+</em>[^)]*)\)'
    new_content, count = re.subn(pattern, replace_paren, content)
    return new_content, count


def remove_em_arrow_examples(content: str) -> tuple[str, int]:
    """Remove <em> from arrow examples like <em>book</em> → <em>books</em>."""
    # Pattern: <em>X</em> → <em>Y</em>
    pattern = r'<em>([^<]+)</em>(\s*→\s*)<em>([^<]+)</em>'
    replacement = r'\1\2\3'
    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count


def remove_em_colon_examples(content: str) -> tuple[str, int]:
    """Remove <em> after colons introducing examples."""
    # Pattern: ": <em>X</em>, <em>Y</em>" etc.
    def replace_after_colon(match):
        text = match.group(0)
        # Only process if it looks like a list of examples
        if text.count('<em>') >= 2:
            return re.sub(r'<em>([^<]+)</em>', r'\1', text)
        return text

    # Match colon followed by space and italicized content
    pattern = r': <em>[^<]+</em>(?:,\s*<em>[^<]+</em>)+'
    new_content, count = re.subn(pattern, replace_after_colon, content)
    return new_content, count


def remove_em_comma_lists(content: str) -> tuple[str, int]:
    """Remove <em> from comma-separated lists of examples."""
    # Pattern: <em>X</em>, <em>Y</em>, <em>Z</em>
    def replace_list(match):
        text = match.group(0)
        return re.sub(r'<em>([^<]+)</em>', r'\1', text)

    # Match 3+ italicized items separated by commas
    pattern = r'<em>[^<]+</em>(?:,\s*<em>[^<]+</em>){2,}'
    new_content, count = re.subn(pattern, replace_list, content)
    return new_content, count


def remove_em_follows_determiner(content: str) -> tuple[str, int]:
    """Remove <em> from patterns like 'the <em>word</em>' or 'a <em>word</em>'."""
    patterns = [
        (r'\bthe <em>([^<]+)</em></em>', r'the \1</em>'),  # nested fix
        (r'\bthe <em>([^<]+)</em>([,\.\)])', r'the \1\2'),
        (r'\ba <em>([^<]+)</em>([,\.\)])', r'a \1\2'),
        (r'\ban <em>([^<]+)</em>([,\.\)])', r'an \1\2'),
    ]

    total_count = 0
    for pattern, replacement in patterns:
        content, count = re.subn(pattern, replacement, content)
        total_count += count

    return content, total_count


def process_chapter5(filepath: Path) -> dict:
    """Special processing for Chapter 5 with its complex patterns."""
    content = filepath.read_text(encoding='utf-8')
    original_count = content.count('<em>')

    counts = {}

    # Apply transformations in order
    content, counts['cells_multi'] = remove_em_in_cells_multi(content)
    content, counts['arrow_examples'] = remove_em_arrow_examples(content)
    content, counts['comma_lists'] = remove_em_comma_lists(content)
    content, counts['word_examples'] = remove_em_word_examples(content)
    content, counts['parentheses'] = remove_em_in_parentheses(content)
    content, counts['colon_examples'] = remove_em_colon_examples(content)

    final_count = content.count('<em>')
    counts['total_removed'] = original_count - final_count

    filepath.write_text(content, encoding='utf-8')
    return counts


def main():
    ch05_path = SOURCE_DIR / "ch-05.ptx"

    print("Processing Chapter 5...")
    print("=" * 50)

    counts = process_chapter5(ch05_path)

    print(f"  Multi-item cells: {counts['cells_multi']}")
    print(f"  Arrow examples: {counts['arrow_examples']}")
    print(f"  Comma-separated lists: {counts['comma_lists']}")
    print(f"  Word examples: {counts['word_examples']}")
    print(f"  Parenthetical examples: {counts['parentheses']}")
    print(f"  Colon examples: {counts['colon_examples']}")
    print("=" * 50)
    print(f"Total <em> tags removed: {counts['total_removed']}")

    # Count remaining
    content = ch05_path.read_text(encoding='utf-8')
    remaining = content.count('<em>')
    print(f"Remaining <em> tags: {remaining}")


if __name__ == "__main__":
    main()
