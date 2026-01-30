# Diagram Examples by Chapter

This document lists the diagrams to include in the "Diagram Examples" section at the end of chapters 5-14. Each entry includes:
- Description of the diagram
- Bracket notation (where available)
- Source (from F25 reference doc, existing assets, or new)

---

## Chapter 5: Open Classes

**Focus:** Phrase structures for open-class words (NP, VP, AdjP, AdvP)

### Noun Phrase Examples

1. **Simple Noun Phrase (N only)**
   - Example: *dogs*
   - Bracket: `[NP [N dogs]]`
   - Status: EXISTS (ch08_simple_np)

2. **NP with Determiner**
   - Example: *the dog*
   - Bracket: `[NP [DET the] [N dog]]`
   - Status: EXISTS (ch08_np_det)

3. **NP with Determiner and Adjective**
   - Example: *the tall student*
   - Bracket: `[NP [DET the] [ADJ tall] [N student]]`
   - Status: EXISTS (ch05_np_simple)
   - From F25: "Determiners", "Adjectives in a Noun Phrase"

4. **NP with Multiple Adjectives**
   - Example: *the big brown dog*
   - Bracket: `[NP [DET the] [ADJ big] [ADJ brown] [N dog]]`
   - Status: EXISTS (ch08_np_multiple_adj)

5. **NP with PP Post-modifier**
   - Example: *the student from Ohio*
   - Bracket: `[NP [DET the] [N student] [PP [PREP from] [NP [N Ohio]]]]`
   - Status: EXISTS (ch05_np_with_pp variant)
   - From F25: "Prepositional Phrase in a Noun Phrase"

### Verb Phrase Examples

6. **Simple VP (intransitive)**
   - Example: *sleeps*
   - Bracket: `[VP [V sleeps]]`
   - Status: EXISTS (ch07_simple_vp)

7. **VP with Direct Object (transitive)**
   - Example: *read the book*
   - Bracket: `[VP [V read] [NP [DET the] [N book]]]`
   - Status: EXISTS (ch05_vp_transitive)
   - From F25: "Transitive Verb with a Direct Object"

8. **VP with Two Objects (ditransitive)**
   - Example: *gave her a present*
   - Bracket: `[VP [V gave] [NP [PRON her]] [NP [DET a] [N present]]]`
   - Status: EXISTS (ch05_vp_ditransitive)
   - From F25: "Transitive (ditransitive) verb with Direct Object and Indirect Object"

### Adjective Phrase Examples

9. **Simple AdjP**
   - Example: *happy*
   - Bracket: `[ADJP [ADJ happy]]`
   - Status: EXISTS (ch05_adjp_simple)

10. **AdjP with Degree Adverb**
    - Example: *very happy*
    - Bracket: `[ADJP [ADV very] [ADJ happy]]`
    - Status: EXISTS (ch05_adjp_degree)
    - From F25: "Adverb in an Adjective Phrase"

11. **AdjP with PP Complement**
    - Example: *proud of her work*
    - Bracket: `[ADJP [ADJ proud] [PP [PREP of] [NP [DET her] [N work]]]]`
    - Status: EXISTS (ch09_adjp_pp_proud)

### Adverb Phrase Examples

12. **Simple AdvP**
    - Example: *quickly*
    - Bracket: `[ADVP [ADV quickly]]`
    - Status: EXISTS (ch05_advp_simple)

13. **AdvP with Degree Modifier**
    - Example: *very quickly*
    - Bracket: `[ADVP [ADV very] [ADV quickly]]`
    - Status: EXISTS (ch05_advp_degree)

---

## Chapter 6: Closed Classes

**Focus:** Determiners, pronouns, prepositions, conjunctions, auxiliaries

### Determiner Examples

1. **Determiner in NP**
   - Example: *the dog*
   - Bracket: `[NP [DET the] [N dog]]`
   - Status: EXISTS (ch08_np_det)
   - From F25: "Determiners"

2. **Possessive Determiner**
   - Example: *her book*
   - Bracket: `[NP [DET her] [N book]]`
   - Status: NEEDED

### Pronoun Examples

3. **Pronoun as Subject**
   - Example: *She sleeps.*
   - Bracket: `[S [NP [PRON She]] [VP [V sleeps]]]`
   - Status: NEEDED

4. **Pronoun as Object**
   - Example: *She read it.*
   - Bracket: `[S [NP [PRON She]] [VP [V read] [NP [PRON it]]]]`
   - Status: EXISTS (ch11_pronouns)

### Preposition/PP Examples

5. **Simple PP**
   - Example: *in the box*
   - Bracket: `[PP [PREP in] [NP [DET the] [N box]]]`
   - Status: EXISTS (ch11_simple_pp)

6. **PP as NP Modifier (Adjectival)**
   - Example: *the man in the hat*
   - Bracket: `[NP [DET the] [N man] [PP [PREP in] [NP [DET the] [N hat]]]]`
   - Status: EXISTS (ch11_adjectival_pp)
   - From F25: "Prepositional Phrase in a Noun Phrase"

7. **PP as VP Modifier (Adverbial)**
   - Example: *She works at home.*
   - Bracket: `[S [NP [PRON She]] [VP [V works] [PP [PREP at] [NP [N home]]]]]`
   - Status: EXISTS (ch10_adverbial_pp)
   - From F25: "Prepositional Phrase in a Verb Phrase"

### Conjunction Examples

8. **Coordinating Conjunction in NP**
   - Example: *cats and dogs*
   - Bracket: `[NP [N cats] [CONJ and] [N dogs]]`
   - Status: NEEDED

---

## Chapter 7: Introduction to Sentence Diagramming

**Focus:** Basic sentence structure, tree diagram conventions

### Basic Sentence Structure

1. **Abstract S → NP + VP**
   - Example: (template)
   - Bracket: `[S [NP] [VP]]`
   - Status: EXISTS (ch06_basic_structure)

2. **Simple Intransitive Sentence**
   - Example: *Thunder rumbled.*
   - Bracket: `[S [NP [N Thunder]] [VP [V rumbled]]]`
   - Status: EXISTS (ch06_intransitive)
   - From F25: "Simple Intransitive Sentence"

3. **Simple Transitive Sentence**
   - Example: *The cat chased the mouse.*
   - Bracket: `[S [NP [DET The] [N cat]] [VP [V chased] [NP [DET the] [N mouse]]]]`
   - Status: EXISTS (ch06_transitive)

4. **Sentence with Determiner and Adjective**
   - Example: *The dog barked.*
   - Bracket: `[S [NP [DET The] [N dog]] [VP [V barked]]]`
   - Status: EXISTS (ch06_dog_barked)
   - From F25: "Determiners"

---

## Chapter 8: Basic Sentence Elements and Sentence Patterns

**Focus:** Six basic sentence patterns, verb valency

### Pattern 1: Intransitive (S-V)

1. **Basic Intransitive**
   - Example: *Cameras flashed.*
   - Bracket: `[S [NP [N Cameras]] [VP [V flashed]]]`
   - Status: EXISTS (ch12_basic_intransitive)
   - From F25: "Simple Intransitive Sentence"

2. **Intransitive with Conjoined Subjects**
   - Example: *Frodo and Sam travel.*
   - Bracket: `[S [NP [N Frodo] [CONJ and] [N Sam]] [VP [V travel]]]`
   - Status: NEEDED
   - From F25: "Intransitive Sentence with Two Noun Phrases"

3. **Intransitive with Conjoined Verbs**
   - Example: *Gandalf thinks and acts.*
   - Bracket: `[S [NP [N Gandalf]] [VP [V thinks] [CONJ and] [V acts]]]`
   - Status: NEEDED
   - From F25: "Intransitive Sentence with Two Verb Phrases"

### Pattern 2: Transitive (S-V-DO)

4. **Basic Transitive**
   - Example: *Weasels stalk rabbits.*
   - Bracket: `[S [NP [N Weasels]] [VP [V stalk] [NP [N rabbits]]]]`
   - Status: EXISTS (ch12_basic_transitive)
   - From F25: "Transitive Verb with a Direct Object"

### Pattern 3: Ditransitive (S-V-IO-DO)

5. **Ditransitive with Indirect and Direct Object**
   - Example: *Marie sent Ramon a gift.*
   - Bracket: `[S [NP [N Marie]] [VP [V sent] [NP [N Ramon]] [NP [DET a] [N gift]]]]`
   - Status: EXISTS (ch12_ditransitive_io_do)
   - From F25: "Transitive (ditransitive) verb with Direct Object and Indirect Object"

### Pattern 4: Linking/Copular (S-V-SC)

6. **Copular with NP as Subject Complement**
   - Example: *I am an optimist.*
   - Bracket: `[S [NP [PRON I]] [VP [V am] [NP [DET an] [N optimist]]]]`
   - Status: EXISTS (ch12_copular_be)
   - From F25: "Copular Be Sentence with NP as Subject Complement"

7. **Copular with AdjP as Subject Complement**
   - Example: *She is happy.*
   - Bracket: `[S [NP [PRON She]] [VP [V is] [ADJP [ADJ happy]]]]`
   - Status: EXISTS (ch06_linking)
   - From F25: "Copular Be Sentence with AdjP as Subject Complement"

8. **Copular with PP as Adverbial**
   - Example: *Phillip is over the moon.*
   - Bracket: `[S [NP [N Phillip]] [VP [V is] [PP [PREP over] [NP [DET the] [N moon]]]]]`
   - Status: NEEDED
   - From F25: "Copular Be Sentence with PP as Adverbial"

9. **Copular with AdvP as Adverbial**
   - Example: *Phillip is here.*
   - Bracket: `[S [NP [N Phillip]] [VP [V is] [ADVP [ADV here]]]]`
   - Status: NEEDED
   - From F25: "Copular Be Sentence with AdvP as Adverbial"

10. **Linking Verb with AdjP**
    - Example: *Phillip became famous.*
    - Bracket: `[S [NP [N Phillip]] [VP [V became] [ADJP [ADJ famous]]]]`
    - Status: NEEDED
    - From F25: "Linking Verb with AdjP as Subject Complement"

11. **Linking Verb with NP**
    - Example: *Phillip became a doctor.*
    - Bracket: `[S [NP [N Phillip]] [VP [V became] [NP [DET a] [N doctor]]]]`
    - Status: NEEDED
    - From F25: "Linking Verb with NP as Subject Complement"

### Pattern 5: Complex Transitive (S-V-DO-OC)

12. **Complex Transitive with AdjP Object Complement**
    - Example: *The jury found him guilty.*
    - Bracket: `[S [NP [DET The] [N jury]] [VP [V found] [NP [PRON him]] [ADJP [ADJ guilty]]]]`
    - Status: EXISTS (ch06_complex_trans_adj)
    - From F25: "Transitive verb with DO and AdjP as Object Complement"

13. **Complex Transitive with NP Object Complement**
    - Example: *They elected her president.*
    - Bracket: `[S [NP [PRON They]] [VP [V elected] [NP [PRON her]] [NP [N president]]]]`
    - Status: EXISTS (ch06_complex_trans_np)
    - From F25: "Transitive verb with DO and NP as Object Complement"

---

## Chapter 9: Compound and Complex Sentences

**Focus:** Coordination, subordination, clause types

### Coordination

1. **Coordinated Independent Clauses**
   - Example: *I laugh and you cry.*
   - Bracket: `[S [S [NP [PRON I]] [VP [V laugh]]] [CONJ and] [S [NP [PRON you]] [VP [V cry]]]]`
   - Status: NEEDED
   - From F25: "Coordination (coordinating conjunction)"

### Subordination

2. **Dependent Clause Second**
   - Example: *I laugh because you cry.*
   - Bracket: `[S [IC [NP [PRON I]] [VP [V laugh]]] [DC [SUB because] [NP [PRON you]] [VP [V cry]]]]`
   - Status: NEEDED
   - From F25: "Subordination (dependent clause second)"

3. **Dependent Clause First**
   - Example: *Because you cry, I laugh.*
   - Bracket: `[S [DC [SUB Because] [NP [PRON you]] [VP [V cry]]] [IC [NP [PRON I]] [VP [V laugh]]]]`
   - Status: NEEDED
   - From F25: "Subordination (dependent clause first)"

4. **Adverbial Clause**
   - Example: *When it rained, they stayed.*
   - Bracket: `[S [DC [SUB When] [NP [PRON it]] [VP [V rained]]] [IC [NP [PRON they]] [VP [V stayed]]]]`
   - Status: EXISTS (ch10_adverbial_clause)

---

## Chapter 10: Verbs Part One: Tense and Aspect

**Focus:** Auxiliary verbs, tense, aspects

### Auxiliary Verbs

1. **Progressive Aspect (be + V-ing)**
   - Example: *is eating*
   - Bracket: `[VP [AUX is] [V eating]]`
   - Status: EXISTS (ch07_vp_progressive)

2. **Perfect Aspect (have + V-en)**
   - Example: *has eaten*
   - Bracket: `[VP [AUX has] [V eaten]]`
   - Status: EXISTS (ch07_vp_perfect)

3. **Perfect Progressive (have + been + V-ing)**
   - Example: *has been eating*
   - Bracket: `[VP [AUX has] [AUX been] [V eating]]`
   - Status: EXISTS (ch07_vp_perfect_progressive)
   - From F25: "Auxiliary Verbs"

4. **Passive (be + V-en)**
   - Example: *was eaten*
   - Bracket: `[VP [AUX was] [V eaten]]`
   - Status: EXISTS (ch07_vp_passive)

5. **Progressive Passive (be + being + V-en)**
   - Example: *is being renovated*
   - Bracket: `[VP [AUX is] [AUX being] [V renovated]]`
   - Status: EXISTS (ch07_vp_progressive_passive)

---

## Chapter 11: Verbs Part Two: Voice and Modals

**Focus:** Passive voice, modal auxiliaries

### Modals

1. **Modal + Verb**
   - Example: *will eat*
   - Bracket: `[VP [MOD will] [V eat]]`
   - Status: EXISTS (ch07_vp_modal)
   - From F25: "Modals"

2. **Modal + Perfect**
   - Example: *will have eaten*
   - Bracket: `[VP [MOD will] [AUX have] [V eaten]]`
   - Status: EXISTS (ch07_vp_modal_perfect)

3. **Complex VP (Modal + Perfect + Progressive)**
   - Example: *should have been studying*
   - Bracket: `[VP [MOD should] [AUX have] [AUX been] [V studying]]`
   - Status: EXISTS (ch07_vp_complex)

4. **Full Complex VP**
   - Example: *will have been being eaten*
   - Bracket: `[VP [MOD will] [AUX have] [AUX been] [AUX being] [V eaten]]`
   - Status: EXISTS (ch07_vp_full_complex)
   - From F25: "Optional Main Verb Phrase Level"

### Passive Voice

5. **Passive with By-phrase**
   - Example: *was written by Maria*
   - Bracket: `[VP [AUX was] [V written] [PP [PREP by] [NP [N Maria]]]]`
   - Status: EXISTS (ch16_passive_by)
   - From F25: "Passive Voice"

---

## Chapter 12: Adverbials

**Focus:** Structures functioning as adverbials

### Adverb as Adverbial

1. **Adverb Modifying Verb**
   - Example: *She spoke quietly.*
   - Bracket: `[S [NP [PRON She]] [VP [V spoke] [ADVP [ADV quietly]]]]`
   - Status: EXISTS (ch10_adv_modifying_verb)
   - From F25: "Adverb in a Verb Phrase"

2. **Sentence Adverb**
   - Example: *Unfortunately, she lost.*
   - Bracket: `[S [ADVP [ADV Unfortunately]] [S [NP [PRON she]] [VP [V lost]]]]`
   - Status: EXISTS (ch10_sentence_adverb)

### PP as Adverbial

3. **PP in VP (Adverbial)**
   - Example: *She works at home.*
   - Bracket: `[S [NP [PRON She]] [VP [V works] [PP [PREP at] [NP [N home]]]]]`
   - Status: EXISTS (ch10_adverbial_pp)
   - From F25: "Prepositional Phrase in a Verb Phrase"

### Nouns as Adverbials

4. **Noun Functioning as Adverbial**
   - Example: *I sleep every day.*
   - Bracket: `[S [NP [PRON I]] [VP [V sleep] [NP [DET every] [N day]]]]`
   - Status: NEEDED
   - From F25: "Nouns as Adverbials"

### Verbs as Adverbials

5. **Present Participle as Adverbial**
   - Example: *I left running.*
   - Bracket: `[S [NP [PRON I]] [VP [V left] [VP [V running]]]]`
   - Status: NEEDED
   - From F25: "Verbs as Adverbials (Present Participles)"

6. **Infinitive as Adverbial**
   - Example: *I went to run.*
   - Bracket: `[S [NP [PRON I]] [VP [V went] [VP [PREP to] [V run]]]]`
   - Status: NEEDED
   - From F25: "Verbs as Adverbials (Infinitives)"

### Multiple Adverbials

7. **Sentence with Multiple Adverbials**
   - Example: *She spoke quietly in the library.*
   - Bracket: `[S [NP [PRON She]] [VP [V spoke] [ADVP [ADV quietly]] [PP [PREP in] [NP [DET the] [N library]]]]]`
   - Status: EXISTS (ch10_sentence_adverbials)

---

## Chapter 13: Nominals

**Focus:** Structures functioning as nominals (noun clauses)

### Complement/Nominal Clauses

1. **That-clause in Object Position**
   - Example: *I know that you cry.*
   - Bracket: `[S [NP [PRON I]] [VP [V know] [CC [COMP that] [NP [PRON you]] [VP [V cry]]]]]`
   - Status: NEEDED
   - From F25: "Complement/Nominal Clause in Object Position (Complementizer as Subject)"

2. **That-clause in Subject Position**
   - Example: *That you cry upsets me.*
   - Bracket: `[S [CC [COMP That] [NP [PRON you]] [VP [V cry]]] [VP [V upsets] [NP [PRON me]]]]`
   - Status: NEEDED
   - From F25: "Complement/Nominal Clause in Subject Position"

3. **If/Whether-clause in Object Position**
   - Example: *I wonder if you cry.*
   - Bracket: `[S [NP [PRON I]] [VP [V wonder] [CC [COMP if] [NP [PRON you]] [VP [V cry]]]]]`
   - Status: NEEDED
   - From F25: "Complement/Nominal Clause in Object Position (Complementizer)"

4. **Missing Complementizer**
   - Example: *I know you cry.*
   - Bracket: `[S [NP [PRON I]] [VP [V know] [CC [COMP _] [NP [PRON you]] [VP [V cry]]]]]`
   - Status: NEEDED
   - From F25: "Missing Complementizer: Complement/Nominal Clause in Object Position"

---

## Chapter 14: Adjectivals

**Focus:** Structures functioning as adjectivals (relative clauses, participial phrases)

### Adjectives in Different Positions

1. **Attributive Position**
   - Example: *the tall man*
   - Bracket: `[NP [DET the] [ADJ tall] [N man]]`
   - Status: EXISTS (ch09_np_attributive)

2. **Predicative Position**
   - Example: *She is happy.*
   - Bracket: `[S [NP [PRON She]] [VP [V is] [ADJP [ADJ happy]]]]`
   - Status: EXISTS (ch09_predicative)

### PP as Adjectival

3. **PP Modifying Noun**
   - Example: *the man in the hat*
   - Bracket: `[NP [DET the] [N man] [PP [PREP in] [NP [DET the] [N hat]]]]`
   - Status: EXISTS (ch11_adjectival_pp)

### Verbs as Adjectivals (Participial Phrases)

4. **Present Participle as Adjectival**
   - Example: *the running dog barks*
   - Bracket: `[S [NP [DET the] [VP [V running]] [N dog]] [VP [V barks]]]`
   - Status: NEEDED
   - From F25: "Verbs as Adjectivals (Present Participle)"

5. **Past Participle as Adjectival**
   - Example: *the frightened dog barks*
   - Bracket: `[S [NP [DET the] [VP [V frightened]] [N dog]] [VP [V barks]]]`
   - Status: NEEDED
   - From F25: "Verbs as Adjectivals (Past Participle)"

### Relative Clauses

6. **Relative Clause with Relative Pronoun as Subject**
   - Example: *the dog who barks sleeps*
   - Bracket: `[S [NP [DET the] [N dog] [RC [REL who] [VP [V barks]]]] [VP [V sleeps]]]`
   - Status: NEEDED
   - From F25: "Relative Clauses with Relative Pronouns (Relative Pronoun as Subject)"

7. **Relative Clause with That (Subject of RC)**
   - Example: *the dog that I saw sleeps*
   - Bracket: `[S [NP [DET the] [N dog] [RC [REL that] [NP [PRON I]] [VP [V saw]]]] [VP [V sleeps]]]`
   - Status: NEEDED
   - From F25: "Relative Clauses (Relativizer as Subject of RC)"

8. **Relative Clause Modifying Object (Relative Adverb)**
   - Example: *I saw the place where you live.*
   - Bracket: `[S [NP [PRON I]] [VP [V saw] [NP [DET the] [N place] [RC [REL where] [NP [PRON you]] [VP [V live]]]]]]`
   - Status: NEEDED
   - From F25: "Relative Clause modifying Direct Object (Relative Adverb as Relativizer)"

9. **Empty Relativizer**
   - Example: *the dog I saw sleeps*
   - Bracket: `[S [NP [DET the] [N dog] [RC [REL _] [NP [PRON I]] [VP [V saw]]]] [VP [V sleeps]]]`
   - Status: NEEDED
   - From F25: "Empty Relativizer – Relative Clause Modifying Subject"

---

## Summary: Diagrams Needed

### Already Exist (can reuse):
- ch05_* (11 diagrams)
- ch06_* (13 diagrams)
- ch07_* (10 diagrams)
- ch08_* (8 diagrams)
- ch09_* (10 diagrams)
- ch10_* (9 diagrams)
- ch11_* (6 diagrams)
- ch12_* (4 diagrams)
- ch16_* (2 diagrams)

### Need to Create:
1. ch06_possessive_det: `[NP [DET her] [N book]]`
2. ch06_pronoun_subject: `[S [NP [PRON She]] [VP [V sleeps]]]`
3. ch06_np_coordination: `[NP [N cats] [CONJ and] [N dogs]]`
4. ch08_intrans_conj_subj: `[S [NP [N Frodo] [CONJ and] [N Sam]] [VP [V travel]]]`
5. ch08_intrans_conj_vp: `[S [NP [N Gandalf]] [VP [V thinks] [CONJ and] [V acts]]]`
6. ch08_copular_pp: `[S [NP [N Phillip]] [VP [V is] [PP [PREP over] [NP [DET the] [N moon]]]]]`
7. ch08_copular_advp: `[S [NP [N Phillip]] [VP [V is] [ADVP [ADV here]]]]`
8. ch08_linking_adjp: `[S [NP [N Phillip]] [VP [V became] [ADJP [ADJ famous]]]]`
9. ch08_linking_np: `[S [NP [N Phillip]] [VP [V became] [NP [DET a] [N doctor]]]]`
10. ch09_coordination: `[S [S [NP [PRON I]] [VP [V laugh]]] [CONJ and] [S [NP [PRON you]] [VP [V cry]]]]`
11. ch09_subord_dc_second: `[S [IC [NP [PRON I]] [VP [V laugh]]] [DC [SUB because] [NP [PRON you]] [VP [V cry]]]]`
12. ch09_subord_dc_first: `[S [DC [SUB Because] [NP [PRON you]] [VP [V cry]]] [IC [NP [PRON I]] [VP [V laugh]]]]`
13. ch12_noun_as_adverbial: `[S [NP [PRON I]] [VP [V sleep] [NP [DET every] [N day]]]]`
14. ch12_participle_adverbial: `[S [NP [PRON I]] [VP [V left] [VP [V running]]]]`
15. ch12_infinitive_adverbial: `[S [NP [PRON I]] [VP [V went] [VP [PREP to] [V run]]]]`
16. ch13_that_clause_object: `[S [NP [PRON I]] [VP [V know] [CC [COMP that] [NP [PRON you]] [VP [V cry]]]]]`
17. ch13_that_clause_subject: `[S [CC [COMP That] [NP [PRON you]] [VP [V cry]]] [VP [V upsets] [NP [PRON me]]]]`
18. ch13_if_clause: `[S [NP [PRON I]] [VP [V wonder] [CC [COMP if] [NP [PRON you]] [VP [V cry]]]]]`
19. ch13_missing_comp: `[S [NP [PRON I]] [VP [V know] [CC [COMP _] [NP [PRON you]] [VP [V cry]]]]]`
20. ch14_participle_present: `[S [NP [DET the] [VP [V running]] [N dog]] [VP [V barks]]]`
21. ch14_participle_past: `[S [NP [DET the] [VP [V frightened]] [N dog]] [VP [V barks]]]`
22. ch14_relcl_who_subject: `[S [NP [DET the] [N dog] [RC [REL who] [VP [V barks]]]] [VP [V sleeps]]]`
23. ch14_relcl_that_object: `[S [NP [DET the] [N dog] [RC [REL that] [NP [PRON I]] [VP [V saw]]]] [VP [V sleeps]]]`
24. ch14_relcl_where: `[S [NP [PRON I]] [VP [V saw] [NP [DET the] [N place] [RC [REL where] [NP [PRON you]] [VP [V live]]]]]]`
25. ch14_relcl_empty: `[S [NP [DET the] [N dog] [RC [REL _] [NP [PRON I]] [VP [V saw]]]] [VP [V sleeps]]]`
