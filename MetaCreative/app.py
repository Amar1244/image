"""
Meta Creative Generator - UPGRADED VERSION
Vertical step indicator, age range dropdown, live mockup phone preview,
skeleton side-by-side, prompt editor textarea, Groq-powered chat
"""

import streamlit as st
import requests
import fal_client
import json
import re
import os
import random
from PIL import Image, ImageDraw
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime
import glob
import streamlit_authenticator as stauth

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# AUTH — Add/remove users here. Generate hashed password:
#   python -c "import bcrypt; print(bcrypt.hashpw(b'yourpassword', bcrypt.gensalt()).decode())"
# ═══════════════════════════════════════════════════════════════════════════════
AUTH_CREDENTIALS = {
    "usernames": {
        "amar": {
            "name": "Amar",
            "password": "$2b$12$K4hr3gBfe.gYmgNO0YOJz.HKOh15IZWinWWzl/.eP2lnQvYU7izhC",
        },
        "pooja": {
            "name": "Pooja",
            "password": "$2b$12$yC7KfodxZwtGkEXQL9dAceIqNfTAub6.1WjdhPDJfUvesGna2XKry",
        },
        "avdhesh": {
            "name": "Avdhesh",
            "password": "$2b$12$Pua/h1U3N14yZ/rKKOu5d.2y0iD4Gen9EGUSq523O8uqYlWNN0Uq.",
        },
        "deepak_sir": {
            "name": "Deepak Sir",
            "password": "$2b$12$dM9Ow7L7QIRg.nXTuhZyZuQ4V.Lna0eYxDGwhZgtH1aBVBKFTSIwC",
        },
        "suresh_sir": {
            "name": "Suresh Sir",
            "password": "$2b$12$JqU61Q9ZSmuT7A7IFzgYLucKLOS7PMTJG6LI3jj9l1MNYmpaRAKhy",
        },
        "siddhart_sir": {
            "name": "Siddhart Sir",
            "password": "$2b$12$SGy81hSEXObTdF7vcueTu.kkwtKCQTUa4jBzG8Agcs78RnvuoFbvG",
        },
        "aaras_sir": {
            "name": "Aras Sir",
            "password": "$2b$12$b4s1cZdMVXnODNxVDjU6Gu1MQeR8SfYyKPIX47/ofAIXuW7R.nmNy",
        },
    }
}

authenticator = stauth.Authenticate(
    AUTH_CREDENTIALS,
    cookie_name="meta_creative_auth",
    cookie_key=os.getenv("AUTH_COOKIE_KEY", "mc_secret_key_2024"),
    cookie_expiry_days=1,
)

st.set_page_config(
    page_title="Meta Creative Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f5f7fa; }

/* ── Dark borders for inputs ── */
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div,
.stTextInput > div > div, .stTextArea > div > div,
.stSelectbox > div > div, div[data-baseweb="select"] > div {
    border-color: #333333 !important;
    border-width: 1.5px !important;
}
div[data-baseweb="input"]:hover > div, div[data-baseweb="textarea"]:hover > div {
    border-color: #6366f1 !important;
}
.stCheckbox > label {
    border: 1.5px solid #333333;
    border-radius: 4px;
    padding: 4px 8px;
    background: white;
}
.stRadio > label {
    border: 1.5px solid #333333;
    border-radius: 4px;
    padding: 6px 12px;
    background: white;
}
div[role="radiogroup"] {
    border: none !important;
}

/* ── Vertical step indicator ── */
.vstep-wrap { display: flex; flex-direction: column; gap: 0; }
.vstep-row  { display: flex; gap: 12px; align-items: stretch; }
.vstep-spine { display: flex; flex-direction: column; align-items: center; width: 28px; flex-shrink: 0; }
.vstep-dot  { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center;
              justify-content: center; font-size: 12px; font-weight: 600; flex-shrink: 0; z-index: 1; }
.vstep-dot-active   { background: #6366f1; color: #fff; }
.vstep-dot-done     { background: #22c55e; color: #fff; }
.vstep-dot-idle     { background: #e2e8f0; color: #94a3b8; border: 1px solid #cbd5e1; }
.vstep-line { width: 2px; flex: 1; min-height: 10px; }
.vstep-line-active  { background: #6366f1; }
.vstep-line-done    { background: #22c55e; }
.vstep-line-idle    { background: #e2e8f0; }
.vstep-body { flex: 1; padding-bottom: 20px; padding-top: 2px; }
.vstep-label { font-size: 10px; font-weight: 600; color: #6366f1; text-transform: uppercase;
               letter-spacing: 0.5px; margin-bottom: 8px; }
.vstep-label-idle { color: #94a3b8; }

/* ── Cards ── */
.card { background: #fff; border-radius: 16px; padding: 16px 18px; margin-bottom: 0;
        border: 1px solid #e8eaf0; }

/* ── Badges ── */
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-problem  { background: #fee2e2; color: #dc2626; }
.badge-solution { background: #dbeafe; color: #2563eb; }
.badge-results  { background: #d1fae5; color: #059669; }

/* ── Settings grid ── */
.sg { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px; }
.sg-cell { background: #f8fafc; border-radius: 10px; padding: 8px 10px; border: 1px solid #e2e8f0; }
.sg-label { font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase;
            letter-spacing: 0.4px; margin-bottom: 3px; }
.sg-val   { font-size: 13px; font-weight: 600; color: #1e293b; }

/* ── Ideas container ── */
.ideas-box { background: #f8fafc; border-radius: 12px; padding: 14px; border: 1px solid #e2e8f0; margin-bottom: 12px; }
.idea-row  { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #e8eaf0; }
.idea-row:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.idea-lbl  { font-size: 10px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 3px; }
.idea-txt  { font-size: 13px; color: #1e293b; font-weight: 500; line-height: 1.4; }

/* ── Char details grid ── */
.cd { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.cd-cell { background: #f8fafc; border-radius: 8px; padding: 7px 9px; border: 1px solid #e2e8f0; }
.cd-lbl  { font-size: 9px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 2px; }
.cd-val  { font-size: 12px; font-weight: 600; color: #1e293b; }

/* ── Chat ── */
.chat-user { background: #e8e8ff; border-radius: 12px 12px 2px 12px; padding: 8px 12px;
             margin: 5px 0; font-size: 12px; color: #1a1a1a; max-width: 85%; margin-left: auto; }
.chat-ai   { background: #fff; border-radius: 2px 12px 12px 12px; padding: 8px 12px;
             margin: 5px 0; font-size: 12px; color: #1a1a1a; border: 1px solid #e0e0f0;
             border-left: 3px solid #6366f1; white-space: pre-wrap; max-width: 92%; }

/* ── Feedback buttons ── */
.feedback-good { background: #22c55e; color: white; border-radius: 20px; padding: 4px 12px; font-size: 12px; }
.feedback-bad  { background: #ef4444; color: white; border-radius: 20px; padding: 4px 12px; font-size: 12px; }

/* ── Credits display ── */
.credits-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 12px; color: white; text-align: center; margin-bottom: 16px; }
.credits-amount { font-size: 24px; font-weight: 700; }
.credits-label { font-size: 10px; opacity: 0.9; }

/* ── History item ── */
.history-item { background: #f8fafc; border-radius: 10px; padding: 8px; margin-bottom: 8px; border-left: 3px solid #6366f1; font-size: 11px; }

/* ── Buttons ── */
.stButton > button { border-radius: 12px; font-weight: 600; font-size: 13px; }
#MainMenu { visibility: hidden; } footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
AGE_RANGES = ["20-30", "25-35", "30-40", "35-45", "40-50"]

# Create directories
PROMPTS_DIR = "generated_prompts"
FEEDBACK_DIR = "feedback_data"
HISTORY_DIR = "generation_history"
USER_LOGS_DIR = "user_logs"

for dir_path in [PROMPTS_DIR, FEEDBACK_DIR, HISTORY_DIR, USER_LOGS_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# ==================== ALL POSES (60 NEW POSES TOTAL) ====================

# Male Hair Loss Poses (10 original + 15 new = 25 total)
MALE_POSES = [
    # Original
    "Touching Crown", "Running Fingers through hair", "Checking Hairline in mirror",
    "Frustrated with Comb", "Head Down Stress position", "Holding Hair Strands",
    "Mirror Check with worried expression", "Pillow Shock - waking up seeing hair",
    # New 15 poses
    "Running both hands through thinning hair in frustration",
    "Leaning close to bathroom mirror inspecting hairline",
    "Head bowed down, hands gripping sink edge sadly",
    "Touching bald spot on crown with fingertips",
    "Comparing old photo of thick hair to current state",
    "Shaking head in disbelief while looking at hair on comb",
    "Kneeling down picking up fallen hair strands",
    "Sitting on bed edge, head in hands depression pose",
    "Looking up at harsh overhead light showing scalp",
    "Wet hair look after shower - scalp clearly visible",
    "Two hands pulling hair gently to show thinning areas",
    "Side profile showing receding hairline clearly",
    "Wearing cap then removing it to reveal hair loss",
    "Partner touching head comforting gesture",
    "Using phone camera to check back of head nervously"
]

# Female Hair Loss Poses (8 original + 15 new = 23 total)
FEMALE_POSES = [
    # Original
    "Touching Parting line", "Checking Mirror anxiously", "Pulling Ponytail to check thickness",
    "Tucking Behind Ear nervously", "Holding Hair Strands sadly", "Brushing Hair and seeing fall",
    "Examining Ends for damage", "Scrolling Solutions on phone",
    # New 15 poses
    "Parting hair with fingers to show widening center",
    "Crying while looking at hairbrush full of strands",
    "Tying ponytail and noticing it's thinner than before",
    "Looking at scalp in compact mirror with distress",
    "Running fingers through hair and seeing fallout",
    "Applying hair oil gently while examining roots",
    "Before bed - checking pillow for fallen hair",
    "At salon chair - stylist showing thinning areas",
    "Comparing hair thickness from months ago photo",
    "Wearing hair extensions - removing to show real hair",
    "Blow drying hair - visible scalp through thin areas",
    "Braiding hair - noticing braid is much thinner",
    "At dermatologist - pointing to thinning crown",
    "Looking at old thick hair pictures sadly",
    "Friend helping check back of head for bald spots"
]

# General Male Poses (5 original + 15 new = 20 total)
GENERAL_MALE_POSES = [
    # Original
    "Confident Smile", "Arms Crossed", "Hands in Pockets",
    "Thoughtful Look", "Phone Check",
    # New 15 poses
    "Looking at phone with slight smile - reading good news",
    "Applying moisturizer on face - skincare routine",
    "Stepping on scale - surprised happy expression",
    "Meditating cross-legged - peaceful eyes closed",
    "Before-after comparison pose - hands showing transformation",
    "High five with doctor victory pose",
    "Buttoning shirt that fits better now confidence pose",
    "Looking at reflection with proud accomplishment smile",
    "Pouring healthy green smoothie - wellness vibe",
    "Walking outdoors confidently - active lifestyle",
    "Showing toned arm muscle after weight loss",
    "Checking skin in mirror - relieved clear skin",
    "Holding supplement bottle - hopeful expression",
    "Tying shoelaces - flexible and pain-free",
    "Thumbs up gesture - positive treatment results"
]

# General Female Poses (5 original + 15 new = 20 total)
GENERAL_FEMALE_POSES = [
    # Original
    "Warm Smile", "Arms Crossed", "Hair Tuck",
    "Hands on Hips", "Phone Browsing",
    # New 15 poses
    "Selfie mode - glowing skin, confident smile",
    "Measuring waist with tape - happy progress",
    "Doing skincare routine - applying serum gently",
    "Yoga pose - peaceful and stress-free",
    "Showing before-after skin transformation joyfully",
    "High five with friend - celebrating success",
    "Trying on old dress that fits again - excited",
    "Looking at mirror - proud of clear glowing face",
    "Making healthy salad - vibrant energy",
    "Walking confidently in park - hair flowing",
    "Showing clear skin close up to camera",
    "Holding water bottle - hydrated healthy glow",
    "Dancing happily - stress free celebration",
    "Applying sunscreen - protecting skin happily",
    "Victory arms up - achieved goal celebration"
]

# ==================== END OF POSES ====================

MALE_LIGHTING_MOODS = [
    {"label":"Morning Window Light",
     "desc":"natural morning window light from one side — warm, soft but directional, gentle shadow"},
    {"label":"Overcast Natural Light",
     "desc":"soft overcast daylight — diffused, slightly cool tone, authentic documentary feel"},
    {"label":"Harsh Side Light",
     "desc":"stronger directional side light — amplifies tiredness and distress on face"},
]
FEMALE_LIGHTING_MOODS = [
    {"label":"Soft Window Light",
     "desc":"soft natural window light, slightly warm, from one side — gentle shadows, candid feel"},
    {"label":"Bathroom Mirror Light",
     "desc":"warm bathroom-style front light — intimate private moment, checking hair in mirror"},
    {"label":"Cool Overcast Light",
     "desc":"cool diffused overcast light — slightly melancholic and emotional tone"},
]
GENERAL_LIGHTING = [
    {"label":"Warm Window Light","desc":"warm natural daylight from one side — soft directional light, gentle shadows, real and candid"},
    {"label":"Soft Overcast","desc":"soft overcast diffused light from one side — natural, authentic, slightly cool tone"},
    {"label":"Golden Hour","desc":"warm golden hour light from one side — soft warm shadows, natural outdoor feel"},
]

# ── Global emotion options mapping ──────────────────────────────────────────
EMOTION_OPTIONS = {
    "worried":    "😢 Worried & Sad",
    "insecure":   "😔 Insecure",
    "overwhelmed":"😶 Overwhelmed",
    "discouraged":"😞 Discouraged",
    "exhausted":  "😩 Exhausted",
    "pain":       "😣 In Pain",
    "hopeful":    "🙂 Cautiously Hopeful",
    "relief":     "😌 Measured Relief",
    "determined": "💪 Determined",
    "confident":  "✨ Radiant Confidence",
    "proud":      "🎉 Proud & Energised",
    "serene":     "😌 Serene & Rested",
    "natural":    "😊 Natural",
}

HISTORY_FILE = os.path.join(HISTORY_DIR, "recent.json")

def load_history_from_disk():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_history_to_disk(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

GOOGLE_SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
ACTIVITY_LOG_HEADERS = [
    "timestamp",
    "username",
    "name",
    "action",
    "topic",
    "layout",
    "details",
]

def _load_google_sheet_config():
    sheet_config = st.secrets.get("google_sheets", {})
    service_account_info = st.secrets.get("gcp_service_account", {})

    if not service_account_info:
        raw_creds = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
        if raw_creds:
            try:
                service_account_info = json.loads(raw_creds)
            except json.JSONDecodeError:
                service_account_info = {}

    spreadsheet_id = sheet_config.get("spreadsheet_id") or os.getenv("GOOGLE_SHEET_ID", "")
    worksheet_name = sheet_config.get("worksheet", "activity_logs") or "activity_logs"
    return service_account_info, spreadsheet_id, worksheet_name

@st.cache_resource(show_spinner=False)
def get_google_activity_sheet():
    if gspread is None or Credentials is None:
        return None

    service_account_info, spreadsheet_id, worksheet_name = _load_google_sheet_config()
    if not service_account_info or not spreadsheet_id:
        return None

    try:
        creds = Credentials.from_service_account_info(
            dict(service_account_info),
            scopes=GOOGLE_SHEETS_SCOPES,
        )
        client = gspread.authorize(creds)
        workbook = client.open_by_key(spreadsheet_id)
        try:
            worksheet = workbook.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = workbook.add_worksheet(title=worksheet_name, rows=1000, cols=20)

        if worksheet.row_values(1) != ACTIVITY_LOG_HEADERS:
            worksheet.update("A1:G1", [ACTIVITY_LOG_HEADERS])
        return worksheet
    except Exception:
        return None

def append_google_sheet_activity(timestamp, username, name, action, topic, layout, details):
    worksheet = get_google_activity_sheet()
    if worksheet is None:
        return False

    try:
        worksheet.append_row(
            [timestamp, username, name, action, topic, layout, details],
            value_input_option="USER_ENTERED",
        )
        return True
    except Exception:
        return False

DEFAULTS = {
    "groq_key": os.getenv("GROQ_API_KEY", ""),
    "fal_key":  os.getenv("FAL_API_KEY",  ""),
    "workflow_step": 1,
    "user_topic": "",
    "detection_mode": None,
    "detected_settings": None,
    "settings_locked": False,
    "settings_applied": False,
    "hair_gender": None,
    "user_age_range": "30-40",
    "use_auto_emotion": True,
    "manual_emotion_select": "worried",
    "manual_phase": "problem",
    "manual_category": "hair",
    "manual_background": "bathroom",
    "ad_data": None,
    "base_prompt": None,
    "edited_prompt": None,
    "image_square": None,
    "image_story": None,
    "feed_url": None,
    "skeleton_square": None,
    "skeleton_story": None,
    "layout_id": "L01",
    "hair_label": None,
    "lighting_label": None,
    "pose_label": None,
    "ad_phase": None,
    "emotion_emoji": None,
    "gender_source": "auto",
    "last_topic": "",
    "ideas_generated": False,
    "settings_changed": False,
    "needs_apply": False,
    "generation_history": load_history_from_disk(),
    "fal_credits": None,
    "last_prompt_saved": None,
    "last_generation_id": None,
    "chat_messages": [{"role": "assistant",
                       "content": "Hi! I'm your Groq-powered creative assistant. Ask me for headlines, CTAs, emotion ideas, or copy feedback."}],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

# ── 30 layouts ─────────────────────────────────────────────────────────────────
LAYOUTS = [
    {"id":"L01","name":"Top-Left Headline + Bottom-Center CTA",
     "groq":"Headline top-left bold, subtext below headline, person center-right, CTA green pill button bottom-center"},
    {"id":"L02","name":"Centered Headline + Bottom-Right CTA",
     "groq":"Headline centered bold at top, subtext below headline centered, person center, CTA pill button bottom-right"},
    {"id":"L03","name":"Bottom-Left Headline + Top CTA Pill",
     "groq":"Headline bold bottom-left overlapping image, CTA pill button top-right"},
    {"id":"L04","name":"Large Top-Center Headline + Bottom-Left CTA",
     "groq":"Headline large top-center bold, subtext below headline, person bottom-center, CTA floating bottom-left"},
    {"id":"L05","name":"Diagonal Banner Headline + Bottom-Center CTA",
     "groq":"Headline in diagonal banner across top-right corner, person left, CTA pill button bottom-center"},
    {"id":"L06","name":"Arc Headline Above Person + Ribbon CTA",
     "groq":"Headline curved in arc above person's head at top, CTA at bottom with colored ribbon"},
    {"id":"L07","name":"Vertical Left Headline + Bottom-Right CTA",
     "groq":"Headline stacked vertically on left side, person right, CTA bottom-right corner"},
    {"id":"L08","name":"Bottom-Left Headline Overlap + Top-Right CTA",
     "groq":"Headline bold bottom-left overlapping image, CTA top-right as small button"},
    {"id":"L09","name":"Center-Right Split Headline + Full-Width CTA Bar",
     "groq":"Headline split into two lines center-right, person left, CTA as wide bar at very bottom"},
    {"id":"L10","name":"Badge Headline Top-Left + Bottom-Center CTA",
     "groq":"Headline inside colored circle badge top-left, person center-right, CTA bottom-center"},
    {"id":"L11","name":"Dead-Center Headline + Underline CTA",
     "groq":"Headline large dead center bold, subtext below, CTA as underline text below subtext"},
    {"id":"L12","name":"Wave Headline Top + Rounded-Rect CTA Bottom-Right",
     "groq":"Headline following wave curve at top, person center, CTA in rounded rectangle bottom-right"},
    {"id":"L13","name":"Small Top Headline + Big CTA Bottom",
     "groq":"Headline small at top, person center, CTA as the biggest element at bottom spanning wide"},
    {"id":"L14","name":"Overlay Box Headline Center-Left + Arrow CTA",
     "groq":"Headline in transparent overlay box center-left, person right, CTA floating bottom with arrow"},
    {"id":"L15","name":"Tilted Headline Top-Left + Straight CTA Bottom",
     "groq":"Headline tilted 10 degrees top-left, person center-right, CTA straight at bottom-center"},
    {"id":"L16","name":"Full-Width Uppercase Headline + Accent Pill CTA",
     "groq":"Headline uppercase spread full width at top, person center, CTA accent colored pill bottom-right"},
    {"id":"L17","name":"Silhouette-Wrap Headline + Bottom-Left CTA",
     "groq":"Headline text wrapped around person silhouette, CTA anchored bottom-left"},
    {"id":"L18","name":"Ribbon Headline Center-Top + Rounded CTA Bottom",
     "groq":"Headline with colored ribbon highlight behind it at center-top, person below, CTA rounded edges bottom"},
    {"id":"L19","name":"Straight Minimal Layout",
     "groq":"Straight horizontal minimal layout — headline top-left, subtext below, person right, CTA bottom-center"},
    {"id":"L20","name":"Highlighted Background Text",
     "groq":"Headline integrated into background with colored highlight strip behind it, person right, CTA bottom"},
    {"id":"L21","name":"Left Panel 40% + Person Right + CTA Below Headline",
     "groq":"Headline left-aligned on solid colored panel left 40%, person on right side, CTA button below headline on panel"},
    {"id":"L22","name":"Top Half Text + Circular Person + CTA Between",
     "groq":"Headline centered on clean beige/white top half, person in circular frame bottom half, CTA between them"},
    {"id":"L23","name":"Bold Top Headline + Person Fills Bottom + Strip CTA",
     "groq":"Headline bold on top with thin accent line below it, subtext under line, person fills bottom 60%, CTA as colored strip at very bottom"},
    {"id":"L24","name":"Curved Banner Top + Vignette Person + Pill CTA",
     "groq":"Headline on colored curved banner across top, person below with soft vignette, CTA rounded pill at bottom-center"},
    {"id":"L25","name":"Left Headline + Framed Person Right + Bottom-Left CTA",
     "groq":"Headline large left-aligned with colored underline accent, person on right in rounded rectangle frame, CTA bottom-left"},
    {"id":"L26","name":"Frosted Glass Overlay Headline + Bold Bar CTA",
     "groq":"Headline on frosted glass overlay box top-center, person behind slightly blurred, CTA as bold bar at bottom"},
    {"id":"L27","name":"Accent Color First Word + Arrow CTA Bottom",
     "groq":"Headline split — first word in accent color rest in dark color top-left, person right, CTA bottom with arrow icon"},
    {"id":"L28","name":"Speech Bubble Headline + Floating Button CTA",
     "groq":"Headline inside colored speech bubble near the person, CTA as a floating button bottom-right"},
    {"id":"L29","name":"Person Fills Top + Card Bottom Headline + CTA",
     "groq":"Person fills top 65% edge-to-edge, headline at bottom on solid white card section, CTA on card below headline"},
    {"id":"L30","name":"Vertical Accent Strip Left + Person Right + Center CTA",
     "groq":"Headline on left with vertical colored accent strip beside it, person on right with soft shadow, CTA bottom-center"},
]

LAYOUT_OPTIONS_FOR_GROQ = "\n".join([f'- "{l["groq"]}"' for l in LAYOUTS])

# ── Helper functions ───────────────────────────────────────────────────────────
def get_next_serial():
    existing_files = glob.glob(f"{PROMPTS_DIR}/prompt_*.txt")
    if not existing_files:
        return 1
    numbers = []
    for f in existing_files:
        match = re.search(r'prompt_(\d+)(?:_.*)?\.txt$', os.path.basename(f))
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) + 1 if numbers else 1

def save_prompt_with_serial(prompt_text, metadata):
    serial = get_next_serial()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{PROMPTS_DIR}/prompt_{serial:04d}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"SERIAL NUMBER: {serial:04d}\n")
        f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TOPIC: {metadata.get('topic', 'N/A')}\n")
        f.write(f"GENDER: {metadata.get('gender', 'N/A')}\n")
        f.write(f"AGE RANGE: {metadata.get('age_range', 'N/A')}\n")
        f.write(f"PHASE: {metadata.get('phase', 'N/A')}\n")
        f.write(f"EMOTION: {metadata.get('emotion', 'N/A')}\n")
        f.write(f"LAYOUT: {metadata.get('layout', 'N/A')}\n")
        f.write(f"{'='*60}\n")
        f.write(f"PROMPT:\n{prompt_text}\n")
        f.write(f"{'='*60}\n")
    
    return serial, filename

def save_feedback(generation_id, rating, comments=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_file = f"{FEEDBACK_DIR}/feedback.json"

    # Prepare feedback entry
    feedback_entry = {
        "serial_no": st.session_state.last_prompt_saved or "unknown",
        "generation_id": generation_id,
        "timestamp": timestamp,
        "username": st.session_state.get("username", "unknown"),
        "name": st.session_state.get("name", "unknown"),
        "rating": rating,  # "good", "bad", or "feedback"
        "comments": comments,
        "topic": st.session_state.user_topic,
        "prompt": (st.session_state.edited_prompt or st.session_state.base_prompt),
        "ad_data": {
            "title": st.session_state.ad_data.get("title", "") if st.session_state.ad_data else "",
            "subtext": st.session_state.ad_data.get("subtext", "") if st.session_state.ad_data else "",
            "cta": st.session_state.ad_data.get("cta", "") if st.session_state.ad_data else ""
        },
        "metadata": {
            "gender": st.session_state.hair_gender,
            "age_range": st.session_state.user_age_range,
            "emotion": st.session_state.manual_emotion_select,
            "phase": st.session_state.ad_phase,
            "layout": st.session_state.layout_id
        },
        "image_url": st.session_state.feed_url or "N/A"
    }

    # Load existing feedbacks or create new list
    feedbacks = []
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedbacks = json.load(f)
        except:
            feedbacks = []

    # Append new feedback
    feedbacks.append(feedback_entry)

    # Save all feedbacks back to file
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, indent=2, ensure_ascii=False)

    return feedback_file

def add_to_history(image_type, serial):
    existing_ids = [
        item.get("id", 0)
        for item in st.session_state.generation_history
        if isinstance(item, dict)
    ]
    history_entry = {
        "id": (max(existing_ids) + 1) if existing_ids else 1,
        "timestamp": datetime.now().strftime("%d %b %H:%M"),
        "topic": st.session_state.user_topic[:30] + "..." if len(st.session_state.user_topic) > 30 else st.session_state.user_topic,
        "image_type": image_type,
        "prompt_serial": serial
    }
    st.session_state.generation_history.insert(0, history_entry)
    st.session_state.generation_history = st.session_state.generation_history[:10]
    save_history_to_disk(st.session_state.generation_history)

def log_user_activity(action, details=""):
    username = st.session_state.get("username", "unknown")
    name = st.session_state.get("name", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_username = re.sub(r"[^A-Za-z0-9_.-]", "_", username) or "unknown"
    log_file = os.path.join(USER_LOGS_DIR, f"{safe_username}.txt")
    topic = st.session_state.get("user_topic") or ""
    layout = st.session_state.get("layout_id") or ""
    line = (
        f"{timestamp} | username={username} | name={name} | action={action}"
        f" | topic={topic} | layout={layout}"
    )
    if details:
        line += f" | details={details}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    append_google_sheet_activity(timestamp, username, name, action, topic, layout, details)

def check_fal_credits(api_key):
    endpoints = [
        "https://fal.run/v1/me",
        "https://rest.alpha.fal.ai/v1/me",
    ]
    for url in endpoints:
        try:
            import urllib.request
            req = urllib.request.Request(
                url,
                headers={"Authorization": f"Key {api_key}"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = json.loads(resp.read())
                for key in ("credits_balance", "credits", "balance", "remaining_credits"):
                    if key in body:
                        val = body[key]
                        try:
                            return f"{float(val):.2f}"
                        except Exception:
                            return str(val)
        except Exception:
            continue
    return "N/A"

# ── Detection helpers ───────────────────────────────────────────────────────────
HAIR_LOSS_KEYWORDS = ["hair loss","hair fall","hairfall","hair thinning","thinning hair",
    "bald","balding","receding hairline","hair regrowth","hair growth",
    "alopecia","scalp","hair density","hair care","dandruff"]

def is_hair_loss_topic(t):
    return any(kw in t.lower() for kw in HAIR_LOSS_KEYWORDS)

def detect_ad_phase(topic):
    t = topic.lower()
    if any(k in t for k in ["result","success","before after","transformation","worked","improved","better","regrew","healed","clear","glowing"]):
        return "results"
    if any(k in t for k in ["treatment","cure","remedy","therapy","medicine","solution","doctor","clinic","consult","help","fix","solve"]):
        return "solution"
    return "problem"

def detect_topic_category(topic):
    t = topic.lower()
    if any(k in t for k in ["hair","bald","alopecia","dandruff","scalp"]): return "hair"
    if any(k in t for k in ["acne","pimple","breakout","skin","pigmentation"]): return "skin"
    if any(k in t for k in ["pcos","thyroid","hormonal","period"]): return "hormonal"
    if any(k in t for k in ["weight","obesity","fat","slim"]): return "weight"
    if any(k in t for k in ["stress","anxiety","tension"]): return "stress"
    if any(k in t for k in ["pain","joint","back","knee"]): return "pain"
    return "general"

SMART_POSES = {
    "hair": {
        "problem": [
            "Checking hairline in mirror with concern",
            "Running fingers through thinning hair and noticing scalp",
            "Looking at fallen hair in hand with worried expression",
            "Seated on bed edge, head slightly down, emotionally low",
            "Touching crown area while checking hair loss",
            "Side profile mirror inspection of receding hairline",
            "Holding comb with visible shed hair, upset expression",
            "Leaning toward mirror, closely examining scalp",
            "Hand on forehead, stressed about hair fall",
            "Pulling hair back gently to inspect widening parting",
            "Looking down at sink after hair wash, discouraged",
            "Covering part of hair with insecurity in public-ready pose",
            "Taking selfie of scalp or hairline to inspect problem",
            "Slouched seated pose, touching temple area in worry",
            "Looking away with frustrated expression, hand in hair",
        ],
        "solution": [
            "Consulting doctor with attentive hopeful posture",
            "Listening carefully during hair treatment consultation",
            "Applying hair serum carefully at scalp",
            "Reading hair care routine on phone with focus",
            "Standing at mirror during treatment routine",
            "Gently massaging scalp as part of treatment",
            "Holding dropper bottle, calm and reassured expression",
            "Brushing hair slowly while checking improvement hopefully",
            "Self-care routine pose with upright posture",
            "Looking into mirror with cautious optimism during treatment",
            "Sitting calmly during guided consultation pose",
            "Following wellness routine with relaxed confidence",
            "Preparing treatment step with organized focused posture",
            "Touching hair softly with early signs of confidence",
            "Neutral balanced pose showing trust in recovery journey",
        ],
        "results": [
            "Confident smile while touching healthy hair",
            "Looking in mirror with satisfaction and relief",
            "Running fingers through hair proudly",
            "Outdoor confident walking pose with relaxed smile",
            "Open-shoulder success posture with direct eye contact",
            "Hair sweep with renewed confidence",
            "Before-after reveal pose showing transformation pride",
            "Happy candid smile with visible self-confidence",
            "Social-ready pose, feeling comfortable in appearance",
            "Side pose highlighting fuller healthier hair",
            "Relaxed seated pose with calm proud smile",
            "Getting ready confidently in front of mirror",
            "Positive thumbs-up with healthy-hair confidence",
            "Proud natural smile, lightly adjusting hair",
            "Radiant relief pose showing restored self-esteem",
        ],
    },
    "skin": {
        "problem": [
            "Looking closely into mirror at acne or skin texture with concern",
            "Touching cheek gently while checking irritated skin",
            "Side-face inspection pose with worried expression",
            "Covering part of face with insecurity",
            "Leaning toward mirror to inspect pimples or rashes",
            "Looking at phone camera in selfie mode to check skin condition",
            "Seated tired pose, touching face with frustration",
            "Hand on chin while noticing breakouts",
            "Looking away with self-conscious expression about skin",
            "Close-up inspection pose of forehead or cheek",
            "Holding face gently with discouraged expression",
            "Getting ready but pausing due to visible skin concern",
            "Mirror pose after washing face, noticing irritation",
            "Low-confidence public-ready pose with skin insecurity",
            "Reflective pose with visible disappointment about skin flare-up",
        ],
        "solution": [
            "Applying serum carefully during skincare routine",
            "Gentle face cleansing pose at sink",
            "Looking at doctor with attentive hopeful posture",
            "Listening during skincare consultation",
            "Reading treatment instructions with focus",
            "Applying cream to affected area carefully",
            "Standing at mirror with calm self-care posture",
            "Holding skincare routine product with trust and reassurance",
            "Checking skin gently while following treatment",
            "Relaxed consultation pose with improving confidence",
            "Washing face with disciplined care routine posture",
            "Balanced upright pose showing commitment to skincare",
            "Following morning skincare step with calm focus",
            "Soft smile during routine, feeling hopeful",
            "Neutral wellness pose reflecting trust in treatment plan",
        ],
        "results": [
            "Confident glowing-skin selfie pose",
            "Looking in mirror with satisfaction and relief",
            "Close-up clear-skin confidence pose",
            "Soft smile with direct eye contact and healthy glow",
            "Natural radiant pose with relaxed face",
            "Outdoor confident walk with clear-skin pride",
            "Light face-touch appreciation pose",
            "Happy candid smile with visible confidence",
            "Social-ready confident pose",
            "Before-after reveal posture showing skin improvement",
            "Calm radiant side-face pose",
            "Getting ready happily with renewed confidence",
            "Proud natural smile highlighting clear skin",
            "Healthy lifestyle glow pose with relaxed energy",
            "Bright confident pose showing comfort without insecurity",
        ],
    },
    "pcos": {
        "problem": [
            "Seated with low energy, hand on forehead",
            "Looking into mirror with concern about appearance changes",
            "Holding lower abdomen gently with discomfort",
            "Tired sitting pose on bed edge with slouched shoulders",
            "Looking at irregular-cycle tracker on phone with stress",
            "Touching face while worried about acne or skin flare-up",
            "Reflective pose with discouraged expression",
            "Hand on waist or stomach, feeling bloated and uneasy",
            "Looking away with emotionally drained posture",
            "Leaning on table or sink with fatigue",
            "Checking weight or body changes with concern",
            "Quiet stressed pose with crossed arms and low confidence",
            "Sitting with head slightly down, overwhelmed expression",
            "Looking at self in mirror with frustration and confusion",
            "Low-mood wellness struggle pose with visible exhaustion",
        ],
        "solution": [
            "Consulting doctor with attentive hopeful posture",
            "Listening carefully during treatment discussion",
            "Reading health plan on phone with focus",
            "Writing or reviewing wellness routine notes",
            "Drinking water with calm self-care posture",
            "Light stretching or yoga preparation pose",
            "Standing upright with ready-to-improve mindset",
            "Healthy meal planning pose in kitchen",
            "Taking first-step wellness routine pose",
            "Calm mirror pose showing gradual hope",
            "Guided consultation pose with reassured expression",
            "Walking lightly as part of active recovery routine",
            "Balanced self-care pose with growing confidence",
            "Relaxed seated pose while following treatment plan",
            "Soft hopeful smile showing trust in the process",
        ],
        "results": [
            "Confident smile with healthy balanced energy",
            "Upright relaxed pose with visible relief",
            "Looking in mirror with satisfaction and self-acceptance",
            "Calm radiant pose with restored confidence",
            "Outdoor walk with light, active, confident body language",
            "Happy wellness-success pose with direct eye contact",
            "Comfortable social-ready pose with renewed self-esteem",
            "Gentle proud smile showing emotional recovery",
            "Healthy lifestyle pose with relaxed confidence",
            "Before-after progress reveal pose",
            "Peaceful yoga-inspired pose with inner balance",
            "Bright natural smile with stress-free posture",
            "Energetic achievement pose with open shoulders",
            "Relaxed candid laugh showing improved well-being",
            "Quiet confident pose reflecting hormonal-balance progress",
        ],
    },
    "hormonal": {
        "problem": [
            "Seated with low energy, hand on forehead",
            "Looking into mirror with concern about appearance changes",
            "Holding lower abdomen gently with discomfort",
            "Tired sitting pose on bed edge with slouched shoulders",
            "Looking at cycle or symptom tracker on phone with stress",
            "Touching face while worried about acne or skin flare-up",
            "Reflective pose with discouraged expression",
            "Hand on waist or stomach, feeling bloated and uneasy",
            "Looking away with emotionally drained posture",
            "Leaning on table or sink with fatigue",
            "Checking body changes with concern",
            "Quiet stressed pose with crossed arms and low confidence",
            "Sitting with head slightly down, overwhelmed expression",
            "Looking at self in mirror with frustration and confusion",
            "Low-mood hormonal-health struggle pose with visible exhaustion",
        ],
        "solution": [
            "Consulting doctor with attentive hopeful posture",
            "Listening carefully during treatment discussion",
            "Reading health plan on phone with focus",
            "Writing or reviewing wellness routine notes",
            "Drinking water with calm self-care posture",
            "Light stretching or yoga preparation pose",
            "Standing upright with ready-to-improve mindset",
            "Healthy meal planning pose in kitchen",
            "Taking first-step wellness routine pose",
            "Calm mirror pose showing gradual hope",
            "Guided consultation pose with reassured expression",
            "Walking lightly as part of active recovery routine",
            "Balanced self-care pose with growing confidence",
            "Relaxed seated pose while following treatment plan",
            "Soft hopeful smile showing trust in the process",
        ],
        "results": [
            "Confident smile with healthy balanced energy",
            "Upright relaxed pose with visible relief",
            "Looking in mirror with satisfaction and self-acceptance",
            "Calm radiant pose with restored confidence",
            "Outdoor walk with light, active, confident body language",
            "Happy wellness-success pose with direct eye contact",
            "Comfortable social-ready pose with renewed self-esteem",
            "Gentle proud smile showing emotional recovery",
            "Healthy lifestyle pose with relaxed confidence",
            "Before-after progress reveal pose",
            "Peaceful yoga-inspired pose with inner balance",
            "Bright natural smile with stress-free posture",
            "Energetic achievement pose with open shoulders",
            "Relaxed candid laugh showing improved well-being",
            "Quiet confident pose reflecting hormonal-balance progress",
        ],
    },
    "weight": {
        "problem": [
            "Looking at mirror with concern about body changes",
            "Measuring waist with disappointed expression",
            "Sitting tired with slouched shoulders",
            "Hand on stomach with low-confidence posture",
            "Looking at old clothes that no longer fit",
            "Seated on bed edge feeling heavy and discouraged",
            "Looking down with frustrated expression after checking weight",
            "Leaning on table with low energy and fatigue",
            "Reflective pose with crossed arms and body insecurity",
            "Checking body shape in side profile with concern",
            "Holding waistband with uncomfortable expression",
            "Looking at weighing scale with discouragement",
            "Pausing during daily activity with visible tiredness",
            "Public-ready but low-confidence pose about body image",
            "Quiet emotionally drained pose about fitness struggle",
        ],
        "solution": [
            "Talking to doctor or coach with focused posture",
            "Listening carefully during health consultation",
            "Measuring waist with hopeful progress mindset",
            "Preparing healthy meal with commitment",
            "Drinking water with wellness-focused posture",
            "Light exercise preparation pose",
            "Tying shoelaces ready for walk or workout",
            "Standing upright with ready-to-change attitude",
            "Tracking progress on phone with cautious optimism",
            "Active walking pose during recovery journey",
            "Balanced meal planning pose in kitchen",
            "Stretching pose with growing confidence",
            "Checking mirror with disciplined motivation",
            "Calm lifestyle-routine pose showing commitment",
            "Soft smile with trust in health-improvement process",
        ],
        "results": [
            "Measuring waist happily with visible progress",
            "Confident mirror pose with satisfaction",
            "Walking outdoors with energetic confidence",
            "Proud smile in better-fitting clothes",
            "Open-shoulder success posture with direct eye contact",
            "Light celebratory victory pose",
            "Before-after transformation reveal posture",
            "Active lifestyle pose with renewed energy",
            "Happy candid smile showing improved self-confidence",
            "Trying on old clothes that fit again with joy",
            "Relaxed upright pose with healthier body confidence",
            "Thumbs-up pose showing progress satisfaction",
            "Healthy strong pose with balanced energy",
            "Social-confidence pose, ready to go out happily",
            "Calm proud smile reflecting successful transformation",
        ],
    },
    "pain": {
        "problem": [
            "Holding knee with visible discomfort",
            "Holding lower back while standing in pain",
            "Seated with shoulder pain and tense expression",
            "Touching neck with stiffness and discomfort",
            "Slow standing pose with painful body language",
            "Leaning on chair or wall for support",
            "Hand on ankle or foot with strained expression",
            "Sitting with one hand on painful joint and tired face",
            "Walking carefully with restricted movement",
            "Wincing while bending slightly",
            "Morning stiffness pose while getting up from bed",
            "Holding wrist or elbow with discomfort",
            "Side profile showing guarded movement due to pain",
            "Frustrated pose after failed movement attempt",
            "Quiet low-energy pose with chronic pain fatigue",
        ],
        "solution": [
            "Consulting doctor with attentive posture",
            "Listening carefully during pain-treatment discussion",
            "Guided stretch pose with controlled movement",
            "Light exercise or rehab preparation posture",
            "Sitting upright with treatment-focused calmness",
            "Following physiotherapy-style movement carefully",
            "Applying care or support to painful area",
            "Standing balanced with cautious optimism",
            "Walking slowly but steadily during recovery",
            "Reading recovery advice with focused expression",
            "Gentle mobility pose with trust in treatment",
            "Controlled seated stretch with reassured mindset",
            "Wellness-routine pose showing commitment to healing",
            "Neutral posture with reduced stiffness and early hope",
            "Soft smile during guided recovery process",
        ],
        "results": [
            "Walking comfortably with relief and confidence",
            "Upright relaxed pose without guarded movement",
            "Light stretch with freedom and ease",
            "Smiling naturally after pain relief",
            "Active daily-life pose with restored mobility",
            "Open-shoulder relief pose showing comfort",
            "Before-after progress pose showing better movement",
            "Confident standing posture with body ease",
            "Outdoor walk with pain-free body language",
            "Gentle celebratory success pose",
            "Relaxed seated pose without discomfort",
            "Calm proud smile reflecting recovery",
            "Daily activity pose done comfortably again",
            "Healthy active posture with restored flexibility",
            "Radiant relief pose showing improved joint comfort",
        ],
    },
    "stress": {
        "problem": [
            "Hand on forehead with stressed expression",
            "Sitting with head slightly down and mental fatigue",
            "Looking at phone with overwhelmed face",
            "Leaning on desk or table with exhaustion",
            "Eyes closed, tense face, trying to cope",
            "Holding temples with anxiety or pressure",
            "Slouched seated pose with low emotional energy",
            "Looking away with emotionally drained expression",
            "Restless posture showing inner tension",
            "Sleepless tired pose on bed edge",
            "Deep sigh pose with visible burnout",
            "Arms crossed with discouraged stressed mood",
            "Reflective low-mood pose with distant gaze",
            "Quiet overwhelmed pose with hunched shoulders",
            "Fatigue posture showing mental overload",
        ],
        "solution": [
            "Talking to doctor or therapist with attentive calmness",
            "Listening carefully during wellness guidance",
            "Deep breathing pose with slow relaxed posture",
            "Meditation preparation pose with focus",
            "Gentle yoga stretch pose",
            "Drinking water with self-care mindset",
            "Journaling or planning wellness steps calmly",
            "Walking lightly with recovery-focused posture",
            "Looking at phone or notes with hopeful clarity",
            "Relaxed seated pose during guided care",
            "Standing upright with emotional reset posture",
            "Self-care routine pose with calm intention",
            "Soft smile while practicing healthier habits",
            "Neutral balanced pose showing trust in recovery",
            "Quiet hopeful pose with easing mental tension",
        ],
        "results": [
            "Peaceful smile with relaxed shoulders",
            "Calm meditation-inspired pose",
            "Outdoor walk with light stress-free body language",
            "Relaxed seated pose with inner peace",
            "Gentle candid smile showing emotional balance",
            "Open posture with visible calm confidence",
            "Before-after wellness progress pose",
            "Rested natural expression with ease",
            "Healthy lifestyle glow pose with relaxed energy",
            "Social-confidence pose without stress tension",
            "Bright relief pose showing mental lightness",
            "Soft side profile with peaceful expression",
            "Quiet radiant pose with emotional stability",
            "Happy natural laugh with reduced stress",
            "Balanced confident posture showing restored wellness",
        ],
    },
}

def normalize_smart_pose_category(category, topic=""):
    if category == "hormonal" and "pcos" in (topic or "").lower():
        return "pcos"
    return category

def get_smart_pose(category, phase, fallback_poses, topic=""):
    category_key = normalize_smart_pose_category(category, topic)
    category_map = SMART_POSES.get(category_key, {})
    poses = category_map.get(phase, [])
    if poses:
        return random.choice(poses)
    return random.choice(fallback_poses)

PLACE_BACKGROUNDS = [
    {"keywords": ["pollution", "smog", "dust", "air quality", "traffic", "commute", "road", "driving"],
     "bg": "very simple plain neutral background with a faint heavily blurred urban tone only, no visible objects",
     "label": "City Road / Traffic"},
    {"keywords": ["city", "urban", "metro", "mumbai", "delhi", "bangalore", "pune"],
     "bg": "very simple plain neutral background with a faint heavily blurred city tone only, no visible objects",
     "label": "City / Urban"},
    {"keywords": ["office", "work", "corporate", "job", "boss", "colleague", "meeting"],
     "bg": "very simple plain neutral office-toned background, heavily blurred, no visible desks, monitors, chairs, or people",
     "label": "Office / Workplace"},
    {"keywords": ["stress", "pressure", "deadline", "anxiety", "tension"],
     "bg": "very simple plain dark neutral background, heavily blurred, no visible interior objects",
     "label": "Stress Environment"},
    {"keywords": ["home", "kitchen", "bedroom", "living room", "couch", "sofa"],
     "bg": "very simple plain warm neutral background, heavily blurred, no visible furniture or decor",
     "label": "Home Interior"},
    {"keywords": ["bathroom", "mirror", "shower", "morning routine"],
     "bg": "very simple plain warm off-white bathroom-toned background, heavily blurred, no visible sink, mirror, or objects",
     "label": "Bathroom / Mirror"},
]

def detect_background(topic):
    topic_lower = (topic or "").lower()
    for place in PLACE_BACKGROUNDS:
        if any(kw in topic_lower for kw in place["keywords"]):
            return place["bg"], place["label"]
    return None, None

def get_lighting_background(light_label, group):
    fallback_map = {
        "male_hair": {
            "Morning Window Light": "very simple plain warm neutral background, heavily blurred, no visible room details",
            "Overcast Natural Light": "very simple plain off-white neutral background, heavily blurred, no visible room details",
            "Harsh Side Light": "very simple plain darker neutral background, heavily blurred, no visible room details",
        },
        "female_hair": {
            "Soft Window Light": "very simple plain warm neutral background, heavily blurred, no visible room details",
            "Bathroom Mirror Light": "very simple plain warm off-white background, heavily blurred, no visible bathroom details",
            "Cool Overcast Light": "very simple plain cool neutral background, heavily blurred, no visible room details",
        },
        "general": {
            "Warm Window Light": "very simple plain warm neutral background, heavily blurred, no visible objects",
            "Soft Overcast": "very simple plain neutral background, heavily blurred, no visible objects",
            "Golden Hour": "very simple plain warm neutral background, heavily blurred, no visible objects",
        },
    }
    return fallback_map.get(group, {}).get(light_label, "softly blurred real environment, natural tones")

def auto_detect_all_settings(topic):
    t = topic.lower()
    if any(k in t for k in ["pcos","pregnancy","menopause","breast","period"]):
        gender = "female"
    elif any(k in t for k in ["prostate","testicular","erectile"]):
        gender = "male"
    else:
        gender = random.choice(["male","female"])

    phase    = detect_ad_phase(topic)
    category = detect_topic_category(topic)

    _, detected_bg_label = detect_background(topic)
    background = {
        "Office / Workplace": "office",
        "Bathroom / Mirror": "bathroom",
        "City / Urban": "city",
        "City Road / Traffic": "city",
        "Stress Environment": "office",
        "Home Interior": "home",
    }.get(detected_bg_label, "home")

    age_range = "30-40"
    if category == "skin": age_range = "20-30"
    elif category == "hair": age_range = "30-40"

    EMOTION_MATRIX = {
        "hair":     {"problem":  ("😢 Worried & Sad",       "worried"),
                     "solution": ("🙂 Cautiously Hopeful",   "hopeful"),
                     "results":  ("✨ Radiant Confidence",   "confident")},
        "skin":     {"problem":  ("😔 Insecure",             "insecure"),
                     "solution": ("🙂 Cautiously Hopeful",   "hopeful"),
                     "results":  ("✨ Radiant Confidence",   "confident")},
        "hormonal": {"problem":  ("😶 Overwhelmed",          "overwhelmed"),
                     "solution": ("😌 Measured Relief",      "relief"),
                     "results":  ("🌸 Balanced Confidence",  "confident")},
        "weight":   {"problem":  ("😞 Discouraged",          "discouraged"),
                     "solution": ("💪 Determined",           "determined"),
                     "results":  ("🎉 Proud & Energised",    "proud")},
        "stress":   {"problem":  ("😩 Exhausted",            "exhausted"),
                     "solution": ("😮 Stress Lifting",       "relief"),
                     "results":  ("😌 Serene & Rested",      "serene")},
        "pain":     {"problem":  ("😣 In Pain",              "pain"),
                     "solution": ("🤔 Cautiously Optimistic","hopeful"),
                     "results":  ("🙌 Pain Free",            "confident")},
        "general":  {"problem":  ("😟 Concerned",            "worried"),
                     "solution": ("🙂 Hopeful",              "hopeful"),
                     "results":  ("😊 Confident",            "confident")},
    }
    cat_map   = EMOTION_MATRIX.get(category, EMOTION_MATRIX["general"])
    emotion_name, emotion_key = cat_map.get(phase, ("🙂 Natural","natural"))

    return {
        "gender": gender, "age_range": age_range,
        "phase": phase, "category": category,
        "background": background,
        "emotion_name": emotion_name, "emotion_key": emotion_key,
    }

# ── Clothing rule ───────────────────────────────────────────────────────────────
MALE_CLOTHING = [
    "plain t-shirt",
    "solid color t-shirt",
    "minimal t-shirt",
    "oversized t-shirt",
    "relaxed fit t-shirt",
    "casual cotton t-shirt",
    "casual button-down shirt",
    "light cotton shirt",
    "minimal casual shirt",
    "soft pastel shirt",
    "modern casual shirt",
    "smart casual shirt",
    "light formal shirt",
    "minimal formal shirt",
    "business casual shirt",
    "modern office shirt",
    "polo t-shirt",
    "minimal polo shirt",
    "linen shirt",
    "soft cotton shirt",
    "modern polo t-shirt",
    "casual kurta",
    "modern short kurta",
    "minimal cotton kurta",
    "light pastel kurta",
    "light sweater",
    "casual sweatshirt",
    "minimal hoodie",
    "soft cardigan",
    "henley t-shirt",
    "minimal collar t-shirt",
    "structured casual shirt",
    "modern relaxed shirt",
    "layered casual outfit",
]
MALE_COLORS = [
    "white",
    "light grey",
    "beige",
    "pastel blue",
    "soft green",
    "cream",
    "light brown",
    "soft navy",
]

def get_male_clothing():
    return f"{random.choice(MALE_COLORS)} {random.choice(MALE_CLOTHING)}"
FEMALE_CLOTHING = [
    "plain pastel t-shirt",
    "soft beige top",
    "light pastel kurti",
    "minimal cotton kurti",
    "casual modern blouse",
    "smart casual top",
    "simple pastel shirt",
    "neutral color top",
    "minimal modern kurti",
    "oversized t-shirt",
    "minimal solid color t-shirt",
    "relaxed fit t-shirt",
    "soft cotton top",
    "minimal graphic-free t-shirt",
    "casual office blouse",
    "formal light shirt",
    "modern office top",
    "soft pastel office shirt",
    "minimal professional blouse",
    "ribbed knit top",
    "minimal crop-length top (modest)",
    "loose fit top",
    "modern basic tee",
    "soft knit sweater",
    "contemporary kurti",
    "short modern kurti",
    "pastel straight kurti",
    "minimal ethnic top",
    "modern fusion kurti",
    "linen top",
    "soft cotton shirt",
    "modern relaxed blouse",
    "minimal neutral sweater",
    "soft cardigan",
    "light cardigan",
    "minimal hoodie",
    "casual sweatshirt",
    "soft knit cardigan",
    "button-down shirt",
    "minimal collar shirt",
    "soft pastel button shirt",
    "casual structured top",
    "modern layered top",
]
FEMALE_COLORS = [
    "white",
    "beige",
    "pastel pink",
    "light blue",
    "soft grey",
    "cream",
    "mint green",
]

def get_female_clothing():
    return f"{random.choice(FEMALE_COLORS)} {random.choice(FEMALE_CLOTHING)}"

# ── Subject builders ────────────────────────────────────────────────────────────
MALE_HAIR_STAGES = {
    "20-30": {
        "desc": "short hair 2-3 cm, dark brown-black — slight M-shaped recession beginning at temples",
        "camera": "Slightly elevated angle showing early temple recession clearly.",
        "norwood": "Stage 1-2",
    },
    "25-35": {
        "desc": "medium length hair 5-7 cm, dark brown-black — M-shaped recession clearly visible",
        "camera": "Slightly elevated top-angle showing M-recession and crown thinning.",
        "norwood": "Stage 2-3",
    },
    "30-40": {
        "desc": "short hair 2-4 cm, dark brown-black — strong M-shaped recession, crown visibly thinning",
        "camera": "Elevated top-angle — crown sparse, M-recession deep and clear.",
        "norwood": "Stage 3-4",
    },
    "35-45": {
        "desc": "short hair 1-3 cm, dark brown-black — significant crown thinning, scalp clearly visible",
        "camera": "Top-down angle clearly showing large sparse crown area.",
        "norwood": "Stage 4-5",
    },
    "40-50": {
        "desc": "very short cropped hair, dark brown-black with some grey — crown nearly bald",
        "camera": "Top-down angle showing horseshoe pattern clearly.",
        "norwood": "Stage 5-6",
    },
}

FEMALE_HAIR_STAGES = {
    "20-30": {
        "desc": "shoulder-length hair — center parting slightly wider than normal (Ludwig Grade 1)",
        "camera": "Close-up front angle showing slightly wider center parting.",
        "ludwig": "Grade 1",
    },
    "25-35": {
        "desc": "shoulder-length hair — center parting noticeably wider (Ludwig Grade 1-2)",
        "camera": "Slight top-angle showing wider parting and hairline thinning.",
        "ludwig": "Grade 1-2",
    },
    "30-40": {
        "desc": "medium length hair — center parting clearly wider than normal (Ludwig Grade 2)",
        "camera": "Elevated angle showing wide parting and sparse temples clearly.",
        "ludwig": "Grade 2",
    },
    "35-45": {
        "desc": "medium to short hair — significantly wider parting (Ludwig Grade 2-3)",
        "camera": "Top-angle showing wide parting and scalp visibility clearly.",
        "ludwig": "Grade 2-3",
    },
    "40-50": {
        "desc": "short or tied hair — diffuse thinning over entire crown (Ludwig Grade 3)",
        "camera": "Top-down angle showing diffuse thinning across entire crown.",
        "ludwig": "Grade 3",
    },
}

def build_hair_subject(gender, age_range="30-40", emotion_key="worried", topic="", phase="problem", category="hair"):
    EMOTION_DESC = {
        "worried": "Deeply worried and visibly sad — furrowed brow, heavy tired eyes with dark circles, downward gaze. Jaw slightly tense. Quiet emotional pain. NOT smiling.",
        "hopeful": "Cautiously hopeful — leaning slightly forward, soft expectant smile.",
        "confident": "Glowing, open, radiant smile — direct eye contact, relaxed jaw.",
        "natural": "Natural, authentic, relatable expression. Relaxed and genuine.",
        "insecure": "Self-conscious — avoiding direct eye contact, slight frown.",
        "overwhelmed": "Quietly overwhelmed — tired eyes, lips pressed together.",
        "discouraged": "Frustrated and discouraged — arms crossed, slight slump.",
        "exhausted": "Visibly exhausted — heavy eyelids, slumped shoulders.",
        "pain": "Tense and guarded — slight wincing around eyes.",
        "relief": "Measured relief — soft exhale, slight uplift at corners of mouth.",
        "determined": "Determined — chin slightly lifted, slight firm smile.",
        "proud": "Proud and energised — big authentic smile, open posture.",
        "serene": "Serene and rested — relaxed open face, soft genuine smile.",
    }
    emotion = EMOTION_DESC.get(emotion_key, EMOTION_DESC["worried"])
    emotion_display = EMOTION_OPTIONS.get(emotion_key, "😢 Worried & Sad")

    age_key = age_range if age_range in MALE_HAIR_STAGES else "30-40"

    if gender == "male":
        stage   = MALE_HAIR_STAGES[age_key]
        light   = random.choice(MALE_LIGHTING_MOODS)
        pose    = get_smart_pose(category, phase, MALE_POSES, topic)
        norwood = stage["norwood"]
        clothes = get_male_clothing()
        detected_bg, _ = detect_background(topic)
        final_bg = detected_bg if detected_bg else get_lighting_background(light["label"], "male_hair")
        subj = (
            f"PHOTOGRAPHY STYLE — RAW EMOTIONAL DOCUMENTARY: NOT a studio shot. Real candid moment. "
            f"South Asian Indian man, age {age_range}, wheatish brown skin, dark brown eyes, light stubble. "
            f"CRITICAL EXPRESSION: {emotion} "
            f"wearing {clothes}. "
            f"Natural skin — visible pores. "

            f"CRITICAL HAIR CONDITION ({norwood}): {stage['desc']}. MUST SHOW hair thinning and scalp clearly. {stage['camera']} "
            f"CAMERA: {stage['camera']} Handheld feel, slight grain, 85mm f/1.4. "
            f"POSE: {pose} "
            f"Fingers must be anatomically correct — five fingers, no distortion, no extra fingers. "
            f"Face must be symmetrical, sharp, and proportionally correct. "
            f"No deformation, no blur, no distortion. "
            f"LIGHTING: {light['desc']} BACKGROUND: {final_bg}. Use a very simple low-clutter plain backdrop with heavy blur. Background must not form a full room scene. No people in background. No desks, no monitors, no chairs, no shelves, no furniture, no plants, no windows, no curtains, no sofa, no table, no frames, no decor, no multiple objects. No readable office or home layout. Person only in sharp focus. "
            f"Photorealistic, natural Indian skin tone, ultra detailed 8K. "
            f"Face sharp, clear eyes, realistic proportions. "
            f"Hands fully visible and anatomically correct. "
            f"Single person only, no products."
        )
        return subj, f"Male {norwood}", light["label"], pose, phase, emotion_display
    else:
        stage  = FEMALE_HAIR_STAGES[age_key]
        light  = random.choice(FEMALE_LIGHTING_MOODS)
        pose   = get_smart_pose(category, phase, FEMALE_POSES, topic)
        ludwig = stage["ludwig"]
        clothes = get_female_clothing()
        detected_bg, _ = detect_background(topic)
        final_bg = detected_bg if detected_bg else get_lighting_background(light["label"], "female_hair")
        subj = (
            f"PHOTOGRAPHY STYLE — RAW EMOTIONAL DOCUMENTARY: NOT a studio shot. Real candid moment. "
            f"South Asian Indian woman, age {age_range}, wheatish brown skin, dark brown eyes. "
            f"CRITICAL EXPRESSION: {emotion} "
            f"wearing {clothes}. Fully clothed, modest, professional healthcare-ad appropriate styling. "
            f"Natural skin — visible pores. HAIR: natural, slight frizz. "
            f"CRITICAL HAIR CONDITION ({ludwig}): {stage['desc']}. MUST SHOW wider parting and hair thinning clearly. {stage['camera']} "
            f"CAMERA: {stage['camera']} Handheld feel, slight grain, 85mm f/1.4. "
            f"POSE: {pose} "
            f"Fingers must be anatomically correct — five fingers, no distortion. "
            f"Face must be symmetrical, sharp, and proportionally correct. "
            f"No deformation, no blur, no distortion. "
            f"LIGHTING: {light['desc']} BACKGROUND: {final_bg}. Use a very simple low-clutter plain backdrop with heavy blur. Background must not form a full room scene. No people in background. No desks, no monitors, no chairs, no shelves, no furniture, no plants, no windows, no curtains, no sofa, no table, no frames, no decor, no multiple objects. No readable office or home layout. Person only in sharp focus. "
            f"Photorealistic, natural Indian skin tone, ultra detailed 8K. "
            f"Face sharp, clear eyes, realistic proportions. "
            f"Hands fully visible and anatomically correct. "
            f"Single person only, no products."
        )
        return subj, f"Female {ludwig}", light["label"], pose, phase, emotion_display

def build_general_subject(gender, age_range="25-35", emotion_key="natural", topic="", phase="problem", category="general"):
    EMOTION_DESC = {
        "worried": "Deeply worried and visibly sad — furrowed brow, heavy tired eyes. NOT smiling.",
        "hopeful": "Cautiously hopeful — leaning slightly forward, soft expectant smile.",
        "confident": "Glowing, open, radiant smile — direct eye contact, relaxed jaw.",
        "natural": "Natural, authentic, relatable expression. Relaxed and genuine.",
        "insecure": "Self-conscious — avoiding direct eye contact, slight frown.",
        "overwhelmed": "Quietly overwhelmed — tired eyes, lips pressed together.",
        "discouraged": "Frustrated and discouraged — arms crossed, slight slump.",
        "exhausted": "Visibly exhausted — heavy eyelids, slumped shoulders.",
        "pain": "Tense and guarded — slight wincing around eyes.",
        "relief": "Measured relief — soft exhale, slight uplift at corners of mouth.",
        "determined": "Determined — chin slightly lifted, slight firm smile.",
        "proud": "Proud and energised — big authentic smile, open posture.",
        "serene": "Serene and rested — relaxed open face, soft genuine smile.",
    }
    emotion = EMOTION_DESC.get(emotion_key, EMOTION_DESC["natural"])
    emotion_display = EMOTION_OPTIONS.get(emotion_key, "😊 Natural")

    if gender == "male":
        pose    = get_smart_pose(category, phase, GENERAL_MALE_POSES, topic)
        light   = random.choice(GENERAL_LIGHTING)
        lbl     = light["label"]
        ldesc   = light["desc"]
        clothes = get_male_clothing()
        detected_bg, _ = detect_background(topic)
        final_bg = detected_bg if detected_bg else get_lighting_background(lbl, "general")
        subj    = (f"PHOTOGRAPHY STYLE — CANDID LIFESTYLE: NOT a studio shot. Real authentic candid moment. "
                   f"South Asian Indian man, age {age_range}, wheatish brown skin, dark brown eyes. "
                   f"CRITICAL EXPRESSION: {emotion} "
                   f"wearing {clothes}. Fully clothed, modest, professional healthcare-ad appropriate styling. "
                   f"Natural skin — visible pores. "
                   f"CAMERA: 85mm f/1.4, handheld feel, slight grain. "
                   f"POSE: {pose} "
                   f"Fingers must be anatomically correct — five fingers, no distortion. "
                   f"Face must be symmetrical, sharp, and proportionally correct. "
                   f"LIGHTING: {ldesc} "
                   f"BACKGROUND: {final_bg}. Use a very simple low-clutter plain backdrop with heavy blur. Background must not form a full room scene. No people in background. No desks, no monitors, no chairs, no shelves, no furniture, no plants, no windows, no curtains, no sofa, no table, no frames, no decor, no multiple objects. No readable office or home layout. Person only in sharp focus. "
                   f"Photorealistic, natural Indian skin tone, ultra detailed 8K. "
                   f"Face sharp, clear eyes, realistic proportions. "
                   f"Hands fully visible and anatomically correct. "
                   f"Single person only, no products.")
        return subj, "Standard", lbl, pose, phase, emotion_display
    else:
        pose    = get_smart_pose(category, phase, GENERAL_FEMALE_POSES, topic)
        light   = random.choice(GENERAL_LIGHTING)
        lbl     = light["label"]
        ldesc   = light["desc"]
        clothes = get_female_clothing()
        detected_bg, _ = detect_background(topic)
        final_bg = detected_bg if detected_bg else get_lighting_background(lbl, "general")
        subj    = (f"PHOTOGRAPHY STYLE — CANDID LIFESTYLE: NOT a studio shot. Real authentic candid moment. "
                   f"South Asian Indian woman, age {age_range}, wheatish brown skin, dark brown eyes. "
                   f"CRITICAL EXPRESSION: {emotion} "
                   f"wearing {clothes}. Fully clothed, modest, professional healthcare-ad appropriate styling. "
                   f"Natural skin — visible pores. "
                   f"CAMERA: 85mm f/1.4, handheld feel, slight grain. "
                   f"POSE: {pose} "
                   f"Fingers must be anatomically correct — five fingers, no distortion. "
                   f"Face must be symmetrical, sharp, and proportionally correct. "
                   f"LIGHTING: {ldesc} "
                   f"BACKGROUND: {final_bg}. Use a very simple low-clutter plain backdrop with heavy blur. Background must not form a full room scene. No people in background. No desks, no monitors, no chairs, no shelves, no furniture, no plants, no windows, no curtains, no sofa, no table, no frames, no decor, no multiple objects. No readable office or home layout. Person only in sharp focus. "
                   f"Photorealistic, natural Indian skin tone, ultra detailed 8K. "
                   f"Face sharp, clear eyes, realistic proportions. "
                   f"Hands fully visible and anatomically correct. "
                   f"Single person only, no products.")
        return subj, "Standard", lbl, pose, phase, emotion_display

# ── Skeleton preview ────────────────────────────────────────────────────────────
def generate_skeleton_preview(layout_id, title, subtext, cta, fmt_key="square"):
    W, H = (540, 540) if fmt_key == "square" else (304, 540)
    img  = Image.new("RGB", (W, H), color=(245,245,247))
    draw = ImageDraw.Draw(img)
    BORDER=(180,180,195); PBG=(200,212,235); DARK=(25,25,40)
    GRAY=(110,110,125); GREEN=(34,139,60); ACC=(99,102,241)
    WHITE=(255,255,255); LOGOBG=(200,200,215)

    def rr(xy,r=10,fill=None,outline=None,w=2):
        draw.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=w)
    def wrap(text,mc=20):
        words=text.split(); lines,line=[],""
        for word in words:
            if len(line)+len(word)+1<=mc: line=(line+" "+word).strip()
            else:
                if line: lines.append(line)
                line=word
        if line: lines.append(line)
        return lines
    def dh(x,y,text,mc=18,color=DARK,bg=None):
        lines=wrap(text.upper(),mc); lh=25
        if bg: rr([x-4,y-4,x+min(W-x-4,200),y+len(lines)*lh+4],r=6,fill=bg,outline=BORDER,w=1)
        for ln in lines: draw.text((x,y),ln,fill=color); y+=lh
        return y
    def ds(x,y,text,mc=24):
        for ln in wrap(text,mc): draw.text((x,y),ln,fill=GRAY); y+=18
        return y
    def dc(cx,cy,text,color=GREEN,width=180):
        bw=min(len(text)*10+30,width); bx=cx-bw//2
        rr([bx,cy,bx+bw,cy+34],r=17,fill=color)
        draw.text((bx+10,cy+9),text,fill=WHITE)
    def logo():
        rr([W-90,8,W-8,36],r=6,fill=LOGOBG)
        draw.text((W-82,14),"BATRA'S",fill=(70,70,90))
    def dp(box):
        rr(box,r=10,fill=PBG,outline=BORDER,w=1)
        cx=(box[0]+box[2])//2; bw=box[2]-box[0]; bh=box[3]-box[1]
        hr=max(12,bw//8); hy=box[1]+int(bh*0.08)
        SKIN=(210,190,170); HAIR=(80,60,50); LIMB=(160,170,190); BODY=(200,210,225)
        draw.ellipse([cx-hr,hy,cx+hr,hy+hr*2],fill=SKIN,outline=BORDER,width=1)
        draw.arc([cx-hr,hy-2,cx+hr,hy+hr],start=180,end=0,fill=HAIR,width=3)
        nb=hy+hr*2; nt=nb+max(4,bh//20)
        draw.line([cx,nb,cx,nt],fill=SKIN,width=3)
        sw=max(20,bw//4); sl=cx-sw; sr=cx+sw; sy=nt
        tb=sy+max(30,int(bh*0.30))
        draw.rounded_rectangle([cx-sw+4,sy,cx+sw-4,tb],radius=4,fill=BODY,outline=BORDER,width=1)
        al=max(18,int(bh*0.18))
        draw.line([sr,sy,sr+10,sy+al],fill=LIMB,width=3)
        draw.line([sl,sy,sl-10,sy+al],fill=LIMB,width=3)
        ll=max(20,int(bh*0.22)); lb=min(tb+ll,box[3]-20)
        draw.line([cx-10,tb,cx-14,lb],fill=LIMB,width=3)
        draw.line([cx+10,tb,cx+14,lb],fill=LIMB,width=3)

    rr([3,3,W-3,H-3],r=14,outline=BORDER,w=2); logo()
    psq=[int(W*0.5),int(H*0.13),W-8,int(H*0.85)]

    lid=layout_id
    if   lid=="L01": dp(psq);y=dh(14,int(H*0.13),title,bg=WHITE);ds(14,y+4,subtext);dc(W//2,H-60,cta)
    elif lid=="L02": dp([int(W*0.2),int(H*0.33),int(W*0.8),int(H*0.85)]);y=dh(W//2-90,int(H*0.1),title,bg=WHITE);ds(W//2-90,y+4,subtext,mc=26);dc(W-90,H-60,cta,width=140)
    elif lid=="L09": dp([8,int(H*0.1),int(W*0.5),int(H*0.85)]);dh(int(W*0.52),int(H*0.22),title,mc=12,bg=WHITE);rr([0,H-58,W,H],r=0,fill=GREEN);draw.text((W//2-25,H-44),cta,fill=WHITE)
    elif lid=="L21": rr([0,0,int(W*0.42),H],r=0,fill=(225,230,245));y=dh(10,int(H*0.15),title,mc=12);ds(10,y+4,subtext,mc=16);dp([int(W*0.44),int(H*0.07),W-6,int(H*0.9)]);rr([10,H-56,int(W*0.38),H-16],r=14,fill=GREEN);draw.text((16,H-46),cta,fill=WHITE)
    elif lid=="L03": dp([int(W*0.15),int(H*0.05),int(W*0.85),int(H*0.67)]);rr([W-160,14,W-10,48],r=14,fill=GREEN);draw.text((W-148,22),cta[:14],fill=WHITE);dh(14,int(H*0.7),title,bg=WHITE)
    elif lid=="L04": y=dh(W//2-100,int(H*0.07),title,mc=22,bg=WHITE);dp([int(W*0.2),int(H*0.3),int(W*0.8),int(H*0.85)]);rr([14,H-56,180,H-16],r=14,fill=GREEN);draw.text((20,H-46),cta[:14],fill=WHITE)
    elif lid=="L05": rr([int(W*0.44),8,W-8,int(H*0.17)],r=8,fill=ACC);draw.text((int(W*0.46),int(H*0.05)),title[:18].upper(),fill=WHITE);dp([8,int(H*0.18),int(W*0.55),int(H*0.85)]);dc(int(W*0.7),H-60,cta)
    elif lid=="L06": rr([30,14,W-30,int(H*0.15)],r=18,fill=(255,200,50));draw.text((46,int(H*0.07)),title[:22].upper(),fill=DARK);dp([int(W*0.2),int(H*0.17),int(W*0.8),int(H*0.8)]);rr([40,H-58,W-40,H-14],r=10,fill=GREEN);draw.text((W//2-25,H-48),cta[:14],fill=WHITE)
    elif lid=="L07": rr([0,0,int(W*0.15),H],r=0,fill=(225,230,245));[draw.text((8,int(H*0.12)+i*36),ch.upper(),fill=DARK) for i,ch in enumerate(title[:8])];dp([int(W*0.17),int(H*0.08),W-8,int(H*0.85)]);dc(W-80,H-60,cta,width=130)
    elif lid=="L08": dp([int(W*0.12),int(H*0.05),int(W*0.88),int(H*0.7)]);rr([W-160,12,W-10,46],r=14,fill=(30,100,200));draw.text((W-148,20),cta[:14],fill=WHITE);rr([8,int(H*0.68),int(W*0.6),H-8],r=8,fill=WHITE,outline=BORDER,w=1);dh(14,int(H*0.7),title,mc=20)
    elif lid=="L10": draw.ellipse([10,10,120,120],fill=ACC);[draw.text((14,18+i*18),ln,fill=WHITE) for i,ln in enumerate(wrap(title.upper(),7)[:3])];dp([int(W*0.38),int(H*0.1),W-8,int(H*0.85)]);dc(W//2,H-60,cta)
    elif lid=="L11": dp([int(W*0.55),int(H*0.13),W-8,int(H*0.85)]);y=dh(int(W*0.06),int(H*0.13),title,mc=14,bg=WHITE);y=ds(int(W*0.06),y+4,subtext);draw.line([int(W*0.06),y+8,int(W*0.5),y+8],fill=ACC,width=2);draw.text((int(W*0.06),y+14),cta[:20],fill=GREEN)
    elif lid=="L14": dp([int(W*0.4),int(H*0.07),W-8,int(H*0.87)]);rr([10,int(H*0.3),int(W*0.46),int(H*0.58)],r=8,fill=WHITE,outline=BORDER,w=1);y=dh(16,int(H*0.32),title,mc=14);ds(16,y+4,subtext,mc=20);dc(int(W*0.1),H-60,cta,width=160)
    elif lid=="L16": rr([0,int(H*0.03),W,int(H*0.17)],r=0,fill=ACC);draw.text((14,int(H*0.07)),title[:26].upper(),fill=WHITE);dp([int(W*0.15),int(H*0.19),int(W*0.85),int(H*0.83)]);dc(W-90,H-60,cta,width=140)
    elif lid=="L18": rr([20,int(H*0.04),W-20,int(H*0.17)],r=8,fill=(255,200,50));draw.text((34,int(H*0.08)),title[:24].upper(),fill=DARK);dp([int(W*0.15),int(H*0.19),int(W*0.85),int(H*0.83)]);dc(W//2,H-60,cta,color=(30,100,200))
    elif lid=="L22": rr([0,0,W,H//2],r=0,fill=(240,243,252));y=dh(W//2-100,int(H*0.07),title,mc=20);ds(W//2-100,y+4,subtext);draw.ellipse([W//2-60,H//2-8,W//2+60,H//2+120],fill=PBG,outline=BORDER,width=1);dc(W//2,H//2-18,cta)
    elif lid=="L23": y=dh(14,int(H*0.04),title,bg=WHITE);draw.line([14,y+6,W-14,y+6],fill=ACC,width=2);ds(14,y+12,subtext);dp([int(W*0.1),y+int(H*0.12),W-int(W*0.1),H-58]);rr([0,H-54,W,H],r=0,fill=GREEN);draw.text((W//2-25,H-40),cta[:14],fill=WHITE)
    elif lid=="L24": rr([0,0,W,int(H*0.16)],r=18,fill=ACC);draw.text((14,int(H*0.05)),title[:26].upper(),fill=WHITE);dp([int(W*0.15),int(H*0.18),int(W*0.85),int(H*0.83)]);dc(W//2,H-60,cta)
    elif lid=="L26": dp([int(W*0.1),int(H*0.13),W-int(W*0.1),int(H*0.85)]);rr([int(W*0.07),int(H*0.07),W-int(W*0.07),int(H*0.26)],r=10,fill=WHITE,outline=BORDER,w=1);draw.text((int(W*0.1),int(H*0.1)),title[:24].upper(),fill=DARK);rr([0,H-54,W,H],r=0,fill=DARK);draw.text((W//2-25,H-40),cta[:14],fill=WHITE)
    elif lid=="L27": words=title.split();draw.text((14,int(H*0.13)),words[0].upper() if words else "",fill=ACC);draw.text((14,int(H*0.2))," ".join(words[1:])[:18].upper(),fill=DARK);dp(psq);dc(14,H-60,cta,width=160)
    elif lid=="L29": dp([8,int(H*0.03),W-8,int(H*0.58)]);rr([0,int(H*0.59),W,H],r=0,fill=WHITE);y=dh(14,int(H*0.62),title,mc=24);dc(W//2,H-60,cta)
    elif lid=="L30": rr([0,0,10,H],r=0,fill=ACC);y=dh(18,int(H*0.13),title);ds(18,y+4,subtext,mc=18);dp([int(W*0.42),int(H*0.09),W-8,int(H*0.85)]);dc(int(W*0.6),H-60,cta)
    else:            dp(psq);y=dh(14,int(H*0.13),title,bg=WHITE);ds(14,y+4,subtext);dc(W//2,H-60,cta)

    draw.text((10,H-16),f"Layout {lid} · {'1:1' if fmt_key=='square' else '9:16'}",fill=(160,160,175))
    buf=BytesIO(); img.save(buf,format="PNG"); buf.seek(0)
    return buf.getvalue()

# ── Groq ────────────────────────────────────────────────────────────────────────
def call_groq(api_key, topic, detected_settings=None):
    gender_constraint = ""
    emotion_instruction = ""
    age_constraint = ""

    if detected_settings:
        gender = detected_settings.get("gender", "")
        emotion_key = detected_settings.get("emotion_key", "")
        age_range = detected_settings.get("age_range", "")

        if gender:
            gender_constraint = f"Gender MUST be {gender}. "
        if emotion_key:
            emotion_descriptions = {
                "worried": "deeply worried and visibly sad - furrowed brow, heavy tired eyes",
                "hopeful": "cautiously hopeful - soft expectant smile, leaning forward",
                "confident": "glowing with radiant confidence - open smile, relaxed jaw, direct eye contact",
                "natural": "natural and relatable expression - relaxed and genuine",
                "insecure": "self-conscious and insecure - avoiding eye contact, slight frown",
                "overwhelmed": "quietly overwhelmed - tired eyes, lips pressed together",
                "discouraged": "frustrated and discouraged - arms crossed, slight slump",
                "exhausted": "visibly exhausted - heavy eyelids, slumped shoulders",
                "pain": "tense and guarded - slight wincing around eyes",
                "relief": "measured relief - soft exhale, slight smile uplift",
                "determined": "determined - chin lifted, firm smile",
                "proud": "proud and energised - big authentic smile, open posture",
                "serene": "serene and rested - relaxed open face, soft smile",
            }
            emotion_desc = emotion_descriptions.get(emotion_key, "natural")
            emotion_instruction = f"CRITICAL: Person MUST show {emotion_desc} expression. Facial expression is key."
        if age_range:
            age_constraint = f"Person age {age_range}. "

    detected_bg, _ = detect_background(topic)
    if detected_bg:
        bg_instruction = (
            f"BACKGROUND: Use this specific setting - {detected_bg}. "
            "Heavily blurred bokeh, person in sharp focus. "
            "Keep background extremely simple, low-clutter, and non-distracting."
        )
    else:
        bg_instruction = (
            "BACKGROUND: Real environment - bathroom, bedroom, home, clinic. "
            "Softly blurred to heavily blurred bokeh, person in sharp focus. "
            "Keep background extremely simple, low-clutter, and secondary."
        )

    system_prompt = (
        "You are a senior creative director for Meta ad campaigns for Dr Batra's healthcare brand. "
        "Given a topic, generate a JSON with EXACTLY these keys: "
        "title (punchy emotional headline, max 8 words), "
        "subtext (supporting line max 15 words, builds trust), "
        "cta (call-to-action max 4 words), "
        "visual_style (Flux image prompt - detailed expression, pose, clothing, emotion, lighting, background. No text/headline/CTA.), "
        "layout (leave blank, will be assigned), "
        f"gender ({gender_constraint}or random if not specified). "
        "LANGUAGE: Simple conversational Indian English. "
        "SCENE RULE: ONE scene, ONE person. No collages, no products. "
        f"{bg_instruction} "
        "Background must stay secondary to the subject. "
        "If any background exists, it must be minimal, heavily blurred, and not compete with the face. "
        "Do not generate a full office, home, or room scene. "
        "Avoid background people, desks, monitors, chairs, shelves, furniture clusters, multiple plants, windows, or busy interiors. "
        "Return ONLY valid JSON. No markdown."
    )

    user_message = f'Topic: "{topic}"'
    if emotion_instruction or age_constraint:
        user_message += f"\n\n{emotion_instruction} {age_constraint}"

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 700,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        },
        timeout=30,
    )
    res.raise_for_status()
    raw = res.json()["choices"][0]["message"]["content"].strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise Exception("Groq did not return valid JSON")
    data = json.loads(match.group())

    chosen = random.choice(LAYOUTS)
    data["layout"] = chosen["groq"]
    data["layout_id"] = chosen["id"]

    if detected_settings and detected_settings.get("emotion_key"):
        emotion_key = detected_settings.get("emotion_key")
        emotion_descriptions = {
            "worried": "deeply worried and visibly sad - furrowed brow, heavy tired eyes",
            "hopeful": "cautiously hopeful - soft expectant smile, leaning forward",
            "confident": "glowing with radiant confidence - open smile, relaxed jaw, direct eye contact",
            "natural": "natural and relatable expression - relaxed and genuine",
            "insecure": "self-conscious and insecure - avoiding eye contact, slight frown",
            "overwhelmed": "quietly overwhelmed - tired eyes, lips pressed together",
            "discouraged": "frustrated and discouraged - arms crossed, slight slump",
            "exhausted": "visibly exhausted - heavy eyelids, slumped shoulders",
            "pain": "tense and guarded - slight wincing around eyes",
            "relief": "measured relief - soft exhale, slight smile uplift",
            "determined": "determined - chin lifted, firm smile",
            "proud": "proud and energised - big authentic smile, open posture",
            "serene": "serene and rested - relaxed open face, soft smile",
        }
        emotion_desc = emotion_descriptions.get(emotion_key, "natural")
        if "visual_style" in data:
            data["visual_style"] += f". Expression: {emotion_desc}"

    return data
def call_groq_chat(api_key, messages):
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "max_tokens": 600, "messages": messages},
        timeout=30,
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()

# ── Image generation ────────────────────────────────────────────────────────────
def generate_flux(api_key, prompt, width, height):
    os.environ["FAL_KEY"] = api_key
    result = fal_client.subscribe(
        "fal-ai/nano-banana-2",
        arguments={"prompt":prompt,"image_size":{"width":width,"height":height},
                   "num_images":1,"enable_safety_checker":True,"output_format":"jpeg"},
        with_logs=False,
    )
    images = result.get("images",[])
    if not images: raise Exception("No image returned from fal.ai")
    return images[0]["url"]

def generate_story_from_feed(api_key, feed_url, title, subtext, cta):
    os.environ["FAL_KEY"] = api_key
    edit_prompt = (
        f"Recompose this Instagram feed ad for vertical 1080x1920 story format. "
        f"KEEP: same person, face, expression, clothing, background, headline '{title}', "
        f"subtext '{subtext}', CTA '{cta}'. "
        f"CHANGE ONLY: canvas to 9:16. Person fully visible, not cropped. Fill entire frame."
    )
    result = fal_client.subscribe(
        "fal-ai/nano-banana-2/edit",
        arguments={"prompt":edit_prompt,"image_urls":[feed_url]},
        with_logs=False,
    )
    images = result.get("images",[])
    if not images: raise Exception("No image returned from fal.ai/edit")
    return images[0]["url"]

def stamp_logo(img):
    try:
        if not os.path.exists(LOGO_PATH): return img
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo = logo.resize((140,70), Image.LANCZOS)
        if img.mode != "RGBA": img = img.convert("RGBA")
        img.paste(logo, (img.width-logo.width-20, 20), logo)
    except Exception: pass
    return img

def generate_and_stamp(prompt, width, height):
    url = generate_flux(st.session_state.fal_key, prompt, width, height)
    res = requests.get(url, timeout=30)
    img = Image.open(BytesIO(res.content)).resize((width,height), Image.LANCZOS)
    img = stamp_logo(img).convert("RGB")
    buf = BytesIO(); img.save(buf,format="JPEG",quality=95); buf.seek(0)
    return url, buf.getvalue()

def url_to_bytes(url, width, height):
    res = requests.get(url, timeout=30)
    img = Image.open(BytesIO(res.content)).resize((width,height), Image.LANCZOS)
    img = stamp_logo(img).convert("RGB")
    buf = BytesIO(); img.save(buf,format="JPEG",quality=95); buf.seek(0)
    return buf.getvalue()

def get_layout_id(layout_text):
    for l in LAYOUTS:
        if l["groq"] == layout_text: return l["id"]
    return "L01"

def build_base_prompt(style, title, subtext, cta, font, layout,
                      hair_gender, is_hair, age_range, emotion_key, topic="",
                      phase="problem", category="general"):
    if hair_gender and is_hair:
        photography, hl, ll, pl, ph, em = build_hair_subject(
            hair_gender, age_range, emotion_key, topic, phase, category
        )
    elif hair_gender:
        photography, hl, ll, pl, ph, em = build_general_subject(
            hair_gender, age_range, emotion_key, topic, phase, category
        )
    else:
        detected_bg, _ = detect_background(topic)
        bg_instruction = detected_bg if detected_bg else "real environment - bathroom, bedroom, home, clinic. Softly blurred."
        photography = (
            f"{style}. Real Indian person, photorealistic, candid feel. {CLOTHING_RULE} "
            f"BACKGROUND: {bg_instruction}. Use a very simple low-clutter plain backdrop with heavy blur. Background must not form a full room scene. No people in background. No desks, no monitors, no chairs, no shelves, no furniture, no plants, no windows, no curtains, no sofa, no table, no frames, no decor, no multiple objects. No readable office or home layout. Person only in sharp focus."
        )
        hl=ll=pl=ph=em=None

    st.session_state.hair_label     = hl
    st.session_state.lighting_label = ll
    st.session_state.pose_label     = pl
    st.session_state.ad_phase       = ph
    st.session_state.emotion_emoji  = em

    return (
        f"PHOTOGRAPHY: {photography} "
        f"Professional social media advertisement graphic design. "
        f"LAYOUT: {layout}. TYPOGRAPHY: All text in {font} font. "
        f"HEADLINE: '{title}' — large bold prominent. "
        f"SUBTEXT: '{subtext}' — medium size below headline. "
        f"CTA BUTTON: Solid pill-shaped vivid green, '{cta}' in white bold centered. "
        f"RULES: Text NOT over face. Single person only. No products. 8K premium."
    )

# ── Vertical step indicator ─────────────────────────────────────────────────────
def vstep_dot_class(step_num, current):
    if current > step_num:  return "vstep-dot vstep-dot-done"
    if current == step_num: return "vstep-dot vstep-dot-active"
    return "vstep-dot vstep-dot-idle"

def vstep_line_class(step_num, current):
    if current > step_num:  return "vstep-line vstep-line-done"
    if current == step_num: return "vstep-line vstep-line-active"
    return "vstep-line vstep-line-idle"

def vstep_label_class(step_num, current):
    return "vstep-label" if current >= step_num else "vstep-label vstep-label-idle"

# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN GATE
# ═══════════════════════════════════════════════════════════════════════════════

authenticator.login(location="main")

if st.session_state.get("authentication_status") is False:
    st.error("❌ Incorrect username or password.")
    st.stop()
elif st.session_state.get("authentication_status") is None:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 10px;">
      <h2 style="color:#1a1a1a;">✨ Meta Creative Generator</h2>
      <p style="color:#64748b;">Dr Batra's · Please login to continue</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Logged in — show logout in sidebar ──────────────────────────────────────
with st.sidebar:
    st.markdown(f"👤 **{st.session_state.get('name', '')}**")
    authenticator.logout("Logout", location="sidebar")
    st.divider()

if not st.session_state.get("login_logged"):
    log_user_activity("login")
    st.session_state.login_logged = True

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN UI
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center;margin-bottom:16px;">
  <h1 style="font-size:28px;margin-bottom:4px;color:#1a1a1a;">✨ Meta Creative Generator</h1>
  <p style="color:#64748b;font-size:13px;">Dr Batra's · Feed 1080×1080 + Story 1080×1920</p>
</div>
""", unsafe_allow_html=True)

cur = st.session_state.workflow_step

# Three-column layout: steps | main | right panel
step_col, main_col, right_col = st.columns([0.06, 1.8, 1.0])

# ── Narrow vertical step spine ──────────────────────────────────────────────────
with step_col:
    STEPS = ["1","2","3","4","5"]
    for i, num in enumerate(STEPS):
        step_n = i + 1
        dc_cls = vstep_dot_class(step_n, cur)
        lc_cls = vstep_line_class(step_n, cur)
        connector = f'<div class="{lc_cls}" style="min-height:80px;"></div>' if i < len(STEPS)-1 else ""
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;">
          <div class="{dc_cls}">{num}</div>
          {connector}
        </div>
        """, unsafe_allow_html=True)

# ── MAIN COLUMN ─────────────────────────────────────────────────────────────────
with main_col:

    # ── STEP 1: Topic ────────────────────────────────────────────────────────────
    lbl1_cls = vstep_label_class(1, cur)
    st.markdown(f'<div class="{lbl1_cls}">Step 1 — Topic</div>', unsafe_allow_html=True)
    with st.container():
        topic = st.text_area("",
            placeholder="e.g. PCOS hair fall treatment, Natural acne solution, Stress relief...",
            height=80, key="topic_input_area", label_visibility="collapsed")
        if topic: st.session_state.user_topic = topic

        ca, cm = st.columns(2)
        with ca:
            if st.button("🤖 Auto Detect", use_container_width=True, key="auto_detect",
                         disabled=not (topic and len(topic) > 5)):
                with st.spinner("Analysing topic..."):
                    s = auto_detect_all_settings(topic)
                    st.session_state.detected_settings  = s
                    st.session_state.detection_mode     = "auto"
                    st.session_state.settings_locked    = True
                    st.session_state.hair_gender        = s["gender"]
                    st.session_state.user_age_range     = s["age_range"]
                    st.session_state.manual_phase       = s["phase"]
                    st.session_state.manual_category    = s["category"]
                    st.session_state.manual_background  = s["background"]
                    st.session_state.manual_emotion_select = s["emotion_key"]
                    st.session_state.settings_applied   = True
                    st.rerun()
        with cm:
            if st.button("✋ Manual", use_container_width=True, key="manual_mode",
                         disabled=not (topic and len(topic) > 5)):
                st.session_state.detection_mode  = "manual"
                st.session_state.settings_locked = True
                st.session_state.needs_apply     = True
                st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── STEP 2: Settings ─────────────────────────────────────────────────────────
    lbl2_cls = vstep_label_class(2, cur)
    st.markdown(f'<div class="{lbl2_cls}">Step 2 — Settings</div>', unsafe_allow_html=True)

    if st.session_state.settings_locked:

        if st.session_state.detection_mode == "auto" and st.session_state.detected_settings:
            s = st.session_state.detected_settings
            phase_badge = {"problem":'<span class="badge badge-problem">Problem</span>',
                           "solution":'<span class="badge badge-solution">Solution</span>',
                           "results":'<span class="badge badge-results">Results</span>'}
            st.markdown(f"""
            <div class="card" style="margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="font-size:13px;font-weight:600;color:#1a1a1a;">AI Detected Settings</span>
              </div>
              <div class="sg">
                <div class="sg-cell"><div class="sg-label">Gender</div>
                  <div class="sg-val">{'Male' if s['gender']=='male' else 'Female'}</div></div>
                <div class="sg-cell"><div class="sg-label">Age range</div>
                  <div class="sg-val">{s['age_range']}</div></div>
                <div class="sg-cell"><div class="sg-label">Phase</div>
                  <div class="sg-val">{phase_badge.get(s['phase'],s['phase'])}</div></div>
                <div class="sg-cell"><div class="sg-label">Category</div>
                  <div class="sg-val">{s['category'].capitalize()}</div></div>
                <div class="sg-cell"><div class="sg-label">Background</div>
                  <div class="sg-val">{s['background'].capitalize()}</div></div>
                <div class="sg-cell"><div class="sg-label">Emotion</div>
                  <div class="sg-val">{s['emotion_name']}</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✏️ Edit Settings", key="edit_auto"):
                st.session_state.detection_mode  = "manual"
                st.session_state.settings_locked = True
                st.session_state.needs_apply     = True
                st.rerun()

        if st.session_state.detection_mode == "manual":
            with st.expander("⚙️ Manual Settings", expanded=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    gender = st.radio("Gender", ["male","female"], horizontal=True, key="man_gender",
                                      index=0 if st.session_state.hair_gender=="male" else 1)
                    age_range = st.selectbox("Age range", AGE_RANGES, key="man_age",
                                             index=AGE_RANGES.index(st.session_state.user_age_range)
                                             if st.session_state.user_age_range in AGE_RANGES else 2)
                with c2:
                    phase    = st.selectbox("Phase",    ["problem","solution","results"], key="man_phase")
                    category = st.selectbox("Category", ["hair","skin","hormonal","weight","stress","pain","general"], key="man_category")
                with c3:
                    background = st.selectbox("Background", ["bathroom","home","office","city"], key="man_bg")
                    emotion = st.selectbox("Emotion", list(EMOTION_OPTIONS.keys()),
                        format_func=lambda x: EMOTION_OPTIONS[x], key="man_emotion")

                if st.button("✅ Apply Settings", use_container_width=True, type="primary", key="apply_manual"):
                    st.session_state.hair_gender           = gender
                    st.session_state.user_age_range        = age_range
                    st.session_state.manual_phase          = phase
                    st.session_state.manual_category       = category
                    st.session_state.manual_background     = background
                    st.session_state.manual_emotion_select = emotion
                    st.session_state.settings_applied      = True
                    st.session_state.detection_mode        = "manual"

                    # Clear ALL downstream data (prompts, images, ad copy)
                    st.session_state.ad_data          = None
                    st.session_state.base_prompt      = None
                    st.session_state.edited_prompt    = None
                    st.session_state.image_square     = None
                    st.session_state.image_story      = None
                    st.session_state.skeleton_square  = None
                    st.session_state.skeleton_story   = None
                    st.session_state.feed_url         = None
                    st.session_state.ideas_generated  = False
                    st.session_state.settings_changed = True
                    st.session_state.needs_apply      = False
                    st.session_state.workflow_step    = 1
                    st.rerun()

        if st.session_state.settings_applied or \
           (st.session_state.detection_mode == "auto" and st.session_state.detected_settings):
            if st.session_state.needs_apply:
                st.warning("⚠️ You have unsaved settings — click **Apply Settings** first.")
            elif st.session_state.settings_changed:
                st.warning("⚠️ Settings changed — click **Generate Ad Ideas** to regenerate.")
            if st.button("✨ Generate Ad Ideas", use_container_width=True,
                         type="primary", key="gen_ideas",
                         disabled=st.session_state.needs_apply):
                if not st.session_state.groq_key:
                    st.error("Enter your Groq API key in the sidebar.")
                else:
                    with st.spinner("Groq is writing your ad copy..."):
                        try:
                            t = st.session_state.user_topic or topic
                            st.session_state.user_topic = t  # Store for later use

                            # Pass settings to Groq — auto uses detected, manual builds from session state
                            if st.session_state.detection_mode == "auto":
                                detected = st.session_state.detected_settings
                            else:
                                detected = {
                                    "gender":      st.session_state.hair_gender,
                                    "emotion_key": st.session_state.manual_emotion_select,
                                    "age_range":   st.session_state.user_age_range,
                                }
                            data = call_groq(st.session_state.groq_key, t, detected)
                            # Only use Groq's gender in manual mode; in auto mode keep the detected value
                            if st.session_state.detection_mode == "manual":
                                st.session_state.hair_gender = data.get("gender", st.session_state.hair_gender)
                            st.session_state.ad_data          = data
                            st.session_state.ideas_generated  = True
                            st.session_state.settings_changed = False
                            st.session_state.workflow_step   = 2
                            st.session_state.image_square    = None
                            st.session_state.image_story     = None
                            st.session_state.base_prompt     = None
                            st.session_state.edited_prompt   = None
                            log_user_activity("generate_ad_ideas", f"mode={st.session_state.detection_mode}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── STEP 3: Edit copy & prompt ───────────────────────────────────────────────
    lbl3_cls = vstep_label_class(3, cur)
    st.markdown(f'<div class="{lbl3_cls}">Step 3 — Edit copy &amp; prompt</div>', unsafe_allow_html=True)

    if st.session_state.ad_data and cur >= 2:
        data = st.session_state.ad_data

        st.markdown(f"""
        <div class="ideas-box">
          <div class="idea-row"><div class="idea-lbl">Headline</div>
            <div class="idea-txt">{data.get('title','')}</div></div>
          <div class="idea-row"><div class="idea-lbl">Subtext</div>
            <div class="idea-txt">{data.get('subtext','')}</div></div>
          <div class="idea-row"><div class="idea-lbl">CTA</div>
            <div class="idea-txt">{data.get('cta','')}</div></div>
        </div>
        """, unsafe_allow_html=True)

        edited_title   = st.text_input("Headline", value=data.get("title",""),   key="edit_title")
        edited_subtext = st.text_input("Subtext",  value=data.get("subtext",""), key="edit_subtext")
        edited_cta     = st.text_input("CTA",      value=data.get("cta",""),     key="edit_cta")

        fc1, fc2 = st.columns(2)
        with fc1:
            FONTS = {"Poppins":"Poppins","Montserrat":"Montserrat","Inter":"Inter",
                     "Roboto":"Roboto","Playfair Display":"Playfair Display"}
            font_choice = st.selectbox("Font", list(FONTS.keys()), key="font_choice")
        with fc2:
            layout_names = [f"{l['id']} — {l['name']}" for l in LAYOUTS]
            layout_choice = st.selectbox("Layout override", ["Random"] + layout_names, key="layout_choice")
        if st.button("Update Prompt", use_container_width=True, key="update_prompt_from_copy"):
            if layout_choice != "Random":
                lid_override = layout_choice.split(" — ")[0]
                chosen_l = next((l for l in LAYOUTS if l["id"] == lid_override), LAYOUTS[0])
            else:
                current_layout_id = st.session_state.get("layout_id", "L01")
                chosen_l = next((l for l in LAYOUTS if l["id"] == current_layout_id), LAYOUTS[0])

            full_prompt = build_base_prompt(
                data.get("visual_style", ""),
                edited_title, edited_subtext, edited_cta,
                FONTS[font_choice], chosen_l["groq"],
                st.session_state.hair_gender,
                is_hair_loss_topic(st.session_state.user_topic),
                st.session_state.user_age_range,
                st.session_state.manual_emotion_select,
                st.session_state.user_topic,
                st.session_state.manual_phase,
                st.session_state.manual_category,
            )
            st.session_state.base_prompt = full_prompt
            st.session_state.edited_prompt = full_prompt
            st.session_state.layout_id = chosen_l["id"]
            st.session_state.skeleton_square = generate_skeleton_preview(chosen_l["id"], edited_title, edited_subtext, edited_cta, "square")
            st.session_state.skeleton_story = generate_skeleton_preview(chosen_l["id"], edited_title, edited_subtext, edited_cta, "story")
            st.session_state.image_square = None
            st.session_state.image_story = None
            st.session_state.feed_url = None
            st.session_state.last_generation_id = None
            st.session_state.ad_data["title"] = edited_title
            st.session_state.ad_data["subtext"] = edited_subtext
            st.session_state.ad_data["cta"] = edited_cta
            st.session_state.workflow_step = 3
            log_user_activity("update_prompt", "copy/font/layout updated")
            st.rerun()


        _emotion_label = EMOTION_OPTIONS.get(st.session_state.manual_emotion_select, "😊 Natural")
        _emotion_text  = _emotion_label.split(" ", 1)[-1].lower()  # strip emoji
        _hair_prefix   = "hair thinning visible, " if is_hair_loss_topic(st.session_state.user_topic) else ""
        auto_prompt = (
            f"Professional social media ad. "
            f"LAYOUT: {data.get('layout', LAYOUTS[0]['groq'])}. "
            f"FONT: {FONTS[font_choice]}. "
            f"HEADLINE: '{edited_title}'. SUBTEXT: '{edited_subtext}'. CTA: '{edited_cta}'. "
            f"SUBJECT: Indian {st.session_state.hair_gender or 'person'}, "
            f"age {st.session_state.user_age_range}, "
            f"{_hair_prefix}{_emotion_text} expression, "
            f"wearing {get_male_clothing() if (st.session_state.hair_gender or '').lower() == 'male' else get_female_clothing() if (st.session_state.hair_gender or '').lower() == 'female' else random.choice([get_male_clothing(), get_female_clothing()])}, {st.session_state.manual_background} background. "
            f"Photorealistic 8K."
        )
        # Keep prompt textarea in sync with title/subtext/CTA edits until
        # the user explicitly clicks "Build Prompt" (which sets base_prompt)
        if st.session_state.base_prompt is None:
            st.session_state.edited_prompt = auto_prompt
        elif st.session_state.edited_prompt is None:
            st.session_state.edited_prompt = auto_prompt

        st.markdown("<div style='font-size:11px;color:#64748b;margin:6px 0 3px;font-weight:600;"
                    "text-transform:uppercase;letter-spacing:0.4px;'>Prompt — edit before generating</div>",
                    unsafe_allow_html=True)
        edited_prompt_val = st.text_area("", value=st.session_state.edited_prompt,
                                         height=110,
                                         label_visibility="collapsed")
        st.session_state.edited_prompt = edited_prompt_val

        pb1, pb4 = st.columns(2)
        with pb1:
            if st.button("🔨 Build prompt", use_container_width=True, key="build_prompt"):
                if layout_choice != "Random":
                    lid_override = layout_choice.split(" — ")[0]
                    chosen_l     = next((l for l in LAYOUTS if l["id"]==lid_override), LAYOUTS[0])
                else:
                    chosen_l     = random.choice(LAYOUTS)
                layout_groq = chosen_l["groq"]
                lid         = chosen_l["id"]

                full_prompt = build_base_prompt(
                    data.get("visual_style",""),
                    edited_title, edited_subtext, edited_cta,
                    FONTS[font_choice], layout_groq,
                    st.session_state.hair_gender,
                    is_hair_loss_topic(st.session_state.user_topic),
                    st.session_state.user_age_range,
                    st.session_state.manual_emotion_select,
                    st.session_state.user_topic,
                    st.session_state.manual_phase,
                    st.session_state.manual_category,
                )
                st.session_state.base_prompt   = full_prompt
                st.session_state.edited_prompt = full_prompt
                st.session_state.layout_id       = lid
                st.session_state.skeleton_square = generate_skeleton_preview(lid, edited_title, edited_subtext, edited_cta, "square")
                st.session_state.skeleton_story  = generate_skeleton_preview(lid, edited_title, edited_subtext, edited_cta, "story")
                st.session_state.image_square    = None
                st.session_state.image_story     = None
                st.session_state.feed_url        = None
                st.session_state.last_generation_id = None
                st.session_state.workflow_step   = 3
                st.session_state.ad_data["title"]   = edited_title
                st.session_state.ad_data["subtext"] = edited_subtext
                st.session_state.ad_data["cta"]     = edited_cta
                log_user_activity("build_prompt", "prompt rebuilt from current copy")
                st.rerun()

        with pb4:
            # Detect if user has manually edited the prompt
            _prompt_edited = (
                st.session_state.edited_prompt is not None and
                st.session_state.base_prompt is not None and
                st.session_state.edited_prompt.strip() != st.session_state.base_prompt.strip()
            )
            if _prompt_edited:
                st.warning("⚠️ You have manually edited the prompt. **New Style** will reset it.", icon=None)

            if st.button("🎨 New Style", use_container_width=True, key="new_style"):
                if not st.session_state.groq_key:
                    st.error("Groq key needed.")
                else:
                    with st.spinner("Generating new ideas..."):
                        try:
                            if st.session_state.detection_mode == "auto":
                                detected = st.session_state.detected_settings
                            else:
                                detected = {
                                    "gender":      st.session_state.hair_gender,
                                    "emotion_key": st.session_state.manual_emotion_select,
                                    "age_range":   st.session_state.user_age_range,
                                }
                            nd = call_groq(st.session_state.groq_key, st.session_state.user_topic, detected)
                            st.session_state.ad_data = nd
                            FONTS_MAP = {"Poppins":"Poppins","Montserrat":"Montserrat",
                                         "Inter":"Inter","Roboto":"Roboto",
                                         "Playfair Display":"Playfair Display"}
                            font_val = FONTS_MAP.get(st.session_state.get("font_choice","Poppins"), "Poppins")
                            lid      = nd.get("layout_id", "L01")
                            full_prompt = build_base_prompt(
                                nd.get("visual_style",""),
                                nd.get("title",""), nd.get("subtext",""), nd.get("cta",""),
                                font_val, nd.get("layout",""),
                                st.session_state.hair_gender,
                                is_hair_loss_topic(st.session_state.user_topic),
                                st.session_state.user_age_range,
                                st.session_state.manual_emotion_select,
                                st.session_state.user_topic,
                                st.session_state.manual_phase,
                                st.session_state.manual_category,
                            )
                            st.session_state.base_prompt     = full_prompt
                            st.session_state.edited_prompt   = full_prompt
                            st.session_state.layout_id       = lid
                            st.session_state.skeleton_square = generate_skeleton_preview(lid, nd.get("title",""), nd.get("subtext",""), nd.get("cta",""), "square")
                            st.session_state.skeleton_story  = generate_skeleton_preview(lid, nd.get("title",""), nd.get("subtext",""), nd.get("cta",""), "story")
                            st.session_state.image_square    = None
                            st.session_state.image_story     = None
                            st.session_state.feed_url        = None
                            st.session_state.last_generation_id = None
                            st.session_state.workflow_step   = 3
                            log_user_activity("new_style", "generated fresh visual style")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── STEP 4: Generate ─────────────────────────────────────────────────────────
    lbl4_cls = vstep_label_class(4, cur)
    st.markdown(f'<div class="{lbl4_cls}">Step 4 — Generate images</div>', unsafe_allow_html=True)

    if st.session_state.base_prompt and cur >= 3:

        if st.session_state.skeleton_square and st.session_state.skeleton_story:
            st.markdown("<div style='font-size:11px;font-weight:600;color:#64748b;"
                        "text-transform:uppercase;letter-spacing:0.4px;margin-bottom:6px;'>"
                        "📺 Live Preview</div>", unsafe_allow_html=True)
            lid_name = next((l["name"] for l in LAYOUTS if l["id"]==st.session_state.layout_id), "")
            st.markdown(f"<div style='font-size:11px;color:#6366f1;margin-bottom:8px;'>"
                        f"<b>{st.session_state.layout_id}</b> — {lid_name}</div>",
                        unsafe_allow_html=True)
            sk1, sk2 = st.columns(2)
            with sk1:
                st.caption("Feed 1:1 — 1080×1080")
                st.image(st.session_state.skeleton_square, width=240)
            with sk2:
                st.caption("Story 9:16 — 1080×1920")
                st.image(st.session_state.skeleton_story, width=135)
            if False:
                ph = st.session_state.ad_phase or ""
                ph_badge = (f'<span class="badge badge-{ph}">{ph.capitalize()}</span>'
                            if ph in ["problem","solution","results"] else ph)
                st.markdown(f"""
                <div class="cd" style="margin-top:10px;">
                  <div class="cd-cell"><div class="cd-lbl">Gender</div>
                    <div class="cd-val">{(st.session_state.hair_gender or "").capitalize()}</div></div>
                  <div class="cd-cell"><div class="cd-lbl">Hair stage</div>
                    <div class="cd-val">{st.session_state.hair_label}</div></div>
                  <div class="cd-cell"><div class="cd-lbl">Lighting</div>
                    <div class="cd-val">{st.session_state.lighting_label or "—"}</div></div>
                  <div class="cd-cell"><div class="cd-lbl">Emotion</div>
                    <div class="cd-val">{st.session_state.emotion_emoji or "—"}</div></div>
                  <div class="cd-cell"><div class="cd-lbl">Phase</div>
                    <div class="cd-val">{ph_badge}</div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if not st.session_state.image_square:
            if st.button("📱 Generate Feed (1080×1080)", use_container_width=True,
                         type="primary", key="gen_feed"):
                if not st.session_state.fal_key:
                    st.error("Enter your fal.ai API key in the sidebar.")
                else:
                    with st.status("Generating feed image...", expanded=True) as status:
                        try:
                            sq_prompt = f"Square 1:1 format 1080x1080. {st.session_state.edited_prompt or st.session_state.base_prompt}"
                            url, sq_bytes = generate_and_stamp(sq_prompt, 1080, 1080)
                            st.session_state.image_square = sq_bytes
                            st.session_state.feed_url     = url
                            
                            # Save prompt with serial number
                            metadata = {
                                "topic": st.session_state.user_topic,
                                "gender": st.session_state.hair_gender,
                                "age_range": st.session_state.user_age_range,
                                "phase": st.session_state.ad_phase,
                                "emotion": st.session_state.manual_emotion_select,
                                "layout": st.session_state.layout_id
                            }
                            serial, filename = save_prompt_with_serial(st.session_state.edited_prompt or st.session_state.base_prompt, metadata)
                            st.session_state.last_prompt_saved = serial
                            st.session_state.last_generation_id = f"feed_{serial}"
                            
                            add_to_history("Feed", serial)
                            
                            st.session_state.workflow_step = 4
                            status.update(label="Feed ready! Prompt saved as #" + str(serial), state="complete")
                            st.success(f"✅ Prompt saved! Serial No: {serial:04d}")
                            log_user_activity("generate_feed", f"serial={serial:04d}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            # ── Row 1: Images side by side ──
            img_col1, img_col2 = st.columns(2)
            with img_col1:
                if st.button("🔄 Regenerate 1080×1080", use_container_width=True, key="regen_feed"):
                    with st.spinner("Regenerating..."):
                        try:
                            sq_prompt = f"Square 1:1 format 1080x1080. {st.session_state.edited_prompt or st.session_state.base_prompt}"
                            url, sq_bytes = generate_and_stamp(sq_prompt, 1080, 1080)
                            st.session_state.image_square = sq_bytes
                            st.session_state.feed_url     = url
                            st.session_state.image_story  = None
                            metadata = {
                                "topic": st.session_state.user_topic,
                                "gender": st.session_state.hair_gender,
                                "age_range": st.session_state.user_age_range,
                                "phase": st.session_state.ad_phase,
                                "emotion": st.session_state.manual_emotion_select,
                                "layout": st.session_state.layout_id
                            }
                            serial, filename = save_prompt_with_serial(st.session_state.edited_prompt or st.session_state.base_prompt, metadata)
                            st.session_state.last_prompt_saved = serial
                            add_to_history("Feed (Regenerated)", serial)
                            log_user_activity("regenerate_feed", f"serial={serial:04d}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                st.caption("📱 Feed 1:1 — 1080×1080")
                st.image(st.session_state.image_square, use_container_width=True)
            with img_col2:
                if st.session_state.image_story:
                    if st.button("🔄 Regenerate 1080×1920", use_container_width=True, key="regen_story"):
                        with st.spinner("Regenerating story..."):
                            try:
                                d = st.session_state.ad_data
                                story_url = generate_story_from_feed(
                                    st.session_state.fal_key,
                                    st.session_state.feed_url,
                                    d.get("title",""), d.get("subtext",""), d.get("cta",""),
                                )
                                st.session_state.image_story = url_to_bytes(story_url, 1080, 1920)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                    st.caption("📲 Story 9:16 — 1080×1920")
                    st.image(st.session_state.image_story, width=280)
                else:
                    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                    if st.button("📲 Generate Story (1080×1920)", use_container_width=True,
                                 type="primary", key="gen_story"):
                        with st.status("Editing feed → story...", expanded=True) as status:
                            try:
                                d = st.session_state.ad_data
                                story_url = generate_story_from_feed(
                                    st.session_state.fal_key,
                                    st.session_state.feed_url,
                                    d.get("title",""), d.get("subtext",""), d.get("cta",""),
                                )
                                st.session_state.image_story   = url_to_bytes(story_url, 1080, 1920)
                                st.session_state.workflow_step = 4
                                metadata = {
                                    "topic": st.session_state.user_topic,
                                    "gender": st.session_state.hair_gender,
                                    "type": "Story 9:16",
                                    "layout": st.session_state.layout_id
                                }
                                serial, filename = save_prompt_with_serial("Story format - converted from feed", metadata)
                                add_to_history("Story", serial)
                                status.update(label="Story ready!", state="complete")
                                log_user_activity("generate_story", f"serial={serial:04d}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")


    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── STEP 5: Download ─────────────────────────────────────────────────────────
    lbl5_cls = vstep_label_class(5, cur)
    st.markdown(f'<div class="{lbl5_cls}">Step 5 — Download</div>', unsafe_allow_html=True)

    if st.session_state.image_square or st.session_state.image_story:
        d1, d2 = st.columns(2)
        with d1:
            if st.session_state.image_square:
                st.download_button("⬇ Download Feed",
                    data=st.session_state.image_square,
                    file_name=f"batra_feed_{datetime.now().strftime('%Y%m%d_%H%M')}.jpg",
                    mime="image/jpeg", use_container_width=True)
                if st.session_state.last_prompt_saved:
                    st.caption(f"📄 Prompt saved as: prompt_{st.session_state.last_prompt_saved:04d}.txt")
        with d2:
            if st.session_state.image_story:
                st.download_button("⬇ Download Story",
                    data=st.session_state.image_story,
                    file_name=f"batra_story_{datetime.now().strftime('%Y%m%d_%H%M')}.jpg",
                    mime="image/jpeg", use_container_width=True)

        # ── Feedback (after download) ─────────────────────────────────────────
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        _sizes = "1080×1080" + (" · 1080×1920" if st.session_state.image_story else "")
        st.markdown(f"<div style='font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;"
                    f"letter-spacing:0.4px;margin-bottom:6px;'>📝 Feedback · Serial #{st.session_state.last_prompt_saved or '—'} · {_sizes}</div>",
                    unsafe_allow_html=True)
        fb_col1, fb_col2, fb_col3 = st.columns([2, 1, 1])
        with fb_col1:
            feedback_text = st.text_area(
                "Feedback",
                placeholder="e.g. Emotion not showing correctly, quality needs improvement...",
                height=68, key="fb_detailed", label_visibility="collapsed"
            )
        with fb_col2:
            rating = st.selectbox(
                "Rating", ["Select...", "👍 Good", "👎 Needs Work", "⭐ Excellent"],
                key="fb_rating", label_visibility="collapsed"
            )
        with fb_col3:
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("💾 Save Feedback", use_container_width=True, type="primary", key="save_fb_btn"):
                if feedback_text.strip():
                    rating_val = rating.split()[1].lower() if rating != "Select..." else "neutral"
                    save_feedback(st.session_state.last_generation_id or "unknown", rating_val, feedback_text)
                    log_user_activity("save_feedback", f"rating={rating_val}")
                    st.success("✅ Feedback saved!")
                else:
                    st.warning("Write feedback first")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("✨ New campaign", use_container_width=True, key="new_campaign"):
            log_user_activity("new_campaign")
            for k in ["workflow_step","user_topic","detection_mode","detected_settings",
                      "settings_locked","settings_applied","ad_data","image_square",
                      "image_story","feed_url","base_prompt","edited_prompt",
                      "skeleton_square","skeleton_story","ideas_generated"]:
                st.session_state[k] = 1 if k=="workflow_step" else None
            st.rerun()

# ── RIGHT COLUMN ─────────────────────────────────────────────────────────────────
with right_col:

    # ── Fal.ai Credits Display ─────────────────────────────────────────────────
    st.markdown("""
    <div style='font-size:11px;font-weight:600;color:#64748b;
    text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;'>
    💰 Credits & Status</div>
    """, unsafe_allow_html=True)

    if st.session_state.fal_key:
        st.markdown("""
        <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;
        padding:10px 14px;margin-bottom:8px;'>
          <div style='font-size:12px;color:#64748b;margin-bottom:4px;'>
            fal.ai does not expose a credits API — check your balance directly on the dashboard.
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 View fal.ai Dashboard", "https://fal.ai/dashboard", use_container_width=True)
    else:
        st.info("⚡ Add fal.ai API key in sidebar to enable image generation")

    # ── Generation History (Last 3) ───────────────────────────────────────────
    st.markdown("""
    <div style='font-size:11px;font-weight:600;color:#64748b;
    text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;margin-top:12px;'>
    📜 Recent Generations</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.generation_history:
        for item in st.session_state.generation_history[:3]:
            st.markdown(f"""
            <div class="history-item">
              <b>#{item['id']}</b> · {item['timestamp']}<br>
              <span style="font-size:10px;color:#64748b;">{item['topic']}</span><br>
              <span style="font-size:10px;color:#22c55e;">{item['image_type']} · Prompt #{item['prompt_serial']:04d}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No generations yet. Generate your first ad!")

    # ── Character details ─────────────────────────────────────────────────────
    if st.session_state.hair_label:
        st.markdown("""
        <div style='font-size:11px;font-weight:600;color:#64748b;
        text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;margin-top:12px;'>
        👤 Character details</div>
        """, unsafe_allow_html=True)
        ph = st.session_state.ad_phase or ""
        ph_badge = (f'<span class="badge badge-{ph}">{ph.capitalize()}</span>' if ph in
                    ["problem","solution","results"] else ph)
        st.markdown(f"""
        <div class="cd">
          <div class="cd-cell"><div class="cd-lbl">Gender</div>
            <div class="cd-val">{(st.session_state.hair_gender or '').capitalize()}</div></div>
          <div class="cd-cell"><div class="cd-lbl">Hair stage</div>
            <div class="cd-val">{st.session_state.hair_label or '—'}</div></div>
          <div class="cd-cell"><div class="cd-lbl">Lighting</div>
            <div class="cd-val">{st.session_state.lighting_label or '—'}</div></div>
          <div class="cd-cell"><div class="cd-lbl">Pose</div>
            <div class="cd-val">{st.session_state.pose_label or '—'}</div></div>
          <div class="cd-cell"><div class="cd-lbl">Emotion</div>
            <div class="cd-val">{st.session_state.emotion_emoji or '—'}</div></div>
          <div class="cd-cell"><div class="cd-lbl">Phase</div>
            <div class="cd-val">{ph_badge}</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Meta Static Ad Chatbot ───────────────────────────────────────────────────
    st.markdown("""
    <div style='font-size:11px;font-weight:600;color:#64748b;
    text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;'>
    🎯 Meta Static Ad Assistant</div>
    <div style='font-size:10px;color:#94a3b8;margin-bottom:8px;'>
    Ask about your ad, tweak the prompt, get copy ideas, or check if your ad is optimised for Meta.</div>
    """, unsafe_allow_html=True)

    chat_box = st.container(height=320)
    with chat_box:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-ai'>{msg['content']}</div>", unsafe_allow_html=True)

    chat_input = st.text_input("", placeholder="e.g. What will my image look like? / Change pose to jumping / Give me 3 headline ideas",
                               key="chat_input_field", label_visibility="collapsed")
    ci1, ci2 = st.columns([4,1])
    with ci1:
        if st.button("Send", use_container_width=True, key="send_chat"):
            if chat_input and chat_input.strip():
                st.session_state.chat_messages.append({"role":"user","content":chat_input})
                if st.session_state.groq_key:
                    # ── Build full ad context ──────────────────────────────────
                    current_prompt = st.session_state.edited_prompt or st.session_state.base_prompt or ""

                    ad_copy_lines = []
                    if st.session_state.get("ad_title"):       ad_copy_lines.append(f"Headline: {st.session_state.ad_title}")
                    if st.session_state.get("ad_subtext"):     ad_copy_lines.append(f"Subtext: {st.session_state.ad_subtext}")
                    if st.session_state.get("ad_cta"):         ad_copy_lines.append(f"CTA: {st.session_state.ad_cta}")
                    if st.session_state.get("user_topic"):     ad_copy_lines.append(f"Topic: {st.session_state.user_topic}")
                    if st.session_state.get("ad_phase"):       ad_copy_lines.append(f"Ad Phase: {st.session_state.ad_phase.capitalize()}")

                    char_lines = []
                    if st.session_state.get("hair_gender"):    char_lines.append(f"Gender: {st.session_state.hair_gender.capitalize()}")
                    if st.session_state.get("hair_label"):     char_lines.append(f"Hair Stage: {st.session_state.hair_label}")
                    if st.session_state.get("emotion_emoji"):  char_lines.append(f"Emotion: {st.session_state.emotion_emoji}")
                    if st.session_state.get("lighting_label"): char_lines.append(f"Lighting: {st.session_state.lighting_label}")
                    if st.session_state.get("pose_label"):     char_lines.append(f"Pose: {st.session_state.pose_label}")

                    context_block = ""
                    if ad_copy_lines:
                        context_block += "\n\nAD COPY:\n" + "\n".join(ad_copy_lines)
                    if char_lines:
                        context_block += "\n\nCHARACTER DETAILS:\n" + "\n".join(char_lines)
                    if current_prompt:
                        context_block += f"\n\nFULL IMAGE PROMPT:\n{current_prompt}"

                    CHAT_SYS = (
                        "You are a Meta Static Ad specialist for Dr Batra's healthcare brand (hair loss, scalp, homeopathy). "
                        "You help create and optimise Facebook/Instagram static image ads (Feed 1080×1080, Story 1080×1920).\n\n"
                        "You can help with:\n"
                        "1. DESCRIBE IMAGE — If asked what image they will get, describe it vividly in plain English based on the prompt.\n"
                        "2. MODIFY PROMPT — If asked to change something (pose, emotion, background, lighting, action like jumping/sitting/applying oil), "
                        "rewrite ONLY the PHOTOGRAPHY section with that change and show the full updated prompt.\n"
                        "3. AD COPY — Suggest headlines, subtext, CTAs optimised for Meta ads. Keep headlines under 40 chars, CTAs under 20 chars.\n"
                        "4. AD STRATEGY — Advise on Problem/Solution/Results phase, audience targeting, hook strength, scroll-stop power.\n"
                        "5. HAIR EXPERTISE — Advise on how hair loss stage, emotion, and lighting work together to make the ad believable.\n\n"
                        "Rules: Be concise. No fluff. If modifying prompt — always output the COMPLETE updated prompt, not just the changed part."
                        + context_block
                    )
                    groq_msgs = [{"role":"system","content":CHAT_SYS}]
                    for m in st.session_state.chat_messages[-12:]:
                        if m["role"] in ["user","assistant"]:
                            groq_msgs.append({"role":m["role"],"content":m["content"]})
                    with st.spinner("Thinking..."):
                        try:
                            reply = call_groq_chat(st.session_state.groq_key, groq_msgs)
                        except Exception as e:
                            reply = f"Error: {e}"
                else:
                    reply = "Please save your Groq API key in the sidebar to enable the Meta Ad Assistant."
                st.session_state.chat_messages.append({"role":"assistant","content":reply})
                st.rerun()
    with ci2:
        if st.button("🗑", use_container_width=True, key="clear_chat"):
            st.session_state.chat_messages = [{"role":"assistant",
                "content":"Hi! I'm your Meta Static Ad Assistant for Dr Batra's. Ask me:\n• What image will I get?\n• Change the pose / emotion / background\n• Give me 3 headline ideas\n• Is this a good Problem-phase ad?"}]
            st.rerun()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 API Keys")
    gk = st.text_input("Groq API Key",   type="password", value=st.session_state.groq_key, key="sb_groq")

    fk_col1, fk_col2 = st.columns([3, 1])
    with fk_col1:
        fk = st.text_input("fal.ai API Key", type="password", value=st.session_state.fal_key,  key="sb_fal")
    with fk_col2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("🔄", key="sb_refresh_credits", disabled=not fk,
                     help="Refresh credits", use_container_width=True):
            st.session_state.fal_credits = check_fal_credits(fk)
            st.success("Refreshed!")
            st.rerun()

    if gk: st.session_state.groq_key = gk
    if fk and fk != st.session_state.fal_key:
        st.session_state.fal_key    = fk
        st.session_state.fal_credits = None  # Reset cache when key changes
    elif fk:
        st.session_state.fal_key = fk

    google_sheet_ready = get_google_activity_sheet() is not None
    if google_sheet_ready:
        st.success("Google Sheets tracking connected")
    else:
        st.caption("Google Sheets tracking not connected")

    st.markdown("---")
    st.markdown("### 📊 Status")
    if st.session_state.user_topic:
        st.markdown(f"**Topic:** {st.session_state.user_topic[:35]}...")
    if st.session_state.hair_gender:
        st.markdown(f"**Subject:** {'Male' if st.session_state.hair_gender=='male' else 'Female'} · {st.session_state.user_age_range}")
    if st.session_state.ad_data:
        st.markdown("✅ Ad copy ready")
    if st.session_state.image_square:
        st.markdown("✅ Feed ready")
    if st.session_state.image_story:
        st.markdown("✅ Story ready")
    if st.session_state.last_prompt_saved:
        st.markdown(f"📄 Last prompt: #{st.session_state.last_prompt_saved:04d}")

    st.markdown("---")
    st.markdown("### 🎯 Tips")
    st.markdown("""
- Auto detect works best
- Build prompt before generating
- Edit prompt textarea for fine control
- Chat is Groq-powered — ask anything
- Rate ads to help improve!
- Prompts auto-save with serial numbers
    """)

