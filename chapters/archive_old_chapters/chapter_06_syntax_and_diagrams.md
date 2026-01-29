# 6. Syntax and Diagrams

## Learning Objectives

By the end of this chapter, you will be able to:
- Explain what sentence diagrams represent and why they're useful
- Identify the basic structure shared by all English sentences
- Read and interpret tree diagrams
- Recognize heads, modifiers, and complements in phrases
- Understand how hierarchical structure determines meaning
- Apply basic diagramming conventions to simple sentences

---

## 6.1 Why Diagram Sentences?

When you read a sentence like *The exhausted hiker from Colorado finally reached the summit*, you process it instantly. Your brain parses the words, groups them into meaningful units, and extracts the meaning—all in a fraction of a second, without conscious effort.

But can you explain *how* you understand it? Which words group together? What modifies what? Why does "from Colorado" describe "hiker" rather than "exhausted"? Why does "finally" modify "reached" and not "summit"?

Sentence diagrams make visible what your brain does automatically. They transform the linear string of words on the page into a picture of grammatical relationships. This visualization serves several purposes.

### Analytical Clarity

Diagrams force you to make explicit decisions about every word's function. You can't diagram a sentence without understanding it. If you're uncertain whether "in the park" modifies "the man" or "saw," the diagram demands a choice—and making that choice reveals your interpretation.

This explicitness is valuable for writing as well as analysis. When a sentence seems unclear or awkward, diagramming it can expose the structural problem. Perhaps a modifier is in an ambiguous position. Perhaps coordinated elements aren't parallel. The diagram makes these issues visible.

### Pattern Recognition

After diagramming many sentences, you'll begin to recognize structural patterns instantly—even in sentences you've never seen before. You'll notice that English sentences, despite their surface variety, follow a small number of fundamental patterns. This recognition transfers to reading and writing: you'll process complex sentences more easily and construct them more confidently.

### A Shared Vocabulary

Diagrams provide a shared vocabulary for discussing sentence structure. Instead of saying "that part," you can point to a specific node or branch. Instead of vague intuitions about what "sounds right," you can make precise claims about structural relationships. This precision matters for learning, teaching, and analysis.

### Revealing Hidden Structure

Most importantly, diagrams reveal that sentences have **hierarchical structure**—structure that isn't obvious from the linear sequence of words. Consider:

*Flying planes can be dangerous.*

This sentence is ambiguous. It could mean:
1. The activity of flying planes is dangerous.
2. Planes that are flying can be dangerous.

The words are the same in both readings, but the structure differs. In the first, "flying" is a gerund (a verb acting as a noun) heading the subject. In the second, "flying" is an adjective modifying "planes." A diagram makes this structural difference visible—two different diagrams for two different meanings.

---

## 6.2 The Basic Structure of English Sentences

Every English sentence—from the simplest to the most complex—shares a fundamental structure. Understanding this structure is the key to understanding English syntax.

### S → NP + VP

At its core, every sentence (S) divides into two parts:
- A **noun phrase (NP)** functioning as the subject
- A **verb phrase (VP)** functioning as the predicate

![Basic S -> NP + VP structure](../assets/diagrams/ch06_basic_structure.svg)

The subject NP tells us *who or what* the sentence is about. The predicate VP tells us *what the subject does, is, or experiences*.

Consider these sentences:

| Sentence | Subject NP | Predicate VP |
|----------|-----------|--------------|
| *Dogs bark.* | Dogs | bark |
| *The old man sat quietly.* | The old man | sat quietly |
| *My brilliant sister from Ohio won the prize.* | My brilliant sister from Ohio | won the prize |

No matter how complex the sentence becomes, this basic division remains. The subject can grow to enormous length (*The extremely talented young musician from the small town in rural Pennsylvania who had never performed professionally before*...) and the predicate can become equally elaborate (...*suddenly found herself standing on the stage of Carnegie Hall in front of thousands of expectant audience members, about to perform the most important concert of her entire life*). But the fundamental structure—subject NP plus predicate VP—persists.

### What's in the NP?

A noun phrase is built around a noun (its **head**). The simplest NP is just a noun or pronoun:

- *Dogs* bark.
- *She* arrived.

But NPs can include additional elements:
- **Determiners**: *the* dog, *my* sister, *three* books
- **Adjectives**: the *old* dog, *my* *brilliant* sister
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

### The Significance of This Structure

Why does this binary division matter? Because it reflects something fundamental about how sentences work. The subject-predicate structure corresponds to a basic semantic distinction: sentences predicate properties or actions of entities.

"Dogs bark" says that a property (barking) is predicated of an entity (dogs). "The old man sat quietly" says that an action (sitting quietly) is predicated of an entity (the old man). This pattern—entity plus predication—underlies virtually all sentences.

Understanding this structure helps you:
- Find the main verb (look in the VP)
- Find the subject (look at what the VP says something about)
- Identify what goes with what (elements are grouped into phrases)
- Diagnose agreement errors (the subject NP must agree with the main verb)

---

## 6.3 Tree Diagrams: Reading and Interpreting

This textbook uses **tree diagrams** (also called phrase structure trees or constituent trees) to represent sentence structure. Tree diagrams show how words group into phrases and phrases group into larger structures.

### The Components of a Tree

**Nodes**: Points in the tree, labeled with category symbols (S, NP, VP, N, V, etc.). Each node represents either a word or a phrase.

**Branches**: Lines connecting nodes, showing which elements belong together. Elements connected to the same higher node form a unit.

**Dominance**: A node dominates everything beneath it. The S node at the top dominates the entire sentence. An NP node dominates everything in that noun phrase.

**Labels**: Each node is labeled with its grammatical category:

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

Here's how to read a tree diagram:

**Example**: *The dog barked.*

![Tree diagram: The dog barked](../assets/diagrams/ch06_dog_barked.svg)

Reading from the top:
1. The S (sentence) divides into NP and VP
2. The NP contains Det (determiner) + N (noun): "the dog"
3. The VP contains just V (verb): "barked"
4. The words themselves appear at the bottom

The tree shows that "the" and "dog" form a unit (the NP), and this unit is the subject of the verb "barked."

### A More Complex Example

**Example**: *The young artist from Paris painted beautiful landscapes.*

![Tree diagram: The young artist from Paris painted beautiful landscapes](../assets/diagrams/ch06_artist_painted.svg)

This tree shows:
- The subject NP contains: determiner ("the") + adjective ("young") + noun ("artist") + prepositional phrase ("from Paris")
- The PP "from Paris" is *inside* the subject NP—it modifies "artist," not the whole sentence
- The VP contains: verb ("painted") + object NP ("beautiful landscapes")
- The object NP contains: adjective ("beautiful") + noun ("landscapes")

### Why Trees Show Hierarchy

Notice that the tree isn't just a flat list of words. It shows **grouping**. "The young artist from Paris" is a unit; "beautiful landscapes" is a unit. These units can be moved, replaced, and manipulated as wholes.

For instance, you can replace the entire subject NP with a pronoun:
- *The young artist from Paris* painted beautiful landscapes. → *She* painted beautiful landscapes.

You can move the entire object NP to the front for emphasis:
- *Beautiful landscapes*, the young artist from Paris painted.

These operations work on constituents—groups that the tree identifies as units.

---

## 6.4 Heads, Modifiers, and Complements

Every phrase is organized around a **head**—the central, obligatory element that determines the phrase's category and core meaning. Other elements are either **modifiers** (optional elements that add information) or **complements** (elements that complete the head's meaning).

### Heads

The head is the word that the phrase is "about." It determines:
- **Category**: A phrase headed by a noun is a noun phrase; a phrase headed by a verb is a verb phrase
- **Core meaning**: The head provides the basic meaning; other elements elaborate on it
- **Grammatical requirements**: The head determines what complements are needed

In the noun phrase "the tall man," the head is "man." "The" and "tall" are additions; without them, you still have a noun phrase (*Man is mortal*), but without "man," you don't.

In the verb phrase "carefully read the instructions," the head is "read." It's the verb that determines the phrase's category and requires an object (the instructions).

### Modifiers

**Modifiers** are optional elements that add information about the head. They can be removed without making the phrase ungrammatical (though the meaning changes).

**In noun phrases:**
- Adjectives: *the **tall** man*
- Prepositional phrases: *the man **in the hat***
- Relative clauses: *the man **who arrived late***

**In verb phrases:**
- Adverbs: *she spoke **quietly***
- Prepositional phrases: *she works **at a hospital***

Modifiers answer questions like "which one?" "what kind?" "how?" "when?" "where?"

### Complements

**Complements** are elements that complete the meaning of the head. Unlike modifiers, they're often required by the head—removing them makes the sentence incomplete or changes its meaning fundamentally.

**In verb phrases**, the main verb often requires certain complements:
- Transitive verbs require objects: *She read **the book***.
- Linking verbs require subject complements: *He is **a doctor***.
- Ditransitive verbs require two objects: *She gave **me** **a book***.

The difference between complements and modifiers can be subtle, but one test is obligatoriness: if removing an element makes the sentence feel incomplete, it's likely a complement.

- *She read the book carefully.* → *She read the book.* (OK—"carefully" is a modifier)
- *She read the book carefully.* → *She read carefully.* (Different meaning—"the book" is a complement)

### Phrase Structure Rules

The organization of phrases follows regular patterns. Linguists capture these patterns with **phrase structure rules**—formulas that describe how phrases are built.

For example:
- **NP → (Det) (Adj)* N (PP)** means a noun phrase consists of an optional determiner, any number of adjectives, a required noun, and an optional PP.
- **VP → V (NP) (PP)** means a verb phrase consists of a required verb, an optional NP object, and an optional PP.

The parentheses indicate optional elements. The asterisk (*) indicates that an element can repeat.

These rules aren't prescriptions for how you should write—they're descriptions of patterns you already follow.

---

## 6.5 How Structure Determines Meaning

One of the most important lessons of syntax is that **meaning depends on structure**, not just on the words themselves. The same words in different structures produce different meanings.

### Structural Ambiguity

When a sentence has two possible structures, it's **structurally ambiguous**.

**Example**: *I saw the man with binoculars.*

This sentence has two readings:
1. I used binoculars to see the man. (PP modifies VP)
2. I saw the man who had binoculars. (PP modifies NP)

**Structure 1** (PP "with binoculars" attached to VP):

![I saw the man with binoculars (PP attaches to VP)](../assets/diagrams/ch06_ambig_binoculars_vp.svg)

**Structure 2** (PP "with binoculars" attached to NP):

![I saw the man with binoculars (PP attaches to NP)](../assets/diagrams/ch06_ambig_binoculars_np.svg)

The diagrams make the ambiguity explicit. In Structure 1, "with binoculars" modifies how I saw. In Structure 2, it modifies which man I saw.

### More Examples of Structural Ambiguity

**Example**: *Flying planes can be dangerous.*

- Reading 1: *[Flying planes]* can be dangerous. (The activity of flying planes)
- Reading 2: *[Flying] planes* can be dangerous. (Planes that are flying)

**Example**: *The professor said the student failed yesterday.*

- Reading 1: The professor said *yesterday* that the student failed. (Yesterday modifies "said")
- Reading 2: The professor said that the student failed *yesterday*. (Yesterday modifies "failed")

### A Worked Example: Coordination Ambiguity

**Example**: *Old men and women gathered.*

This sentence demonstrates a particularly common type of structural ambiguity involving coordination. The adjective "old" might modify just "men," or it might modify the entire coordinated phrase "men and women."

**Reading 1**: Old men, and women (of any age)

In this reading, "old" modifies only "men." The coordinated structure joins two NPs: "old men" and "women."

![Old men and women gathered (only men are old)](../assets/diagrams/ch06_ambig_old_men_1.svg)

**Reading 2**: Old people of both genders

In this reading, "old" modifies the entire coordinated NP "men and women"—both groups are old.

![Old men and women gathered (both are old)](../assets/diagrams/ch06_ambig_old_men_2.svg)

Notice how the tree diagrams make visible what the words alone cannot show. In the first structure, "old" and "men" form a unit (an NP) before combining with "women." In the second structure, "men and women" form a unit first, and then "old" modifies that entire unit.

This kind of ambiguity matters in contexts ranging from legal documents ("old cars and trucks") to everyday conversation ("hot dogs and buns"). Careful writers rephrase to eliminate ambiguity: "old men and old women" (both old) or "women and old men" (only men are old).

In each case, the ambiguity arises from structural options—different ways of grouping the words.

### Why This Matters

Understanding structural ambiguity matters for several reasons:

**For reading**: Recognizing that a sentence has multiple possible structures helps you interpret texts accurately. Sometimes context resolves the ambiguity; sometimes it's genuinely uncertain.

**For writing**: Awareness of structural ambiguity helps you avoid writing sentences that could be misread. If a sentence has an unintended reading, restructure it.

**For analysis**: Structural ambiguity demonstrates that meaning isn't just in the words—it's in how the words are organized. This insight is fundamental to understanding grammar.

---

## 6.6 Basic Sentence Patterns

English sentences follow a limited number of **basic patterns**, determined by the main verb. Each pattern specifies what elements must appear in the VP.

### Pattern 1: Intransitive (S + V)

Some verbs don't require any complement—they can stand alone after the subject.

*Thunder rumbled.*
*The baby slept.*
*She laughed.*

![Thunder rumbled (intransitive pattern)](../assets/diagrams/ch06_intransitive.svg)

Intransitive verbs describe actions or states that don't need an object. Notice the simplicity of the VP—it contains only the verb itself. Of course, intransitive sentences often include adverbials (*Thunder rumbled ominously*, *She laughed nervously*), but these are modifiers, not required elements.

Many verbs are strictly intransitive: *arrive*, *exist*, *die*, *sneeze*. You can't *arrive something* or *exist something*. Other verbs can be either intransitive or transitive depending on context—*eat* in "She ate" is intransitive, but in "She ate an apple," it's transitive.

### Pattern 2: Transitive (S + V + DO)

Transitive verbs require a direct object—an NP that receives the action.

*The cat chased the mouse.*
*She read the book.*
*They built a house.*

![The cat chased the mouse (transitive pattern)](../assets/diagrams/ch06_transitive.svg)

The direct object answers the question "what?" or "whom?" after the verb. Transitive verbs describe actions that affect or involve something beyond the subject—the cat doesn't just chase; it chases *something*. This "something" is what the grammar calls the direct object.

The transitive pattern is extremely common. In fact, when people think of typical sentences, they often imagine the transitive pattern: Actor + Action + Thing Acted Upon. But not all verbs describe actions that affect external objects. Some describe states or conditions of the subject itself.

### Pattern 3: Linking (S + V + SC)

Linking verbs connect the subject to a **subject complement**—an element that describes or identifies the subject.

*She is a doctor.* (NP complement)
*The soup tastes delicious.* (AdjP complement)
*He seems tired.* (AdjP complement)

![She is happy (linking verb pattern)](../assets/diagrams/ch06_linking.svg)

Common linking verbs include *be*, *seem*, *become*, *appear*, *feel*, *look*, *sound*, *taste*, *smell*. The linking pattern is essential for description and definition—it lets us say what things *are*, not just what they *do*.

Notice that the complement after a linking verb describes the *subject*, not something separate. In "She is a doctor," the NP "a doctor" refers to the same person as "she." This differs fundamentally from transitive patterns, where the object is a different entity from the subject. In "She met a doctor," the doctor is someone else.

The patterns so far involve at most one complement. But some verbs require two.

### Pattern 4: Ditransitive (S + V + IO + DO)

Ditransitive verbs take two objects: an **indirect object** (recipient) and a **direct object** (thing given). This pattern describes acts of transfer—giving, telling, showing, sending.

*She gave me a book.*
*He told the children a story.*
*The teacher showed us the answer.*

![She gave me a book (ditransitive pattern)](../assets/diagrams/ch06_ditransitive.svg)

The indirect object (here, "me") typically comes first and identifies the recipient. The direct object ("a book") identifies what is transferred. Notice that both objects are NPs within the VP—they're sisters to the verb, completing its meaning.

You can often rephrase a ditransitive as a transitive with a PP: "She gave a book to me." The meaning is similar, but the structure differs—and sometimes the emphasis shifts.

### Pattern 5: Complex Transitive (S + V + DO + OC)

Some verbs take a direct object plus an **object complement**—an element that describes or identifies the object. This pattern describes causation or judgment: something causes the object to be or become something, or someone judges the object to be something.

*They elected her president.*
*The jury found him guilty.*
*She considers herself an expert.*

![They elected her president (complex transitive with NP)](../assets/diagrams/ch06_complex_trans_np.svg)

The object complement ("president") says something about the direct object ("her")—not about the subject. After the election, *she* is president; *they* are not. This relationship between the direct object and its complement distinguishes complex transitive from ditransitive: in "They gave her a book," the book doesn't describe her; in "They elected her president," president does describe her.

When the complement is an adjective, the structure is similar:

*The jury found him guilty.*

![The jury found him guilty (complex transitive with AdjP)](../assets/diagrams/ch06_complex_trans_adj.svg)

### Why Patterns Matter

These patterns aren't arbitrary—they reflect the different ways verbs relate to the entities and events they describe:

- **Intransitive** verbs describe actions/states that don't affect anything else
- **Transitive** verbs describe actions that affect something (the object)
- **Linking** verbs describe states or changes in the subject
- **Ditransitive** verbs describe transfer from one entity to another
- **Complex transitive** verbs describe causing a change in something

Understanding patterns helps you in concrete ways as both a reader and a writer.

**For using verbs correctly**: Each verb has a preferred pattern (or patterns). If you use a verb in the wrong pattern, the sentence sounds awkward or becomes ungrammatical. *She discussed the problem* is fine (transitive), but *She discussed* alone feels incomplete—*discuss* demands an object. Conversely, *He arrived the station* sounds wrong because *arrive* is intransitive; you need *He arrived at the station*. Knowing patterns means knowing what each verb requires.

**For identifying sentence elements**: When you encounter a complex sentence, pattern knowledge helps you parse it. Consider: *The committee appointed her chair of the department.* Is this ditransitive (two objects: her, chair) or complex transitive (object + complement: her, chair)? The complex transitive reading is correct—"chair of the department" describes who she became, not a separate thing given. Understanding patterns helps you interpret correctly.

**For writing more varied sentences**: Different patterns create different rhythms and effects. A series of short intransitive sentences creates staccato energy: *Night fell. The wind rose. Rain came.* Transitive patterns foreground action and its effects: *The storm destroyed the crops, flooded the roads, and uprooted ancient trees.* Linking patterns work for description and characterization: *The silence was oppressive. The darkness seemed absolute.* Pattern awareness gives you options.

**For diagnosing problems**: When a sentence feels wrong but you can't say why, check the pattern. Many writing problems stem from pattern confusion: mixing up transitive and intransitive uses (*The situation aggravated* vs. *The situation aggravated me*), forgetting required complements (*She considered* vs. *She considered the options*), or misidentifying sentence elements. The fix often becomes clear once you identify the pattern.

---

## 6.7 Looking Ahead: Diagrams in Part II

This chapter has introduced the fundamentals of sentence diagramming: the basic S → NP + VP structure, how to read tree diagrams, the concepts of heads and modifiers, and the major sentence patterns.

In Part II, you'll learn to diagram specific constructions in detail:
- **Chapter 7 (Verbs)**: Verb phrase structure, auxiliary verbs, tense and aspect
- **Chapter 8 (Nouns)**: Complex noun phrase structures, determiners, post-modifiers
- **Chapter 9 (Adjectives)**: Adjective phrases, modification patterns
- **Chapter 10 (Adverbs)**: Adverb phrases, adverbial positions
- **Chapter 11 (Closed Classes)**: Prepositions, determiners, pronouns

Each chapter will include diagrams that show how the relevant phrase types work. By the end of Part II, you'll be able to diagram most sentences you encounter—and more importantly, you'll understand the structural patterns that make English sentences work.

---

## Exercises

### Comprehension Questions

1. What is the basic structure shared by all English sentences? Draw the simplest possible tree.

2. Explain the difference between a head and a modifier. Give an example of each in a noun phrase.

3. What does it mean for a sentence to be structurally ambiguous? Why can't ambiguity be seen from the words alone?

4. List the five basic sentence patterns and give an example of each.

5. What's the difference between a complement and a modifier?

### Diagram Practice

6. Draw tree diagrams for the following simple sentences:
   a. *Birds sing.*
   b. *The cat slept.*
   c. *She is happy.*
   d. *John ate the pizza.*

7. Draw tree diagrams for these sentences with modifiers:
   a. *The old dog barked loudly.*
   b. *A beautiful sunset appeared.*
   c. *She spoke very quietly.*

8. Identify the sentence pattern (intransitive, transitive, linking, ditransitive, or complex transitive):
   a. *The train arrived.*
   b. *She became a lawyer.*
   c. *He gave her flowers.*
   d. *They considered the plan risky.*
   e. *The children played.*
   f. *We elected him leader.*

### Ambiguity Analysis

9. Each sentence below is ambiguous. Describe the two meanings and explain what structural difference creates the ambiguity.
   a. *I saw her duck.*
   b. *The chicken is ready to eat.*
   c. *Visiting relatives can be boring.*

10. Draw two different trees for: *She saw the man with the telescope.*

### Application

11. Find a complex sentence in a newspaper or textbook. Identify:
    - The subject NP
    - The predicate VP
    - The main verb
    - Any modifiers in the subject
    - Any complements or modifiers in the predicate

12. Write three sentences, each illustrating a different sentence pattern. Then draw tree diagrams for each.

---

## Glossary

**Complement**: An element that completes the meaning of a head; often required by the head (e.g., objects of transitive verbs, subject complements after linking verbs).

**Constituent**: A word or group of words that functions as a structural unit; constituents can be identified by movement, replacement, and coordination tests.

**Direct object (DO)**: An NP in the VP that receives the action of a transitive verb.

**Dominance**: The relationship in a tree where a higher node contains (dominates) lower nodes.

**Head**: The central, obligatory element of a phrase that determines its category and core meaning.

**Indirect object (IO)**: An NP in the VP that identifies the recipient in ditransitive constructions.

**Intransitive**: A verb that does not require an object.

**Linking verb**: A verb that connects the subject to a subject complement describing or identifying the subject.

**Modifier**: An optional element that adds information about a head.

**Node**: A labeled point in a tree diagram representing a word or phrase category.

**Object complement (OC)**: An element that describes or identifies the direct object.

**Phrase structure rules**: Formulas that describe how phrases are built from smaller elements.

**Predicate**: The part of the sentence that says something about the subject; corresponds to the VP.

**Structural ambiguity**: A situation where a sentence has multiple possible structures, each with a different meaning.

**Subject**: The NP that the sentence is about; typically what the predicate says something about.

**Subject complement (SC)**: An element after a linking verb that describes or identifies the subject.

**Transitive**: A verb that requires a direct object.

**Tree diagram**: A visual representation of sentence structure showing hierarchical relationships between constituents.
