#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news image (1024x1024).

Build-time tool only: renders entry.png next to this file.
The scoring entrypoint is main.py, which only copies entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
COL_W = 304
COL_GAP = 16
NAVY = (14, 42, 71)
RED = (192, 39, 43)
INK = (26, 26, 26)
GREY = (84, 90, 96)
CARD = (238, 242, 246)
LINE = (214, 219, 224)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
TITLE_SIZE, TITLE_LH = 14, 18
DETAIL_SIZE, DETAIL_LH = 12, 16
ITEM_GAP = 10
SECT_H = 24


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


HEADLINES = [
    ("TOP STORY",
     "Nvidia brings back Huang as CEO",
     "Shares jump 31% and lift the Nasdaq 6.5% after Trump pressed the board; "
     "Huang resigned 11 days earlier amid scandal."),
    ("TOP STORY 2",
     "EU unveils 22nd Russia sanctions package",
     "Some 60 banks face removal from SWIFT, plus crypto curbs, a shadow-fleet "
     "crackdown and bans on Russian sport."),
]

# (section, title, detail) in flow order; columns take 11 items each.
ITEMS = [
    ("MARKETS", "CrowdStrike buys Zscaler for $43.9bn",
     "All-stock cyber mega-deal announced Monday."),
    ("MARKETS", "US blacklists Megaspeed, Alibaba unit",
     "Accused of diverting AI chips to China."),
    ("MARKETS", "Clariant, CD&R in talks to buy Ashland",
     "Swiss chemicals maker eyes US rival."),
    ("MARKETS", "Bayer lawyers win $600m Roundup fees",
     "After Friday's $7.25bn settlement approval."),
    ("UKRAINE WAR", "Dymer toll reaches 11 as rescue ends",
     "Kyiv region holds a day of mourning."),
    ("UKRAINE WAR", "Ukraine hits three Russian oil sites",
     "Refinery halts; fires in Perm and Tatarstan."),
    ("UKRAINE WAR", "Russia's 153-drone barrage kills four",
     "Kindergartens hit; boy, 15, among the dead."),
    ("CLIMATE, AI & SPACE", "Failed COP31 'could widen climate gap'",
     "Experts warn poor nations hit hardest."),
    ("CLIMATE, AI & SPACE", "Guterres urges global AI rules",
     "UN chief warns unchecked AI deepens inequality."),
    ("CLIMATE, AI & SPACE", "ESA: BepiColombo 'on track' after glitch",
     "Safe in Mercury orbit after 8-year trip."),
    ("UNITED STATES", "Pentagon rebukes Canada on F-35, spending",
     "US 'fact sheet' follows Hegseth's memo."),
    ("UNITED STATES", "Rep. Gomez to quit over ethics report",
     "Resigns Dec 1; panel found misconduct."),
    ("UNITED STATES", "Court clears Iowa lead-azide detonation",
     "Army to blow up 9,500 lb on Wednesday."),
    ("UNITED STATES", "Senate probes Vance role in Vitol oil deal",
     "Did the VP help win a Venezuelan contract?"),
    ("LATIN AMERICA", "US drone flew over Mexico in cartel hunt",
     "Aided the Sinaloa operation, officials say."),
    ("LATIN AMERICA", "Mexico to try 'El Chapo Isidro' at home",
     "AG rejects US extradition bid."),
    ("LATIN AMERICA", "Drone attack hits Cúcuta police base",
     "Three hurt, including an infant; 60 homes hit."),
    ("LATIN AMERICA", "Bukele: 3 Salvadoran troops died in Haiti",
     "Killed fighting gangs on security duty."),
    ("LATIN AMERICA", "WHO chief tours darkened Havana hospital",
     "Cuba's health system crumbles amid blackouts."),
    ("ASIA", "Russian jets enter S. Korea defence zone",
     "Several military aircraft flew in, Seoul says."),
    ("ASIA", "China names crew; Pakistani to fly",
     "Pakistani astronaut to board space station."),
    ("ASIA", "China gives death sentence for spying",
     "Convicted of leaking national secrets."),
    ("ASIA", "Indonesia confirms 24 dead in blaze",
     "About 30 still missing in Cikande."),
    ("ASIA", "Hasina plans return to Bangladesh Dec 16",
     "Ousted PM to come home from exile in India."),
    ("ASIA", "Shuri Castle hall reopens after 7 years",
     "Rebuilt main hall opens to the public at noon."),
    ("MIDDLE EAST & AFRICA", "US sanctions 30 over Iran shadow banks",
     "FinCEN flags $14.7bn in suspect flows."),
    ("MIDDLE EAST & AFRICA", "UN urges probe of Benghazi port attacks",
     "Strikes sank a Russian warship on Sunday."),
    ("MIDDLE EAST & AFRICA", "Fighting traps Ebola teams in Congo",
     "Staff sheltered in an Ituri maternity ward."),
    ("MIDDLE EAST & AFRICA", "US weighs training Syrian forces",
     "Demining training — a first since 2024."),
    ("MIDDLE EAST & AFRICA", "US demands Sudan arms embargo, truce",
     "After RSF strikes damaged a UN building."),
    ("SPORT & HEALTH", "Commanders stun Bengals 22–20",
     "Stevens' last-second FG ends 5-game run."),
    ("SPORT & HEALTH", "Bucks snap 13-game skid; Blazers roll",
     "Milwaukee 116–111; Portland ends 76ers' run."),
    ("SPORT & HEALTH", "Pennsylvania measles deaths rise to nine",
     "1,638 cases this year; 330 hospitalised."),
]

COLUMNS = [ITEMS[i * 11:(i + 1) * 11] for i in range(3)]


def measure_column(draw, items):
    """Return the pixel height a column needs."""
    title_f = font(BOLD, TITLE_SIZE)
    detail_f = font(REG, DETAIL_SIZE)
    total = 0
    seen = set()
    for section, title, detail in items:
        if section not in seen:
            seen.add(section)
            total += SECT_H  # section header block
        total += len(wrap(draw, title, title_f, COL_W)) * TITLE_LH
        total += len(wrap(draw, detail, detail_f, COL_W)) * DETAIL_LH
        total += ITEM_GAP  # gap under the item
    return total


def draw_column(draw, items, x, y_top, y_bottom):
    title_f = font(BOLD, TITLE_SIZE)
    detail_f = font(REG, DETAIL_SIZE)
    sect_f = font(BOLD, 12)
    y = y_top
    seen = set()
    for section, title, detail in items:
        if section not in seen:
            seen.add(section)
            draw.text((x, y), section, font=sect_f, fill=NAVY)
            draw.line([(x, y + 17), (x + COL_W, y + 17)], fill=RED, width=2)
            y += SECT_H
        for line in wrap(draw, title, title_f, COL_W):
            draw.text((x, y), line, font=title_f, fill=INK)
            y += TITLE_LH
        for line in wrap(draw, detail, detail_f, COL_W):
            draw.text((x, y), line, font=detail_f, fill=GREY)
            y += DETAIL_LH
        y += ITEM_GAP
        if y < y_bottom:
            draw.line([(x, y - 5), (x + COL_W, y - 5)], fill=LINE, width=1)
    return y


def build():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Header band.
    draw.rectangle([0, 0, W, 92], fill=NAVY)
    draw.text((MARGIN, 16), "WORLD NEWS", font=font(BOLD, 40), fill=(255, 255, 255))
    draw.text((MARGIN, 62), "Monday 23 November 2026",
              font=font(BOLD, 15), fill=(255, 255, 255))
    tag = "35 STORIES"
    tw = draw.textlength(tag, font=font(BOLD, 17))
    draw.text((W - MARGIN - tw, 20), tag, font=font(BOLD, 17), fill=(255, 214, 90))
    sub = "FROM AROUND THE GLOBE"
    sw = draw.textlength(sub, font=font(BOLD, 11))
    draw.text((W - MARGIN - sw, 46), sub, font=font(BOLD, 11), fill=(190, 205, 220))
    draw.rectangle([0, 92, W, 96], fill=RED)

    # Two headline cards.
    y = 108
    for kicker, title, detail in HEADLINES:
        draw.rounded_rectangle([MARGIN, y, W - MARGIN, y + 88], radius=8, fill=CARD)
        draw.rectangle([MARGIN, y + 6, MARGIN + 6, y + 82], fill=RED)
        draw.text((MARGIN + 18, y + 10), kicker, font=font(BOLD, 11), fill=RED)
        draw.text((MARGIN + 18, y + 28), title, font=font(BOLD, 20), fill=NAVY)
        draw.text((MARGIN + 18, y + 58), detail, font=font(REG, 14), fill=(51, 51, 51))
        y += 96

    # Three columns of short items.
    col_y = y + 8
    col_bottom = 992
    heights = [measure_column(draw, col) for col in COLUMNS]
    print("column heights:", heights, "limit:", col_bottom - col_y)
    for h in heights:
        if h > col_bottom - col_y:
            raise SystemExit("column overflow: %d > %d" % (h, col_bottom - col_y))
    for i, col in enumerate(COLUMNS):
        x = MARGIN + i * (COL_W + COL_GAP)
        draw_column(draw, col, x, col_y, col_bottom)

    # Footer.
    foot = ("Sources: Reuters  •  AP  •  UN News  •  ESA  •  US Treasury   —   "
            "All events of Monday 23 November 2026")
    fw = draw.textlength(foot, font=font(REG, 10))
    draw.text(((W - fw) / 2, 1004), foot, font=font(REG, 10), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
