# 7. Introduction to Sentence Diagramming

## Learning Objectives

By the end of this chapter, you will be able to:
- Explain what sentence diagrams represent and why they are useful
- Identify the basic structure shared by all English sentences (S → NP + VP)
- Read and interpret tree diagrams
- Recognize heads, modifiers, and complements in phrases
- Understand how hierarchical structure determines meaning
- Apply basic diagramming conventions to simple sentences

## Key Terms

- Tree diagram
- Node
- Constituent
- Head
- Modifier
- Complement
- Dominance
- Structural ambiguity
- S → NP + VP

---

## 7.1 Why Diagram Sentences?

When you read a sentence like *The exhausted hiker from Colorado finally reached the summit*, you process it instantly. Your brain parses the words, groups them into meaningful units, and extracts the meaning—all in a fraction of a second, without conscious effort.

But can you explain *how* you understand it? Which words group together? What modifies what? Why does "from Colorado" describe "hiker" rather than "exhausted"? Why does "finally" modify "reached" and not "summit"?

**Sentence diagrams** make visible what your brain does automatically. They transform the linear string of words on the page into a picture of grammatical relationships.

### Analytical Clarity

Diagrams force you to make explicit decisions about every word's function. You cannot diagram a sentence without understanding it. If you are uncertain whether "in the park" modifies "the man" or "saw," the diagram demands a choice—and making that choice reveals your interpretation.

This explicitness is valuable for writing as well as analysis. When a sentence seems unclear or awkward, diagramming it can expose the structural problem.

### Pattern Recognition

After diagramming many sentences, you will begin to recognize structural patterns instantly—even in sentences you have never seen before. You will notice that English sentences, despite their surface variety, follow a small number of fundamental patterns. This recognition transfers to reading and writing.

### A Shared Vocabulary

Diagrams provide a shared vocabulary for discussing sentence structure. Instead of saying "that part," you can point to a specific node or branch. Instead of vague intuitions about what "sounds right," you can make precise claims about structural relationships.

### Revealing Hidden Structure

Most importantly, diagrams reveal that sentences have **hierarchical structure**—structure that is not obvious from the linear sequence of words. Consider:

*Flying planes can be dangerous.*

This sentence is ambiguous. It could mean:
1. The activity of flying planes is dangerous.
2. Planes that are flying can be dangerous.

The words are the same in both readings, but the structure differs. A diagram makes this structural difference visible—two different diagrams for two different meanings.

---

## 7.2 The Basic Structure of English Sentences

Every English sentence—from the simplest to the most complex—shares a fundamental structure.

### S → NP + VP

At its core, every sentence (S) divides into two parts:
- A **noun phrase (NP)** functioning as the subject
- A **verb phrase (VP)** functioning as the predicate

```
         S
       /   \
     NP     VP
   (subject) (predicate)
```

The subject NP tells us *who or what* the sentence is about. The predicate VP tells us *what the subject does, is, or experiences*.

Consider these sentences:

| Sentence | Subject NP | Predicate VP |
|----------|-----------|--------------|
| *Dogs bark.* | Dogs | bark |
| *The old man sat quietly.* | The old man | sat quietly |
| *My brilliant sister from Ohio won the prize.* | My brilliant sister from Ohio | won the prize |

No matter how complex the sentence becomes, this basic division remains. The subject can grow elaborate (*The extremely talented young musician from the small town in rural Pennsylvania who had never performed professionally before*...) and the predicate can become equally elaborate (...*suddenly found herself standing on the stage of Carnegie Hall*). But the fundamental structure—subject NP plus predicate VP—persists.

### What's in the NP?

A noun phrase is built around a noun (its **head**). The simplest NP is just a noun or pronoun:

- *Dogs* bark.
- *She* arrived.

But NPs can include additional elements:
- **Determiners**: *the* dog, *my* sister
- **Adjectives**: the *old* dog, my *brilliant* sister
- **Prepositional phrases**: the dog *on the porch*, my sister *from Ohio*
- **Relative clauses**: the dog *that barked*, my sister *who lives in Ohio*

All of these elements cluster around the head noun, forming a unit—the noun phrase.

### What's in the VP?

A verb phrase is built around a verb (its **head**). The simplest VP is just a verb:

- Dogs *bark*.
- She *arrived*.

But VPs typically include additional elements:
- **Objects**: She *read the book*.
- **Complements**: He *is a doctor*. She *became famous*.
- **Adverbials**: She *arrived yesterday*. He *spoke loudly*.

The verb phrase contains everything in the predicate—the verb itself plus whatever follows it.

---

## 7.3 Tree Diagrams: Reading and Interpreting

This textbook uses **tree diagrams** (also called phrase structure trees or constituent trees) to represent sentence structure. Tree diagrams show how words group into phrases and phrases group into larger structures.

### The Components of a Tree

**Nodes**: Points in the tree, labeled with category symbols (S, NP, VP, N, V, etc.). Each node represents either a word or a phrase.

**Branches**: Lines connecting nodes, showing which elements belong together. Elements connected to the same higher node form a unit.

**Dominance**: A node dominates everything beneath it. The S node at the top dominates the entire sentence. An NP node dominates everything in that noun phrase.

### Common Labels

| Label | Meaning | Examples |
|-------|---------|----------|
| S | Sentence | Complete clause |
| NP | Noun phrase | *the dog*, *she*, *my old friend* |
| VP | Verb phrase | *runs*, *ate the sandwich*, *is happy* |
| PP | Prepositional phrase | *in the house*, *with enthusiasm* |
| AdjP | Adjective phrase | *very tall*, *happy* |
| AdvP | Adverb phrase | *quickly*, *very slowly* |
| N | Noun | *dog*, *happiness*, *Sarah* |
| V | Verb | *run*, *is*, *consider* |
| Adj | Adjective | *tall*, *blue*, *interesting* |
| Adv | Adverb | *quickly*, *never*, *there* |
| Det | Determiner | *the*, *a*, *my*, *this* |
| Pro | Pronoun | *she*, *it*, *they* |
| Prep | Preposition | *in*, *on*, *with*, *to* |
| Conj | Conjunction | *and*, *but*, *or* |
| Aux | Auxiliary | *has*, *will*, *been*, *can* |

### Reading a Simple Tree

**Example**: *The dog barked.*

```
         S
       /   \
     NP      VP
    /  \      |
  Det   N     V
   |    |     |
  the  dog  barked
```

Reading from the top:
1. The S (sentence) divides into NP and VP
2. The NP contains Det (determiner) + N (noun): "the dog"
3. The VP contains just V (verb): "barked"
4. The words themselves appear at the bottom

The tree shows that "the" and "dog" form a unit (the NP), and this unit is the subject of the verb "barked."

### A More Complex Example

**Example**: *The young artist from Paris painted beautiful landscapes.*

```
                          S
                    ______|______
                   |             |
                  NP             VP
           _______|_______    ___|____
          |    |    |     |  |        |
         Det  Adj   N    PP  V       NP
          |    |    |    |   |     __|__
         the young artist |  painted |   |
                          PP       Adj   N
                        __|__       |    |
                       |     |   beautiful landscapes
                      Prep  NP
                       |    |
                      from Paris
```

This tree shows:
- The subject NP contains: determiner + adjective + noun + prepositional phrase
- The PP "from Paris" is *inside* the subject NP—it modifies "artist"
- The VP contains: verb + object NP
- The object NP contains: adjective + noun

### Why Trees Show Hierarchy

Notice that the tree is not just a flat list of words. It shows **grouping**. "The young artist from Paris" is a unit; "beautiful landscapes" is a unit. These units can be moved, replaced, and manipulated as wholes.

For instance, you can replace the entire subject NP with a pronoun:
- *The young artist from Paris* painted... → *She* painted...

You can move the entire object NP to the front for emphasis:
- *Beautiful landscapes*, the young artist from Paris painted.

These operations work on **constituents**—groups that the tree identifies as units.

---

## 7.4 Heads, Modifiers, and Complements

Every phrase is organized around a **head**—the central, obligatory element that determines the phrase's category and core meaning. Other elements are either **modifiers** (optional elements that add information) or **complements** (elements that complete the head's meaning).

### Heads

The head is the word that the phrase is "about." It determines:
- **Category**: A phrase headed by a noun is a noun phrase; a phrase headed by a verb is a verb phrase
- **Core meaning**: The head provides the basic meaning; other elements elaborate on it
- **Grammatical requirements**: The head determines what complements are needed

In the noun phrase "the tall man," the head is "man." Without "man," you don't have a noun phrase.

In the verb phrase "carefully read the instructions," the head is "read." It determines the phrase's category and requires an object.

### Modifiers

**Modifiers** are optional elements that add information about the head. They can be removed without making the phrase ungrammatical.

**In noun phrases:**
- Adjectives: *the **tall** man*
- Prepositional phrases: *the man **in the hat***
- Relative clauses: *the man **who arrived late***

**In verb phrases:**
- Adverbs: *she spoke **quietly***
- Prepositional phrases: *she works **at a hospital***

Modifiers answer questions like "which one?" "what kind?" "how?" "when?" "where?"

### Complements

**Complements** are elements that complete the meaning of the head. Unlike modifiers, they are often required by the head.

**In verb phrases**, the main verb often requires certain complements:
- Transitive verbs require objects: *She read **the book***.
- Linking verbs require subject complements: *He is **a doctor***.
- Ditransitive verbs require two objects: *She gave **me** **a book***.

The difference between complements and modifiers can be subtle, but one test is obligatoriness: if removing an element makes the sentence feel incomplete, it's likely a complement.

- *She read the book carefully.* → *She read the book.* (OK—"carefully" is a modifier)
- *She read the book carefully.* → *She read carefully.* (Changed meaning—"the book" is a complement)

---

## 7.5 How Structure Determines Meaning

One of the most important lessons of syntax is that **meaning depends on structure**, not just on the words themselves. The same words in different structures produce different meanings.

### Structural Ambiguity

When a sentence has two possible structures, it is **structurally ambiguous**.

**Example**: *I saw the man with binoculars.*

This sentence has two readings:
1. I used binoculars to see the man. (PP modifies VP)
2. I saw the man who had binoculars. (PP modifies NP)

**Structure 1** (PP attaches to VP—adverbial):
```
        S
      /   \
    NP     VP
    |    __|____|___
    I   V    NP    PP
        |     |     |
       saw  the man with binoculars
```

**Structure 2** (PP attaches to NP—adjectival):
```
        S
      /   \
    NP     VP
    |     /  \
    I    V   NP
         |  ___|____
        saw |   |   |
           the man  PP
                    |
              with binoculars
```

The diagrams make the ambiguity explicit. In Structure 1, "with binoculars" modifies how I saw. In Structure 2, it modifies which man I saw.

### More Examples of Structural Ambiguity

**Example**: *Flying planes can be dangerous.*
- Reading 1: The activity of flying planes is dangerous.
- Reading 2: Planes that are flying can be dangerous.

**Example**: *Old men and women gathered.*
- Reading 1: Old men, and women (of any age)
- Reading 2: Old people of both genders

In each case, the ambiguity arises from structural options—different ways of grouping the words.

### Why This Matters

Understanding structural ambiguity matters for several reasons:

**For reading**: Recognizing that a sentence has multiple possible structures helps you interpret texts accurately.

**For writing**: Awareness of structural ambiguity helps you avoid writing sentences that could be misread. If a sentence has an unintended reading, restructure it.

**For analysis**: Structural ambiguity demonstrates that meaning is not just in the words—it's in how the words are organized.

---

## 7.6 Diagramming Conventions

This textbook follows standard conventions for tree diagrams.

### Basic Conventions

1. **Top-down structure**: S is at the top; words are at the bottom
2. **Binary branching preferred**: Most nodes have two daughters, though some have more
3. **Labels on every node**: Each node is labeled with its category
4. **Words as terminals**: Actual words appear only at the bottom of the tree
5. **Lines connect related elements**: Branches show constituency

### Category Labels

Use standard abbreviations consistently:
- Phrases: S, NP, VP, PP, AdjP, AdvP
- Words: N, V, Adj, Adv, Det, Pro, Prep, Conj, Aux

### Handling Complex Structures

For complex structures:
- Nested phrases are shown as branches within branches
- Movement and gaps (in questions, relative clauses) are indicated with traces
- Coordination is shown with parallel branches joined at a higher node

---

## Homework: Introduction to Sentence Diagramming

---

### Part 1: Subject and Predicate Identification (approx. 10 minutes)

**Instructions:** For each sentence, identify the complete subject NP and the complete predicate VP. Then identify the head of each.

#### Example (completed):

**Sentence:** *The exhausted marathon runner from Kenya finally collapsed at the finish line.*

Subject NP: *The exhausted marathon runner from Kenya*
Head of subject NP: *runner*

Predicate VP: *finally collapsed at the finish line*
Head of predicate VP: *collapsed*

---

**1.** *The curious students from the advanced chemistry class carefully examined the unusual compound.*

Subject NP:

Head of subject NP:

Predicate VP:

Head of predicate VP:

**2.** *My extremely talented older sister from Portland won the national competition.*

Subject NP:

Head of subject NP:

Predicate VP:

Head of predicate VP:

**3.** *Several angry protesters outside the courthouse demanded immediate action.*

Subject NP:

Head of subject NP:

Predicate VP:

Head of predicate VP:

---

### Part 2: Heads and Modifiers (approx. 5 minutes)

**Instructions:** For each phrase, identify the head and list all modifiers. Classify each modifier by type (determiner, adjective, adverb, prepositional phrase, etc.).

#### Example (completed):

**Phrase:** *the very tall young basketball player from Chicago*

Head: *player*

Modifiers:
- *the* — determiner
- *very tall* — adjective phrase (containing adverb "very" + adjective "tall")
- *young* — adjective
- *basketball* — noun (functioning adjectivally)
- *from Chicago* — prepositional phrase

---

**4.** *my grandmother's beautiful antique wooden jewelry box*

Head:

Modifiers:

**5.** *extremely carefully*

Head:

Modifiers:

**6.** *quite proud of her remarkable achievement*

Head:

Modifiers:

---

### Part 3: Sentence Writing (approx. 5 minutes)

**Instructions:** Write original sentences following each prompt.

---

**7.** Write a sentence following the basic S → NP + VP structure with a complex subject NP containing at least a determiner, an adjective, and a prepositional phrase:

**8.** Write a sentence that is structurally ambiguous (has two possible meanings due to different possible structures). Then explain both meanings.

Sentence:

Meaning 1:

Meaning 2:

**9.** Expand the simple sentence below by adding modifiers to both the subject NP and the predicate VP:

Original: *Dogs bark.*

Your expanded version:

---

### Part 4: Tree Diagram Analysis (approx. 10 minutes)

**Instructions:** For each sentence, draw a tree diagram showing its hierarchical structure. Label all nodes (S, NP, VP, PP, Det, N, V, Adj, Adv, Prep, etc.). You may draw by hand and photograph, use a digital tool, or describe the structure in bracket notation.

#### Example (completed):

**Sentence:** *The cat slept.*

Tree diagram (bracket notation): [S [NP [Det the] [N cat]] [VP [V slept]]]

Or as a visual tree:
```
       S
     /   \
   NP     VP
  /  \     |
Det   N    V
 |    |    |
the  cat  slept
```

---

**10.** Diagram: *The dog barked loudly.*

---

**11.** Diagram: *The talented student from Ohio won the award.*

---

**12.** Diagram: *She carefully read the interesting book in the library.*

---

### Part 5: Structural Ambiguity Analysis (approx. 10 minutes)

**Instructions:** Analyze the structurally ambiguous sentences below.

---

**13.** The sentence *I saw the man with the telescope* is structurally ambiguous.

a) Describe the two possible meanings:

Meaning 1:

Meaning 2:

b) For each meaning, explain how the PP "with the telescope" attaches differently:

Attachment for Meaning 1:

Attachment for Meaning 2:

c) Draw or describe a simple tree structure for ONE of the readings:

---

**14.** The sentence *Old men and women attended the meeting* is structurally ambiguous.

a) Describe the two possible meanings:

Meaning 1:

Meaning 2:

b) Explain what structural difference creates the ambiguity:

---

**15.** In 3-4 sentences, explain why understanding hierarchical sentence structure (as shown in tree diagrams) matters for both reading comprehension and clear writing. Use a specific example to support your explanation.

---

*Total estimated time: 30-40 minutes*

---

## Chapter Summary

- **Sentence diagrams** make visible the hierarchical structure of sentences.
- Every English sentence follows the basic pattern **S → NP + VP**.
- **Tree diagrams** show how words group into phrases and phrases into sentences.
- **Heads** are the central elements of phrases; **modifiers** add optional information; **complements** complete meaning.
- **Structural ambiguity** arises when words can be grouped in multiple ways.
- Understanding structure is essential for accurate interpretation and clear writing.

---

## Glossary

**Complement**: An element that completes the meaning of a head; often required by the head.

**Constituent**: A word or group of words that functions as a structural unit.

**Dominance**: The relationship in a tree where a higher node contains lower nodes.

**Head**: The central, obligatory element of a phrase that determines its category.

**Modifier**: An optional element that adds information about a head.

**Node**: A labeled point in a tree diagram representing a word or phrase category.

**Structural ambiguity**: A situation where a sentence has multiple possible structures, each with a different meaning.

**Tree diagram**: A visual representation of sentence structure showing hierarchical relationships between constituents.
