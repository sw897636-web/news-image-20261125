#!/usr/bin/env python3
"""Render the 25 November 2026 world-news infographic (1024x1024) with Pillow.

Layout: masthead, one large lead story (Riyadh), then a 2 + 3 grid of the
other five stories, and a sources footer. Newspaper style: cream paper,
dark navy ink, dark-red accent. All facts come from the build brief only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---
PAPER = (247, 243, 232)
INK = (26, 42, 68)
INK_SOFT = (58, 68, 88)
RED = (165, 42, 42)
RULE = (26, 42, 68)
CARD = (255, 253, 247)
CARD_EDGE = (205, 198, 182)
SKY = (214, 226, 238)
TOWER = (26, 42, 68)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LOCAL_DIR = os.path.expanduser(
    "~/workspace/makefun/news-image-20261122-review/dejavu-fonts-ttf-2.37/ttf")


def font(name, size):
    for d in (FONT_DIR, LOCAL_DIR):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


F_TITLE = font("DejaVuSans-Bold.ttf", 88)
F_DATE = font("DejaVuSans-Bold.ttf", 29)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 36)
F_BODY = font("DejaVuSans.ttf", 22)
F_CELL_KICK = font("DejaVuSans-Bold.ttf", 16)
F_CELL_TITLE = font("DejaVuSans-Bold.ttf", 24)
F_CELL_BODY = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 17)
F_CALLOUT = font("DejaVuSans-Bold.ttf", 40)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.32)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ================= masthead =================
d.text((W // 2, 10), "WORLD NEWS", font=F_TITLE, fill=INK, anchor="ma")
d.line([(40, 116), (984, 116)], fill=RULE, width=4)
d.text((W // 2, 126), "Wednesday, 25 November 2026",
       font=F_DATE, fill=RED, anchor="ma")
d.line([(40, 170), (984, 170)], fill=RULE, width=2)

# ================= lead story: Riyadh =================
LX, LY, LW, LH = 40, 184, 944, 236
d.rectangle([LX, LY, LX + LW, LY + LH], fill=CARD, outline=CARD_EDGE, width=2)
d.rectangle([LX, LY, LX + LW, LY + 6], fill=RED)
d.text((LX + 24, LY + 20), "MIDDLE EAST  ·  RIYADH", font=F_KICK, fill=RED)

# tower illustration on the right, fully inside the card
TX0 = 800
TOP = LY + 26
BOT = LY + LH - 44
d.rectangle([TX0, TOP + 30, TX0 + 160, BOT], fill=SKY, outline=INK, width=2)
# main tower with a small peaked roof kept inside the sky box
d.rectangle([TX0 + 52, TOP + 14, TX0 + 108, BOT], fill=TOWER)
d.polygon([(TX0 + 52, TOP + 14), (TX0 + 80, TOP - 2), (TX0 + 108, TOP + 14)],
          fill=TOWER)
# lit windows
for row in range(6):
    for col in range(2):
        wx = TX0 + 62 + col * 22
        wy = TOP + 34 + row * 24
        d.rectangle([wx, wy, wx + 12, wy + 12], fill=(255, 214, 120))
# small side buildings
d.rectangle([TX0 + 4, TOP + 86, TX0 + 44, BOT], fill=INK_SOFT)
d.rectangle([TX0 + 116, TOP + 106, TX0 + 156, BOT], fill=INK_SOFT)
# smoke puffs, inside the sky box
d.ellipse([TX0 + 118, TOP + 8, TX0 + 146, TOP + 26], fill=(140, 140, 140))
d.ellipse([TX0 + 128, TOP + 2, TX0 + 152, TOP + 18], fill=(165, 165, 165))
# red "11 INJURED" badge below the tower illustration
d.rectangle([TX0, LY + LH - 38, TX0 + 160, LY + LH - 10], fill=RED)
d.text(((TX0 + TX0 + 160) // 2, LY + LH - 24), "11 INJURED",
       font=font("DejaVuSans-Bold.ttf", 20), fill=(255, 255, 255),
       anchor="mm")

y = LY + 52
for ln in wrap(d, "DRONE STRIKE HITS RIYADH'S TALLEST TOWER — AGAIN",
               F_HEAD, 700):
    d.text((LX + 24, y), ln, font=F_HEAD, fill=INK)
    y += 44
body = ("A Houthi drone attack hits the 80-storey, 385 m PIF Tower for "
        "the second time in a week. Eleven people hurt, two critically; "
        "the Saudi-led coalition calls it a terrorist attack.")
draw_wrapped(d, body, F_BODY, LX + 24, y + 4, 700, INK_SOFT, leading=29)

# ================= grid: 5 stories =================
stories = [
    ("CHINA  ·  POLITICS", "SHANGHAI VOWS LOYALTY AFTER TOP OFFICIAL PROBED",
     "Politburo member Chen Jining, Shanghai's party chief, is under "
     "investigation for \"severe violations of discipline and law\". "
     "City leaders pledged loyalty to Beijing.", RED),
    ("USA  ·  TECH", "US JURY CONVICTS HUAWEI ON 10 OF 12 COUNTS",
     "A Brooklyn jury convicted Huawei of bank and wire fraud, sanctions "
     "violations and conspiring to steal trade secrets, but acquitted it "
     "of racketeering. Sentencing: 14 Sep 2027.", INK),
    ("LATIN AMERICA  ·  COLOMBIA", "HOSTAGE SIEGE IN CARTAGENA",
     "Armed men fled into an Éxito supermarket after a failed "
     "armoured-truck heist, taking about 25 hostages; five elderly women "
     "were among the first freed.", INK),
    ("GLOBAL  ·  SOCIETY", "FAMILY, PARTNERS KILL 5 WOMEN EVERY HOUR",
     "UN data: about 47,000 women and girls were killed by a partner or "
     "relative in 2025, 60% of all femicides.", INK),
    ("USA  ·  LIGHTER SIDE", "TRUMP PARDONS THANKSGIVING TURKEY",
     "Trump spared turkeys Freedom and Feathers at the annual White "
     "House pardon, ahead of Thanksgiving on 26 November.", INK),
]

GX, GY = 40, 436
GAP = 14
row1_h, row2_h = 250, 268
cell_w1 = (944 - GAP) // 2
cell_w2 = (944 - 2 * GAP) // 3


def cell(x, y, w, h, kicker, title, body, accent, title_lines=None,
         body_leading=23, callout=None, callout_size=40):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_EDGE, width=2)
    d.rectangle([x, y, x + w, y + 6], fill=accent)
    d.text((x + 18, y + 24), kicker, font=F_CELL_KICK, fill=accent)
    if callout:
        f_call = font("DejaVuSans-Bold.ttf", callout_size)
        cw = d.textlength(callout, font=f_call)
        d.text((x + w - 18 - cw, y + 12), callout, font=f_call,
               fill=RED)
    ty = y + 60
    lines = title_lines if title_lines else wrap(d, title, F_CELL_TITLE,
                                                  w - 36)
    for ln in lines:
        d.text((x + 18, ty), ln, font=F_CELL_TITLE, fill=INK)
        ty += 28
    draw_wrapped(d, body, F_CELL_BODY, x + 18, ty + 4, w - 36,
                 INK_SOFT, leading=body_leading)


cell(GX, GY, cell_w1, row1_h, *stories[0])
cell(GX + cell_w1 + GAP, GY, cell_w1, row1_h, *stories[1],
     title_lines=["US JURY CONVICTS HUAWEI", "ON 10 OF 12 COUNTS"],
     callout="10/12")
cell(GX, GY + row1_h + GAP, cell_w2, row2_h, *stories[2],
     body_leading=22)
cell(GX + cell_w2 + GAP, GY + row1_h + GAP, cell_w2, row2_h, *stories[3],
     title_lines=["FAMILY, PARTNERS", "KILL 5 WOMEN", "EVERY HOUR"],
     callout="5/hr", callout_size=36)
cell(GX + 2 * (cell_w2 + GAP), GY + row1_h + GAP, cell_w2, row2_h,
     *stories[4])

# ================= footer =================
fy = GY + row1_h + GAP + row2_h + 12
d.line([(40, fy), (984, fy)], fill=RULE, width=2)
d.text((W // 2, fy + 9),
       "Sources: Reuters · AP · AFP · CNN · UN Women/UNODC · Xinhua",
       font=F_FOOT, fill=INK_SOFT, anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
