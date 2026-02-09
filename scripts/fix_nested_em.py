#!/usr/bin/env python3
"""
Fix nested <em> tags in Chapter 5.

Patterns:
1. Short phrase examples: <em>the <em>word</em></em> → the word (plain)
2. Example sentences: <em>Sentence with <em>word</em>.</em> → "Sentence with <em>word</em>."
3. List items with just phrases: remove outer em, keep inner for emphasis if meaningful
"""

import re
from pathlib import Path

SOURCE_DIR = Path(__file__).parent.parent / "pretext" / "source"


def fix_short_phrase_examples(content: str) -> tuple[str, int]:
    """Fix patterns like <em>the <em>word</em></em> → the word."""
    # These are short examples where the whole thing is a phrase, not a sentence
    # Pattern: <em>determiner <em>word</em></em> or <em><em>word</em> word</em>

    # Simple determiner + word patterns
    patterns = [
        # <em>the <em>word</em></em> → the word
        (r'<em>the <em>([^<]+)</em></em>', r'the \1'),
        # <em>a <em>word</em></em> → a word
        (r'<em>a <em>([^<]+)</em></em>', r'a \1'),
        # <em>an <em>word</em></em> → an word
        (r'<em>an <em>([^<]+)</em></em>', r'an \1'),
        # <em>every <em>word</em></em> → every word
        (r'<em>every <em>([^<]+)</em></em>', r'every \1'),
        # <em><em>word</em> word</em> → word word (for patterns like "very tall")
        (r'<em><em>([^<]+)</em> ([^<]+)</em>', r'\1 \2'),
    ]

    total = 0
    for pattern, replacement in patterns:
        content, count = re.subn(pattern, replacement, content)
        total += count

    return content, total


def fix_sentence_examples(content: str) -> tuple[str, int]:
    """Fix example sentences: <em>Sentence with <em>word</em>.</em> → "Sentence with <em>word</em>." """
    # Match sentences (ending with period, question mark, etc.)
    pattern = r'<em>([A-Z][^<]*<em>[^<]+</em>[^<]*[.!?])</em>'

    def replace_sentence(match):
        inner = match.group(1)
        return f'"{inner}"'

    content, count = re.subn(pattern, replace_sentence, content)
    return content, count


def fix_phrase_with_pp(content: str) -> tuple[str, int]:
    """Fix phrases with prepositional phrases like <em>word <em>of phrase</em></em>."""
    # Pattern: <em>word <em>prep phrase</em></em>
    pattern = r'<em>([a-z]+) <em>([^<]+)</em></em>'

    def replace_phrase(match):
        word1 = match.group(1)
        word2 = match.group(2)
        return f'{word1} {word2}'

    content, count = re.subn(pattern, replace_phrase, content)
    return content, count


def fix_determiner_adj_noun(content: str) -> tuple[str, int]:
    """Fix patterns like <em>the <em>tall</em> man</em> → the tall man."""
    pattern = r'<em>(the|a|an) <em>([^<]+)</em> ([^<]+)</em>'

    def replace_pattern(match):
        det = match.group(1)
        adj = match.group(2)
        noun = match.group(3)
        return f'{det} {adj} {noun}'

    content, count = re.subn(pattern, replace_pattern, content)
    return content, count


def fix_remaining_nested(content: str) -> tuple[str, int]:
    """Fix any remaining simple nested patterns."""
    # <em>X <em>Y</em></em> where X and Y are simple words/phrases
    pattern = r'<em>([^<]+) <em>([^<]+)</em></em>'

    def replace_nested(match):
        part1 = match.group(1)
        part2 = match.group(2)
        # If it looks like a sentence (starts with cap, ends with punctuation), use quotes
        combined = f'{part1} {part2}'
        if part1[0].isupper() and part2[-1] in '.!?':
            return f'"{combined}"'
        return combined

    content, count = re.subn(pattern, replace_nested, content)
    return content, count


def process_file(filepath: Path) -> dict:
    """Process the file through multiple passes."""
    content = filepath.read_text(encoding='utf-8')
    original_count = content.count('<em>')

    counts = {}

    # Multiple passes to handle nested patterns
    for pass_num in range(3):
        content, c1 = fix_short_phrase_examples(content)
        content, c2 = fix_determiner_adj_noun(content)
        content, c3 = fix_sentence_examples(content)
        content, c4 = fix_phrase_with_pp(content)
        content, c5 = fix_remaining_nested(content)

        if pass_num == 0:
            counts = {
                'short_phrases': c1,
                'det_adj_noun': c2,
                'sentences': c3,
                'phrase_pp': c4,
                'remaining_nested': c5,
            }
        else:
            counts['short_phrases'] += c1
            counts['det_adj_noun'] += c2
            counts['sentences'] += c3
            counts['phrase_pp'] += c4
            counts['remaining_nested'] += c5

    final_count = content.count('<em>')
    counts['total_removed'] = original_count - final_count

    filepath.write_text(content, encoding='utf-8')
    return counts


def main():
    ch05_path = SOURCE_DIR / "ch-05.ptx"

    print("Fixing nested <em> tags in Chapter 5...")
    print("=" * 50)

    counts = process_file(ch05_path)

    print(f"  Short phrase examples: {counts['short_phrases']}")
    print(f"  Det + adj + noun patterns: {counts['det_adj_noun']}")
    print(f"  Sentence examples: {counts['sentences']}")
    print(f"  Phrase with PP: {counts['phrase_pp']}")
    print(f"  Other nested: {counts['remaining_nested']}")
    print("=" * 50)
    print(f"Total <em> tags removed: {counts['total_removed']}")

    # Count remaining
    content = ch05_path.read_text(encoding='utf-8')
    remaining = content.count('<em>')
    print(f"Remaining <em> tags: {remaining}")


if __name__ == "__main__":
    main()
