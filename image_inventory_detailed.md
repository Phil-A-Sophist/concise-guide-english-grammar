# Detailed Image Inventory and Chapter Mapping

## Sentence Diagram Images for Textbook

### Chapter 5: Parts of Speech Overview
*Basic phrase structure*

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| (Create new or use existing ASCII) | diagram-05-np-basic.png | Basic NP tree | Demonstrate NP structure |

### Chapter 10: Prepositional Phrases

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F25 - W6D2 - 3110_image2.png | diagram-10-pp-dogs-chase.png | "dogs chase after cats" with PP | PP as adverbial |
| F25 W6D1 - 3110_image7.png | diagram-10-pp-fight.png | "My dogs got in a fight" with PP | PP in sentence |

### Chapter 11: Basic Sentence Elements
*Intransitive patterns*

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| (Create simple S-V diagram) | diagram-11-basic-sv.png | Simple subject-verb | Basic sentence structure |

### Chapter 12: The Six Basic Sentence Patterns

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F25 - W6D2 - 3110_image9.png | diagram-12-intransitive.png | "All dogs go home" | Pattern 1: Intransitive |
| F25 W6D1 - 3110_image2.png | diagram-12-copular-be-np.png | "Dogs are mammals" | Pattern 2: Copular be (NP) |
| F25 W6D1 - 3110_image3.png | diagram-12-copular-be-adj.png | "Dogs are dumb" | Pattern 2: Copular be (AdjP) |
| F25 W6D1 - 3110_image4.png | diagram-12-copular-be-pp.png | "My dogs were in the house" | Pattern 2: Copular be (PP) |
| F25 W6D1 - 3110_image5.png | diagram-12-linking-adj.png | "Dogs seem dumb" | Pattern 3: Linking verb (AdjP) |
| F25 - W6D2 - 3110_image5.png | diagram-12-linking-adj2.png | "My dog seems dumb" | Pattern 3: Linking verb |
| F25 - W6D2 - 3110_image6.png | diagram-12-linking-np.png | "My dog became a butthead" | Pattern 3: Linking verb (NP) |
| F25 W6D1 - 3110_image6.png | diagram-12-linking-np2.png | "Wolves became dogs" | Pattern 3: Linking verb (NP) |
| F25 - W6D2 - 3110_image7.png | diagram-12-transitive-simple.png | "dogs chase cats" | Pattern 4: Transitive |
| F25 - W6D2 - 3110_image8.png | diagram-12-transitive-pro.png | "My dog kisses me" | Pattern 4: Transitive (pronoun obj) |
| F25 - W6D2 - 3110_image10.png | diagram-12-ditransitive.png | "Phillip mailed Jean flowers" | Pattern 5: Ditransitive (IO+DO) |

### Chapter 13: Compound Sentences

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F25 - W8D1 - Compound and Complex Sentences_image2.png | diagram-13-compound-subj.png | "Frodo and Sam travel" | Compound subject |
| F25 - W8D1 - Compound and Complex Sentences_image3.png | diagram-13-compound-pred.png | "Gandalf thinks and acts" | Compound predicate |
| F25 - W8D1 - Compound and Complex Sentences_image4.png | diagram-13-compound-sent.png | "Suzie yelled and Tommy cried" | Compound sentence |

### Chapter 14: Complex Sentences

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F25 - W8D1 - Compound and Complex Sentences_image5.png | diagram-14-complex-sub.png | "Suzie yelled when Tommy cried" | Subordinate clause |

### Chapter 16: Auxiliary Verbs

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F25 - W11D1_image2.png | diagram-16-aux-structure1.png | "Ahmed has been dancing the salsa on Fridays" | Aux verb structure |
| F25 - W11D1_image3.png | diagram-16-aux-structure2.png | Same sentence with MVP notation | Aux with MVP |
| F25 - W11D1_image4.png | (check content) | Possibly modal structure | Modal diagramming |

### Chapter 22: Relative Clauses

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F2 Class (Adverbials)_image5.png | diagram-22-relative.png | "the man who fell cried" | Relative clause structure |

### Chapter 25: Sentence Diagramming
*Showcase chapter - multiple diagrams demonstrating the technique*

Use selection of diagrams from above plus:

| Current Filename | New Filename | Description | Use |
|-----------------|--------------|-------------|-----|
| F25 - Video - Parts of Speech One_image2.png | diagram-25-basic-tree.png | Basic tree structure | Introduction to trees |
| F25 - Video - Parts of Speech One_image3.png | diagram-25-example2.png | Check content | Demonstration |

---

## Images to Exclude (Not Sentence Diagrams)

These are course logos, decorative images, or duplicates:

- All `*_image1.jpeg` files (7.8KB course header - identical across PPTs)
- `F25 - W1D1 - 3110_image5.png` (256KB - likely decorative/photo)
- `F25 - W1D2 - 3110_image6.png` (270KB - likely decorative/photo)
- `F25 - W1D2 - 3110_image5.jpeg` (14KB - check content)
- Duplicate images from "Copy" PPT file

---

## Renaming Script

```python
import os
import shutil
from pathlib import Path

PROJECT_DIR = Path(r"C:\Users\irphy\Documents\bookmaker\Writing Projects\concise_guide_to_english_grammar")
SOURCE_DIR = PROJECT_DIR / "assets" / "images" / "diagrams"
TARGET_DIR = PROJECT_DIR / "assets" / "images" / "diagrams" / "renamed"

RENAME_MAP = {
    "F25 - W6D2 - 3110_image2.png": "diagram-10-pp-dogs-chase.png",
    "F25 W6D1 - 3110_image7.png": "diagram-10-pp-fight.png",
    "F25 - W6D2 - 3110_image9.png": "diagram-12-intransitive.png",
    "F25 W6D1 - 3110_image2.png": "diagram-12-copular-be-np.png",
    "F25 W6D1 - 3110_image3.png": "diagram-12-copular-be-adj.png",
    "F25 W6D1 - 3110_image4.png": "diagram-12-copular-be-pp.png",
    "F25 W6D1 - 3110_image5.png": "diagram-12-linking-adj.png",
    "F25 - W6D2 - 3110_image5.png": "diagram-12-linking-adj2.png",
    "F25 - W6D2 - 3110_image6.png": "diagram-12-linking-np.png",
    "F25 W6D1 - 3110_image6.png": "diagram-12-linking-np2.png",
    "F25 - W6D2 - 3110_image7.png": "diagram-12-transitive-simple.png",
    "F25 - W6D2 - 3110_image8.png": "diagram-12-transitive-pro.png",
    "F25 - W6D2 - 3110_image10.png": "diagram-12-ditransitive.png",
    "F25 - W8D1 - Compound and Complex Sentences_image2.png": "diagram-13-compound-subj.png",
    "F25 - W8D1 - Compound and Complex Sentences_image3.png": "diagram-13-compound-pred.png",
    "F25 - W8D1 - Compound and Complex Sentences_image4.png": "diagram-13-compound-sent.png",
    "F25 - W8D1 - Compound and Complex Sentences_image5.png": "diagram-14-complex-sub.png",
    "F25 - W11D1_image2.png": "diagram-16-aux-structure1.png",
    "F25 - W11D1_image3.png": "diagram-16-aux-structure2.png",
    "F2 Class (Adverbials)_image5.png": "diagram-22-relative.png",
}

TARGET_DIR.mkdir(parents=True, exist_ok=True)

for old_name, new_name in RENAME_MAP.items():
    src = SOURCE_DIR / old_name
    dst = TARGET_DIR / new_name
    if src.exists():
        shutil.copy2(src, dst)
        print(f"Copied: {old_name} -> {new_name}")
    else:
        print(f"Not found: {old_name}")
```

---

## PreTeXt Figure Templates

### Basic Figure for Sentence Diagram

```xml
<figure xml:id="fig-pattern-intransitive">
  <caption>Tree diagram of an intransitive sentence</caption>
  <image source="diagrams/diagram-12-intransitive.png" width="60%">
    <description>
      A tree diagram showing the sentence "All dogs go home" with S at the root,
      branching into NP (Det "All" + N "dogs") and VP (V "go" + NP "home").
    </description>
  </image>
</figure>
```

### Cross-reference Usage

```xml
<p>As shown in <xref ref="fig-pattern-intransitive"/>, an intransitive sentence
consists of a subject noun phrase and a verb phrase with no complement.</p>
```

---

## Summary Statistics

- **Total images extracted**: 87
- **Useful sentence diagrams identified**: ~25
- **Duplicate/decorative images**: ~15 (course headers)
- **Images needing verification**: ~47 (may contain additional useful diagrams)

---

*Detailed inventory completed: Phase 1*
