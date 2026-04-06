"""
Generate Meta Creative Generator - Full Documentation PDF
With flowchart, iteration history, issues, and final architecture
"""

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

OUT_DIR = os.path.dirname(__file__)


# ─────────────────────────────────────────────
# FLOWCHART IMAGE
# ─────────────────────────────────────────────
def draw_flowchart_page1():
    W, H = 2400, 4500
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Colors
    BG_BLUE = (220, 235, 255)
    BG_GREEN = (220, 248, 230)
    BG_ORANGE = (255, 238, 220)
    BG_PURPLE = (235, 225, 255)
    BG_PINK = (255, 225, 240)
    BG_YELLOW = (255, 248, 215)
    BG_GRAY = (238, 238, 242)
    BG_MALE = (215, 235, 255)
    BG_FEMALE = (255, 220, 240)
    BORDER = (90, 90, 120)
    ARROW = (70, 70, 110)
    TEXT_DARK = (25, 25, 45)
    TEXT_GRAY = (100, 100, 120)
    ACCENT = (99, 102, 241)
    GREEN = (34, 139, 60)
    RED = (200, 50, 50)
    MALE_C = (30, 100, 200)
    FEMALE_C = (200, 40, 100)

    def rr(xy, r=16, fill=None, outline=None, w=2):
        draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

    def arrow_down(x, y1, y2, color=ARROW):
        draw.line([x, y1, x, y2], fill=color, width=3)
        draw.polygon([(x-8, y2-10), (x+8, y2-10), (x, y2)], fill=color)

    def arrow_right(x1, x2, y, color=ARROW):
        draw.line([x1, y, x2, y], fill=color, width=3)
        draw.polygon([(x2-10, y-8), (x2-10, y+8), (x2, y)], fill=color)

    def arrow_left(x1, x2, y, color=ARROW):
        draw.line([x1, y, x2, y], fill=color, width=3)
        draw.polygon([(x2+10, y-8), (x2+10, y+8), (x2, y)], fill=color)

    def box(x, y, w, h, text, subtitle="", fill=BG_BLUE, border=BORDER):
        rr([x, y, x+w, y+h], r=14, fill=fill, outline=border, w=2)
        lines = text.split("\n")
        ty = y + h//2 - len(lines)*13
        for line in lines:
            tw = len(line) * 9
            draw.text((x + w//2 - tw//2, ty), line, fill=TEXT_DARK)
            ty += 26
        if subtitle:
            tw2 = len(subtitle) * 7
            draw.text((x + w//2 - tw2//2, y + h - 26), subtitle, fill=TEXT_GRAY)

    def small_box(x, y, w, h, text, fill=BG_GRAY, border=BORDER, text_color=TEXT_DARK):
        rr([x, y, x+w, y+h], r=10, fill=fill, outline=border, w=1)
        lines = text.split("\n")
        ty = y + 6
        for line in lines:
            draw.text((x + 10, ty), line, fill=text_color)
            ty += 18

    def diamond(cx, cy, w, h, text, fill=BG_YELLOW):
        points = [(cx, cy-h//2), (cx+w//2, cy), (cx, cy+h//2), (cx-w//2, cy)]
        draw.polygon(points, fill=fill, outline=BORDER, width=2)
        tw = len(text) * 9
        draw.text((cx - tw//2, cy - 12), text, fill=TEXT_DARK)

    def label(x, y, text, color=GREEN, bg=None):
        if bg:
            rr([x-4, y-2, x+len(text)*9+4, y+20], r=6, fill=bg)
        draw.text((x, y), text, fill=color)

    cx = W // 2

    # ── TITLE
    rr([50, 20, W-50, 90], r=20, fill=ACCENT, outline=ACCENT)
    draw.text((cx - 280, 35), "META CREATIVE GENERATOR", fill=(255,255,255))
    draw.text((cx - 200, 62), "Complete Workflow Flowchart", fill=(200,210,255))

    # ── ROW 1: User Input
    box(cx-220, 120, 440, 75, "USER ENTERS TOPIC", 'e.g. "hair fall due to stress in office"', fill=BG_BLUE)

    # Input examples on left
    small_box(60, 110, 380, 100,
        "Example Topics:\n* hair fall due to stress in office\n* PCOS treatment for women\n* dandruff won't go away\n* skin care routine",
        fill=(245,248,255), border=BORDER, text_color=TEXT_GRAY)

    arrow_down(cx, 195, 245)

    # ── ROW 2: Hair Detection Diamond
    diamond(cx, 310, 400, 120, "HAIR TOPIC?", fill=BG_YELLOW)

    # Hair keywords panel (left)
    small_box(60, 240, 420, 140,
        "DETECTION KEYWORDS (20):\nhair loss, hair fall, hairfall,\nhair thinning, bald, balding,\nreceding hairline, alopecia,\nscalp, hair density, dandruff,\nhair regrowth, hair growth,\nhair care, hair treatment...",
        fill=BG_YELLOW, border=(200,190,100), text_color=TEXT_DARK)
    # Arrow from keywords to diamond
    arrow_right(480, cx-200, 310, color=(200,190,100))

    # YES branch (down) - detailed
    label(cx-60, 375, "YES", GREEN, bg=(220,248,230))
    arrow_down(cx, 370, 420)

    # NO branch (right)
    arrow_right(cx+200, cx+420, 310, color=RED)
    label(cx+320, 288, "NO", RED, bg=(255,230,230))
    box(cx+430, 255, 380, 110,
        "STANDARD PROMPT\nGeneric Indian person\nage 25-45, casual kurta/t-shirt\nNo special hair rules",
        fill=BG_GRAY)

    # ── ROW 3: Gender Split Diamond
    diamond(cx, 490, 420, 120, "GENDER? (Random)", fill=BG_YELLOW)
    label(cx-190, 448, "50% chance", TEXT_GRAY)
    label(cx+110, 448, "50% chance", TEXT_GRAY)

    # Seed note
    small_box(cx+230, 440, 300, 90,
        "SEED GENERATED HERE\nrandom.randint(1, 999999)\nSame seed used for BOTH\nFeed + Story formats",
        fill=(255,255,235), border=(200,190,100), text_color=TEXT_DARK)
    arrow_right(cx+210, cx+230, 490, color=(200,190,100))

    # MALE branch (LEFT)
    arrow_left(cx-210, cx-400, 490, color=MALE_C)
    label(cx-380, 468, "MALE", MALE_C, bg=BG_MALE)

    # FEMALE branch (RIGHT)
    arrow_right(cx+210, cx+400, 490, color=FEMALE_C)
    label(cx+330, 468, "FEMALE", FEMALE_C, bg=BG_FEMALE)

    # ── MALE DETAIL PANEL (LEFT)
    mx = 40
    my = 570
    pw = 560
    rr([mx, my, mx+pw, my+720], r=16, fill=BG_MALE, outline=MALE_C, w=3)
    draw.text((mx+20, my+12), "MALE WORKFLOW (50% probability)", fill=MALE_C)
    draw.line([mx+20, my+38, mx+pw-20, my+38], fill=MALE_C, width=2)

    # Male - Person
    small_box(mx+15, my+50, pw-30, 70,
        "SUBJECT: South Asian Indian man\nAge 30-35, wheatish brown skin, dark brown eyes\nLight stubble, furrowed brow, under-eye fatigue\nVisible frustration - NOT smiling",
        fill=(235,245,255), border=MALE_C)

    # Male - Hair
    draw.text((mx+20, my+135), "HAIR (Norwood Stage 2-3 - NOT bald, max 25% hair loss):", fill=MALE_C)
    small_box(mx+15, my+158, 170, 80, "Short\n2-3cm, dark brown\nCrown thinning\nScalp visible on top", fill=(240,248,255), border=MALE_C)
    small_box(mx+195, my+158, 170, 80, "Medium\n5-7cm, disheveled\nDensity difference\nSides vs crown", fill=(240,248,255), border=MALE_C)
    small_box(mx+375, my+158, 170, 80, "Slightly Longer\n8-10cm\nM-shaped recession\nTemples thinner", fill=(240,248,255), border=MALE_C)

    # Male - Camera
    draw.text((mx+20, my+252), "CAMERA:", fill=MALE_C)
    small_box(mx+15, my+272, pw-30, 36,
        "Slightly elevated top-angle, handheld feel, slight grain, 85mm f/1.4, 8K",
        fill=(240,248,255), border=MALE_C)

    # Male - Lighting
    draw.text((mx+20, my+322), "LIGHTING (random):", fill=MALE_C)
    small_box(mx+15, my+342, 170, 55, "Morning Window\nWarm, soft, one side\nGentle shadow", fill=(240,248,255), border=MALE_C)
    small_box(mx+195, my+342, 170, 55, "Overcast Natural\nDiffused, cool tone\nAuthentic feel", fill=(240,248,255), border=MALE_C)
    small_box(mx+375, my+342, 170, 55, "Harsh Side Light\nDeep shadow\nAmplifies tiredness", fill=(240,248,255), border=MALE_C)

    # Male - Poses
    draw.text((mx+20, my+412), "POSES - 10 total (5 on-head / 5 off-head):", fill=MALE_C)
    on_poses = ["Touching Crown", "Running Fingers", "Checking Hairline", "Frustrated w/ Comb", "Head Down Stress"]
    off_poses = ["Holding Strands", "Mirror Check", "Pillow Shock", "Old Photo Compare", "Staring at Drain"]

    rr([mx+15, my+435, mx+275, my+580], r=8, fill=(230,248,230), outline=GREEN, w=1)
    draw.text((mx+25, my+440), "Hands ON Head (50%):", fill=GREEN)
    py = my+462
    for p in on_poses:
        draw.text((mx+35, py), f"* {p}", fill=TEXT_DARK); py += 24

    rr([mx+285, my+435, mx+pw-15, my+580], r=8, fill=(255,235,235), outline=RED, w=1)
    draw.text((mx+295, my+440), "Hands OFF Head (50%):", fill=RED)
    py = my+462
    for p in off_poses:
        draw.text((mx+305, py), f"* {p}", fill=TEXT_DARK); py += 24

    # Male - Rules
    draw.text((mx+20, my+595), "STRICT RULES:", fill=MALE_C)
    rules_m = [
        "NOT bald - max 25% hair loss visible",
        "Fingers: anatomically correct, 5 fingers, no distortion",
        "Face: symmetrical, sharp, no deformation",
        "Consistent hand position across Feed + Story",
        "Style: Raw emotional documentary, NOT studio",
    ]
    ry = my+615
    for r in rules_m:
        draw.text((mx+35, ry), f"* {r}", fill=TEXT_DARK); ry += 20

    # ── FEMALE DETAIL PANEL (RIGHT)
    fx = W - 600
    fy = 570
    fw = 560
    rr([fx, fy, fx+fw, fy+720], r=16, fill=BG_FEMALE, outline=FEMALE_C, w=3)
    draw.text((fx+20, fy+12), "FEMALE WORKFLOW (50% probability)", fill=FEMALE_C)
    draw.line([fx+20, fy+38, fx+fw-20, fy+38], fill=FEMALE_C, width=2)

    # Female - Person
    small_box(fx+15, fy+50, fw-30, 70,
        "SUBJECT: South Asian Indian woman\nAge 25-35, wheatish brown skin, dark brown eyes\nWorried and concerned expression\nSlight frown, tired eyes",
        fill=(255,235,245), border=FEMALE_C)

    # Female - Hair
    draw.text((fx+20, fy+135), "HAIR (Early Stage Thinning - NO bald patches):", fill=FEMALE_C)
    small_box(fx+15, fy+158, 130, 80, "Short Bob\nJaw-length\nWider parting\nThin temples", fill=(255,240,248), border=FEMALE_C)
    small_box(fx+155, fy+158, 130, 80, "Medium\nShoulder-length\nWider parting\nWispy strands", fill=(255,240,248), border=FEMALE_C)
    small_box(fx+295, fy+158, 125, 80, "Long\nBelow shoulder\nReduced density\nAt parting", fill=(255,240,248), border=FEMALE_C)
    small_box(fx+430, fy+158, 115, 80, "Tied Up\nBun/ponytail\nWider parting\nThin temple", fill=(255,240,248), border=FEMALE_C)

    # Female - Camera
    draw.text((fx+20, fy+252), "CAMERA:", fill=FEMALE_C)
    small_box(fx+15, fy+272, fw-30, 36,
        "Close-up front or slight top-angle, handheld feel, 85mm f/1.4, 8K",
        fill=(255,240,248), border=FEMALE_C)

    # Female - Lighting
    draw.text((fx+20, fy+322), "LIGHTING (random):", fill=FEMALE_C)
    small_box(fx+15, fy+342, 170, 55, "Soft Window\nSlightly warm\nGentle shadows", fill=(255,240,248), border=FEMALE_C)
    small_box(fx+195, fy+342, 170, 55, "Bathroom Mirror\nWarm front light\nIntimate, private", fill=(255,240,248), border=FEMALE_C)
    small_box(fx+375, fy+342, 170, 55, "Cool Overcast\nDesaturated\nMelancholic mood", fill=(255,240,248), border=FEMALE_C)

    # Female - Poses
    draw.text((fx+20, fy+412), "POSES - 8 total (4 on-head / 4 off-head):", fill=FEMALE_C)
    on_f = ["Touching Parting", "Checking Mirror", "Pulling Ponytail", "Tucking Behind Ear"]
    off_f = ["Holding Strands", "Brushing Hair", "Examining Ends", "Scrolling Solutions"]

    rr([fx+15, fy+435, fx+275, fy+555], r=8, fill=(230,248,230), outline=GREEN, w=1)
    draw.text((fx+25, fy+440), "Hands ON Head (50%):", fill=GREEN)
    py = fy+462
    for p in on_f:
        draw.text((fx+35, py), f"* {p}", fill=TEXT_DARK); py += 24

    rr([fx+285, fy+435, fx+fw-15, fy+555], r=8, fill=(255,235,235), outline=RED, w=1)
    draw.text((fx+295, fy+440), "Hands OFF Head (50%):", fill=RED)
    py = fy+462
    for p in off_f:
        draw.text((fx+305, py), f"* {p}", fill=TEXT_DARK); py += 24

    # Female - Rules
    draw.text((fx+20, fy+570), "STRICT RULES:", fill=FEMALE_C)
    rules_f = [
        "NO bald patches - wider parting only",
        "Fingers: anatomically correct, no distortion",
        "Face: symmetrical, sharp, no deformation",
        "Consistent pose across Feed + Story",
        "Style: Raw emotional documentary, NOT studio",
    ]
    ry = fy+590
    for r in rules_f:
        draw.text((fx+35, ry), f"* {r}", fill=TEXT_DARK); ry += 20

    # ── Clothing Rule (center, between panels)
    cbox_x = cx - 230
    cbox_y = 750
    rr([cbox_x, cbox_y, cbox_x+460, cbox_y+150], r=12, fill=BG_ORANGE, outline=(200,120,50), w=2)
    draw.text((cbox_x+20, cbox_y+10), "CLOTHING RULE (both genders)", fill=(180,80,20))
    draw.line([cbox_x+20, cbox_y+32, cbox_x+440, cbox_y+32], fill=(200,120,50), width=1)
    draw.text((cbox_x+20, cbox_y+40), "MUST WEAR:", fill=GREEN)
    draw.text((cbox_x+20, cbox_y+60), "Plain light grey or white round-neck t-shirt", fill=TEXT_DARK)
    draw.text((cbox_x+20, cbox_y+82), "Same shirt color across all formats", fill=TEXT_DARK)
    draw.text((cbox_x+20, cbox_y+106), "BANNED:", fill=RED)
    draw.text((cbox_x+100, cbox_y+106), "Towel, bathrobe, bare shoulders,", fill=RED)
    draw.text((cbox_x+100, cbox_y+126), "sleeveless, swimwear, blue/dark shirt", fill=RED)

    # ── Merge male/female back to center
    merge_y = 1350
    # Left line from male panel
    draw.line([mx+pw//2, my+720, mx+pw//2, merge_y], fill=MALE_C, width=2)
    draw.line([mx+pw//2, merge_y, cx, merge_y], fill=ARROW, width=3)
    # Right line from female panel
    draw.line([fx+fw//2, fy+720, fx+fw//2, merge_y], fill=FEMALE_C, width=2)
    draw.line([fx+fw//2, merge_y, cx, merge_y], fill=ARROW, width=3)
    arrow_down(cx, merge_y, merge_y+40)

    # ── Place Detection
    diamond(cx, merge_y+100, 400, 110, "PLACE KEYWORDS?", fill=BG_YELLOW)

    # YES branch - right with all categories
    arrow_right(cx+200, cx+380, merge_y+100, color=GREEN)
    label(cx+300, merge_y+78, "YES", GREEN, bg=(220,248,230))

    # Place categories panel
    pc_x = cx + 390
    pc_y = merge_y + 30
    rr([pc_x, pc_y, pc_x+520, pc_y+250], r=14, fill=BG_GREEN, outline=GREEN, w=2)
    draw.text((pc_x+20, pc_y+10), "BACKGROUND DETECTION (6 categories)", fill=GREEN)
    draw.line([pc_x+20, pc_y+34, pc_x+500, pc_y+34], fill=GREEN, width=1)

    places = [
        ("Traffic/Road", "pollution, traffic, commute", "Blurred city road + smog"),
        ("City/Urban", "city, metro, mumbai, delhi", "Blurred skyline + buildings"),
        ("Office", "office, work, corporate, job", "Blurred office interior"),
        ("Stress", "stress, pressure, anxiety", "Dimly lit, moody atmosphere"),
        ("Home", "home, kitchen, bedroom", "Warm home interior"),
        ("Bathroom", "bathroom, mirror, shower", "Warm whites, mirror feel"),
    ]
    py_p = pc_y + 42
    for place_name, keywords, bg_desc in places:
        rr([pc_x+10, py_p, pc_x+510, py_p+30], r=6, fill=(240,255,240), outline=(180,220,190), w=1)
        draw.text((pc_x+18, py_p+6), place_name, fill=GREEN)
        draw.text((pc_x+130, py_p+6), keywords, fill=TEXT_GRAY)
        draw.text((pc_x+340, py_p+6), bg_desc, fill=TEXT_DARK)
        py_p += 34

    # NO label
    label(cx-60, merge_y+160, "NO (default bg)", TEXT_GRAY)

    arrow_down(cx, merge_y+155, merge_y+210)

    # ── Emotion Detection panel (left side)
    em_x = 60
    em_y = merge_y + 30
    rr([em_x, em_y, em_x+440, em_y+250], r=14, fill=BG_ORANGE, outline=(200,140,60), w=2)
    draw.text((em_x+20, em_y+10), "EMOTION DETECTION (Groq logic)", fill=(180,80,20))
    draw.line([em_x+20, em_y+34, em_x+420, em_y+34], fill=(200,140,60), width=1)

    emotions = [
        ("PROBLEM topic", "hair loss, acne, PCOS", "Frustration, concern,\ninsecurity, furrowed brow", RED),
        ("SOLUTION topic", "treatment, therapy, cure", "Hope, relief,\nslight smile, trust", (30,130,80)),
        ("RESULT topic", "success, before-after", "Confidence, happiness,\ndirect eye contact", GREEN),
    ]
    ey = em_y + 45
    for emo_type, keywords, expression, emo_color in emotions:
        rr([em_x+10, ey, em_x+430, ey+60], r=8, fill=(255,248,235), outline=(220,200,160), w=1)
        draw.text((em_x+18, ey+6), emo_type, fill=emo_color)
        draw.text((em_x+18, ey+24), f"Keywords: {keywords}", fill=TEXT_GRAY)
        draw.text((em_x+250, ey+6), "Expression:", fill=TEXT_DARK)
        draw.text((em_x+250, ey+24), expression, fill=emo_color)
        ey += 66

    # ── Groq
    box(cx-260, merge_y+220, 520, 130,
        "GROQ (LLaMA 3.3 70B) - FREE API\nGenerates JSON:\nTitle (max 8 words) + Subtext (max 15)\n+ CTA (max 4) + Visual Style + Layout",
        fill=BG_PURPLE)

    # Groq details (left)
    small_box(60, merge_y+220, 360, 130,
        "GROQ OUTPUT RULES:\n* Language: Simple Indian English\n* One scene, one person\n* No products, no medicine\n* Emotion matches topic mood\n* Layout forced random from\n  Python (Groq repeats L01/L03)",
        fill=(245,240,255), border=ACCENT, text_color=TEXT_DARK)

    # Layout info (right)
    small_box(cx+280, merge_y+220, 350, 130,
        "30 LAYOUTS (L01-L30):\nTop-Left Headline, Centered,\nDiagonal Banner, Arc Headline,\nVertical Left, Frosted Glass,\nSpeech Bubble, Person Fills Top,\nSplit Panel, Ribbon Headline...\n+ 20 more variations",
        fill=(245,240,255), border=ACCENT, text_color=TEXT_DARK)

    arrow_down(cx, merge_y+350, merge_y+390)

    # ── User Edit
    box(cx-220, merge_y+400, 440, 80,
        "USER REVIEWS & EDITS\nTitle / Subtext / CTA / Font Style",
        fill=BG_BLUE)

    # Font styles panel (right)
    small_box(cx+240, merge_y+380, 390, 120,
        "13 FONT STYLES:\nRoboto, Impact, Playfair Display,\nMontserrat, Poppins, Arial Black,\nOswald, Bebas Neue, Lato,\nOpen Sans, Merriweather,\nFutura, Nunito Sans",
        fill=(240,248,255), border=BORDER, text_color=TEXT_DARK)

    arrow_down(cx, merge_y+480, merge_y+520)

    # ── Skeleton Preview
    box(cx-260, merge_y+530, 520, 120,
        "SKELETON PREVIEW\nLayout wireframe (Feed 1:1 + Story 9:16)\n+ Stick figure with pose-specific arms\n+ Character Details card below",
        fill=BG_ORANGE)

    # Skeleton details (left)
    small_box(60, merge_y+530, 380, 120,
        "PREVIEW SHOWS:\n* Layout positions (headline, CTA)\n* Person placeholder with pose\n* Gender, Hair, Lighting, Pose labels\n* Helps decide BEFORE API call\n* Saves $0.08 per bad generation!",
        fill=(255,248,230), border=(200,180,100), text_color=TEXT_DARK)

    arrow_down(cx, merge_y+650, merge_y+690)

    # ── Prompt Builder
    box(cx-280, merge_y+700, 560, 120,
        "PROMPT BUILDER\nCombines ALL into one Flux prompt:\nCopy + Visual Style + Font + Layout\n+ Hair Rules + Clothing + Pose + Lighting + BG",
        fill=BG_PURPLE)

    # Prompt details (right)
    small_box(cx+300, merge_y+700, 330, 120,
        "PROMPT INCLUDES:\n* Exact headline/CTA text\n* Photography style\n* Subject description\n* Pose instructions\n* 'No watermarks, no Meta text'\n* '8K premium, photorealistic'",
        fill=(245,240,255), border=ACCENT, text_color=TEXT_DARK)

    arrow_down(cx, merge_y+820, merge_y+860)

    # ── Flux Generation
    rr([cx-300, merge_y+870, cx+300, merge_y+960], r=16, fill=(200,215,255), outline=ACCENT, w=3)
    draw.text((cx-220, merge_y+882), "FLUX (nano-banana-2) via fal.ai", fill=ACCENT)
    draw.text((cx-220, merge_y+907), "$0.08/image  |  Same seed for both formats", fill=TEXT_DARK)
    draw.text((cx-220, merge_y+930), "Safety checker ON  |  JPEG output  |  8K quality", fill=TEXT_GRAY)

    # Two arrows
    arrow_down(cx-140, merge_y+960, merge_y+1010)
    arrow_down(cx+140, merge_y+960, merge_y+1010)

    # Feed box
    box(cx-360, merge_y+1020, 340, 130,
        "FEED 1080x1080\nSquare composition\nHalf-body or close-up\nHeadline + CTA visible\nBalanced square layout",
        fill=BG_GREEN, border=GREEN)

    # Story box
    box(cx+20, merge_y+1020, 340, 130,
        "STORY 1080x1920\nDedicated vertical prompt\nFull body / waist-up\nFull frame edge-to-edge\nNO empty space or borders",
        fill=BG_GREEN, border=GREEN)

    # Story detail
    small_box(cx+380, merge_y+1020, 260, 130,
        "STORY COMPOSITION:\nTop 25% = Headline area\nMiddle 50% = Person\nBottom 25% = CTA area\n\nPerson large & dominant\nZoomed naturally\nFace clearly visible",
        fill=(240,255,240), border=GREEN, text_color=TEXT_DARK)

    # Merge
    merge_y2 = merge_y + 1190
    arrow_down(cx-170, merge_y+1150, merge_y2)
    arrow_down(cx+170, merge_y+1150, merge_y2)
    draw.line([cx-170, merge_y2, cx+170, merge_y2], fill=ARROW, width=3)
    arrow_down(cx, merge_y2, merge_y2+40)

    # ── Logo Stamp
    box(cx-200, merge_y2+50, 400, 75,
        "PILLOW STAMPS LOGO\nDr Batra's logo.png top-right corner\nResized to 140x70, RGBA overlay",
        fill=BG_ORANGE)

    arrow_down(cx, merge_y2+125, merge_y2+165)

    # ── Final Output
    rr([cx-250, merge_y2+175, cx+250, merge_y2+260], r=16, fill=(210,255,210), outline=GREEN, w=3)
    draw.text((cx-150, merge_y2+185), "FINAL OUTPUT", fill=GREEN)
    draw.text((cx-200, merge_y2+210), "Feed 1080x1080 JPG + Story 1080x1920 JPG", fill=TEXT_DARK)
    draw.text((cx-130, merge_y2+232), "Ready to download & post", fill=TEXT_GRAY)

    # ── Chat Assistant (side note)
    small_box(60, merge_y2+50, 380, 130,
        "CHAT ASSISTANT (Right Panel):\n* Paste prompt, ask for edits\n* 'Generate an ad for hair fall'\n* AI writes Flux prompt directly\n* 'Make it more vibrant'\n* Generate from chat response\n* Full conversation history",
        fill=(240,248,255), border=BORDER, text_color=TEXT_DARK)

    path = os.path.join(OUT_DIR, "flowchart.png")
    img.save(path, "PNG")
    return path


# ─────────────────────────────────────────────
# ITERATION TIMELINE IMAGE
# ─────────────────────────────────────────────
def draw_iteration_timeline():
    W, H = 1800, 900
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    ACCENT = (99, 102, 241)
    GREEN = (34, 139, 60)
    TEXT_DARK = (30, 30, 50)
    TEXT_GRAY = (100, 100, 120)
    BORDER = (100, 100, 130)

    colors = [
        (230, 240, 255), (230, 250, 235), (255, 240, 225),
        (240, 230, 255), (255, 230, 240), (230, 250, 235),
        (255, 250, 220), (220, 255, 220),
    ]

    versions = [
        ("V1", "app.py", "Flux 2 Pro\n+ Pillow overlay", "Basic, amateur\nlook", "flux-2-pro"),
        ("V2", "app.py", "Flux 2 Pro\n+ Pillow templates\n(8 layouts)", "Better but\nrigid", "flux-2-pro"),
        ("V3", "main.py", "Flux generates\neverything +\nPillow logo only", "Best quality\nbut expensive", "flux-2-pro"),
        ("V3.1", "flux2pro.py", "Added chat\nassistant +\neditable copy", "Full workflow\nstill expensive", "flux-2-pro"),
        ("V4", "nano.py", "Switched to\nnano-banana-2", "5x cheaper\nsimilar quality", "nano-banana-2"),
        ("V5", "n.py", "30 layouts +\nskeleton preview\n+ hair detection", "Layout variety\nhair rules", "nano-banana-2"),
        ("V6", "m.py", "Dual format\nFeed + Story\n+ clothing rule", "Both formats\nstory poor", "nano-banana-2"),
        ("V7", "Metaimg.py", "Dedicated story\nprompt + pose\nvariety + fixes", "FINAL POC", "nano-banana-2"),
    ]

    draw.text((W//2 - 200, 20), "ITERATION TIMELINE", fill=ACCENT)
    draw.line([50, 55, W-50, 55], fill=ACCENT, width=2)

    # Timeline line
    tl_y = 160
    draw.line([80, tl_y, W-80, tl_y], fill=BORDER, width=4)

    bw = 180
    gap = (W - 160) // len(versions)
    for i, (ver, fname, desc, result, model) in enumerate(versions):
        cx = 80 + gap * i + gap//2
        # dot on timeline
        draw.ellipse([cx-10, tl_y-10, cx+10, tl_y+10], fill=ACCENT if i < 7 else GREEN, outline=BORDER, width=2)
        # version label above
        draw.text((cx-20, tl_y-40), ver, fill=ACCENT)

        # box below
        bx = cx - bw//2
        by = tl_y + 30
        draw.rounded_rectangle([bx, by, bx+bw, by+220], radius=10, fill=colors[i], outline=BORDER, width=2)

        draw.text((bx+10, by+10), fname, fill=TEXT_DARK)
        draw.line([bx+10, by+30, bx+bw-10, by+30], fill=BORDER, width=1)

        dy = by + 40
        for line in desc.split("\n"):
            draw.text((bx+10, dy), line, fill=TEXT_DARK)
            dy += 20

        dy += 10
        draw.line([bx+10, dy, bx+bw-10, dy], fill=BORDER, width=1)
        dy += 8
        for line in result.split("\n"):
            draw.text((bx+10, dy), line, fill=GREEN if "FINAL" in result else TEXT_GRAY)
            dy += 20

        # model tag
        mc = GREEN if "nano" in model else (200, 50, 50)
        draw.rounded_rectangle([bx+5, by+195, bx+bw-5, by+215], radius=6, fill=mc)
        mt = model[:18]
        draw.text((bx+12, by+198), mt, fill=(255, 255, 255))

    # Legend
    draw.text((80, tl_y + 280), "Model:", fill=TEXT_DARK)
    draw.rounded_rectangle([150, tl_y+275, 290, tl_y+295], radius=6, fill=(200, 50, 50))
    draw.text((160, tl_y+278), "flux-2-pro ($0.03)", fill=(255, 255, 255))
    draw.rounded_rectangle([310, tl_y+275, 460, tl_y+295], radius=6, fill=GREEN)
    draw.text((320, tl_y+278), "nano-banana-2 ($0.08)", fill=(255, 255, 255))

    # Side tools
    draw.text((80, tl_y + 320), "Side Tools:", fill=TEXT_DARK)
    draw.rounded_rectangle([200, tl_y+310, 450, tl_y+360], radius=8, fill=(240, 240, 245), outline=BORDER, width=1)
    draw.text((210, tl_y+318), "ad_editor.py", fill=TEXT_DARK)
    draw.text((210, tl_y+338), "OCR text editor", fill=TEXT_GRAY)

    draw.rounded_rectangle([470, tl_y+310, 700, tl_y+360], radius=8, fill=(240, 240, 245), outline=BORDER, width=1)
    draw.text((480, tl_y+318), "reel.py", fill=TEXT_DARK)
    draw.text((480, tl_y+338), "1080->1920 converter", fill=TEXT_GRAY)

    path = os.path.join(OUT_DIR, "timeline.png")
    img.save(path, "PNG")
    return path


# ─────────────────────────────────────────────
# PDF GENERATION
# ─────────────────────────────────────────────
def generate_pdf():
    timeline_path = draw_iteration_timeline()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── PAGE 1: Cover
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 60, "", ln=True)
    pdf.cell(0, 15, "Meta Creative Generator", ln=True, align="C")
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 12, "Full Project Documentation", ln=True, align="C")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "AI-Powered Ad Creative Generator for Dr Batra's Healthcare", ln=True, align="C")
    pdf.cell(0, 8, "Built by: Amar", ln=True, align="C")
    pdf.cell(0, 8, "Tech: Python | Streamlit | Groq (LLaMA 3.3 70B) | Flux nano-banana-2 (fal.ai) | Pillow", ln=True, align="C")
    pdf.cell(0, 8, "Final POC: Metaimg.py (1077 lines)", ln=True, align="C")
    pdf.cell(0, 8, "Date: April 2026", ln=True, align="C")

    # ── PAGE 2: Main Flow (text-based, clean)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Workflow - Main Flow", ln=True, align="C")
    pdf.ln(4)

    def flow_step(num, title, details, color=(230,240,255)):
        pdf.set_fill_color(*color)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(8, 7, str(num), border=1, align="C", fill=True)
        pdf.cell(177, 7, f"  {title}", border=1, fill=True)
        pdf.ln()
        pdf.set_font("Helvetica", "", 9)
        for d in details:
            pdf.cell(8, 5, "", border=0)
            pdf.cell(177, 5, f"    {d}", border=0)
            pdf.ln()
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(100,100,100)
        pdf.cell(0, 3, "        |", ln=True)
        pdf.cell(0, 3, "        v", ln=True)
        pdf.set_text_color(0,0,0)

    flow_step(1, "USER ENTERS TOPIC", [
        'Example: "hair fall due to stress in office", "PCOS treatment", "dandruff care"'
    ], (220,235,255))

    flow_step(2, "HAIR TOPIC DETECTION (20 keywords)", [
        "Keywords: hair loss, hair fall, bald, alopecia, scalp, dandruff, hair thinning...",
        "YES -> Assign gender (50% Male / 50% Female), random hair style + lighting + pose",
        "NO -> Standard prompt (generic Indian person age 25-45)"
    ], (255,250,215))

    flow_step(3, "PLACE/BACKGROUND DETECTION (6 categories)", [
        "Traffic/Road -> blurred city road + smog  |  City/Urban -> blurred skyline",
        "Office/Work -> blurred office interior  |  Stress -> dimly lit moody atmosphere",
        "Home -> warm home interior  |  Bathroom -> warm whites, mirror feel"
    ], (220,248,230))

    flow_step(4, "EMOTION DETECTION (Groq logic)", [
        "PROBLEM topic (hair loss, acne) -> Frustration, concern, furrowed brow",
        "SOLUTION topic (treatment, cure) -> Hope, relief, slight smile",
        "RESULT topic (success, before-after) -> Confidence, happiness, eye contact"
    ], (255,238,220))

    flow_step(5, "GROQ (LLaMA 3.3 70B) - FREE API", [
        "Generates JSON: Title (max 8 words) + Subtext (max 15) + CTA (max 4)",
        "+ Visual Style + Layout (forced random from 30 layouts L01-L30)",
        "Language: Simple conversational Indian English, NOT American marketing"
    ], (235,225,255))

    flow_step(6, "USER REVIEWS & EDITS", [
        "Edit Title, Subtext, CTA before generating",
        "Select from 13 font styles: Roboto, Impact, Playfair, Montserrat, Poppins..."
    ], (220,235,255))

    flow_step(7, "SKELETON PREVIEW (saves API credits!)", [
        "Layout wireframe showing headline, CTA, person positions",
        "Stick figure with pose-specific arms (e.g. hand on head, holding comb)",
        "Character Details card: Gender, Hair Style, Lighting, Pose labels"
    ], (255,238,220))

    flow_step(8, "PROMPT BUILDER", [
        "Combines: Copy + Visual Style + Font + Layout + Hair Rules",
        "+ Clothing Rule + Pose + Lighting + Background into one Flux prompt"
    ], (235,225,255))

    flow_step(9, "FLUX (nano-banana-2) via fal.ai - $0.08/image - SAME SEED", [
        "FEED 1080x1080: Square composition, half-body/close-up",
        "STORY 1080x1920: Dedicated vertical prompt (Top 25%=headline, Mid 50%=person, Bot 25%=CTA)",
        "Safety checker ON | JPEG output | 8K photorealistic quality"
    ], (200,215,255))

    # Remove arrow for last step
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 3, "        |", ln=True)
    pdf.cell(0, 3, "        v", ln=True)
    pdf.set_text_color(0,0,0)

    pdf.set_fill_color(255,238,220)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(8, 7, "10", border=1, align="C", fill=True)
    pdf.cell(177, 7, "  PILLOW STAMPS LOGO (Dr Batra's logo.png top-right, 140x70)", border=1, fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 3, "        |", ln=True)
    pdf.cell(0, 3, "        v", ln=True)
    pdf.set_text_color(0,0,0)

    pdf.set_fill_color(210,255,210)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(8, 10, "11", border=1, align="C", fill=True)
    pdf.cell(177, 10, "  FINAL OUTPUT: Feed 1080x1080 JPG + Story 1080x1920 JPG", border=1, fill=True)
    pdf.ln()

    # ── PAGE 3: Hair Fall Detail
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Workflow - Hair Fall Detection Detail", ln=True, align="C")
    pdf.ln(4)

    # Male section
    pdf.set_fill_color(215,235,255)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "  MALE WORKFLOW (50% probability)", border=1, ln=True, fill=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "  Subject: Indian man, 30-35, wheatish skin, stubble, frustrated, NOT smiling", border=1, ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "  Hair Styles (Norwood Stage 2-3 - NOT bald, max 25% loss):", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    col = [62, 62, 62]
    for h in ["Short (2-3cm)", "Medium (5-7cm)", "Longer (8-10cm)"]:
        pdf.cell(col[0], 6, h, border=1, align="C")
    pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    descs = ["Crown thinning, scalp visible", "Density diff sides vs crown", "M-shaped recession, temples thin"]
    for i, d in enumerate(descs):
        pdf.cell(col[i], 5, d, border=1, align="C")
    pdf.ln(7)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "  Lighting (random):", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(62, 5, "Morning Window - warm side", border=1)
    pdf.cell(62, 5, "Overcast - diffused cool", border=1)
    pdf.cell(62, 5, "Harsh Side - deep shadow", border=1)
    pdf.ln(7)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "  Poses (5 on-head / 5 off-head = 50/50 split):", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230,248,230)
    pdf.cell(93, 6, "Hands ON Head", border=1, align="C", fill=True)
    pdf.set_fill_color(255,235,235)
    pdf.cell(93, 6, "Hands OFF Head", border=1, align="C", fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    on_m = ["Touching Crown", "Running Fingers", "Checking Hairline", "Frustrated with Comb", "Head Down Stress"]
    off_m = ["Holding Hair Strands", "Mirror Check", "Pillow Shock", "Comparing Old Photo", "Staring at Drain"]
    for i in range(5):
        pdf.cell(93, 5, on_m[i], border=1)
        pdf.cell(93, 5, off_m[i], border=1)
        pdf.ln()

    pdf.ln(6)

    # Female section
    pdf.set_fill_color(255,220,240)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "  FEMALE WORKFLOW (50% probability)", border=1, ln=True, fill=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "  Subject: Indian woman, 25-35, wheatish skin, worried, slight frown, tired eyes", border=1, ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "  Hair Styles (Early Stage Thinning - NO bald patches):", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    for h in ["Short Bob", "Medium", "Long", "Tied Up"]:
        pdf.cell(46, 6, h, border=1, align="C")
    pdf.ln()
    pdf.set_font("Helvetica", "", 7)
    f_descs = ["Jaw-length, wide parting", "Shoulder, wispy strands", "Below shoulder, thin part", "Bun/ponytail, thin temple"]
    for d in f_descs:
        pdf.cell(46, 5, d, border=1, align="C")
    pdf.ln(7)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "  Lighting (random):", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(62, 5, "Soft Window - warm gentle", border=1)
    pdf.cell(62, 5, "Bathroom Mirror - intimate", border=1)
    pdf.cell(62, 5, "Cool Overcast - melancholic", border=1)
    pdf.ln(7)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "  Poses (4 on-head / 4 off-head = 50/50 split):", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230,248,230)
    pdf.cell(93, 6, "Hands ON Head", border=1, align="C", fill=True)
    pdf.set_fill_color(255,235,235)
    pdf.cell(93, 6, "Hands OFF Head", border=1, align="C", fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    on_f = ["Touching Parting", "Checking Mirror", "Pulling Ponytail", "Tucking Behind Ear"]
    off_f = ["Holding Hair Strands", "Brushing Hair", "Examining Ends", "Scrolling Solutions"]
    for i in range(4):
        pdf.cell(93, 5, on_f[i], border=1)
        pdf.cell(93, 5, off_f[i], border=1)
        pdf.ln()

    pdf.ln(6)

    # Clothing Rule
    pdf.set_fill_color(255,238,220)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "  CLOTHING RULE (both genders)", border=1, ln=True, fill=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "  MUST: Plain light grey or white round-neck t-shirt. Same color across all formats.", ln=True)
    pdf.set_text_color(200,50,50)
    pdf.cell(0, 6, "  BANNED: Towel, bathrobe, bare shoulders, sleeveless, swimwear, low-cut, blue/dark shirt", ln=True)
    pdf.set_text_color(0,0,0)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "  Camera: Handheld feel, slight grain, 85mm f/1.4, 8K photorealistic", ln=True)
    pdf.cell(0, 6, "  Style: Raw emotional documentary - NOT studio. Natural skin, visible pores.", ln=True)
    pdf.cell(0, 6, "  Strict: Fingers anatomically correct (5 fingers). Face symmetrical. No distortion.", ln=True)

    # ── PAGE 3: Timeline
    pdf.add_page("L")
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Iteration Timeline - V1 to V7 (Final POC)", ln=True, align="C")
    pdf.image(timeline_path, x=10, y=25, w=275)

    # ── PAGE 4: Architecture
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Final Architecture", ln=True)
    pdf.set_font("Courier", "", 9)

    arch = """USER enters topic (e.g. "hair fall due to stress in office")
        |
  HAIR DETECTION - checks 20 keywords
    -> If hair topic: assigns gender (50% male / 50% female)
    -> Randomizes: hair style, lighting mood, pose
        |
  PLACE DETECTION - checks background keywords
    -> office, city, home, bathroom, traffic, stress
    -> Sets context-appropriate blurred background
        |
  GROQ (LLaMA 3.3 70B) generates:
    Title + Subtext + CTA + Visual Style + Layout
    (Layout forced random from 30 options)
        |
  USER reviews & edits all fields + selects font
        |
  SKELETON PREVIEW shows:
    Layout wireframe + Stick figure pose + Character Details
        |
  PROMPT BUILDER combines:
    Copy + Style + Font + Layout + Hair Rules
    + Clothing Rule + Pose + Lighting
        |
  FLUX (nano-banana-2) renders TWO images - SAME SEED:
    Feed: 1080x1080 (square prompt)
    Story: 1080x1920 (dedicated vertical prompt)
        |
  PILLOW stamps Dr Batra logo (top-right)
        |
  FINAL OUTPUT: Both JPGs ready to download"""

    for line in arch.split("\n"):
        pdf.cell(0, 5, line, ln=True)

    # ── PAGE 5: Model Evolution
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Model Evolution & Cost", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 10)
    headers = ["Phase", "File", "Model", "Cost/Image", "Why Changed"]
    col_w = [20, 35, 45, 25, 65]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 8, h, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    models = [
        ("V1-V3", "app.py, main.py", "flux-2-pro", "~$0.03", "Started here - good quality"),
        ("V3.1", "flux2pro.py", "flux-2-pro", "~$0.03", "Testing pro variant"),
        ("V4", "nano.py", "nano-banana-2", "~$0.08", "Switched model"),
        ("V5", "n.py", "nano-banana-2", "~$0.08", "Added layouts + hair detection"),
        ("V6", "m.py", "nano-banana-2", "~$0.08", "Dual format + clothing rule"),
        ("V7", "Metaimg.py", "nano-banana-2", "~$0.08", "FINAL POC - all fixes"),
    ]
    for row in models:
        for i, val in enumerate(row):
            pdf.cell(col_w[i], 7, val, border=1)
        pdf.ln()

    # ── Issues Section
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "All Issues - Tested, Failed, Fixed", ln=True)

    issues = [
        ("1", "Generic/Boring Prompts", "Vague prompts gave bland images",
         "Detailed system prompt: subject, lighting, camera, composition", "FIXED", "app.py"),
        ("2", "Flux Rendering Text ON Photos", "Pillow dark overlay looked amateur (2015 FB ad)",
         "Built 8 Pillow templates matching real ad designs", "FIXED but rigid", "app.py"),
        ("3", "Pillow Templates Too Rigid", "Templates couldn't match dynamic real ads",
         "Let Flux generate EVERYTHING, Pillow only stamps logo", "FIXED - breakthrough", "main.py"),
        ("4", "Text Spelling Errors", "Flux misspells long words",
         "Short text (max 8 words), repeated CTA, 'no spelling errors' in prompt", "80% fixed", "main.py"),
        ("5", "Duplicate CTA Buttons", "CTA mentioned 3x in prompt, Flux rendered 3 buttons",
         "Reduced CTA mention to once: 'only ONE button'", "FIXED", "main.py"),
        ("6", "Edited Text Not Matching", "Groq visual_style had OLD text, user edited NEW text",
         "Told Groq to never include text in visual_style", "FIXED", "main.py"),
        ("7", "Flux Adding 'Meta' Text", "Prompt said 'Meta ad' so Flux wrote 'Meta'",
         "Changed to 'social media ad' + 'Do not write Meta'", "FIXED", "main.py"),
        ("8", "Fake Copyright Text", "Flux added random copyright at bottom",
         "Added 'No copyright text, no watermark, no small print'", "FIXED", "main.py"),
        ("9", "Logo White Background", "logo.png has white rect background",
         "Needs transparent PNG version", "OPEN", "all"),
        ("10", "Double Logo", "Groq told Flux to render logo + Pillow stamped real logo",
         "Removed logo from Groq prompt, only Pillow stamps", "FIXED", "main.py"),
        ("11", "Non-Indian Faces", "Flux generated Western/Caucasian faces",
         "Added 'All people MUST be Indian, age 25-45'", "FIXED", "main.py"),
        ("12", "Medicine/Pills in Images", "Healthcare topic = Flux added pills/syringes",
         "Strict rule: 'No medicine bottles, pills, tablets, syringes'", "FIXED", "main.py"),
        ("13", "American English", "Groq wrote formal American marketing jargon",
         "Added 'simple conversational Indian English'", "FIXED", "main.py"),
        ("14", "Same Layout Every Time", "Flux repeated same text placement",
         "Added 35 text placement variations", "FIXED", "main.py"),
        ("15", "Dull/Muted Colors", "Images had boring beige/brown tones",
         "Added 12 bright color palette options", "FIXED", "main.py"),
        ("16", "Groq Repeating L01/L03", "Groq kept picking same 2-3 layouts",
         "Force random layout from Python: random.choice(LAYOUTS)", "FIXED", "n.py"),
        ("17", "No Story Format", "Only 1080x1080 Feed, no Instagram Story",
         "Added dual format: Feed + Story using same seed", "FIXED", "m.py"),
        ("18", "Story Person Cropped", "Person cut off at waist in 1080x1920",
         "Dedicated story_prompt: Top 25% headline, Mid 50% person, Bot 25% CTA", "FIXED", "Metaimg.py"),
        ("19", "Towel/Revealing Clothing", "AI generated people in towels/bathrobes",
         "CLOTHING_RULE: plain grey/white t-shirt ONLY, banned towel/bathrobe/etc", "FIXED", "m.py"),
        ("20", "Hands/Fingers Distorted", "6 fingers, warped joints, melted fingers",
         "Added anatomical correctness rules for hands", "FIXED", "Metaimg.py"),
        ("21", "Face Deformation", "Face different/distorted between Feed and Story",
         "Added 'Face symmetrical, sharp, proportionally correct'", "FIXED", "Metaimg.py"),
        ("22", "Hand Position Changing", "Right hand in Feed, left hand in Story",
         "Specified RIGHT hand + 'maintain consistent position across formats'", "FIXED", "Metaimg.py"),
        ("23", "Pose Always Same", "Every hair fall image = hand on head (boring)",
         "Added 10 male + 8 female poses, 50/50 on-head/off-head split", "FIXED", "Metaimg.py"),
        ("24", "Can't Preview Pose", "Skeleton just showed PERSON box, no pose info",
         "Added stick figure drawings + Character Details card", "FIXED", "Metaimg.py"),
        ("25", "Phone Screen Showing Face", "Comparing Old Photo pose: weird face on phone",
         "Changed to phone screen facing away from camera", "FIXED", "Metaimg.py"),
    ]

    pdf.set_font("Helvetica", "", 8)
    # Table header
    pdf.set_font("Helvetica", "B", 8)
    issue_cols = [8, 38, 45, 50, 22, 22]
    issue_headers = ["#", "Issue", "Problem", "Solution", "Status", "File"]
    for i, h in enumerate(issue_headers):
        pdf.cell(issue_cols[i], 7, h, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 7)
    for issue in issues:
        max_h = 7
        # Calculate height needed
        for i, val in enumerate(issue):
            lines_needed = max(1, len(val) // (issue_cols[i] - 2) + 1)
            max_h = max(max_h, lines_needed * 4 + 3)
        max_h = min(max_h, 18)

        if pdf.get_y() + max_h > 275:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 8)
            for i, h in enumerate(issue_headers):
                pdf.cell(issue_cols[i], 7, h, border=1, align="C")
            pdf.ln()
            pdf.set_font("Helvetica", "", 7)

        y_before = pdf.get_y()
        x_start = pdf.get_x()
        for i, val in enumerate(issue):
            pdf.set_xy(x_start + sum(issue_cols[:i]), y_before)
            pdf.multi_cell(issue_cols[i], 4, val, border=1)
        pdf.set_y(y_before + max_h)

    # ── Hair Rules Page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Hair Fall Detection System", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Detection Keywords (20):", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5,
        "hair loss, hair fall, hairfall, hair thinning, thinning hair, bald, balding, "
        "receding hairline, hair regrowth, hair growth, alopecia, scalp, hair density, "
        "hair care, dandruff, hair issue, hair problem, hair damage, hair treatment, hair fall control")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Gender Split: 50% Male / 50% Female (random)", ln=True)
    pdf.ln(2)

    # Male table
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "Male Hair Styles:", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(30, 6, "Style", border=1); pdf.cell(155, 6, "Description", border=1); pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    m_hair = [
        ("Short (2-3cm)", "Close-cropped, crown thinning visible, scalp visible through sparse hair"),
        ("Medium (5-7cm)", "Slightly disheveled, density difference between sides and thinning crown"),
        ("Longer (8-10cm)", "M-shaped recession at temples, crown noticeably less dense"),
    ]
    for s, d in m_hair:
        pdf.cell(30, 6, s, border=1); pdf.cell(155, 6, d, border=1); pdf.ln()

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "Female Hair Styles:", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(30, 6, "Style", border=1); pdf.cell(155, 6, "Description", border=1); pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    f_hair = [
        ("Short Bob", "Jaw-length, wider center parting, thin temples"),
        ("Medium", "Shoulder-length, wider parting, wispy hairline strands"),
        ("Long", "Below shoulder, reduced density at parting and temples"),
        ("Tied Up", "Messy bun/ponytail, wider parting, thin temples"),
    ]
    for s, d in f_hair:
        pdf.cell(30, 6, s, border=1); pdf.cell(155, 6, d, border=1); pdf.ln()

    # Poses
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "Pose Variety (50/50 Hands On/Off Head):", ln=True)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 7, "Male Poses (10):", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(93, 6, "Hands ON Head (5)", border=1, align="C")
    pdf.cell(93, 6, "Hands OFF Head (5)", border=1, align="C"); pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    on_m = ["Touching Crown", "Running Fingers", "Checking Hairline", "Frustrated with Comb", "Head Down Stress"]
    off_m = ["Holding Hair Strands", "Mirror Check", "Pillow Shock", "Comparing Old Photo", "Staring at Drain"]
    for i in range(5):
        pdf.cell(93, 5, on_m[i], border=1); pdf.cell(93, 5, off_m[i], border=1); pdf.ln()

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 7, "Female Poses (8):", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(93, 6, "Hands ON Head (4)", border=1, align="C")
    pdf.cell(93, 6, "Hands OFF Head (4)", border=1, align="C"); pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    on_f = ["Touching Parting", "Checking Mirror", "Pulling Ponytail", "Tucking Behind Ear"]
    off_f = ["Holding Hair Strands", "Brushing Hair", "Examining Ends", "Scrolling Solutions"]
    for i in range(4):
        pdf.cell(93, 5, on_f[i], border=1); pdf.cell(93, 5, off_f[i], border=1); pdf.ln()

    # Clothing & lighting
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "Clothing Rule:", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 5,
        "MUST: Plain light grey or white round-neck t-shirt\n"
        "BANNED: Towel, bathrobe, bare shoulders, revealing clothing, swimwear, "
        "sleeveless, low-cut, blue shirt, dark shirt")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "Lighting Moods:", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "Male: Morning Window Light | Overcast Natural | Harsh Side Light", ln=True)
    pdf.cell(0, 5, "Female: Soft Window Light | Bathroom Mirror Light | Cool Overcast Light", ln=True)

    # Background detection
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "Place/Background Detection:", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(60, 6, "Keywords", border=1, align="C")
    pdf.cell(125, 6, "Background Applied", border=1, align="C"); pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    bgs = [
        ("pollution, traffic, road", "Blurred busy city road with vehicles and smog"),
        ("city, urban, metro, mumbai", "Blurred city skyline with buildings"),
        ("office, work, corporate", "Blurred modern office interior"),
        ("stress, pressure, anxiety", "Blurred dimly lit home/office, moody"),
        ("home, kitchen, bedroom", "Softly blurred warm home interior"),
        ("bathroom, mirror, shower", "Softly blurred bathroom, warm whites"),
    ]
    for kw, bg in bgs:
        pdf.cell(60, 5, kw, border=1); pdf.cell(125, 5, bg, border=1); pdf.ln()

    # ── File Structure Page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Final File Structure", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 8)
    file_cols = [30, 18, 22, 115]
    file_headers = ["File", "Lines", "Model", "Purpose"]
    for i, h in enumerate(file_headers):
        pdf.cell(file_cols[i], 7, h, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    files = [
        ("Metaimg.py", "1077", "nano-banana-2", "FINAL POC - all features, pose variety, dual format, stick figures"),
        ("m.py", "829", "nano-banana-2", "Previous version - simpler poses, same story prompt as feed"),
        ("n.py", "810", "nano-banana-2", "Added 30 layouts + skeleton previews + hair detection"),
        ("nano.py", "619", "nano-banana-2", "First nano-banana-2 switch from flux-2-pro"),
        ("main.py", "597", "flux-2-pro", "Layout system added, Flux generates everything"),
        ("flux2pro.py", "612", "flux-2-pro", "Flux 2 Pro variant testing + chat"),
        ("app.py", "576", "flux-2-pro", "Original V1 - basic flow"),
        ("ad_editor.py", "465", "N/A", "Side tool: OCR text editor for images"),
        ("reel.py", "374", "N/A", "Side tool: 1080x1080 to 1080x1920 converter"),
    ]
    for row in files:
        for i, val in enumerate(row):
            pdf.cell(file_cols[i], 6, val, border=1)
        pdf.ln()

    # ── Iterations Summary
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Complete Iterations Summary", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 8)
    iter_cols = [14, 25, 55, 45, 46]
    iter_headers = ["Ver", "File", "Approach", "Model", "Outcome"]
    for i, h in enumerate(iter_headers):
        pdf.cell(iter_cols[i], 7, h, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 7)
    iters = [
        ("V1", "app.py", "Flux photo + Pillow dark overlay", "flux-2-pro ($0.03)", "Basic, looked amateur"),
        ("V2", "app.py", "Flux photo + Pillow templates (8 layouts)", "flux-2-pro ($0.03)", "Better but rigid"),
        ("V3", "main.py", "Flux generates everything + Pillow logo", "flux-2-pro ($0.03)", "Best quality, expensive"),
        ("V3.1", "flux2pro.py", "Added chat + editable copy + regenerate", "flux-2-pro ($0.03)", "Full workflow, expensive"),
        ("V4", "nano.py", "Switched to nano-banana-2", "nano-banana-2 ($0.08)", "5x cheaper, similar quality"),
        ("V5", "n.py", "30 layouts + skeleton + hair detection", "nano-banana-2 ($0.08)", "Layout variety + hair rules"),
        ("V6", "m.py", "Dual format Feed+Story + clothing rule", "nano-banana-2 ($0.08)", "Both formats, story poor"),
        ("V7", "Metaimg.py", "Story prompt + poses + stick figures", "nano-banana-2 ($0.08)", "FINAL POC"),
    ]
    for row in iters:
        for i, val in enumerate(row):
            pdf.cell(iter_cols[i], 6, val, border=1)
        pdf.ln()

    # ── Known Limitations
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Known Limitations", ln=True)
    pdf.set_font("Helvetica", "", 9)
    limitations = [
        "1. Text Spelling: Flux sometimes misspells words (~80% accuracy). Short text works better.",
        "2. Logo Transparency: Current logo.png has white background. Needs transparent PNG.",
        "3. Feed vs Story Consistency: Same seed but different prompts = similar but not 100% identical person.",
        "4. Font Control: Flux approximates font styles but can't load actual font files.",
        "5. No Edit Without Regeneration: Changing text requires full image regeneration.",
        "6. Hindi/Regional Scripts: Cannot be rendered by Flux. Would need Pillow hybrid.",
    ]
    for lim in limitations:
        pdf.cell(0, 6, lim, ln=True)

    # ── Future Improvements
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Future Improvements", ln=True)
    pdf.set_font("Helvetica", "", 9)
    futures = [
        "[ ] Transparent logo support",
        "[ ] Image-to-image for Feed-Story consistency (IP-Adapter / FaceSwap)",
        "[ ] Multiple image variations in one click",
        "[ ] A/B testing support (2 versions side by side)",
        "[ ] Hindi/regional language text via Pillow overlay",
        "[ ] Template library (save & reuse successful layouts)",
        "[ ] Batch generation (multiple topics at once)",
        "[ ] Integration with Meta Ads Manager API",
    ]
    for f in futures:
        pdf.cell(0, 6, f, ln=True)

    # Save
    pdf_path = os.path.join(OUT_DIR, "Meta_Creative_Generator_Documentation.pdf")
    pdf.output(pdf_path)
    print(f"PDF saved: {pdf_path}")

    # Cleanup temp images
    os.remove(timeline_path)

    return pdf_path


if __name__ == "__main__":
    generate_pdf()
