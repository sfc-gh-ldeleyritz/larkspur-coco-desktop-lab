"""Build a Larkspur slide deck as HTML and PPTX from one JSON spec.

Usage:
    uv run --with python-pptx build_deck.py deck.json [--out-dir DIR]
    python3 build_deck.py deck.json --html-only

Spec shape:
{
  "title": "Deck title",
  "subtitle": "Audience, date",
  "slides": [
    {"type": "title", "title": "...", "subtitle": "..."},
    {"type": "bullets", "title": "...", "bullets": ["...", "..."], "notes": "..."},
    {"type": "stats", "title": "...", "stats": [{"value": "384.5 MW", "label": "..."}]},
    {"type": "table", "title": "...", "columns": ["A", "B"], "rows": [["1", "2"]]},
    {"type": "closing", "title": "...", "bullets": ["..."]}
  ]
}
"""
import argparse
import html
import json
import os
import sys

# Blackfinch Group palette (blackfinch.com stylesheet)
MIDNIGHT = "23293A"   # group navy: text, cover background
MID_BLUE = "23293A"   # stat values, table headers
SF_BLUE = "E6361A"    # coral accent bar
TEAL = "449CB3"       # secondary accent
MUTED = "5D759E"
BORDER = "E9EAEB"
BG_SECTION = "F6F4F3"
WHITE = "FFFFFF"


def esc(text):
    return html.escape(str(text))


def html_slide(s):
    kind = s.get("type", "bullets")
    title = esc(s.get("title", ""))
    if kind == "title":
        return (f'<section class="slide cover"><h1>{title}</h1>'
                f'<p class="sub">{esc(s.get("subtitle", ""))}</p></section>')
    body = ""
    if kind in ("bullets", "closing"):
        body = "<ul>" + "".join(f"<li>{esc(b)}</li>" for b in s.get("bullets", [])) + "</ul>"
    elif kind == "stats":
        body = '<div class="stats">' + "".join(
            f'<div class="stat"><div class="v">{esc(x["value"])}</div>'
            f'<div class="l">{esc(x.get("label", ""))}</div></div>'
            for x in s.get("stats", [])) + "</div>"
    elif kind == "table":
        head = "".join(f"<th>{esc(c)}</th>" for c in s.get("columns", []))
        rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>"
                       for r in s.get("rows", []))
        body = f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"
    source = s.get("source")
    src = f'<p class="src">Source: {esc(source)}</p>' if source else ""
    return f'<section class="slide"><h2>{title}</h2>{body}{src}</section>'


def build_html(spec, path):
    slides = "\n".join(html_slide(s) for s in spec["slides"])
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec.get("title", "Deck"))}</title>
<style>
body {{ margin:0; background:#{BG_SECTION}; font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; color:#{MIDNIGHT}; }}
.slide {{ box-sizing:border-box; width:1280px; height:720px; margin:24px auto; background:#{WHITE};
  border:1px solid #{BORDER}; border-radius:16px; padding:64px 80px; position:relative;
  border-top:8px solid #{SF_BLUE}; page-break-after:always; overflow:hidden; }}
.cover {{ background:#{MIDNIGHT}; color:#{WHITE}; display:flex; flex-direction:column; justify-content:center; }}
h1 {{ font-size:54px; margin:0 0 16px; }} h2 {{ font-size:36px; margin:0 0 32px; color:#{MIDNIGHT}; }}
.sub {{ font-size:22px; color:#{TEAL}; margin:0; }}
ul {{ font-size:24px; line-height:1.6; padding-left:28px; }} li {{ margin-bottom:10px; }}
.stats {{ display:flex; gap:24px; flex-wrap:wrap; }}
.stat {{ flex:1; min-width:220px; border:1px solid #{BORDER}; border-radius:16px; padding:28px; background:#{BG_SECTION}; }}
.stat .v {{ font-size:44px; font-weight:700; color:#{MID_BLUE}; }} .stat .l {{ font-size:18px; color:#{MUTED}; margin-top:8px; }}
table {{ border-collapse:collapse; width:100%; font-size:20px; }}
th {{ background:#{MID_BLUE}; color:#{WHITE}; text-align:left; padding:12px 16px; }}
td {{ border-bottom:1px solid #{BORDER}; padding:12px 16px; }}
.src {{ position:absolute; bottom:28px; left:80px; font-size:14px; color:#{MUTED}; }}
@media print {{ body {{ background:#{WHITE}; }} .slide {{ margin:0; border-radius:0; }} @page {{ size:1280px 720px; margin:0; }} }}
</style></head><body>
{slides}
</body></html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)


def build_pptx(spec, path):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Inches, Pt

    def rgb(h):
        return RGBColor.from_string(h)

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, value, size, color=MIDNIGHT, bold=False):
        tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = str(value)
        p.font.size, p.font.bold, p.font.name = Pt(size), bold, "Arial"
        p.font.color.rgb = rgb(color)
        return tf

    def bar(slide):
        shp = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
        shp.fill.solid(); shp.fill.fore_color.rgb = rgb(SF_BLUE); shp.line.fill.background()

    for s in spec["slides"]:
        slide = prs.slides.add_slide(blank)
        kind = s.get("type", "bullets")
        if kind == "title":
            bg = slide.background.fill
            bg.solid(); bg.fore_color.rgb = rgb(MIDNIGHT)
            text(slide, 0.9, 2.6, 11.5, 1.4, s.get("title", ""), 44, WHITE, True)
            text(slide, 0.9, 4.0, 11.5, 0.8, s.get("subtitle", ""), 20, TEAL)
        else:
            bar(slide)
            text(slide, 0.9, 0.6, 11.5, 0.9, s.get("title", ""), 30, MIDNIGHT, True)
            if kind in ("bullets", "closing"):
                tf = text(slide, 0.9, 1.7, 11.5, 5.0, "", 20)
                for i, b in enumerate(s.get("bullets", [])):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.text = "\u2022  " + str(b)
                    p.font.size, p.font.name = Pt(20), "Arial"
                    p.font.color.rgb = rgb(MIDNIGHT)
                    p.space_after = Pt(10)
            elif kind == "stats":
                stats = s.get("stats", [])
                n = max(len(stats), 1)
                w = (11.5 - 0.3 * (n - 1)) / n
                for i, st in enumerate(stats):
                    x = 0.9 + i * (w + 0.3)
                    box = slide.shapes.add_shape(5, Inches(x), Inches(2.0), Inches(w), Inches(2.4))
                    box.fill.solid(); box.fill.fore_color.rgb = rgb(BG_SECTION)
                    box.line.color.rgb = rgb(BORDER)
                    text(slide, x + 0.25, 2.3, w - 0.5, 1.0, st["value"], 34, MID_BLUE, True)
                    text(slide, x + 0.25, 3.3, w - 0.5, 1.0, st.get("label", ""), 15, MUTED)
            elif kind == "table":
                cols, rows = s.get("columns", []), s.get("rows", [])
                tbl = slide.shapes.add_table(len(rows) + 1, len(cols), Inches(0.9), Inches(1.7),
                                             Inches(11.5), Inches(0.5 * (len(rows) + 1))).table
                for c, name in enumerate(cols):
                    cell = tbl.cell(0, c)
                    cell.text = str(name)
                    cell.fill.solid(); cell.fill.fore_color.rgb = rgb(MID_BLUE)
                    f = cell.text_frame.paragraphs[0].font
                    f.size, f.bold, f.name = Pt(14), True, "Arial"
                    f.color.rgb = rgb(WHITE)
                for r, row in enumerate(rows, start=1):
                    for c, val in enumerate(row):
                        cell = tbl.cell(r, c)
                        cell.text = str(val)
                        cell.fill.solid(); cell.fill.fore_color.rgb = rgb(WHITE if r % 2 else BG_SECTION)
                        f = cell.text_frame.paragraphs[0].font
                        f.size, f.name = Pt(13), "Arial"
                        f.color.rgb = rgb(MIDNIGHT)
            if s.get("source"):
                text(slide, 0.9, 6.8, 11.5, 0.4, "Source: " + s["source"], 11, MUTED)
        if s.get("notes"):
            slide.notes_slide.notes_text_frame.text = s["notes"]
    prs.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out-dir", default=os.path.expanduser("~/Downloads"))
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args()
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    base = spec.get("file_name") or os.path.splitext(os.path.basename(args.spec))[0]
    os.makedirs(args.out_dir, exist_ok=True)
    html_path = os.path.join(args.out_dir, base + ".html")
    build_html(spec, html_path)
    print("HTML:", html_path)
    if args.html_only:
        return
    try:
        import pptx  # noqa: F401
    except ImportError:
        sys.exit("python-pptx is missing. Run with: uv run --with python-pptx build_deck.py ... "
                 "or install it with: python3 -m pip install --user python-pptx")
    pptx_path = os.path.join(args.out_dir, base + ".pptx")
    build_pptx(spec, pptx_path)
    print("PPTX:", pptx_path)


if __name__ == "__main__":
    main()
