#!/usr/bin/env python3
"""
Generate SVG sentence diagrams from bracket notation.

This script reads diagram specifications from documents/diagram_sources.txt
and generates SVG files in assets/diagrams/.

Style matches instructor conventions:
- Blue text for category labels (S, NP, VP, etc.)
- Green text for terminal words
- Clean tree structure with connecting lines
"""

import os
import re
import sys
from pathlib import Path

try:
    import svgling
    from svgling import draw_tree
    HAS_SVGLING = True
except ImportError:
    HAS_SVGLING = False
    print("Warning: svgling not installed. Run: pip install svgling")

# Project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
SOURCES_FILE = PROJECT_DIR / "documents" / "diagram_sources.txt"
OUTPUT_DIR = PROJECT_DIR / "assets" / "diagrams"

# Style configuration matching instructor's diagrams
STYLE_CONFIG = {
    'node_color': '#0000FF',      # Blue for category labels
    'leaf_color': '#008000',       # Green for terminal words
    'line_color': '#000000',       # Black for lines
    'font_family': 'Arial, sans-serif',
    'font_size': 14,
}


def parse_bracket_notation(bracket_str):
    """Parse bracket notation into nested tuple structure for svgling."""
    bracket_str = bracket_str.strip()

    # Simple recursive parser
    def parse(s, pos=0):
        if pos >= len(s):
            return None, pos

        # Skip whitespace
        while pos < len(s) and s[pos].isspace():
            pos += 1

        if pos >= len(s):
            return None, pos

        if s[pos] == '[':
            pos += 1  # Skip '['

            # Get the label
            label_start = pos
            while pos < len(s) and s[pos] not in '[] \t\n':
                pos += 1
            label = s[label_start:pos]

            # Skip whitespace
            while pos < len(s) and s[pos].isspace():
                pos += 1

            children = []
            while pos < len(s) and s[pos] != ']':
                if s[pos] == '[':
                    child, pos = parse(s, pos)
                    if child:
                        children.append(child)
                else:
                    # Terminal word
                    word_start = pos
                    while pos < len(s) and s[pos] not in '[] \t\n':
                        pos += 1
                    word = s[word_start:pos]
                    if word:
                        children.append(word)

                # Skip whitespace
                while pos < len(s) and s[pos].isspace():
                    pos += 1

            if pos < len(s) and s[pos] == ']':
                pos += 1  # Skip ']'

            if children:
                return (label, *children), pos
            else:
                return label, pos

        return None, pos

    result, _ = parse(bracket_str)
    return result


def parse_source_file(filepath):
    """Parse the diagram source file and extract all diagram specifications."""
    diagrams = []
    current_chapter = None
    current_diagram = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            # Chapter header
            if line.startswith('### '):
                current_chapter = line[4:].strip()
                continue

            # Diagram ID
            if line.startswith('# diagram_id:'):
                if current_diagram and current_diagram.get('bracket'):
                    diagrams.append(current_diagram)
                current_diagram = {
                    'id': line.split(':')[1].strip(),
                    'chapter': current_chapter,
                    'caption': '',
                    'bracket': ''
                }
                continue

            # Caption
            if line.startswith('# caption:') and current_diagram:
                current_diagram['caption'] = line.split(':', 1)[1].strip()
                continue

            # Skip other comments
            if line.startswith('#'):
                continue

            # Empty line - might end current diagram
            if not line.strip():
                if current_diagram and current_diagram.get('bracket'):
                    diagrams.append(current_diagram)
                    current_diagram = None
                continue

            # Bracket notation line
            if line.strip().startswith('[') and current_diagram:
                current_diagram['bracket'] = line.strip()

    # Don't forget the last diagram
    if current_diagram and current_diagram.get('bracket'):
        diagrams.append(current_diagram)

    return diagrams


def generate_svg_with_svgling(bracket_str, output_path, diagram_id):
    """Generate SVG using svgling library."""
    tree = parse_bracket_notation(bracket_str)
    if not tree:
        print(f"  Error: Could not parse bracket notation for {diagram_id}")
        return False

    try:
        # Create the tree drawing
        drawing = draw_tree(tree)

        # Get SVG content
        svg_content = drawing._repr_svg_()

        # Apply custom styling
        svg_content = apply_custom_styling(svg_content)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return True
    except Exception as e:
        print(f"  Error generating {diagram_id}: {e}")
        return False


def apply_custom_styling(svg_content):
    """Apply instructor's style conventions to SVG."""
    # Add CSS styling for colors
    style_css = '''
    <style>
        text.nltk-tree-node { fill: #0000FF; font-family: Arial, sans-serif; }
        text.nltk-tree-leaf { fill: #008000; font-family: Arial, sans-serif; }
        line { stroke: #000000; }
    </style>
    '''

    # Insert style after opening svg tag
    svg_content = re.sub(
        r'(<svg[^>]*>)',
        r'\1\n' + style_css,
        svg_content,
        count=1
    )

    return svg_content


def generate_simple_svg(bracket_str, output_path, diagram_id):
    """Generate a simple SVG without svgling (fallback)."""
    tree = parse_bracket_notation(bracket_str)
    if not tree:
        print(f"  Error: Could not parse bracket notation for {diagram_id}")
        return False

    # Simple SVG generation (basic implementation)
    # This is a fallback if svgling is not available

    def get_tree_dimensions(node, depth=0):
        """Calculate dimensions needed for the tree."""
        if isinstance(node, str):
            return 1, depth

        label, *children = node
        if not children:
            return 1, depth

        total_width = 0
        max_depth = depth
        for child in children:
            w, d = get_tree_dimensions(child, depth + 1)
            total_width += w
            max_depth = max(max_depth, d)

        return max(1, total_width), max_depth

    width, depth = get_tree_dimensions(tree)
    svg_width = max(200, width * 80)
    svg_height = max(100, (depth + 1) * 60 + 40)

    elements = []

    def draw_node(node, x, y, available_width):
        """Recursively draw tree nodes."""
        if isinstance(node, str):
            # Terminal node (leaf)
            elements.append(
                f'<text x="{x}" y="{y}" text-anchor="middle" '
                f'fill="#008000" font-family="Arial" font-size="14">{node}</text>'
            )
            return

        label, *children = node

        # Draw label
        elements.append(
            f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'fill="#0000FF" font-family="Arial" font-size="14">{label}</text>'
        )

        if not children:
            return

        # Calculate child positions
        num_children = len(children)
        child_width = available_width / num_children
        start_x = x - available_width / 2 + child_width / 2
        child_y = y + 50

        for i, child in enumerate(children):
            child_x = start_x + i * child_width

            # Draw line to child
            elements.append(
                f'<line x1="{x}" y1="{y + 5}" x2="{child_x}" y2="{child_y - 15}" '
                f'stroke="#000000" stroke-width="1"/>'
            )

            # Draw child
            draw_node(child, child_x, child_y, child_width)

    draw_node(tree, svg_width / 2, 30, svg_width - 40)

    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">
  <rect width="100%" height="100%" fill="white"/>
  {''.join(elements)}
</svg>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    return True


def generate_all_diagrams():
    """Generate all diagrams from the source file."""
    if not SOURCES_FILE.exists():
        print(f"Source file not found: {SOURCES_FILE}")
        print("Please create the diagram source file first.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    diagrams = parse_source_file(SOURCES_FILE)
    print(f"Found {len(diagrams)} diagrams to generate")

    successful = 0
    failed = 0

    for diagram in diagrams:
        diagram_id = diagram['id']
        bracket = diagram['bracket']
        output_path = OUTPUT_DIR / f"{diagram_id}.svg"

        print(f"Generating: {diagram_id}")

        if HAS_SVGLING:
            success = generate_svg_with_svgling(bracket, output_path, diagram_id)
        else:
            success = generate_simple_svg(bracket, output_path, diagram_id)

        if success:
            successful += 1
            print(f"  Created: {output_path.name}")
        else:
            failed += 1

    print(f"\nGeneration complete:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")

    # Generate manifest
    manifest_path = OUTPUT_DIR / "manifest.txt"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# Diagram Manifest\n")
        f.write(f"# Generated diagrams: {successful}\n\n")
        for diagram in diagrams:
            svg_path = OUTPUT_DIR / f"{diagram['id']}.svg"
            if svg_path.exists():
                f.write(f"{diagram['id']}: {diagram.get('caption', '')}\n")

    print(f"Manifest written to: {manifest_path}")


if __name__ == '__main__':
    generate_all_diagrams()
