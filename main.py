#!/usr/bin/env python3
"""The Daily Meridian - front page for Tuesday 24 November 2026.

Renders a dense, newspaper-grade front page as a full-bleed portrait
image (entry.png) summing up the day's world news. Standard library plus
Pillow only; no network, no external assets, fully deterministic.
"""

import random

from PIL import Image, ImageDraw, ImageFont

random.seed(20261124)

W, H = 1240, 1754
MARGIN = 56
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (163, 22, 33)
GREY = (96, 92, 84)
LIGHT_RULE = (180, 174, 160)
ORANGE = (214, 96, 32)
SMOKE = (120, 118, 112)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS_I = "DejaVuSerif.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; return the y coordinate below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.26)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, width, weight=2, fill=INK):
    draw.rectangle([x, y, x + width, y + weight - 1], fill=fill)
    return y + weight


def centre(draw, y, text, fnt, fill=INK, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)
    return y + int(fnt.size * 1.25)


def draw_masthead(draw):
    """Masthead, date line and price furniture across the top."""
    y = 34
    y = rule(draw, MARGIN, y, W - 2 * MARGIN, weight=4)
    y += 6
    mast_size = 96
    while (draw.textlength("THE DAILY MERIDIAN", font=font(SERIF_B, mast_size))
           > W - 2 * MARGIN and mast_size > 40):
        mast_size -= 2
    y = centre(draw, y, "THE DAILY MERIDIAN", font(SERIF_B, mast_size))
    y -= 8
    y = centre(draw, y, "All the world's news, on a single page",
               font(SANS_I, 24), fill=GREY)
    y += 2
    y = rule(draw, MARGIN, y, W - 2 * MARGIN, weight=2)
    y += 8
    left = "Tuesday 24 November 2026"
    right = "Price $2.50  |  No. 328  |  Vol. XII"
    draw.text((MARGIN, y), left, font=font(SANS_B, 22), fill=INK)
    tw = draw.textlength(right, font=font(SANS_B, 22))
    draw.text((W - MARGIN - tw, y), right, font=font(SANS_B, 22), fill=INK)
    y += 30
    y = rule(draw, MARGIN, y, W - 2 * MARGIN, weight=5)
    return y + 14


def draw_lead_graphic(draw, x, y, w, h):
    """Stylised factory skyline at dusk: dark sheds, smoke and flame."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 34, 30))
    # dusk sky band
    draw.rectangle([x, y, x + w, y + 46], fill=(74, 52, 44))
    # ground
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(22, 20, 18))
    # factory sheds
    sheds = [(0, 150, 190, 96), (205, 118, 240, 128), (460, 140, 210, 106),
             (685, 108, 190, 138), (890, 132, 150, 114)]
    for sx, sw, _, sh in sheds:
        draw.rectangle([x + sx, y + h - 26 - sh, x + sx + sw, y + h - 26],
                       fill=(58, 54, 50))
        draw.rectangle([x + sx, y + h - 26 - sh, x + sx + sw,
                        y + h - 26 - sh + 8], fill=(44, 40, 36))
    # chimneys with smoke, kept inside the panel
    for cx0 in (x + 240, x + 640, x + 920):
        draw.rectangle([cx0, y + 58, cx0 + 26, y + h - 26], fill=(48, 44, 40))
        for i, r in enumerate((16, 22, 28, 34)):
            cy = y + 66 - i * 12
            draw.ellipse([cx0 - r, cy - int(r * 0.6), cx0 + 26 + r,
                          cy + int(r * 0.6)], fill=SMOKE)
    # flames over the middle shed, rooted at the ground line
    for fx, fh in ((300, 52), (360, 72), (430, 58), (500, 66), (560, 48)):
        draw.polygon([(x + fx, y + h - 26), (x + fx + 34, y + h - 26 - fh),
                      (x + fx + 68, y + h - 26)], fill=ORANGE)
        draw.polygon([(x + fx + 14, y + h - 26),
                      (x + fx + 34, y + h - 26 - fh + 26),
                      (x + fx + 54, y + h - 26)], fill=(232, 168, 48))
    # caption bar
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 0, 0))
    cap = "Firefighters battled the blaze at the Cikande candy factory for 14 hours."
    draw.text((x + 14, y + h - 23), cap, font=font(SANS, 19), fill=(235, 230, 220))
    return y + h


def draw_lead(draw, y):
    """Lead story: the Banten factory fire, full width."""
    x = MARGIN
    w = W - 2 * MARGIN
    head_size = 78
    while (draw.textlength("24 DEAD AS FACTORY FIRE",
                           font=font(SERIF_B, head_size)) > w
           and head_size > 40):
        head_size -= 2
    y = centre(draw, y, "24 DEAD AS FACTORY FIRE", font(SERIF_B, head_size),
               cx=W // 2)
    y = centre(draw, y - 6, "RAGES IN BANTEN", font(SERIF_B, head_size),
               cx=W // 2)
    y += 4
    y = centre(draw, y, "Rescuers search unstable ruins for about 30 workers still missing",
               font(SANS_B, 25), fill=RED)
    y += 10
    y = draw_lead_graphic(draw, x, y, w, 172)
    y += 12
    standfirst = ("CIKANDE, INDONESIA \u2014 Fire swept through the PT Fonusa Agung "
                  "Mulia candy factory on Saturday evening, killing at least 24 "
                  "people. About 300 workers were on shift and 29 were rescued; "
                  "families wait for DNA tests to identify the dead. Officials "
                  "say an air-conditioner short circuit may have started it.")
    y = draw_wrapped(draw, x, y, standfirst, font(SERIF, 23), w)
    return y + 6


def draw_story(draw, x, y, w, headline, dateline, body, head_size=30,
               body_size=21, red_kicker=None):
    """One story: optional red kicker, headline, dateline + body."""
    if red_kicker:
        draw.text((x, y), red_kicker, font=font(SANS_B, 19), fill=RED)
        y += 26
    y = draw_wrapped(draw, x, y, headline, font(SERIF_B, head_size), w,
                     leading=int(head_size * 1.12))
    y += 4
    full = dateline + " \u2014 " + body
    y = draw_wrapped(draw, x, y, full, font(SERIF, body_size), w)
    return y


STORIES_LEFT = [
    ("CLIMATE", "COP31 ENDS WITHOUT A DEAL",
     "ANTALYA, T\u00dcRKIYE",
     "Two weeks of talks in Antalya have collapsed with no agreement, "
     "after the European Union rejected a final text that said nothing "
     "about fossil fuels. It is the first climate summit to fail outright "
     "since Copenhagen in 2009."),
    ("JUSTICE", "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
     "THE HAGUE",
     "The International Court of Justice has ruled, by nine votes to six, "
     "that Myanmar's 2017 campaign against the Rohingya was genocide \u2014 "
     "the first time any state has been found responsible for the crime. "
     "About 10,000 Rohingya were killed."),
    ("SPORT", "ALCARAZ WINS FIRST ATP FINALS TITLE",
     "TURIN",
     "Carlos Alcaraz beat Alexander Zverev in Turin to lift the "
     "season-ending ATP Finals crown for the first time, closing the year "
     "as the game's dominant force."),
]

STORIES_RIGHT = [
    ("WAR AT SEA", "KYIV SAYS IT SANK RUSSIAN WARSHIP OFF LIBYA",
     "KYIV",
     "Ukraine claims a strike set the Russian corvette Merkury ablaze at "
     "the port of Benghazi, far from the Black Sea. Russia, meanwhile, "
     "struck homes in the Kyiv region, killing several people."),
    ("CHESS", "GUKESH OPENS TITLE DEFENCE IN GENEVA",
     "GENEVA",
     "World champion D Gukesh begins his title defence against "
     "Uzbekistan's Javokhir Sindarov today, in a match that opens the "
     "2026 World Chess Championship."),
    ("TECH", "WAYMO PULLS CARS OFF US FREEWAYS",
     "SAN FRANCISCO",
     "The driverless taxi firm has suspended freeway trips across the "
     "United States after California banned its cars from state freeways "
     "following traffic incidents."),
    ("ASIA", "INDIA AND NEPAL SIGN EIGHT DEALS",
     "NEW DELHI",
     "Narendra Modi and Nepal's PM Balendra Shah signed eight agreements "
     "and a Rs 15,000 crore package covering energy, trade and "
     "connectivity."),
]


def draw_columns(draw, y):
    """Two columns of further stories under the lead."""
    x = MARGIN
    w = W - 2 * MARGIN
    col_w = (w - 34) // 2
    right_x = x + col_w + 34
    left_y = y
    for kicker, head, date, body in STORIES_LEFT:
        left_y = draw_story(draw, x, left_y, col_w, head, date, body,
                            red_kicker=kicker)
        left_y += 8
        left_y = rule(draw, x, left_y, col_w, weight=1, fill=LIGHT_RULE)
        left_y += 10
    right_y = y
    for kicker, head, date, body in STORIES_RIGHT:
        right_y = draw_story(draw, right_x, right_y, col_w, head, date, body,
                             red_kicker=kicker)
        right_y += 8
        right_y = rule(draw, right_x, right_y, col_w, weight=1,
                       fill=LIGHT_RULE)
        right_y += 10
    # vertical divider between the columns
    draw.rectangle([x + col_w + 16, y, x + col_w + 17,
                    max(left_y, right_y) - 12], fill=LIGHT_RULE)
    return max(left_y, right_y)


def draw_footer(draw, y):
    """Index, weather strip and footer furniture."""
    x = MARGIN
    w = W - 2 * MARGIN
    y = rule(draw, x, y, w, weight=3)
    y += 6
    idx = ("INSIDE:  Factory fire  \u00b7  Climate talks collapse  \u00b7  Genocide "
           "ruling  \u00b7  War at sea  \u00b7  Alcaraz  \u00b7  Chess  \u00b7  Waymo")
    y = draw_wrapped(draw, x, y, idx, font(SANS_B, 20), w)
    y += 2
    weather = ("WEATHER:  London 9\u00b0C, rain  \u00b7  New York 12\u00b0C, clear  "
               "\u00b7  Jakarta 31\u00b0C, storms  \u00b7  Sydney 24\u00b0C, sun")
    y = draw_wrapped(draw, x, y, weather, font(SANS, 20), w, fill=GREY)
    y += 2
    y = rule(draw, x, y, w, weight=1, fill=LIGHT_RULE)
    y += 6
    foot = ("The Daily Meridian  \u00b7  Tuesday 24 November 2026  \u00b7  All stories "
            "checked against reporting published 19\u201324 November 2026")
    y = centre(draw, y, foot, font(SANS, 18), fill=GREY)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y += 8
    y = rule(draw, MARGIN, y, W - 2 * MARGIN, weight=2)
    y += 12
    y = draw_columns(draw, y)
    y += 4
    draw_footer(draw, y)
    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
