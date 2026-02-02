# Diagram Bracket Notation Reference

This document lists all syntax tree diagrams generated for the textbook using the SyntaxTreeHybrid tool, including their bracket notation for reference and regeneration.

## Generation Tool

Diagrams are generated using [SyntaxTreeHybrid](C:\Users\irphy\Documents\SyntaxTreeHybrid).

To regenerate diagrams:
1. Navigate to the SyntaxTreeHybrid directory
2. Run `node generate-diagrams.js` or use the web interface
3. Copy generated PNGs to `assets/diagrams/new/`

---

## Chapter 5: Open Classes

### Noun Phrase Diagrams

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch05_np_simple.png` | `[NP [DET the] [ADJP [ADJ tall]] [N student]]` | Simple NP: "the tall student" |
| `ch05_np_with_pp.png` | `[NP [DET the] [ADJP [ADJ tall]] [N student] [PP [PREP from] [NP [N Ohio]]]]` | NP with PP: "the tall student from Ohio" |
| `ch05_np_complex.png` | `[NP [DET the] [ADJP [ADJ brilliant]] [ADJP [ADJ young]] [N student] [PP [PREP from] [NP [N Ohio]]]]` | Complex NP: "the brilliant young student from Ohio" |

### Verb Phrase Diagrams

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch05_vp_intransitive.png` | `[VP [V slept]]` | Intransitive VP: "slept" |
| `ch05_vp_transitive.png` | `[VP [V read] [NP [DET the] [N book]]]` | Transitive VP: "read the book" |
| `ch05_vp_ditransitive.png` | `[VP [V gave] [NP [PRON her]] [NP [DET a] [N present]]]` | Ditransitive VP: "gave her a present" |

### Adjective Phrase Diagrams

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch05_adjp_simple.png` | `[ADJP [ADJ happy]]` | Simple AdjP: "happy" |
| `ch05_adjp_degree.png` | `[ADJP [ADVP [ADV very]] [ADJ happy]]` | AdjP with degree: "very happy" |
| `ch05_adjp_complex.png` | `[ADJP [ADVP [ADV very]] [ADJ proud] [PP [PREP of] [NP [DET her] [N work]]]]` | Complex AdjP: "very proud of her work" |

### Adverb Phrase Diagrams

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch05_advp_simple.png` | `[ADVP [ADV quickly]]` | Simple AdvP: "quickly" |
| `ch05_advp_degree.png` | `[ADVP [ADVP [ADV very]] [ADV quickly]]` | AdvP with degree: "very quickly" |

---

## Chapter 6: Closed Classes

### Sentence Structure Basics

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_basic_structure.png` | `[S [NP] [VP]]` | Abstract sentence structure |
| `ch06_dog_barked.png` | `[S [NP [DET The] [N dog]] [VP [V barked]]]` | Simple sentence: "The dog barked" |
| `ch06_artist_painted.png` | `[S [NP [DET The] [ADJP [ADJ young]] [N artist] [PP [PREP from] [NP [N Paris]]]] [VP [V painted] [NP [ADJP [ADJ beautiful]] [N landscapes]]]]` | Complex sentence: "The young artist from Paris painted beautiful landscapes" |

### Determiner Examples

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_possessive_det.png` | `[NP [DET her] [N book]]` | Possessive determiner: "her book" |
| `ch06_predeterminer.png` | `[NP [PREDET all] [DET the] [N students]]` | Predeterminer structure: "all the students" |

### Pronoun Examples

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_pronoun_subject.png` | `[S [NP [PRON She]] [VP [V sleeps]]]` | Pronoun as subject: "She sleeps" |
| `ch06_ditransitive.png` | `[S [NP [PRON She]] [VP [V gave] [NP [PRON me]] [NP [DET a] [N book]]]]` | Pronouns in ditransitive: "She gave me a book" |

### Prepositional Phrase Attachment

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_ambig_binoculars_np.png` | `[S [NP [PRON I]] [VP [V saw] [NP [DET the] [N man] [PP [PREP with] [NP [N binoculars]]]]]]` | PP as NP modifier (adjectival): "I saw the man with binoculars" |
| `ch06_ambig_binoculars_vp.png` | `[S [NP [PRON I]] [VP [V saw] [NP [DET the] [N man]] [PP [PREP with] [NP [N binoculars]]]]]` | PP as VP modifier (adverbial): "I saw the man with binoculars" |

### Sentence Patterns

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_intransitive.png` | `[S [NP [N Thunder]] [VP [V rumbled]]]` | Intransitive: "Thunder rumbled" |
| `ch06_transitive.png` | `[S [NP [DET The] [N cat]] [VP [V chased] [NP [DET the] [N mouse]]]]` | Transitive: "The cat chased the mouse" |
| `ch06_linking.png` | `[S [NP [PRON She]] [VP [V is] [ADJP [ADJ happy]]]]` | Linking verb: "She is happy" |
| `ch06_complex_trans_np.png` | `[S [NP [PRON They]] [VP [V elected] [NP [PRON her]] [NP [N president]]]]` | Complex transitive (NP): "They elected her president" |
| `ch06_complex_trans_adj.png` | `[S [NP [DET The] [N jury]] [VP [V found] [NP [PRON him]] [ADJP [ADJ guilty]]]]` | Complex transitive (AdjP): "The jury found him guilty" |

---

## Reserved for Later Chapters

The following diagrams were generated but are reserved for later chapters:

### For Chapter 9 (Compound and Complex Sentences)

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_np_coordination.png` | `[NP [NP [N cats]] [CONJ and] [NP [N dogs]]]` | NP coordination: "cats and dogs" |
| `ch06_ambig_old_men_1.png` | `[S [NP [NP [ADJP [ADJ old]] [N men]] [CONJ and] [NP [N women]]] [VP [V gathered]]]` | Coordination ambiguity (modifier on first): "Old men and women gathered" |
| `ch06_ambig_old_men_2.png` | `[S [NP [ADJP [ADJ old]] [NP [NP [N men]] [CONJ and] [NP [N women]]]] [VP [V gathered]]]` | Coordination ambiguity (modifier on both): "Old men and women gathered" |
| `ch06_subordinate_because.png` | `[S [SBAR [CONJ Because] [S [NP [PRON she]] [VP [V was] [ADJP [ADJ tired]]]]] [S [NP [PRON she]] [VP [V left]]]]` | Subordinating conjunction: "Because she was tired, she left" |

### For Adverbials Chapter (Relative Clauses)

| File | Bracket Notation | Description |
|------|------------------|-------------|
| `ch06_relative_clause.png` | `[NP [DET the] [N book] [SBAR [REL that] [S [NP [PRON I]] [VP [V read]]]]]` | Relative clause: "the book that I read" |

---

## Node Type Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| S | Sentence |
| NP | Noun Phrase |
| VP | Verb Phrase |
| ADJP | Adjective Phrase |
| ADVP | Adverb Phrase |
| PP | Prepositional Phrase |
| SBAR | Subordinate clause (clause bar) |
| DET | Determiner |
| PREDET | Predeterminer |
| N | Noun |
| V | Verb |
| ADJ | Adjective |
| ADV | Adverb |
| PREP | Preposition |
| PRON | Pronoun |
| CONJ | Conjunction |
| REL | Relative pronoun |

---

## Generation Script

The generation script is located at `C:\Users\irphy\Documents\SyntaxTreeHybrid\generate-diagrams.js`.

To add new diagrams:
1. Add entries to the `diagrams` array in the script
2. Run `node generate-diagrams.js`
3. Update this documentation with the new entries
