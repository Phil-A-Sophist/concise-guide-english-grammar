# Diagramming Guide

## Authoritative Reference for Sentence Diagrams

This document is the authoritative reference for all diagram creation in the *Concise Guide to English Grammar* project. Future sessions should consult this guide to maintain consistency.

---

## 1. Overview

### Purpose of Diagrams

Sentence diagrams serve several purposes in this textbook:
- Make visible the hierarchical structure of sentences
- Show how words group into constituents (phrases)
- Illustrate the relationship between form and function
- Demonstrate structural ambiguity
- Provide a shared vocabulary for discussing grammar

### When to Use Diagrams

Use diagrams when:
- Introducing a new phrase type or sentence pattern
- Showing structural relationships that prose cannot clearly convey
- Demonstrating ambiguity (multiple structures for same words)
- Providing practice exercises for students

Use prose description when:
- The structure is simple enough to explain verbally
- The focus is on meaning rather than structure
- Space is limited

### Target Audience

Undergraduate students taking an introductory English grammar course. Diagrams should be:
- Clear and uncluttered
- Consistently labeled
- Accompanied by explanatory prose
- Gradually increasing in complexity

---

## 2. Style Conventions

### Node Labels (Category Labels)

Use abbreviated category labels consistently throughout:

| Label | Full Name | Example |
|-------|-----------|---------|
| S | Sentence | Top-level clause |
| NP | Noun Phrase | *the tall man* |
| VP | Verb Phrase | *chased the cat* |
| PP | Prepositional Phrase | *in the house* |
| AdjP | Adjective Phrase | *very tall* |
| AdvP | Adverb Phrase | *quite quickly* |
| N | Noun | *dog*, *happiness* |
| V | Verb | *run*, *is* |
| Adj | Adjective | *tall*, *happy* |
| Adv | Adverb | *quickly*, *never* |
| Det | Determiner | *the*, *a*, *my* |
| Pro | Pronoun | *she*, *it*, *they* |
| P / Prep | Preposition | *in*, *on*, *with* |
| Conj | Conjunction | *and*, *but*, *or* |
| Aux | Auxiliary Verb | *has*, *is*, *been* |
| Modal | Modal Verb | *can*, *will*, *must* |
| Sub | Subordinator | *that*, *if*, *when* |
| RelCl | Relative Clause | *who arrived late* |
| InfP | Infinitive Phrase | *to leave* |
| AdvCl | Adverbial Clause | *when it rained* |

### Dual Labels (Category/Function)

When showing both category and function, use slash notation:
- `NP/IO` - Noun Phrase functioning as Indirect Object
- `NP/DO` - Noun Phrase functioning as Direct Object
- `PP/Adverbial` - Prepositional Phrase functioning as Adverbial

### Color Conventions

Based on instructor's materials:
- **Blue (#0000FF)**: Category labels (S, NP, VP, Det, N, V, etc.)
- **Green (#008000)**: Terminal words (actual words from the sentence)
- **Black (#000000)**: Connecting lines

### Branch Style

- Use **binary branching** where linguistically appropriate
- Flat structures (multiple children from one node) are acceptable for:
  - Multiple adjectives in NP
  - Multiple auxiliaries in VP
  - Coordinate structures

### Terminal Node Formatting

- Terminal words appear at the bottom of the tree
- Words are displayed in regular weight (not bold)
- Use the exact words from the example sentence (including capitalization for first word)

### Triangles

Triangles may be used to abbreviate complex structures that aren't the focus of the current discussion. Use sparingly.

---

## 3. Phrase Structure Patterns

### Basic Sentence (S → NP + VP)

Every sentence divides into subject NP and predicate VP:

```
[S [NP ...] [VP ...]]
```

Example: *The dog barked.*
```
[S [NP [Det The] [N dog]] [VP [V barked]]]
```

### Noun Phrases

**Simple NP (noun only):**
```
[NP [N dogs]]
```

**NP with determiner:**
```
[NP [Det the] [N dog]]
```

**NP with determiner and adjective:**
```
[NP [Det the] [Adj tall] [N man]]
```

**NP with multiple adjectives:**
```
[NP [Det the] [Adj big] [Adj brown] [N dog]]
```

**NP with PP post-modifier:**
```
[NP [Det the] [N man] [PP [P in] [NP [Det the] [N hat]]]]
```

**NP with relative clause:**
```
[NP [Det the] [N man] [RelCl who arrived late]]
```

### Verb Phrases

**Simple VP (main verb only):**
```
[VP [V sleeps]]
```

**VP with modal:**
```
[VP [Modal will] [V eat]]
```

**VP with auxiliary (perfect):**
```
[VP [Aux has] [V eaten]]
```

**VP with auxiliary (progressive):**
```
[VP [Aux is] [V eating]]
```

**VP with auxiliary (passive):**
```
[VP [Aux was] [V eaten]]
```

**Complex VP (modal + perfect + progressive):**
```
[VP [Modal should] [Aux have] [Aux been] [V studying]]
```

**VP with direct object:**
```
[VP [V chased] [NP [Det the] [N mouse]]]
```

**VP with subject complement:**
```
[VP [V is] [AdjP [Adj happy]]]
```

### Sentence Patterns

**Pattern 1: Intransitive (S + V)**
```
[S [NP [N Thunder]] [VP [V rumbled]]]
```

**Pattern 2: Transitive (S + V + DO)**
```
[S [NP [Det The] [N cat]] [VP [V chased] [NP [Det the] [N mouse]]]]
```

**Pattern 3: Linking (S + V + SC)**
```
[S [NP [Pro She]] [VP [V is] [AdjP [Adj happy]]]]
```

**Pattern 4: Ditransitive (S + V + IO + DO)**
```
[S [NP [Pro She]] [VP [V gave] [NP [Pro me]] [NP [Det a] [N book]]]]
```

**Pattern 5: Complex Transitive (S + V + DO + OC)**
```
[S [NP [Pro They]] [VP [V elected] [NP [Pro her]] [NP [N president]]]]
```

### Prepositional Phrases

**Simple PP:**
```
[PP [P in] [NP [Det the] [N house]]]
```

**PP as adjectival (modifying noun):**
```
[NP [Det the] [N man] [PP [P in] [NP [Det the] [N hat]]]]
```

**PP as adverbial (modifying verb):**
```
[VP [V waited] [PP [P in] [NP [Det the] [N lobby]]]]
```

### Adjective Phrases

**Simple AdjP:**
```
[AdjP [Adj tall]]
```

**AdjP with degree modifier:**
```
[AdjP [Adv very] [Adj tall]]
```

**AdjP with PP complement:**
```
[AdjP [Adj afraid] [PP [P of] [NP [N spiders]]]]
```

### Adverb Phrases

**Simple AdvP:**
```
[AdvP [Adv quickly]]
```

**AdvP with degree modifier:**
```
[AdvP [Adv very] [Adv quickly]]
```

---

## 4. Technical Specifications

### Bracket Notation Syntax

```
[CATEGORY child1 child2 child3 ...]
```

Where:
- `CATEGORY` is a node label (S, NP, VP, N, V, etc.)
- Children can be:
  - Terminal words (bare strings): `The`, `dog`, `barked`
  - Nested structures: `[Det the]`, `[NP [Det the] [N dog]]`

### Rules

1. Every non-terminal node must have square brackets
2. Terminal words (leaves) appear without brackets, just the word
3. Spaces separate children within a bracket
4. Category label comes immediately after opening bracket
5. Nested brackets can be arbitrarily deep

### File Naming Convention

```
ch##_descriptive_name.svg
```

Examples:
- `ch06_dog_barked.svg`
- `ch06_ambig_binoculars_vp.svg`
- `ch08_complex_np.svg`

### Directory Structure

```
assets/
  diagrams/
    ch04_morpheme_unhappiness.svg
    ch06_dog_barked.svg
    ch06_transitive.svg
    ...
    manifest.txt
```

### Image Dimensions

SVG diagrams are vector graphics and scale automatically. The generation script produces SVGs that:
- Have viewBox for proper scaling
- Use percentage-based positioning
- Work at any display size

For EPUB output, images are embedded directly. For HTML output, SVGs can be linked or embedded.

---

## 5. Generation Workflow

### Adding a New Diagram

1. **Add entry to `documents/diagram_sources.txt`:**
   ```
   # diagram_id: ch##_new_diagram
   # caption: Description of the diagram
   [S [NP [Det The] [N dog]] [VP [V barked]]]
   ```

2. **Run the generation script:**
   ```bash
   python scripts/generate_diagrams.py
   ```

3. **Verify the output:**
   - Check `assets/diagrams/ch##_new_diagram.svg`
   - Open in browser to confirm rendering

4. **Insert image reference in markdown:**
   ```markdown
   ![Tree diagram: The dog barked](assets/diagrams/ch06_dog_barked.svg)
   ```

5. **Test in EPUB build:**
   ```bash
   python generate_epub.py
   ```

### Modifying an Existing Diagram

1. Edit the bracket notation in `documents/diagram_sources.txt`
2. Run `python scripts/generate_diagrams.py`
3. Verify the updated SVG
4. Rebuild EPUB to confirm

### Batch Regeneration

To regenerate all diagrams:
```bash
python scripts/generate_diagrams.py
```

The script will:
- Read all entries from `documents/diagram_sources.txt`
- Generate SVGs for each
- Write to `assets/diagrams/`
- Update `manifest.txt`

---

## 6. Bracket Notation Reference

### Basic Structure

```
[CATEGORY children...]
```

### Examples

**Single word with category:**
```
[N dog]
```

**Phrase with multiple children:**
```
[NP [Det the] [N dog]]
```

**Deeply nested:**
```
[S [NP [Det The] [Adj young] [N artist] [PP [P from] [NP [N Paris]]]] [VP [V painted] [NP [Adj beautiful] [N landscapes]]]]
```

**Coordination:**
```
[NP [NP [Adj old] [N men]] [Conj and] [NP [N women]]]
```

**Clauses:**
```
[S [AdvCl When it rained] [S [NP [Pro they]] [VP [V stayed]]]]
```

---

## 7. Common Patterns Quick Reference

| Structure | Bracket Notation |
|-----------|------------------|
| Simple NP | `[NP [N dog]]` |
| NP + Det | `[NP [Det the] [N dog]]` |
| NP + Det + Adj | `[NP [Det the] [Adj big] [N dog]]` |
| NP + PP | `[NP [Det the] [N man] [PP [P in] [NP [Det the] [N hat]]]]` |
| Simple VP | `[VP [V runs]]` |
| VP + Modal | `[VP [Modal will] [V run]]` |
| VP + Aux | `[VP [Aux has] [V run]]` |
| VP + DO | `[VP [V chased] [NP [Det the] [N cat]]]` |
| Simple PP | `[PP [P in] [NP [Det the] [N house]]]` |
| Simple AdjP | `[AdjP [Adj tall]]` |
| AdjP + Deg | `[AdjP [Adv very] [Adj tall]]` |
| Simple AdvP | `[AdvP [Adv quickly]]` |
| Intransitive S | `[S [NP [N Birds]] [VP [V sing]]]` |
| Transitive S | `[S [NP [N She]] [VP [V read] [NP [Det the] [N book]]]]` |
| Linking S | `[S [NP [Pro She]] [VP [V is] [AdjP [Adj happy]]]]` |
| Ditransitive S | `[S [NP [Pro She]] [VP [V gave] [NP [Pro me]] [NP [Det a] [N book]]]]` |

---

## 8. Troubleshooting

### Common Bracket Notation Errors

**Missing closing bracket:**
```
[S [NP [Det the] [N dog] [VP [V barked]]]
                        ^ missing ]
```

**Mismatched brackets:**
```
[S [NP [Det the] [N dog]] [VP [V barked]]
                                       ^ extra ]
```

**Missing category label:**
```
[[Det the] [N dog]]
 ^ category label missing
```

### SVG Rendering Issues

**Diagram too wide:**
- Break into multiple diagrams
- Use triangles for complex sub-structures

**Text overlap:**
- Simplify structure
- Abbreviate long words in examples

**Wrong colors:**
- Check CSS styling in SVG
- Ensure custom styles were applied

### EPUB Integration Issues

**Images not appearing:**
- Verify image path in markdown
- Ensure SVG exists in `assets/diagrams/`
- Check EPUB generator includes SVG mime type

**Images too small/large:**
- SVGs scale automatically
- Adjust surrounding text/context

---

## 9. Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-12 | 1.0 | Initial creation |

---

## 10. Source Files

- **Diagram sources:** `documents/diagram_sources.txt`
- **Generation script:** `scripts/generate_diagrams.py`
- **Generated SVGs:** `assets/diagrams/*.svg`
- **Manifest:** `assets/diagrams/manifest.txt`

---

*This guide is the authoritative reference for diagram creation. When in doubt, follow the conventions documented here.*
