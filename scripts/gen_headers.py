"""Generates the section-header and divider SVGs in assets/.

Run: python scripts/gen_headers.py
Every header is the same shape: a small monospace label with a prompt-style
prefix, a hairline rule, and a short accent segment under it.
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

BG, RULE, ACCENT, FG, DIM = "#0d1117", "#1f2733", "#1f6feb", "#e6edf3", "#6e7681"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

HEADER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 64" width="1000" height="64" font-family="{font}">
  <defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{accent}"/><stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
  </linearGradient></defs>
  <rect width="1000" height="64" fill="{bg}"/>
  <text x="0" y="26" fill="{accent}" font-size="16" font-weight="700">#</text>
  <text x="22" y="26" fill="{fg}" font-size="18" font-weight="700" letter-spacing="1">{label}</text>
  <text x="1000" y="26" fill="{dim}" font-size="13" text-anchor="end">{note}</text>
  <line x1="0" y1="42" x2="1000" y2="42" stroke="{rule}"/>
  <line x1="0" y1="42" x2="180" y2="42" stroke="url(#a)" stroke-width="2"/>
</svg>
"""

RULE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 24" width="1000" height="24">
  <rect width="1000" height="24" fill="{bg}"/>
  <line x1="0" y1="12" x2="1000" y2="12" stroke="{rule}"/>
  <circle cx="500" cy="12" r="2.5" fill="{accent}"/>
</svg>
"""

# (filename, label, right-aligned note)
HEADERS = [
    ("h-built",  "things i've built",   "gridpulse · gateway · cidra"),
    ("h-exp",    "experience",          "two internships, sole developer"),
    ("h-path",   "how i got here",      "2023 → now"),
    ("h-oss",    "open source",         "early days"),
    ("h-stack",  "stack",               "what i reach for"),
    ("h-dsa",    "dsa",                 "852 solved"),
    ("h-lately", "lately",              "contribution activity"),
]


def main():
    OUT.mkdir(exist_ok=True)
    for name, label, note in HEADERS:
        (OUT / f"{name}.svg").write_text(
            HEADER.format(font=FONT, bg=BG, rule=RULE, accent=ACCENT,
                          fg=FG, dim=DIM, label=label, note=note),
            encoding="utf-8")
    (OUT / "rule.svg").write_text(
        RULE_SVG.format(bg=BG, rule=RULE, accent=ACCENT), encoding="utf-8")
    print(f"wrote {len(HEADERS) + 1} files to {OUT}")


if __name__ == "__main__":
    main()
