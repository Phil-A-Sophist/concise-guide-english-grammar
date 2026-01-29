# Diagram Conversion Log

This document tracks the conversion of ASCII diagrams to bracket notation for SVG generation.

## Conversion Summary

- **Date:** 2026-01-12
- **Total diagrams converted:** 64
- **Source:** ASCII tree diagrams in chapter markdown files
- **Target:** Bracket notation in `documents/diagram_sources.txt`

## Chapters Processed

| Chapter | Diagrams Found | Diagrams Converted |
|---------|----------------|-------------------|
| Chapter 4: Morphology | 2 | 2 |
| Chapter 6: Syntax and Diagrams | 14 | 14 |
| Chapter 7: Verbs | 10 | 10 |
| Chapter 8: Nouns | 8 | 8 |
| Chapter 9: Adjectives | 10 | 10 |
| Chapter 10: Adverbs | 9 | 9 |
| Chapter 11: Closed Classes | 6 | 6 |
| Chapter 12: Basic Sentence Elements | 4 | 4 |
| Chapter 16: Auxiliary Verbs | 2 | 2 |
| **Total** | **65** | **64** |

## Interpretation Decisions

### Node Label Standardization

The following labels were standardized across all diagrams:
- `Det` for determiners (articles, demonstratives, possessives)
- `Pro` for pronouns
- `Aux` for auxiliary verbs (be, have, do as helping verbs)
- `Modal` for modal verbs (can, will, must, should, etc.)
- `P` or `Prep` for prepositions (used interchangeably)
- `Conj` for conjunctions
- `Sub` for subordinators (that, if, when in subordinate clauses)

### Structural Decisions

1. **Adverbial clauses**: Represented as `[AdvCl ...]` without internal structure
2. **Relative clauses**: Represented as `[RelCl ...]` without internal structure
3. **Infinitive phrases**: Represented as `[InfP [to] [VP ...]]` or `[InfP [to] [V ...]]`
4. **Coordinated structures**: Explicit `[Conj and]` node between conjuncts

### Diagrams Not Converted

Some ASCII diagrams in the chapters were:
- Incomplete sketches (placeholders)
- Duplicates of other diagrams
- Practice exercises without complete solutions

These were noted but not added to the master source file.

## Files Modified

- `documents/diagram_sources.txt` - Master bracket notation file (created)
- `assets/diagrams/*.svg` - Generated SVG diagrams (64 files)
- `assets/diagrams/manifest.txt` - Diagram manifest (created)

## Verification

All 64 SVG files were successfully generated and verified:
- SVG files render correctly in browser
- CSS styling applies (blue labels, green words)
- Tree structures are accurately represented

## Next Steps

1. Replace ASCII diagrams in markdown chapters with image references
2. Test EPUB generation with new images
3. Verify diagrams display correctly in EPUB reader
