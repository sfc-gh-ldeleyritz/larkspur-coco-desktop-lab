---
name: larkspur-deck
description: Build a short Larkspur slide deck as an HTML file and a PowerPoint file, saved to the user's Downloads folder. Use when the user asks for slides, a deck, a presentation, an HTML deck or a .pptx from Larkspur documents or data.
---

# Larkspur deck

Turn a document or query result into a short deck. One JSON spec drives both outputs, so the HTML preview and the PowerPoint file always match. The script applies the Blackfinch Group palette (navy, coral, teal) with no logo; do not change the colours.

## Steps

1. **Read the source.** Use the documents or data the user names. Every figure on a slide must come from that source. If a figure is missing, leave it out rather than estimate it.
2. **Plan the slides.** Default to 5 slides: a title slide, 3 content slides, a closing slide with next steps. Use the user's slide count if they give one.
3. **Write the copy.**
   - Titles are labels with figures, not sentences. Example: "Generation: 384.5 MW, 6.2% below forecast".
   - At most 5 bullets a slide, each under 15 words.
   - Prefer a `stats` or `table` slide over bullets when the content is numbers.
   - Add a `source` line on any slide with figures, naming the document or table.
   - Put the explanation in `notes`, written as what the presenter will say.
   - No dashes as punctuation, no marketing words, no emojis.
4. **Write the spec** to a JSON file in the working folder, for example `deck.json`. Shape:

   ```json
   {
     "file_name": "larkspur-ic-generation-q3",
     "title": "Deck title",
     "slides": [
       {"type": "title", "title": "...", "subtitle": "Audience, date"},
       {"type": "stats", "title": "...", "stats": [{"value": "384.5 MW", "label": "Total generation"}], "source": "..."},
       {"type": "table", "title": "...", "columns": ["Site", "Variance"], "rows": [["Kestrel Ridge", "-18%"]], "source": "..."},
       {"type": "bullets", "title": "...", "bullets": ["..."], "notes": "..."},
       {"type": "closing", "title": "Next steps: 3 actions", "bullets": ["..."]}
     ]
   }
   ```

5. **Build both files.** Run the script in this skill's `scripts/` folder. It writes to `~/Downloads` by default.

   ```bash
   uv run --with python-pptx <skill-folder>/scripts/build_deck.py deck.json
   ```

   If `uv` is not installed, run `python3 -m pip install --user python-pptx`, then `python3 <skill-folder>/scripts/build_deck.py deck.json`.

   If python-pptx cannot be installed, run with `--html-only`, tell the user, and stop there.

6. **Show the result.** Open the HTML file in the CoCo browser so the user can review it. Give both file paths. Tell the user the PowerPoint file is in Downloads and opens in PowerPoint, Keynote or Google Slides.
7. **Edits.** When the user asks for a change, edit the JSON spec and rebuild both files. Never edit the HTML or PPTX by hand.
