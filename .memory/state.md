# Project State

Task: 3
Last updated: 2026-02-11

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Formatting consistency audit (completed):** Chapters 5 and 6 audited for formatting consistency. All `<em>~~...~~</em>` patterns removed in both files. Ch-05: 168 remaining `<em>` tags (all legitimate). Ch-06: 105 remaining `<em>` tags (all legitimate). Style guide updated. Zero nested `<em>` tags remain. Working copy also includes earlier `<paragraphs>` to `<figure>` conversion changes that are not yet committed.
- **Figure element conversion:** Converting diagram labels from `<paragraphs>` elements to proper `<figure>` elements in chapters 5 and 6. Already done in working copy (unstaged). CSS in `build.py` needs updating to match.
- **Chapter 6 Homework Revision:** Script `scripts/generate_ch06_homework.py` generates updated Homework, Answer Key, and Overhead files.
- **Homework format standardization:** A README.md in `Homework/` documents the standard formats.

## Open Questions
- Answer keys exist only for Chapters 4-15; Chapters 1-3 and 16-21 may still need them
- The REVISION_AUDIT.md references an older 27-chapter structure; not updated to reflect current 21-chapter organization
- The `<paragraphs>` to `<figure>` conversion will need to be applied to chapters 7-16
- Strikethrough example formatting (em-wrapped vs plain) confirmed still present in chapters 7-21 (ch-08, ch-09, ch-10, ch-11, ch-12, ch-13, ch-14, ch-16, ch-18, ch-19, ch-21)
- The working copy has extensive uncommitted changes across both PTX and HTML files

## Recent Direction
- Style guide now explicitly states: do NOT use italics for linguistic examples
- Formatting consistency work focuses on removing `<em>` from: strikethrough examples, morpheme/affix labels, and linguistic examples in lists
- Legitimate `<em>` uses preserved: technical terms, category labels, test labels, emphasis, figure captions
