#!/usr/bin/env python3
"""Render a 1024x1024 newspaper front page for Thursday 26 November 2026.

Deterministic: no timestamps, no randomness, fixed layout and fonts.
Run:  python3 gen_image.py   -> writes entry.png next to this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 32
CONTENT_W = W - 2 * MARGIN

PAPER = (250, 247, 238)
INK = (16, 16, 16)
NAVY = (18, 44, 84)
NAVY_DEEP = (10, 28, 58)
GOLD = (176, 132, 32)
RULE = (16, 16, 16)
MUTED = (96, 92, 82)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (208, 203, 190)
NUM_BG = (232, 226, 210)
TICKER_BG = (16, 16, 16)
TICKER_FG = (238, 236, 228)
STAR = (240, 236, 220)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit_lines(draw, text, font, max_w, max_lines=None):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def draw_block(draw, lines, font, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_rocket_panel(draw, box):
    """Stylised night-sky panel: stars, orbit rings, a rising rocket."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY_DEEP)
    # stars
    stars = [(18, 26), (52, 12), (88, 40), (120, 16), (150, 48),
             (34, 74), (70, 92), (108, 66), (140, 96), (164, 30),
             (96, 118), (30, 130), (150, 128), (60, 150), (128, 152)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=STAR)
    # orbit rings
    cx, cy = x0 + (x1 - x0) // 2, y0 + 150
    draw.ellipse([cx - 78, cy - 26, cx + 78, cy + 26], outline=GOLD, width=2)
    draw.ellipse([cx - 58, cy - 18, cx + 58, cy + 18], outline=(120, 140, 170),
                 width=1)
    # planet
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(196, 120, 60))
    # rocket: body, nose, fins, flame
    rx, ry = cx, y0 + 52
    draw.polygon([(rx - 10, ry + 34), (rx - 10, ry + 4), (rx, ry - 14),
                  (rx + 10, ry + 4), (rx + 10, ry + 34)], fill=(235, 235, 230))
    draw.polygon([(rx - 10, ry + 34), (rx - 20, ry + 48), (rx - 10, ry + 40)],
                 fill=(176, 132, 32))
    draw.polygon([(rx + 10, ry + 34), (rx + 20, ry + 48), (rx + 10, ry + 40)],
                 fill=(176, 132, 32))
    draw.ellipse([rx - 4, ry + 8, rx + 4, ry + 16], fill=NAVY)
    draw.polygon([(rx - 6, ry + 36), (rx + 6, ry + 36), (rx, ry + 58)],
                 fill=(232, 150, 40))
    draw.text((x0 + 12, y1 - 26), "SHENZHOU-24  •  TIANGONG",
              font=load(SANS_B, 11), fill=STAR)


def story_row(draw, x, y, w, kicker, headline, deck):
    """One compact story: kicker, bold headline (2 lines), deck (2 lines)."""
    draw.line([(x, y), (x + w, y)], fill=PANEL_EDGE, width=1)
    cy = y + 6
    draw.text((x, cy), kicker.upper(), font=load(SANS_B, 11), fill=NAVY)
    cy += 16
    h_font = load(SERIF_B, 15)
    h_lines = fit_lines(draw, headline, h_font, w, max_lines=2)
    cy = draw_block(draw, h_lines, h_font, x, cy, INK, 18)
    cy += 2
    d_font = load(SANS, 13)
    d_lines = fit_lines(draw, deck, d_font, w, max_lines=2)
    cy = draw_block(draw, d_lines, d_font, x, cy, MUTED, 15)
    return cy + 2


def build(dest=None):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    title_font = load(SERIF_B, 48)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 22), title, font=title_font, fill=INK)

    date_font = load(SANS, 15)
    dateline = "THURSDAY 26 NOVEMBER 2026  •  ONE DAY, ONE PAGE"
    dw = draw.textlength(dateline, font=date_font)
    draw.text(((W - dw) / 2, 88), dateline, font=date_font, fill=MUTED)

    draw.line([(MARGIN, 120), (W - MARGIN, 120)], fill=RULE, width=3)
    draw.line([(MARGIN, 126), (W - MARGIN, 126)], fill=RULE, width=1)

    # ---- Hero: lead story + rocket panel ----
    hero_y0, hero_y1 = 142, 344
    hero_w = CONTENT_W
    panel_w = 210
    text_w = hero_w - panel_w - 18
    draw.rectangle([MARGIN, hero_y0, W - MARGIN, hero_y1],
                   fill=PANEL_BG, outline=PANEL_EDGE, width=1)
    draw.rectangle([MARGIN, hero_y0, W - MARGIN, hero_y0 + 5], fill=NAVY)
    draw_rocket_panel(draw, (W - MARGIN - panel_w, hero_y0 + 5,
                             W - MARGIN, hero_y1))
    lx = MARGIN + 16
    ly = hero_y0 + 20
    draw.text((lx, ly), "LEAD STORY  —  TRADE  •  AP",
              font=load(SANS_B, 13), fill=NAVY)
    ly += 28
    head_font = load(SERIF_B, 30)
    head = ("US readies new tariffs on China, "
            "the EU and 14 more economies")
    h_lines = fit_lines(draw, head, head_font, text_w - 16, max_lines=3)
    ly = draw_block(draw, h_lines, head_font, lx, ly, INK, 36)
    ly += 8
    deck_font = load(SANS, 15)
    deck = ("The Trump administration is preparing higher tariffs after a "
            "probe into subsidised production, AP sources say — rates "
            "reported as high as 20% on China and 15% on the EU, Japan "
            "and South Korea.")
    d_lines = fit_lines(draw, deck, deck_font, text_w - 16, max_lines=3)
    draw_block(draw, d_lines, deck_font, lx, ly, MUTED, 20)

    # ---- Two-column story list ----
    col_gap = 28
    col_w = (CONTENT_W - col_gap) // 2
    left = [
        ("Space", "First Pakistani astronaut reaches China's Tiangong station",
         "Shenzhou-24 carries Muhammad Zeeshan Ali, the first foreigner "
         "aboard the Chinese space station."),
        ("War", "Ukraine war spills into Libya as officers die in drone hit",
         "Two Libyan naval officers die of wounds after a Ukrainian drone "
         "strikes a Russian warship in Benghazi."),
        ("War", "Russia has lost nearly 500,000 people in Ukraine war",
         "Moscow's own figures put the toll near half a million; other "
         "counts put Russian soldiers killed above 700,000."),
        ("Americas", "Police free 20 hostages after 17-hour supermarket siege",
         "Colombian forces storm a Cartagena supermarket and free everyone "
         "held since the day before."),
    ]
    right = [
        ("USA", "Six dead, two of them children, in plane crash off Mississippi",
         "A small plane goes down off the Mississippi coast; investigators "
         "are working to establish the cause."),
        ("China", "Xi graft probe ensnares Shanghai party chief Chen Jining",
         "The anti-corruption campaign reaches a rising star once seen as "
         "a future leader."),
        ("Pacific", "Solomon Islands signs security treaty with Australia",
         "The pact bars foreign military bases — a setback for Beijing's "
         "influence in the Pacific."),
        ("Middle East", "Two tankers hit mines in Hormuz as US blockade bites",
         "Iran says shipping will not resume until Washington lifts its "
         "naval blockade; a Houthi drone injures 11 in Riyadh."),
    ]
    top = 362
    y = top
    for kicker, headline, deck in left:
        y = story_row(draw, MARGIN, y, col_w, kicker, headline, deck)
    y = top
    for kicker, headline, deck in right:
        y = story_row(draw, MARGIN + col_w + col_gap, y, col_w,
                      kicker, headline, deck)

    # ---- By the numbers ----
    num_y0, num_y1 = 742, 830
    draw.rectangle([MARGIN, num_y0, W - MARGIN, num_y1], fill=NUM_BG,
                   outline=PANEL_EDGE, width=1)
    draw.text((MARGIN + 14, num_y0 + 8), "BY THE NUMBERS",
              font=load(SANS_B, 12), fill=NAVY)
    nums = [("500,000", "Russians lost in the Ukraine war, per Moscow's figures"),
            ("20", "hostages freed in Colombia"),
            ("17", "hours of the supermarket siege"),
            ("6", "dead in the Mississippi plane crash")]
    seg_w = CONTENT_W // 4
    for i, (num, label) in enumerate(nums):
        sx = MARGIN + i * seg_w + 14
        draw.text((sx, num_y0 + 30), num, font=load(SERIF_B, 24), fill=INK)
        lab_lines = fit_lines(draw, label, load(SANS, 11), seg_w - 28,
                              max_lines=2)
        draw_block(draw, lab_lines, load(SANS, 11), sx, num_y0 + 58,
                   MUTED, 14)

    # ---- Also today ticker ----
    tick = (MARGIN, 848, W - MARGIN, 992)
    draw.rectangle(tick, fill=TICKER_BG)
    tx = MARGIN + 14
    ty = 860
    draw.text((tx, ty), "ALSO TODAY", font=load(SANS_B, 13), fill=(232, 184, 84))
    ty += 24
    ticker_font = load(SANS, 13)
    items = [
        "EU leaders gather for a special summit in Brussels",
        "North Korea expels Swiss diplomats over Ukraine-linked sanctions",
        "Huawei found guilty of stealing trade secrets and violating sanctions",
        "Mumbai marks 18 years since the 26/11 attacks",
        "India pledges \u20b915,000 crore in aid for Nepal",
        "Melania Trump reunites a seventh group of Ukrainian and Russian children",
        "Senegal reinstated as AFCON champions",
        "1,220 players register for the IPL 2027 auction",
    ]
    ticker = "  •  ".join(items)
    t_lines = fit_lines(draw, ticker, ticker_font, CONTENT_W - 28, max_lines=4)
    draw_block(draw, t_lines, ticker_font, tx, ty, TICKER_FG, 17)

    target = dest or OUT
    img.save(target, format="PNG", optimize=True)
    print("wrote", target, img.size)


if __name__ == "__main__":
    build()
