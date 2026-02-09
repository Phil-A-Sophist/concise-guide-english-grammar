#!/usr/bin/env python3
"""
Process multiple chapters to remove italics from language examples.
Combines all the patterns from previous scripts.
"""

import re
from pathlib import Path

SOURCE_DIR = Path(__file__).parent.parent / "pretext" / "source"


def remove_em_in_cells(content: str) -> tuple[str, int]:
    """Remove <em> tags from table cells."""
    def replace_cell(match):
        cell_content = match.group(1)
        cleaned = re.sub(r'<em>([^<]+)</em>', r'\1', cell_content)
        return f'<cell>{cleaned}</cell>'

    pattern = r'<cell>((?:[^<]*<em>[^<]+</em>[^<]*)+)</cell>'
    return re.subn(pattern, replace_cell, content)


def remove_em_in_list_items_whole(content: str) -> tuple[str, int]:
    """Remove <em> from list items that are entirely emphasized."""
    pattern = r'<li><p><em>([^<]+)</em></p></li>'
    return re.subn(pattern, r'<li><p>\1</p></li>', content)


def remove_em_at_list_item_start(content: str) -> tuple[str, int]:
    """Remove <em> from the beginning of list items."""
    pattern = r'<li><p><em>([^<]+)</em>(\s*[-–—:,])'
    return re.subn(pattern, r'<li><p>\1\2', content)


def remove_em_arrow_examples(content: str) -> tuple[str, int]:
    """Remove <em> from arrow examples like X → Y."""
    pattern = r'<em>([^<]+)</em>(\s*→\s*)<em>([^<]+)</em>'
    return re.subn(pattern, r'\1\2\3', content)


def remove_em_comma_lists(content: str) -> tuple[str, int]:
    """Remove <em> from comma-separated lists of 3+ examples."""
    def replace_list(match):
        return re.sub(r'<em>([^<]+)</em>', r'\1', match.group(0))

    pattern = r'<em>[^<]+</em>(?:,\s*<em>[^<]+</em>){2,}'
    return re.subn(pattern, replace_list, content)


def remove_em_in_parentheses(content: str) -> tuple[str, int]:
    """Remove <em> from examples in parentheses."""
    def replace_paren(match):
        paren_content = match.group(1)
        cleaned = re.sub(r'<em>([^<]+)</em>', r'\1', paren_content)
        return f'({cleaned})'

    pattern = r'\(([^)]*<em>[^<]+</em>[^)]*)\)'
    return re.subn(pattern, replace_paren, content)


def fix_nested_em_short(content: str) -> tuple[str, int]:
    """Fix short nested patterns like <em>the <em>word</em></em>."""
    patterns = [
        (r'<em>the <em>([^<]+)</em></em>', r'the \1'),
        (r'<em>a <em>([^<]+)</em></em>', r'a \1'),
        (r'<em>an <em>([^<]+)</em></em>', r'an \1'),
        (r'<em>every <em>([^<]+)</em></em>', r'every \1'),
        (r'<em><em>([^<]+)</em> ([^<]+)</em>', r'\1 \2'),
    ]

    total = 0
    for pattern, replacement in patterns:
        content, count = re.subn(pattern, replacement, content)
        total += count
    return content, total


def fix_nested_em_sentences(content: str) -> tuple[str, int]:
    """Fix example sentences with nested em."""
    pattern = r'<em>([A-Z][^<]*<em>[^<]+</em>[^<]*[.!?])</em>'

    def replace_sentence(match):
        return f'"{match.group(1)}"'

    return re.subn(pattern, replace_sentence, content)


def fix_det_adj_noun(content: str) -> tuple[str, int]:
    """Fix patterns like <em>the <em>tall</em> man</em>."""
    pattern = r'<em>(the|a|an) <em>([^<]+)</em> ([^<]+)</em>'

    def replace_pattern(match):
        return f'{match.group(1)} {match.group(2)} {match.group(3)}'

    return re.subn(pattern, replace_pattern, content)


def fix_remaining_nested(content: str) -> tuple[str, int]:
    """Fix any remaining simple nested patterns."""
    pattern = r'<em>([^<]+) <em>([^<]+)</em></em>'

    def replace_nested(match):
        part1 = match.group(1)
        part2 = match.group(2)
        combined = f'{part1} {part2}'
        if part1[0].isupper() and part2[-1] in '.!?':
            return f'"{combined}"'
        return combined

    return re.subn(pattern, replace_nested, content)


def process_chapter(filepath: Path) -> dict:
    """Process a single chapter file."""
    content = filepath.read_text(encoding='utf-8')
    original_count = content.count('<em>')

    # Apply all transformations (multiple passes for nested patterns)
    for _ in range(3):
        content, _ = remove_em_in_cells(content)
        content, _ = remove_em_in_list_items_whole(content)
        content, _ = remove_em_at_list_item_start(content)
        content, _ = remove_em_arrow_examples(content)
        content, _ = remove_em_comma_lists(content)
        content, _ = remove_em_in_parentheses(content)
        content, _ = fix_nested_em_short(content)
        content, _ = fix_nested_em_sentences(content)
        content, _ = fix_det_adj_noun(content)
        content, _ = fix_remaining_nested(content)

    final_count = content.count('<em>')
    removed = original_count - final_count

    filepath.write_text(content, encoding='utf-8')

    return {
        'original': original_count,
        'final': final_count,
        'removed': removed
    }


def main(chapters: list[int]):
    """Process specified chapters."""
    print("Processing chapters...")
    print("=" * 50)

    total_removed = 0

    for ch_num in chapters:
        filename = f"ch-{ch_num:02d}.ptx"
        filepath = SOURCE_DIR / filename

        if not filepath.exists():
            print(f"  {filename}: not found")
            continue

        result = process_chapter(filepath)
        total_removed += result['removed']

        print(f"  {filename}: {result['original']} -> {result['final']} ({result['removed']} removed)")

    print("=" * 50)
    print(f"Total removed: {total_removed}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapters = [int(x) for x in sys.argv[1:]]
    else:
        chapters = list(range(6, 11))  # Default: chapters 6-10

    main(chapters)
