# How to Use SyntaxTreeHybrid

## Getting Started

Open SyntaxTreeHybrid in your web browser (your instructor will provide the link). You will see four main areas:

| Area | Location | What It Does |
|------|----------|--------------|
| **Top palette bar** | Top of screen | Clause and phrase tiles: S, NP, VP, PP, ADJP, ADVP |
| **Canvas** | Center | Where your tree diagram appears |
| **Right panel** | Right side | "Add Word" input box and Bracket Notation editor |
| **Bottom palette bar** | Bottom of screen | Part-of-speech tiles: NOUN, VERB, ADJ, ADV, DET, PREP, etc. |

## Which Method Should I Use?

SyntaxTreeHybrid gives you two ways to build syntax trees. You can use either one, or mix and match.

| | **Drag and Drop** | **Bracket Notation** |
|---|---|---|
| **Best for** | Beginners; visual learners | Speed; experienced users |
| **Pros** | Intuitive and visual; you can see the tree take shape as you build it | Much faster once you learn the syntax; easy to copy, paste, and share |
| **Cons** | Slower for complex trees; requires more clicks and drags | Steeper learning curve; harder to spot mistakes at first |
| **Recommendation** | Start here to understand how trees work | Switch to this once you are comfortable with tree structures |

Both methods stay synchronized — if you build a tree by dragging tiles, the bracket notation updates automatically on the right, and vice versa.

## Method 1: Drag and Drop

### Adding Phrase and Part-of-Speech Tiles

1. Find the tile you need on the **top palette bar** (for phrases like NP, VP, PP, ADJP, ADVP) or the **bottom palette bar** (for parts of speech like NOUN, VERB, ADJ, ADV, DET, PREP).
2. **Click and drag** the tile from the palette onto the canvas.
3. Release the tile where you want it. Do not worry about exact placement — you can move tiles around after dropping them.

### Connecting Tiles (Parent to Child)

Once you have tiles on the canvas, you need to connect them to show the tree structure:

1. **Drag a child tile** close to the tile you want to be its parent.
2. When the child is close enough, a line will automatically appear connecting the two tiles.
3. The child tile will snap into position below its parent.

### Changing a Connection

If you connected a tile to the wrong parent:

1. **Click on the line** connecting the two tiles. This removes the connection.
2. Now **drag the child tile** close to the correct parent tile to create a new connection.

### Adding Words (Terminal Nodes)

Words go at the bottom of each branch. To add a word:

1. Find the **"Add Word"** input box on the right panel.
2. **Type your word** in the text box (e.g., *dogs*).
3. A preview tile will appear next to the text box.
4. **Drag the preview tile** onto the canvas and drop it near the part-of-speech tile it belongs under (e.g., drag *dogs* near the NOUN tile).
5. The word tile will connect automatically.

### Editing Text on a Tile

If you need to change the label on any tile that is already on the canvas:

1. **Ctrl+click** (or **Cmd+click** on Mac) on the tile you want to edit.
2. A text cursor will appear — type the new label.
3. Click elsewhere on the canvas to finish editing.

### Deleting Tiles

To remove a tile from the canvas:

1. **Click** on the tile to select it (you will see it highlighted).
2. Press the **Delete** key on your keyboard.
3. The tile and any lines connected to it will be removed.

### Deleting Connection Lines

To remove a line without deleting either tile:

1. **Click directly on the line** connecting two tiles.
2. The line will disappear, but both tiles remain on the canvas.
3. You can then drag either tile to create a new connection if needed.

## Method 2: Bracket Notation

### How It Works

Bracket notation lets you type your entire tree as text in the **Bracket Notation** box on the right side of the screen. The tree diagram appears automatically on the canvas as you type.

Every node in the tree is wrapped in square brackets. Inside the brackets, you write the **label** first, then its **children** (which are also in brackets).

**Example:** To diagram the sentence *"Dogs bark,"* type:

```
[S [NP [N Dogs]] [VP [V bark]]]
```

This produces the following tree:

![Dogs bark diagram](diagrams/example_dogs_bark.png)

Reading from outside in:

- `[S ...]` — the whole thing is a **Sentence**
- `[NP [N Dogs]]` — the subject is a **Noun Phrase** containing a **Noun** (*Dogs*)
- `[VP [V bark]]` — the predicate is a **Verb Phrase** containing a **Verb** (*bark*)

### Tips for Bracket Notation

- Make sure every opening bracket `[` has a matching closing bracket `]`.
- If your bracket notation has an error, the **status bar** at the bottom of the bracket panel will show a message in red.
- You can clear the text box and start over at any time.

## Key Abbreviations

| Abbreviation | Meaning | Example |
|---|---|---|
| **S** | Sentence | The whole clause |
| **NP** | Noun Phrase | *the big dog* |
| **VP** | Verb Phrase | *runs quickly* |
| **PP** | Prepositional Phrase | *in the park* |
| **ADJP** | Adjective Phrase | *very tall* |
| **ADVP** | Adverb Phrase | *quite slowly* |
| **N** | Noun | *dog, city, music* |
| **V** | Verb | *runs, sings, is* |
| **ADJ** | Adjective | *tall, spicy, old* |
| **ADV** | Adverb | *quickly, very, often* |
| **DET** | Determiner | *the, a, some, many* |
| **PREP** | Preposition | *in, on, with, from* |

## Exporting Your Work

When assignments ask you to submit your diagrams, you need to submit **both** a tree image and the bracket notation.

1. **Download your tree image:** Click the **"download tree"** button in the top-right corner. This saves a PNG image file.
2. **Copy your bracket notation:** Click the **"copy tree"** button in the top-left corner, or select all the text in the bracket notation box and copy it (Ctrl+C).
3. **Submit both** for each exercise.

## General Tips

- Use the **zoom controls** (+, -, Reset) in the top-right corner of the canvas to adjust your view.
- If something goes wrong, you can always clear the bracket notation box and start fresh.
- Try building the same tree both ways (drag-and-drop, then bracket notation) to see how they compare.
