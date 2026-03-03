# Knowledge Base Archive — 2026

Archived topics from knowledge-base.md (pre-2026-03-03).

## Chapter 7 Major Revision (Task 16)

Complete structural overhaul:
- Replaced ASCII art diagrams with 10 SyntaxTreeHybrid PNG images (ch07_*)
- Standardized all diagram labels to ALL CAPS (DET, PRON, ADJ, ADV, PREP, CONJ, AUX, ADJP, ADVP)
- Renamed "Complements" to "Objects and Complements"
- Added "Sentence Labeling Tables" (MVP concept, Subject/Predicate roles)
- Added "Step-by-Step Sentence Analysis" (top-down and bottom-up parsing)
- Homework Parts 3-5 rewritten: table exercises, diagram+table, structural ambiguity
- 10 new bracket notation entries in `bracket_notations.txt` (old ch07 VP entries preserved — ch-05/10/11 reference them by ID)

## Ch7 Homework Structure (14 Exercises)

- Part 1 (Ex 1-3): Subject and Predicate Identification
- Part 2 (Ex 4-6): Heads and Modifiers
- Part 3 (Ex 7-9): Completing Sentence Tables (pre-merged blanks)
- Part 4 (Ex 10-12): Completing Diagrams and Tables (free-form)
- Part 5 (Ex 13-14): Structural Ambiguity Analysis (Ex13: Groucho Marx joke; Ex14: garden-path sentence, "VP modifying horse" framing)

## MVP Removal (Completed — commits b819566, 6397474)

MVP (Main Verb Phrase) terminology removed from all sources: ch-07.ptx, ch-08.ptx, 6 Homework/Exams files, generate_ch07_answer_key.py. All table cells MVP→VP.

## Chapter Reorganization (27 → 21 Chapters)

Consolidated from 27 to 21 chapters in 6 thematic sections:
Foundations (1-4), Core Grammar (5-9), The Verb System (10-11), Form and Function (12-15), Writing and Style (16-19), Applied Grammar (20-21).
REVISION_AUDIT.md still references old 27-chapter structure — content analysis remains useful.

## Completed Chapter Commit Hashes

- Ch8: 426b103 (213 `<foreign>` instances)
- Ch9: 858a9b4 (113 `<foreign>` instances)
- Ch10: c57d00a (181 `<foreign>` instances)
- Ch11: 7cc7b51 (174 `<foreign>` instances)
- Ch12: f0c02fc (127 `<foreign>` instances)
- Ch13: de41b9e (131 `<foreign>` instances)
- Ch14: 395ae45 (147 `<foreign>` instances)
- Ch15: 89f308d (98 `<foreign>` instances)
- Ch16: b6f048e (126 `<foreign>` instances)
- Ch17: 1899dee (Stylistic Choices)
- Ch18: 9e56a92 (83 `<foreign>` instances, 20 exercises); answer key 1b8c3b2

## Revision Priorities (from REVISION_AUDIT.md)

Foundation chapters (1-3): well-developed. Core grammar chapters: need diagram integration and example freshness review. Verb system and advanced structure chapters: need significant expansion. ASCII diagrams throughout need replacement with SVG/PNG tree diagrams. Note: REVISION_AUDIT.md references old 27-chapter structure.
