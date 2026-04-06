"""
Meta Creative Generator
Generate BOTH 1080x1080 + 1080x1920 using SAME SEED
Fix 1: Story full body visible, not cropped
Fix 2: Clothing rule — no towel, no revealing clothing
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

load_dotenv()

st.set_page_config(page_title="Meta Creative Generator", page_icon="✦", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f5f5f7; color: #1a1a1a; }
    h1, h2, h3, h4, h5 { font-weight: 600; color: #1a1a1a; }
    .stButton > button {
        width: 100%; border-radius: 12px; font-family: 'Inter', sans-serif;
        font-weight: 600; font-size: 14px; padding: 0.6rem 1rem;
        border: none; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white;
    }
    .stTextInput > div > div > input, textarea {
        border-radius: 10px !important; font-family: 'Inter', sans-serif !important;
        background-color: #ffffff !important; color: #1a1a1a !important; border: 1px solid #d0d0d0 !important;
    }
    [data-testid="stSidebar"] { background-color: #eeeef2; }
    .chat-msg-user { background: #e8e8ff; border-radius: 12px; padding: 10px 14px; margin: 6px 0; font-size: 13px; color: #1a1a1a !important; }
    .chat-msg-ai { background: #ffffff; border-radius: 12px; padding: 10px 14px; margin: 6px 0; font-size: 13px; border: 1px solid #d0d0e0; color: #1a1a1a !important; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔑 API Keys")
    st.markdown("---")
    if "groq_key" not in st.session_state and os.getenv("GROQ_API_KEY"):
        st.session_state["groq_key"] = os.getenv("GROQ_API_KEY")
    if "fal_key" not in st.session_state and os.getenv("FAL_API_KEY"):
        st.session_state["fal_key"] = os.getenv("FAL_API_KEY")
    groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...", key="groq_key_input",
                              value=st.session_state.get("groq_key", ""))
    fal_key  = st.text_input("fal.ai API Key", type="password", placeholder="fal key...", key="fal_key_input",
                              value=st.session_state.get("fal_key", ""))
    if st.button("Save Keys"):
        if groq_key and fal_key:
            st.session_state["groq_key"] = groq_key
            st.session_state["fal_key"]  = fal_key
            st.success("Keys saved!")
        else:
            st.error("Both keys required.")

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

# ─────────────────────────────────────────────
# 30 LAYOUTS
# ─────────────────────────────────────────────
LAYOUTS = [
    {"id": "L01", "name": "Top-Left Headline + Bottom-Center CTA",
     "groq": "Headline top-left bold, subtext below headline, person center-right, CTA green pill button bottom-center"},
    {"id": "L02", "name": "Centered Headline + Bottom-Right CTA",
     "groq": "Headline centered bold at top, subtext below headline centered, person center, CTA pill button bottom-right"},
    {"id": "L03", "name": "Bottom-Left Headline + Top CTA Pill",
     "groq": "Headline bold bottom-left overlapping image, CTA pill button top-right"},
    {"id": "L04", "name": "Large Top-Center Headline + Bottom-Left CTA",
     "groq": "Headline large top-center bold, subtext below headline, person bottom-center, CTA floating bottom-left"},
    {"id": "L05", "name": "Diagonal Banner Headline + Bottom-Center CTA",
     "groq": "Headline in diagonal banner across top-right corner, person left, CTA pill button bottom-center"},
    {"id": "L06", "name": "Arc Headline Above Person + Ribbon CTA",
     "groq": "Headline curved in arc above person's head at top, CTA at bottom with colored ribbon"},
    {"id": "L07", "name": "Vertical Left Headline + Bottom-Right CTA",
     "groq": "Headline stacked vertically on left side, person right, CTA bottom-right corner"},
    {"id": "L08", "name": "Bottom-Left Headline Overlap + Top-Right CTA",
     "groq": "Headline bold bottom-left overlapping image, CTA top-right as small button"},
    {"id": "L09", "name": "Center-Right Split Headline + Full-Width CTA Bar",
     "groq": "Headline split into two lines center-right, person left, CTA as wide bar at very bottom"},
    {"id": "L10", "name": "Badge Headline Top-Left + Bottom-Center CTA",
     "groq": "Headline inside colored circle badge top-left, person center-right, CTA bottom-center"},
    {"id": "L11", "name": "Dead-Center Headline + Underline CTA",
     "groq": "Headline large dead center bold, subtext below, CTA as underline text below subtext"},
    {"id": "L12", "name": "Wave Headline Top + Rounded-Rect CTA Bottom-Right",
     "groq": "Headline following wave curve at top, person center, CTA in rounded rectangle bottom-right"},
    {"id": "L13", "name": "Small Top Headline + Big CTA Bottom",
     "groq": "Headline small at top, person center, CTA as the biggest element at bottom spanning wide"},
    {"id": "L14", "name": "Overlay Box Headline Center-Left + Arrow CTA",
     "groq": "Headline in transparent overlay box center-left, person right, CTA floating bottom with arrow"},
    {"id": "L15", "name": "Tilted Headline Top-Left + Straight CTA Bottom",
     "groq": "Headline tilted 10 degrees top-left, person center-right, CTA straight at bottom-center"},
    {"id": "L16", "name": "Full-Width Uppercase Headline + Accent Pill CTA",
     "groq": "Headline uppercase spread full width at top, person center, CTA accent colored pill bottom-right"},
    {"id": "L17", "name": "Silhouette-Wrap Headline + Bottom-Left CTA",
     "groq": "Headline text wrapped around person silhouette, CTA anchored bottom-left"},
    {"id": "L18", "name": "Ribbon Headline Center-Top + Rounded CTA Bottom",
     "groq": "Headline with colored ribbon highlight behind it at center-top, person below, CTA rounded edges bottom"},
    {"id": "L19", "name": "Straight Minimal Layout",
     "groq": "Straight horizontal minimal layout — headline top-left, subtext below, person right, CTA bottom-center"},
    {"id": "L20", "name": "Highlighted Background Text",
     "groq": "Headline integrated into background with colored highlight strip behind it, person right, CTA bottom"},
    {"id": "L21", "name": "Left Panel 40% + Person Right + CTA Below Headline",
     "groq": "Headline left-aligned on solid colored panel left 40%, person on right side, CTA button below headline on panel"},
    {"id": "L22", "name": "Top Half Text + Circular Person + CTA Between",
     "groq": "Headline centered on clean beige/white top half, person in circular frame bottom half, CTA between them"},
    {"id": "L23", "name": "Bold Top Headline + Person Fills Bottom + Strip CTA",
     "groq": "Headline bold on top with thin accent line below it, subtext under line, person fills bottom 60%, CTA as colored strip at very bottom"},
    {"id": "L24", "name": "Curved Banner Top + Vignette Person + Pill CTA",
     "groq": "Headline on colored curved banner across top, person below with soft vignette, CTA rounded pill at bottom-center"},
    {"id": "L25", "name": "Left Headline + Framed Person Right + Bottom-Left CTA",
     "groq": "Headline large left-aligned with colored underline accent, person on right in rounded rectangle frame, CTA bottom-left"},
    {"id": "L26", "name": "Frosted Glass Overlay Headline + Bold Bar CTA",
     "groq": "Headline on frosted glass overlay box top-center, person behind slightly blurred, CTA as bold bar at bottom"},
    {"id": "L27", "name": "Accent Color First Word + Arrow CTA Bottom",
     "groq": "Headline split — first word in accent color rest in dark color top-left, person right, CTA bottom with arrow icon"},
    {"id": "L28", "name": "Speech Bubble Headline + Floating Button CTA",
     "groq": "Headline inside colored speech bubble near the person, CTA as a floating button bottom-right"},
    {"id": "L29", "name": "Person Fills Top + Card Bottom Headline + CTA",
     "groq": "Person fills top 65% edge-to-edge, headline at bottom on solid white card section, CTA on card below headline"},
    {"id": "L30", "name": "Vertical Accent Strip Left + Person Right + Center CTA",
     "groq": "Headline on left with vertical colored accent strip beside it, person on right with soft shadow, CTA bottom-center"},
]

LAYOUT_OPTIONS_FOR_GROQ = "\n".join([f'- "{l["groq"]}"' for l in LAYOUTS])


# ─────────────────────────────────────────────
# SKELETON PREVIEW
# ─────────────────────────────────────────────
def generate_skeleton_preview(layout_id, title, subtext, cta, fmt_key="square", pose_label=None):
    W, H = (540, 540) if fmt_key == "square" else (304, 540)
    img  = Image.new("RGB", (W, H), color=(245, 245, 247))
    draw = ImageDraw.Draw(img)

    BORDER=(180,180,195); PERSON_BG=(200,212,235); TEXT_DARK=(25,25,40)
    TEXT_GRAY=(110,110,125); CTA_GREEN=(34,139,60); CTA_BLUE=(30,100,200)
    PANEL_BG=(225,230,245); ACCENT=(99,102,241); RIBBON=(255,200,50)
    WHITE=(255,255,255); LOGO_BG=(200,200,215)

    def rr(xy,r=10,fill=None,outline=None,w=2): draw.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=w)
    def wrap(text,max_chars=20):
        words=text.split(); lines,line=[],""
        for word in words:
            if len(line)+len(word)+1<=max_chars: line=(line+" "+word).strip()
            else:
                if line: lines.append(line)
                line=word
        if line: lines.append(line)
        return lines
    def dh(x,y,text,mc=18,color=TEXT_DARK,bg=None):
        lines=wrap(text.upper(),mc); lh=25
        if bg: rr([x-4,y-4,x+min(W-x-4,200),y+len(lines)*lh+4],r=6,fill=bg,outline=BORDER,w=1)
        for ln in lines: draw.text((x,y),ln,fill=color); y+=lh
        return y
    def ds(x,y,text,mc=24):
        for ln in wrap(text,mc): draw.text((x,y),ln,fill=TEXT_GRAY); y+=18
        return y
    def dc(cx,cy,text,color=CTA_GREEN,width=180):
        bw=min(len(text)*10+30,width); bx=cx-bw//2
        rr([bx,cy,bx+bw,cy+34],r=17,fill=color); draw.text((bx+10,cy+9),text,fill=WHITE)
    def dcl(x,y,text,color=CTA_GREEN):
        bw=min(len(text)*10+30,160); rr([x,y,x+bw,y+34],r=17,fill=color); draw.text((x+10,y+9),text,fill=WHITE)
    def dp(box):
        rr(box,r=10,fill=PERSON_BG,outline=BORDER,w=1)
        cx=(box[0]+box[2])//2
        bw=box[2]-box[0]; bh=box[3]-box[1]
        # scale factors
        hr=max(12,bw//8)  # head radius
        head_y=box[1]+int(bh*0.08)
        head_cx=cx; head_cy=head_y+hr
        # head
        SKIN=(210,190,170); HAIR_C=(80,60,50); LIMB=(160,170,190); BODY_C=(200,210,225)
        draw.ellipse([head_cx-hr,head_y,head_cx+hr,head_y+hr*2],fill=SKIN,outline=BORDER,width=1)
        # hair on top of head
        draw.arc([head_cx-hr,head_y-2,head_cx+hr,head_y+hr],start=180,end=0,fill=HAIR_C,width=3)
        # neck
        neck_top=head_y+hr*2; neck_bot=neck_top+max(4,bh//20)
        draw.line([head_cx,neck_top,head_cx,neck_bot],fill=SKIN,width=3)
        # shoulder
        sh_y=neck_bot; sh_w=max(20,bw//4)
        shoulder_l=head_cx-sh_w; shoulder_r=head_cx+sh_w
        draw.line([shoulder_l,sh_y,shoulder_r,sh_y],fill=LIMB,width=3)
        # torso
        torso_bot=sh_y+max(30,int(bh*0.30))
        draw.rounded_rectangle([head_cx-sh_w+4,sh_y,head_cx+sh_w-4,torso_bot],radius=4,fill=BODY_C,outline=BORDER,width=1)
        # waist
        waist_y=torso_bot
        # legs
        leg_len=max(20,int(bh*0.22))
        leg_bot=min(waist_y+leg_len,box[3]-20)
        draw.line([head_cx-10,waist_y,head_cx-14,leg_bot],fill=LIMB,width=3)
        draw.line([head_cx+10,waist_y,head_cx+14,leg_bot],fill=LIMB,width=3)
        # arms based on pose
        arm_len=max(18,int(bh*0.18))
        elbow_l=shoulder_l; elbow_r=shoulder_r
        hand_c=(200,175,155)  # hand color
        prop_c=(120,120,140)  # prop color (comb/phone/pillow)
        p=pose_label or ""
        if p in ["Touching Crown","Touching Parting"]:
            # right arm up to head
            draw.line([shoulder_r,sh_y,shoulder_r+6,sh_y-arm_len//2],fill=LIMB,width=3)
            draw.line([shoulder_r+6,sh_y-arm_len//2,head_cx+hr//2,head_y+4],fill=LIMB,width=3)
            draw.ellipse([head_cx+hr//2-3,head_y,head_cx+hr//2+5,head_y+8],fill=hand_c)
            # left arm down
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p=="Running Fingers":
            # right arm up, fingers spread on top
            draw.line([shoulder_r,sh_y,shoulder_r+4,sh_y-arm_len//2],fill=LIMB,width=3)
            draw.line([shoulder_r+4,sh_y-arm_len//2,head_cx,head_y+2],fill=LIMB,width=3)
            for fx in [-4,0,4]: draw.line([head_cx+fx,head_y+2,head_cx+fx,head_y-4],fill=hand_c,width=2)
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p in ["Checking Hairline","Checking Mirror"]:
            # both arms up to forehead
            draw.line([shoulder_r,sh_y,shoulder_r+6,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_r+6,sh_y-arm_len//3,head_cx+hr-2,head_y+hr],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-6,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_l-6,sh_y-arm_len//3,head_cx-hr+2,head_y+hr],fill=LIMB,width=3)
            draw.ellipse([head_cx+hr-5,head_y+hr-3,head_cx+hr+3,head_y+hr+5],fill=hand_c)
            draw.ellipse([head_cx-hr-3,head_y+hr-3,head_cx-hr+5,head_y+hr+5],fill=hand_c)
        elif p=="Frustrated with Comb":
            # right arm up holding comb near head
            draw.line([shoulder_r,sh_y,shoulder_r+8,sh_y-arm_len//2],fill=LIMB,width=3)
            draw.line([shoulder_r+8,sh_y-arm_len//2,head_cx+hr+6,head_y+hr],fill=LIMB,width=3)
            comb_x=head_cx+hr+4; comb_y=head_y+hr-6
            draw.rectangle([comb_x,comb_y,comb_x+10,comb_y+16],fill=prop_c,outline=BORDER,width=1)
            for ty in range(comb_y,comb_y+14,3): draw.line([comb_x+10,ty,comb_x+14,ty],fill=prop_c,width=1)
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p=="Head Down Stress":
            # head tilted, right hand on neck
            draw.line([shoulder_r,sh_y,shoulder_r-2,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_r-2,sh_y-arm_len//3,head_cx+4,neck_top],fill=LIMB,width=3)
            draw.ellipse([head_cx+1,neck_top-3,head_cx+9,neck_top+5],fill=hand_c)
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p in ["Holding Hair Strands"]:
            # right arm out, palm up with strands
            draw.line([shoulder_r,sh_y,shoulder_r+arm_len,sh_y+arm_len//2],fill=LIMB,width=3)
            hx=shoulder_r+arm_len; hy=sh_y+arm_len//2
            draw.ellipse([hx-4,hy-3,hx+6,hy+5],fill=hand_c)
            for sx in range(-3,5,2): draw.line([hx+sx,hy-3,hx+sx+1,hy-10],fill=HAIR_C,width=1)
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p=="Mirror Check":
            # both arms down on counter
            draw.line([shoulder_r,sh_y,shoulder_r+10,sh_y+arm_len],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-10,sh_y+arm_len],fill=LIMB,width=3)
            # counter
            ctr_y=sh_y+arm_len
            draw.rectangle([box[0]+8,ctr_y,box[2]-8,ctr_y+6],fill=(180,180,195),outline=BORDER,width=1)
        elif p=="Pillow Shock":
            # both arms holding pillow at lap
            pw_h=max(10,bh//12); pw_w=max(30,bw//4)
            pill_y=waist_y-pw_h//2
            draw.line([shoulder_r,sh_y,head_cx+pw_w//2,pill_y],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,head_cx-pw_w//2,pill_y],fill=LIMB,width=3)
            draw.rounded_rectangle([head_cx-pw_w//2,pill_y,head_cx+pw_w//2,pill_y+pw_h],radius=3,fill=(240,235,220),outline=BORDER,width=1)
            for sx in range(-pw_w//4,pw_w//4,4): draw.line([head_cx+sx,pill_y+2,head_cx+sx+1,pill_y-4],fill=HAIR_C,width=1)
        elif p=="Comparing Old Photo":
            # right arm holding phone at chest level
            draw.line([shoulder_r,sh_y,shoulder_r+arm_len//2,sh_y+arm_len//2],fill=LIMB,width=3)
            px=shoulder_r+arm_len//2; py=sh_y+arm_len//2
            draw.rectangle([px-4,py-8,px+8,py+8],fill=(60,60,80),outline=BORDER,width=1)
            draw.rectangle([px-2,py-6,px+6,py+4],fill=(180,210,240))
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p=="Staring at Drain":
            # crouching pose — shorter torso, arms on knees
            draw.line([shoulder_r,sh_y,shoulder_r+12,sh_y+arm_len*2//3],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-12,sh_y+arm_len*2//3],fill=LIMB,width=3)
        elif p=="Pulling Ponytail":
            # both hands pulling hair back
            draw.line([shoulder_r,sh_y,shoulder_r+4,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_r+4,sh_y-arm_len//3,head_cx+hr,head_y+hr],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-4,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_l-4,sh_y-arm_len//3,head_cx-hr,head_y+hr],fill=LIMB,width=3)
            # ponytail line behind
            draw.line([head_cx,head_y+hr,head_cx+hr+8,head_y+hr+12],fill=HAIR_C,width=3)
        elif p=="Tucking Behind Ear":
            # right hand near ear
            draw.line([shoulder_r,sh_y,shoulder_r+4,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_r+4,sh_y-arm_len//3,head_cx+hr,head_cy],fill=LIMB,width=3)
            draw.ellipse([head_cx+hr-2,head_cy-3,head_cx+hr+6,head_cy+5],fill=hand_c)
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p=="Brushing Hair":
            # holding brush in right hand
            draw.line([shoulder_r,sh_y,shoulder_r+arm_len//2,sh_y+arm_len//3],fill=LIMB,width=3)
            bx=shoulder_r+arm_len//2; by=sh_y+arm_len//3
            draw.rounded_rectangle([bx-3,by-2,bx+12,by+6],radius=2,fill=prop_c,outline=BORDER,width=1)
            for sx in range(0,10,3): draw.line([bx+sx,by+6,bx+sx,by+12],fill=prop_c,width=1)
            for sx2 in range(-2,6,3): draw.line([bx+sx2,by-2,bx+sx2+1,by-8],fill=HAIR_C,width=1)
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        elif p=="Examining Ends":
            # both hands at chest holding hair ends
            draw.line([shoulder_r,sh_y,head_cx+12,sh_y+arm_len//2],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,head_cx-12,sh_y+arm_len//2],fill=LIMB,width=3)
            ey=sh_y+arm_len//2
            for sx in range(-8,10,3): draw.line([head_cx+sx,ey,head_cx+sx,ey+10],fill=HAIR_C,width=1)
        elif p=="Scrolling Solutions":
            # right arm holding phone at lap
            draw.line([shoulder_r,sh_y,shoulder_r+6,sh_y+arm_len],fill=LIMB,width=3)
            px2=shoulder_r+6; py2=sh_y+arm_len
            draw.rectangle([px2-4,py2-6,px2+8,py2+8],fill=(60,60,80),outline=BORDER,width=1)
            draw.rectangle([px2-2,py2-4,px2+6,py2+4],fill=(180,210,240))
            draw.line([shoulder_l,sh_y,shoulder_l-6,sh_y+arm_len],fill=LIMB,width=3)
        elif p in ["Arms Crossed"]:
            # arms crossed at chest
            draw.line([shoulder_r,sh_y,head_cx+8,sh_y+arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,head_cx-8,sh_y+arm_len//3],fill=LIMB,width=3)
            draw.line([head_cx-8,sh_y+arm_len//3,head_cx+12,sh_y+arm_len//3+4],fill=LIMB,width=3)
            draw.line([head_cx+8,sh_y+arm_len//3,head_cx-12,sh_y+arm_len//3+4],fill=LIMB,width=3)
        elif p in ["Hands in Pockets"]:
            draw.line([shoulder_r,sh_y,shoulder_r+6,waist_y-4],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-10,sh_y+arm_len],fill=LIMB,width=3)
        elif p in ["Hands on Hips"]:
            draw.line([shoulder_r,sh_y,shoulder_r+sh_w//2,sh_y+arm_len//2],fill=LIMB,width=3)
            draw.line([shoulder_r+sh_w//2,sh_y+arm_len//2,shoulder_r+4,waist_y],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-sh_w//2,sh_y+arm_len//2],fill=LIMB,width=3)
            draw.line([shoulder_l-sh_w//2,sh_y+arm_len//2,shoulder_l-4,waist_y],fill=LIMB,width=3)
        elif p in ["Thoughtful Look"]:
            # hand on chin
            draw.line([shoulder_r,sh_y,shoulder_r+4,sh_y-arm_len//3],fill=LIMB,width=3)
            draw.line([shoulder_r+4,sh_y-arm_len//3,head_cx+hr-2,head_cy+hr],fill=LIMB,width=3)
            draw.ellipse([head_cx+hr-5,head_cy+hr-2,head_cx+hr+3,head_cy+hr+6],fill=hand_c)
            draw.line([shoulder_l,sh_y,shoulder_l-10,sh_y+arm_len],fill=LIMB,width=3)
        elif p in ["Phone Check","Phone Browsing"]:
            draw.line([shoulder_r,sh_y,shoulder_r+arm_len//2,sh_y+arm_len//2],fill=LIMB,width=3)
            px=shoulder_r+arm_len//2; py_ph=sh_y+arm_len//2
            draw.rectangle([px-4,py_ph-8,px+8,py_ph+8],fill=(60,60,80),outline=BORDER,width=1)
            draw.rectangle([px-2,py_ph-6,px+6,py_ph+4],fill=(180,210,240))
            draw.line([shoulder_l,sh_y,shoulder_l-8,sh_y+arm_len],fill=LIMB,width=3)
        else:
            # default: arms relaxed at sides
            draw.line([shoulder_r,sh_y,shoulder_r+10,sh_y+arm_len],fill=LIMB,width=3)
            draw.line([shoulder_l,sh_y,shoulder_l-10,sh_y+arm_len],fill=LIMB,width=3)
        # pose label tag
        if pose_label:
            pose_y=box[3]-22
            draw.rounded_rectangle([box[0]+4,pose_y-2,box[2]-4,pose_y+12],radius=4,fill=(99,102,241))
            pt=pose_label if len(pose_label)<=16 else pose_label[:15]+"…"
            draw.text((cx-len(pt)*3,pose_y-1),pt,fill=WHITE)
    def logo(): rr([W-90,8,W-8,36],r=6,fill=LOGO_BG); draw.text((W-82,14),"BATRA'S",fill=(70,70,90))

    rr([3,3,W-3,H-3],r=14,outline=BORDER,w=2); logo()
    lid=layout_id; psq=[int(W*0.5),int(H*0.13),W-8,int(H*0.85)]; pfl=[int(W*0.1),int(H*0.13),W-int(W*0.1),int(H*0.85)]

    if lid=="L01": dp(psq);y=dh(14,int(H*0.13),title,bg=WHITE);ds(14,y+4,subtext);dc(W//2,H-60,cta)
    elif lid=="L02": dp([int(W*0.2),int(H*0.33),int(W*0.8),int(H*0.85)]);y=dh(W//2-90,int(H*0.1),title,bg=WHITE);ds(W//2-90,y+4,subtext,mc=26);dc(W-90,H-60,cta,width=140)
    elif lid=="L03": dp([int(W*0.15),int(H*0.05),int(W*0.85),int(H*0.67)]);dcl(W-160,14,cta,color=CTA_BLUE);dh(14,int(H*0.7),title,bg=WHITE)
    elif lid=="L04": y=dh(W//2-100,int(H*0.07),title,mc=22,bg=WHITE);dp([int(W*0.2),int(H*0.3),int(W*0.8),int(H*0.85)]);dcl(14,H-60,cta)
    elif lid=="L05": rr([int(W*0.44),8,W-8,int(H*0.17)],r=8,fill=ACCENT);draw.text((int(W*0.46),int(H*0.05)),title[:18].upper(),fill=WHITE);dp([8,int(H*0.18),int(W*0.55),int(H*0.85)]);dc(int(W*0.7),H-60,cta)
    elif lid=="L06": rr([30,14,W-30,int(H*0.15)],r=18,fill=RIBBON);draw.text((46,int(H*0.07)),title[:22].upper(),fill=TEXT_DARK);dp([int(W*0.2),int(H*0.17),int(W*0.8),int(H*0.8)]);rr([40,H-58,W-40,H-14],r=10,fill=CTA_GREEN);draw.text((W//2-25,H-48),cta,fill=WHITE)
    elif lid=="L07": rr([0,0,int(W*0.15),H],r=0,fill=PANEL_BG);[draw.text((8,int(H*0.12)+i*36),ch.upper(),fill=TEXT_DARK) for i,ch in enumerate(title[:8])];dp([int(W*0.17),int(H*0.08),W-8,int(H*0.85)]);dc(W-80,H-60,cta,width=130)
    elif lid=="L08": dp([int(W*0.12),int(H*0.05),int(W*0.88),int(H*0.7)]);dcl(W-160,12,cta,color=CTA_BLUE);rr([8,int(H*0.68),int(W*0.6),H-8],r=8,fill=WHITE,outline=BORDER,w=1);dh(14,int(H*0.7),title,mc=20)
    elif lid=="L09": dp([8,int(H*0.1),int(W*0.5),int(H*0.85)]);dh(int(W*0.52),int(H*0.22),title,mc=12,bg=WHITE);rr([0,H-58,W,H],r=0,fill=CTA_GREEN);draw.text((W//2-25,H-44),cta,fill=WHITE)
    elif lid=="L10": r2=min(55,int(H*0.1));draw.ellipse([10,10,10+r2*2,10+r2*2],fill=ACCENT);[draw.text((14,18+i*18),ln,fill=WHITE) for i,ln in enumerate(wrap(title.upper(),7)[:3])];dp([int(W*0.38),int(H*0.1),W-8,int(H*0.85)]);dc(W//2,H-60,cta)
    elif lid=="L11": dp([int(W*0.55),int(H*0.13),W-8,int(H*0.85)]);y=dh(int(W*0.06),int(H*0.13),title,mc=14,bg=WHITE);y=ds(int(W*0.06),y+4,subtext);draw.line([int(W*0.06),y+8,int(W*0.5),y+8],fill=ACCENT,width=2);draw.text((int(W*0.06),y+14),cta,fill=CTA_GREEN)
    elif lid=="L12": draw.text((14,int(H*0.05)),title[:26].upper(),fill=TEXT_DARK);dp([int(W*0.15),int(H*0.17),int(W*0.85),int(H*0.82)]);dc(W-90,H-60,cta,width=140,color=CTA_BLUE)
    elif lid=="L13": draw.text((14,int(H*0.04)),title[:30].upper(),fill=TEXT_GRAY);dp([int(W*0.15),int(H*0.12),int(W*0.85),int(H*0.73)]);rr([14,H-72,W-14,H-14],r=20,fill=CTA_GREEN);draw.text((W//2-28,H-56),cta,fill=WHITE)
    elif lid=="L14": dp([int(W*0.4),int(H*0.07),W-8,int(H*0.87)]);rr([10,int(H*0.3),int(W*0.46),int(H*0.58)],r=8,fill=WHITE,outline=BORDER,w=1);y=dh(16,int(H*0.32),title,mc=14);ds(16,y+4,subtext,mc=20);dcl(int(W*0.1),H-60,cta)
    elif lid=="L15": dp([int(W*0.45),int(H*0.13),W-8,int(H*0.85)]);[draw.text((12+i*3,int(H*0.13)+i*26),ln,fill=TEXT_DARK) for i,ln in enumerate(wrap(title.upper(),14))];dc(W//2,H-60,cta)
    elif lid=="L16": rr([0,int(H*0.03),W,int(H*0.17)],r=0,fill=ACCENT);draw.text((14,int(H*0.07)),title[:26].upper(),fill=WHITE);dp([int(W*0.15),int(H*0.19),int(W*0.85),int(H*0.83)]);dc(W-90,H-60,cta,width=140,color=RIBBON)
    elif lid=="L17": dp(pfl);draw.text((10,int(H*0.14)),title[:10].upper(),fill=TEXT_DARK);draw.text((int(W*0.7),int(H*0.35)),title[10:18].upper(),fill=TEXT_DARK);dcl(10,H-60,cta)
    elif lid=="L18": rr([20,int(H*0.04),W-20,int(H*0.17)],r=8,fill=RIBBON);draw.text((34,int(H*0.08)),title[:24].upper(),fill=TEXT_DARK);dp([int(W*0.15),int(H*0.19),int(W*0.85),int(H*0.83)]);dc(W//2,H-60,cta,color=CTA_BLUE)
    elif lid=="L19": dp(psq);y=dh(14,int(H*0.13),title,bg=WHITE);ds(14,y+4,subtext);dc(W//2,H-60,cta)
    elif lid=="L20": dp(psq);rr([8,int(H*0.14),int(W*0.48),int(H*0.3)],r=6,fill=RIBBON);dh(14,int(H*0.16),title,mc=16);ds(14,int(H*0.32),subtext);dc(W//2,H-60,cta)
    elif lid=="L21": rr([0,0,int(W*0.42),H],r=0,fill=PANEL_BG);y=dh(10,int(H*0.15),title,mc=12);ds(10,y+4,subtext,mc=16);dcl(10,H-60,cta);dp([int(W*0.44),int(H*0.07),W-6,int(H*0.9)])
    elif lid=="L22": rr([0,0,W,H//2],r=0,fill=(240,243,252));y=dh(W//2-100,int(H*0.07),title,mc=20);ds(W//2-100,y+4,subtext);draw.ellipse([W//2-60,H//2-8,W//2+60,H//2+120],fill=PERSON_BG,outline=BORDER,width=1);draw.text((W//2-18,H//2+50),"PERSON",fill=(120,135,160));dc(W//2,H//2-18,cta)
    elif lid=="L23": y=dh(14,int(H*0.04),title,bg=WHITE);draw.line([14,y+6,W-14,y+6],fill=ACCENT,width=2);ds(14,y+12,subtext);dp([int(W*0.1),y+int(H*0.12),W-int(W*0.1),H-58]);rr([0,H-54,W,H],r=0,fill=CTA_GREEN);draw.text((W//2-25,H-40),cta,fill=WHITE)
    elif lid=="L24": rr([0,0,W,int(H*0.16)],r=18,fill=ACCENT);draw.text((14,int(H*0.05)),title[:26].upper(),fill=WHITE);dp([int(W*0.15),int(H*0.18),int(W*0.85),int(H*0.83)]);dc(W//2,H-60,cta)
    elif lid=="L25": y=dh(14,int(H*0.13),title);draw.line([14,y+4,int(W*0.4),y+4],fill=ACCENT,width=3);ds(14,y+10,subtext,mc=18);rr([int(W*0.45),int(H*0.09),W-8,int(H*0.8)],r=16,fill=PERSON_BG,outline=BORDER,w=2);draw.text((int(W*0.53),int(H*0.42)),"PERSON",fill=(120,135,160));dcl(14,H-60,cta)
    elif lid=="L26": dp(pfl);rr([int(W*0.07),int(H*0.07),W-int(W*0.07),int(H*0.26)],r=10,fill=WHITE,outline=BORDER,w=1);draw.text((int(W*0.1),int(H*0.1)),title[:24].upper(),fill=TEXT_DARK);ds(int(W*0.1),int(H*0.19),subtext,mc=28);rr([0,H-54,W,H],r=0,fill=TEXT_DARK);draw.text((W//2-25,H-40),cta,fill=WHITE)
    elif lid=="L27": words=title.split();draw.text((14,int(H*0.13)),words[0].upper() if words else "",fill=ACCENT);draw.text((14,int(H*0.2))," ".join(words[1:])[:18].upper(),fill=TEXT_DARK);dp(psq);dcl(14,H-60,cta)
    elif lid=="L28": dp([8,int(H*0.1),int(W*0.55),int(H*0.85)]);rr([int(W*0.52),int(H*0.14),W-8,int(H*0.37)],r=12,fill=WHITE,outline=ACCENT,w=2);dh(int(W*0.54),int(H*0.17),title,mc=10);dc(W-80,H-60,cta,width=130,color=CTA_BLUE)
    elif lid=="L29": dp([8,int(H*0.03),W-8,int(H*0.58)]);rr([0,int(H*0.59),W,H],r=0,fill=WHITE);draw.line([0,int(H*0.59),W,int(H*0.59)],fill=BORDER,width=1);y=dh(14,int(H*0.61),title,mc=24);dc(W//2,H-60,cta)
    elif lid=="L30": rr([0,0,10,H],r=0,fill=ACCENT);y=dh(18,int(H*0.13),title);ds(18,y+4,subtext,mc=18);dp([int(W*0.42),int(H*0.09),W-8,int(H*0.85)]);dc(int(W*0.6),H-60,cta)
    else: dp(psq);y=dh(14,int(H*0.13),title,bg=WHITE);ds(14,y+4,subtext);dc(W//2,H-60,cta)

    draw.text((10,H-16),f"Layout {lid} · {'1:1' if fmt_key=='square' else '9:16'}",fill=(160,160,175))
    buf=BytesIO(); img.save(buf,format="PNG"); buf.seek(0)
    return buf.getvalue()


# ─────────────────────────────────────────────
# HAIR DETECTION
# ─────────────────────────────────────────────
HAIR_LOSS_KEYWORDS = [
    "hair loss","hair fall","hairfall","hair thinning","thinning hair",
    "bald","balding","receding hairline","hair regrowth","hair growth",
    "alopecia","scalp","hair density","hair care","dandruff",
    "hair issue","hair problem","hair damage","hair treatment","hair fall control"
]

def is_hair_loss_topic(t): return any(kw in t.lower() for kw in HAIR_LOSS_KEYWORDS)
def pick_hair_gender(): return "male" if random.random() < 0.50 else "female"


# ─────────────────────────────────────────────
# PLACE / BACKGROUND DETECTION
# ─────────────────────────────────────────────
PLACE_BACKGROUNDS = [
    {"keywords": ["pollution", "traffic", "commute", "road", "driving"],
     "bg": "blurred busy city road with vehicles and slight smog haze, urban outdoor setting",
     "label": "City Road / Traffic"},
    {"keywords": ["city", "urban", "metro", "mumbai", "delhi", "bangalore", "pune"],
     "bg": "blurred city skyline with buildings and streets, urban backdrop",
     "label": "City / Urban"},
    {"keywords": ["office", "work", "corporate", "job", "boss", "colleague", "meeting"],
     "bg": "blurred modern office interior with desks and screens, corporate setting",
     "label": "Office / Workplace"},
    {"keywords": ["stress", "pressure", "deadline", "anxiety", "tension"],
     "bg": "blurred dimly lit home or office space, moody and tense atmosphere",
     "label": "Stress Environment"},
    {"keywords": ["home", "kitchen", "bedroom", "living room", "couch", "sofa"],
     "bg": "softly blurred warm home interior, cozy living space",
     "label": "Home Interior"},
    {"keywords": ["bathroom", "mirror", "shower", "morning routine"],
     "bg": "softly blurred bathroom environment, warm whites and neutrals, mirror reflection feel",
     "label": "Bathroom / Mirror"},
]


def detect_background(topic):
    """Detect place/context from topic and return appropriate background."""
    topic_lower = topic.lower()
    for place in PLACE_BACKGROUNDS:
        if any(kw in topic_lower for kw in place["keywords"]):
            return place["bg"], place["label"]
    return None, None


MALE_HAIR_LENGTHS = [
    {"label":"Short","desc":"short hair (2-3 cm), dark brown-black, dry and natural, close-cropped sides — crown thinning clearly visible, scalp visible through sparse hair on top","camera_note":"Slightly elevated top-angle — camera looking DOWN at crown. M-shaped recession and scalp clearly visible."},
    {"label":"Medium","desc":"medium length hair (5-7 cm), dark brown-black, slightly disheveled — noticeable density difference between full sides and thinning crown, scalp visible at crown","camera_note":"Slightly elevated top-angle — hair parts naturally to reveal clearly thinner crown. Scalp visible through thinning hair on top."},
    {"label":"Slightly Longer","desc":"slightly longer hair (8-10 cm), dark brown-black — temples noticeably thinner, clear M-shaped recession at forehead hairline","camera_note":"Slight top-angle — M-shape recession at forehead clearly visible. Crown noticeably less dense."},
]

FEMALE_HAIR_STYLES = [
    {"label":"Short Bob","desc":"short bob, jaw-length, dark brown-black — center parting noticeably wider than normal, temples clearly thin and wispy","camera_note":"Close-up front angle showing wider center parting and hairline thinning clearly."},
    {"label":"Medium","desc":"shoulder-length, dark brown-black, natural straight or wavy — center parting clearly wider, fine wispy strands at hairline","camera_note":"Slight top-angle or close-up showing wider parting line and hairline thinning clearly."},
    {"label":"Long","desc":"long hair below shoulder, dark brown-black — center parting noticeably wider, density visibly reduced at parting and temples","camera_note":"Slightly elevated or straight-on angle showing wider parting line clearly."},
    {"label":"Tied Up","desc":"hair loosely tied in messy bun or low ponytail — center parting clearly wider than normal, temples noticeably thinner and wispier","camera_note":"Top-angle or front close-up showing wider parting, hairline thinning, and tied-up style clearly."},
]

MALE_LIGHTING_MOODS = [
    {"label":"Morning Window Light","desc":"natural morning window light from one side — warm, soft but directional, gentle shadow on one side of face","bg":"softly blurred home environment — bathroom or bedroom, warm neutral tones"},
    {"label":"Overcast Natural Light","desc":"soft overcast daylight — diffused, slightly cool tone, authentic and documentary","bg":"softly blurred indoor background — warm neutral or off-white wall"},
    {"label":"Harsh Side Light","desc":"stronger directional side light — one side brighter, other in deeper shadow, amplifies tiredness","bg":"dark or dimly lit blurred background — private moment alone at home"},
]

FEMALE_LIGHTING_MOODS = [
    {"label":"Soft Window Light","desc":"soft natural window light, slightly warm, from one side — gentle shadows, real and candid","bg":"softly blurred warm home background — bedroom or bathroom"},
    {"label":"Bathroom Mirror Light","desc":"bathroom-style warm front light — feels like checking hair in a mirror, intimate and private","bg":"softly blurred bathroom environment — warm whites and neutrals"},
    {"label":"Cool Overcast Light","desc":"cool diffused overcast light — slightly desaturated, melancholic and emotional","bg":"neutral blurred background — cool white or pale grey"},
]

# ✅ FIX 2 — CLOTHING RULE (no towel, no revealing)
CLOTHING_RULE = (
    "CLOTHING — VERY IMPORTANT: "
    "Person MUST be wearing a plain light grey or white round-neck t-shirt. "
    "SAME exact shirt color must appear on all formats — light grey or white ONLY. "
    "Fully clothed, professional and modest appearance. "
    "STRICTLY NO towel, NO bathrobe, NO bare shoulders, NO revealing clothing, "
    "NO swimwear, NO sleeveless top, NO low-cut clothing, NO blue shirt, NO dark shirt. "
    "This is a healthcare advertisement — clothing must be appropriate and decent."
)

MALE_POSES = [
    # ── HANDS ON HEAD (5) ──
    {"label": "Touching Crown", "desc": "RIGHT hand gently touching hair or scalp near crown. Left hand relaxed at side."},
    {"label": "Running Fingers", "desc": "RIGHT hand running fingers through thinning hair on top, feeling the sparse strands. Left hand down."},
    {"label": "Checking Hairline", "desc": "Both hands pulling hair back from forehead, examining receding hairline in front of a mirror. Worried expression."},
    {"label": "Frustrated with Comb", "desc": "Holding a comb in RIGHT hand near head, staring at hair stuck on comb. Frustrated and worried."},
    {"label": "Head Down Stress", "desc": "Head slightly tilted forward, RIGHT hand on back of neck, showing visible crown thinning from above. Stressed posture."},
    # ── HANDS OFF HEAD (5) ──
    {"label": "Holding Hair Strands", "desc": "Looking down at loose hair strands fallen on RIGHT palm. Left hand at side. Concerned expression."},
    {"label": "Mirror Check", "desc": "Standing in front of bathroom mirror, leaning slightly forward, examining crown area. Both hands on sink counter."},
    {"label": "Pillow Shock", "desc": "Sitting on bed edge, looking down at hair strands on pillow held in both hands. Shocked and worried expression."},
    {"label": "Comparing Old Photo", "desc": "Holding a switched-off black phone in RIGHT hand at chest level, staring at it with regret and worry. Phone screen facing away from camera. Left hand on desk."},
    {"label": "Staring at Drain", "desc": "Crouching near bathroom drain, staring at clump of fallen hair. Both hands on knees. Distressed and worried expression."},
]

FEMALE_POSES = [
    # ── HANDS ON HEAD (4) ──
    {"label": "Touching Parting", "desc": "Hand gently touching wider center parting on scalp, looking slightly downward. Worried expression."},
    {"label": "Checking Mirror", "desc": "Standing in front of mirror, parting hair with both hands to examine scalp thinning. Concerned look."},
    {"label": "Pulling Ponytail", "desc": "Pulling hair back into ponytail, revealing thinner temples and wider parting. Noticing thinning with concern."},
    {"label": "Tucking Behind Ear", "desc": "Tucking thin wispy hair behind ear, exposing sparse temple area. Slight frown, self-conscious."},
    # ── HANDS OFF HEAD (4) ──
    {"label": "Holding Hair Strands", "desc": "Looking at loose hair strands collected in palm after brushing. Worried and emotional."},
    {"label": "Brushing Hair", "desc": "Holding hairbrush with visible hair strands stuck in it. Staring at brush. Upset expression."},
    {"label": "Examining Ends", "desc": "Holding thin hair ends in both hands at chest level, comparing density. Looking down with worry and sadness."},
    {"label": "Scrolling Solutions", "desc": "Sitting on couch, scrolling phone searching for hair fall solutions. Other hand resting on lap. Anxious and tired expression."},
]


GENERAL_MALE_POSES = [
    {"label": "Confident Smile", "desc": "Standing upright, slight confident smile, arms relaxed at sides. Direct eye contact with camera."},
    {"label": "Arms Crossed", "desc": "Arms crossed casually at chest, slight smile, relaxed confident posture. Looking at camera."},
    {"label": "Hands in Pockets", "desc": "One hand in pocket, other hand relaxed at side. Casual confident stance. Slight smile."},
    {"label": "Leaning Forward", "desc": "Leaning slightly forward with interest, one hand on table/desk. Engaged and attentive expression."},
    {"label": "Walking Towards", "desc": "Walking towards camera confidently, natural stride. Slight smile, direct eye contact."},
    {"label": "Sitting Relaxed", "desc": "Sitting on chair or couch, leaning slightly back, one arm on armrest. Calm and relaxed expression."},
    {"label": "Phone Check", "desc": "Holding phone in one hand at chest level, looking at it with interest. Other hand relaxed."},
    {"label": "Thoughtful Look", "desc": "Hand on chin, looking slightly to the side, thoughtful and contemplative expression."},
]

GENERAL_FEMALE_POSES = [
    {"label": "Warm Smile", "desc": "Standing with warm natural smile, hands clasped gently in front. Friendly and approachable."},
    {"label": "Arms Crossed", "desc": "Arms crossed lightly, confident posture, slight smile. Direct eye contact with camera."},
    {"label": "Hair Tuck", "desc": "One hand gently tucking hair behind ear, slight smile. Natural and candid."},
    {"label": "Looking Away", "desc": "Looking slightly to the side with soft smile, one hand on hip. Confident and elegant."},
    {"label": "Sitting Graceful", "desc": "Sitting on chair, legs crossed, hands on lap. Poised and calm expression."},
    {"label": "Walking Confident", "desc": "Walking towards camera, natural stride, gentle smile. Confident and happy."},
    {"label": "Phone Browsing", "desc": "Holding phone, scrolling with slight smile. Other hand relaxed. Casual moment."},
    {"label": "Hands on Hips", "desc": "Both hands on hips, standing tall, confident smile. Strong and empowered posture."},
]

GENERAL_LIGHTING = [
    {"label": "Warm Natural", "desc": "warm natural daylight, soft golden tones, inviting and friendly", "bg": "softly blurred clean modern background, warm neutral tones"},
    {"label": "Bright Studio", "desc": "bright clean studio-style light, even and professional", "bg": "clean white or light grey blurred background"},
    {"label": "Soft Overcast", "desc": "soft overcast diffused light, natural and authentic feel", "bg": "softly blurred outdoor or indoor neutral background"},
]


def build_general_subject(gender):
    if gender == "male":
        pose = random.choice(GENERAL_MALE_POSES)
        light = random.choice(GENERAL_LIGHTING)
        subject = (
            "PHOTOGRAPHY STYLE — CANDID LIFESTYLE: Real authentic moment. "
            "South Asian Indian man, age 25-40, wheatish brown skin, dark brown eyes. "
            "Natural confident expression. "
            "CLOTHING: wearing casual kurta or plain t-shirt, fully clothed, "
            "NOT wearing towel or revealing clothing. "
            "Natural skin — visible pores. "
            "CAMERA: 85mm f/1.4, handheld feel, slight grain. "
            f"POSE: {pose['desc']} "
            "Fingers must be anatomically correct — five fingers, no distortion. "
            "Face must be symmetrical, sharp, and proportionally correct. "
            f"LIGHTING: {light['desc']} BACKGROUND: {light['bg']} "
            "Photorealistic, natural Indian skin tone, ultra detailed 8K. "
            "Single person only, no products."
        )
        return subject, "Standard", light["label"], pose["label"]
    else:
        pose = random.choice(GENERAL_FEMALE_POSES)
        light = random.choice(GENERAL_LIGHTING)
        subject = (
            "PHOTOGRAPHY STYLE — CANDID LIFESTYLE: Real authentic moment. "
            "South Asian Indian woman, age 25-35, wheatish brown skin, dark brown eyes. "
            "Natural warm expression. "
            "CLOTHING: wearing casual kurta or plain t-shirt, fully clothed, "
            "NOT wearing towel or revealing clothing. "
            "Natural skin — visible pores. "
            "CAMERA: 85mm f/1.4, handheld feel, slight grain. "
            f"POSE: {pose['desc']} "
            "Fingers must be anatomically correct — five fingers, no distortion. "
            "Face must be symmetrical, sharp, and proportionally correct. "
            f"LIGHTING: {light['desc']} BACKGROUND: {light['bg']} "
            "Photorealistic, natural Indian skin tone, ultra detailed 8K. "
            "Single person only, no products."
        )
        return subject, "Standard", light["label"], pose["label"]


def build_hair_subject(gender):
    if gender == "male":
        hair  = random.choice(MALE_HAIR_LENGTHS)
        light = random.choice(MALE_LIGHTING_MOODS)
        pose  = random.choice(MALE_POSES)
        subject = (
            "PHOTOGRAPHY STYLE — RAW EMOTIONAL DOCUMENTARY: NOT a studio shot. Real candid moment. "
            "South Asian Indian man, age 30-35, wheatish brown skin, dark brown eyes, light stubble. "
            "Visible frustration — furrowed brow, under-eye fatigue, tired look. NOT smiling. "
            f"{CLOTHING_RULE} "
            "Natural skin — visible pores. "
            f"HAIR — NORWOOD STAGE 2-3: NOT bald but thinning clearly visible. Style: {hair['desc']}. "
            "Hairline receded at temples — clear M-shape. Crown less dense — scalp visible. "
            "DO NOT make him bald. DO NOT remove more than 25% of hair. "
            f"CAMERA: {hair['camera_note']} Handheld feel, slight grain, 85mm f/1.4. "
            f"POSE: Natural realistic human pose. {pose['desc']} "
"Maintain consistent pose across all formats. "
"Fingers must be anatomically correct — five fingers, no distortion, no extra fingers. "
"Hand position must look natural and relaxed, not stiff or awkward. "
"Face must be symmetrical, sharp, and proportionally correct. "
"No deformation, no blur, no distortion. "
            f"LIGHTING: {light['desc']} BACKGROUND: {light['bg']} "
            # "Photorealistic, natural Indian skin tone, ultra detailed 8K. Single person only, no products."
            "Photorealistic, natural Indian skin tone, ultra detailed 8K. "
"Face sharp, clear eyes, realistic proportions. "
"Hands fully visible and anatomically correct. "
"No distortion, no warped fingers, no artifacts. "
"Single person only, no products."
        )
        return subject, hair["label"], light["label"], pose["label"]
    else:
        hair  = random.choice(FEMALE_HAIR_STYLES)
        light = random.choice(FEMALE_LIGHTING_MOODS)
        pose  = random.choice(FEMALE_POSES)
        subject = (
            "PHOTOGRAPHY STYLE — RAW EMOTIONAL DOCUMENTARY: NOT a studio shot. Real candid moment. "
            "South Asian Indian woman, age 25-35, wheatish brown skin, dark brown eyes. "
            "Worried and concerned — slight frown, tired eyes. "
            f"{CLOTHING_RULE} "
            "Natural skin — visible pores. "
            f"HAIR — EARLY STAGE THINNING: {hair['desc']}. NO bald patches. Visibly thinner at parting. "
            f"CAMERA: {hair['camera_note']} Handheld feel, slight grain, 85mm f/1.4. "
            f"POSE: {pose['desc']} "
            f"LIGHTING: {light['desc']} BACKGROUND: {light['bg']} "
            # "Photorealistic, natural Indian skin tone, ultra detailed 8K. Single person only, no products."
            "Photorealistic, natural Indian skin tone, ultra detailed 8K. "
"Face sharp, clear eyes, realistic proportions. "
"Hands fully visible and anatomically correct. "
"No distortion, no warped fingers, no artifacts. "
"Single person only, no products."
        )
        return subject, hair["label"], light["label"], pose["label"]


# ─────────────────────────────────────────────
# GROQ
# ─────────────────────────────────────────────
def call_groq(api_key, topic):
    # Detect background from topic
    detected_bg, _ = detect_background(topic)
    if detected_bg:
        bg_instruction = f"BACKGROUND: Use this specific setting — {detected_bg}. Heavily blurred bokeh, person in sharp focus."
    else:
        bg_instruction = "BACKGROUND: Real environment — bathroom, bedroom, home, clinic. Softly blurred."

    system_prompt = (
        "You are a senior creative director for Meta ad campaigns for Dr Batra's healthcare brand. "
        "Given a topic, generate a JSON with EXACTLY these keys: "
        "title (punchy emotional headline, max 8 words), "
        "subtext (supporting line max 15 words, builds trust), "
        "cta (call-to-action max 4 words, action-driven), "
        "visual_style (Flux image prompt — subject expression, pose, clothing, emotion, lighting, background. No text/headline/CTA.), "
        f"layout (MUST be one of these EXACT strings:\n{LAYOUT_OPTIONS_FOR_GROQ}). "
        "LANGUAGE: Simple conversational Indian English. "
        "SCENE RULE: ONE scene, ONE person. No collages, no products. "
        f"{bg_instruction} "
        "All people: Indian, age 25-45, realistic skin, fully clothed in kurta or casual top. "
        "EMOTION: Problem → raw concern. Solution → genuine relief. Results → real confidence. "
        "STYLE: raw documentary / candid lifestyle / emotional editorial. NOT stock photo. "
        "Return ONLY valid JSON. No markdown. No explanation."
    )
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "max_tokens": 700,
              "messages": [{"role": "system", "content": system_prompt},
                           {"role": "user", "content": f'Topic: "{topic}"'}]},
        timeout=20,
    )
    res.raise_for_status()
    raw = res.json()["choices"][0]["message"]["content"].strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match: raise Exception("Groq did not return valid JSON")
    data = json.loads(match.group())
    # Force random layout from Python — Groq tends to repeat L01/L03
    forced_layout = random.choice(LAYOUTS)
    data["layout"] = forced_layout["groq"]
    return data


def call_groq_chat(api_key, messages):
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "max_tokens": 800, "messages": messages},
        timeout=20,
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()


# ─────────────────────────────────────────────
# FLUX — SAME SEED
# ─────────────────────────────────────────────
def generate_flux(api_key, prompt, width, height, seed):
    os.environ["FAL_KEY"] = api_key
    result = fal_client.subscribe(
        "fal-ai/nano-banana-2",
        arguments={
            "prompt": prompt,
            "image_size": {"width": width, "height": height},
            "num_images": 1,
            "enable_safety_checker": True,
            "output_format": "jpeg",
            "seed": seed,
        },
        with_logs=False,
    )
    images = result.get("images", [])
    if not images: raise Exception("No image returned from Flux")
    return images[0]["url"]


def stamp_logo(img):
    try:
        if not os.path.exists(LOGO_PATH): return img
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo = logo.resize((140, 70), Image.LANCZOS)
        if img.mode != "RGBA": img = img.convert("RGBA")
        img.paste(logo, (img.width - logo.width - 20, 20), logo)
    except Exception: pass
    return img


def generate_and_stamp(prompt, width, height, seed):
    img_url = generate_flux(st.session_state["fal_key"], prompt, width, height, seed)
    res = requests.get(img_url, timeout=30)
    img = Image.open(BytesIO(res.content))
    img = img.resize((width, height), Image.LANCZOS)
    img = stamp_logo(img)
    img = img.convert("RGB")
    buf = BytesIO(); img.save(buf, format="JPEG", quality=95); buf.seek(0)
    return buf.getvalue()


def get_layout_id(layout_text):
    best_match_id    = "L01"
    best_match_score = 0
    layout_lower     = layout_text.lower()
    for l in LAYOUTS:
        # count how many words match
        groq_words  = set(l["groq"].lower().split())
        text_words  = set(layout_lower.split())
        score       = len(groq_words & text_words)
        if score > best_match_score:
            best_match_score = score
            best_match_id    = l["id"]
    return best_match_id


def _build_base_prompt(style, title, subtext, cta, font, layout, hair_gender=None, is_hair_topic=False):
    hair_label = lighting_label = pose_label = None
    if hair_gender and is_hair_topic:
        photography, hair_label, lighting_label, pose_label = build_hair_subject(hair_gender)
    elif hair_gender:
        photography, hair_label, lighting_label, pose_label = build_general_subject(hair_gender)
    else:
        photography = (
            f"{style}. Real Indian person age 25-45, photorealistic, candid authentic feel, "
            f"natural skin texture, 85mm f/1.4, NOT a stock photo. "
            f"CLOTHING: wearing casual kurta or plain t-shirt, fully clothed, "
            f"NOT wearing towel or revealing clothing."
        )
    prompt = (
        f"Professional social media advertisement graphic design. "
        f"LAYOUT: {layout} "
        f"TYPOGRAPHY: {font} "
        f"GRAPHIC DESIGN ELEMENTS: "
        f"1. HEADLINE: Exact words '{title}' — large bold, 72px, dark color, sharp edges. "
        f"2. SUBTEXT: Exact words '{subtext}' — 28px, medium gray, below headline. "
        f"3. CTA BUTTON: Solid pill-shaped, vivid green background, "
        f"exact words '{cta}' in white bold centered inside. ONE button only. "
        f"PHOTOGRAPHY: {photography} "
        f"RULES: Text spelled correctly. Text NOT over face. CTA clearly visible. "
        f"No watermarks, no Meta text, no products, single person. 8K premium."
    )
    return prompt, hair_label, lighting_label, pose_label


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, default in {
    "chat_messages": [], "hair_gender": None, "hair_label": None,
    "lighting_label": None, "pose_label": None, "ideas_generated": False,
    "base_prompt": None, "ad_data": None,
    "image_square": None, "image_story": None,
    "skeleton_square": None, "skeleton_story": None,
    "layout_id": "L01", "generation_seed": None,
}.items():
    if key not in st.session_state: st.session_state[key] = default

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;font-size:28px;margin-bottom:2px'>✦ Meta Creative Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#888;font-size:13px;margin-bottom:20px'>Generates <b>1080×1080</b> Feed + <b>1080×1920</b> Story · Same seed · Proper clothing · Full body visible</p>", unsafe_allow_html=True)

left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("### 🎨 Ad Workflow")

    topic = st.text_input("Topic", placeholder="e.g. PCOS treatment, hair regrowth, skin care...",
                          label_visibility="collapsed", key="topic_input")

    hair_detected = is_hair_loss_topic(topic) if topic else False
    bg_detected, bg_label = detect_background(topic) if topic else (None, None)

    if bg_label and not hair_detected:
        st.markdown(
            f"<div style='background:#f0fff4;border:1px solid #a0d0b0;border-radius:8px;"
            f"padding:8px 12px;font-size:13px;color:#2d6a4f;margin-bottom:8px'>"
            f"📍 Place detected → Background: <b>{bg_label}</b> (blurred)</div>",
            unsafe_allow_html=True
        )

    if st.session_state["ideas_generated"] and st.session_state["hair_gender"]:
        hg    = st.session_state["hair_gender"]
        icon  = "👨 Indian Male" if hg == "male" else "👩 Indian Female"
        color = "#1a73e8" if hg == "male" else "#d81b60"
        topic_type = "Hair topic" if hair_detected else "Topic"
        style_note = "Raw emotional · Proper clothing enforced" if hair_detected else "Candid lifestyle · Proper clothing enforced"
        st.markdown(
            f"<div style='background:{color}15;border:1px solid {color}40;border-radius:8px;"
            f"padding:8px 12px;font-size:13px;color:{color};margin-bottom:8px'>"
            f"🎯 {topic_type} → Subject: <b>{icon}</b> &nbsp;"
            f"<span style='opacity:0.65'>(50% male · 50% female)</span>"
            f"<br><span style='opacity:0.55;font-size:11px'>"
            f"🎲 Pose & lighting randomised · {style_note}</span></div>",
            unsafe_allow_html=True
        )

    if st.button("✦ Generate Ideas", disabled=not topic):
        if not st.session_state.get("groq_key"):
            st.error("Save your Groq API key in the sidebar.")
        else:
            st.session_state["hair_gender"]     = pick_hair_gender()
            st.session_state["hair_label"]      = None
            st.session_state["lighting_label"]  = None
            st.session_state["ideas_generated"] = True
            st.session_state["skeleton_square"] = None
            st.session_state["skeleton_story"]  = None
            st.session_state["generation_seed"] = random.randint(1, 999999)
            with st.spinner("Groq is writing ad copy..."):
                try:
                    data = call_groq(st.session_state["groq_key"], topic)
                    st.session_state["ad_data"]      = data
                    st.session_state["last_topic"]   = topic
                    st.session_state["image_square"] = None
                    st.session_state["image_story"]  = None
                    st.session_state["base_prompt"]  = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state["ad_data"]:
        data = st.session_state["ad_data"]
        st.markdown("---")
        st.markdown("##### ✏️ Edit Ad Copy")

        edited_title   = st.text_input("Title",   value=data.get("title", ""),   key="edit_title")
        edited_subtext = st.text_input("Subtext", value=data.get("subtext", ""), key="edit_subtext")
        edited_cta     = st.text_input("CTA",     value=data.get("cta", ""),     key="edit_cta")

        font_styles = {
            "Clean Sans-serif (Roboto)":  "All text in clean modern Roboto sans-serif font.",
            "Bold Impact":                "Headlines in bold thick Impact font, subtext in clean sans-serif.",
            "Elegant Serif (Playfair)":   "Headlines in elegant Playfair Display serif font, subtext in light sans-serif.",
            "Minimal Thin (Montserrat)":  "All text in thin minimal Montserrat font.",
            "Rounded (Poppins)":          "All text in rounded friendly Poppins font.",
            "Classic (Arial Black)":      "Headlines in bold Arial Black font, subtext in regular Arial.",
            "Modern Condensed (Oswald)":  "Headlines in condensed uppercase Oswald font, subtext in light sans-serif.",
            "Tall Caps (Bebas Neue)":     "Headlines in tall narrow all-caps Bebas Neue font, subtext in clean sans-serif.",
            "Professional (Lato)":        "All text in clean professional Lato font, lightweight and readable.",
            "Universal (Open Sans)":      "All text in highly readable Open Sans font, clean and universal.",
            "Warm Serif (Merriweather)":  "Headlines in warm trustworthy Merriweather serif font, subtext in light sans-serif.",
            "Geometric (Futura)":         "All text in geometric modern Futura font, clean and premium.",
            "Soft (Nunito Sans)":         "All text in soft approachable Nunito Sans font, friendly and warm.",
        }
        font_choice = st.selectbox("Font Style", list(font_styles.keys()))
        font_prompt = font_styles[font_choice]

        col_gp, col_rp = st.columns(2)
        generate_prompt_clicked   = col_gp.button("✦ Generate Prompt")
        regenerate_prompt_clicked = col_rp.button("🔄 New Style")

        def build_and_store(style, title, subtext, cta, font, layout):
            current_topic = topic if topic else st.session_state.get("last_topic", "")
            built, hl, ll, pl = _build_base_prompt(
                style, title, subtext, cta, font, layout,
                hair_gender=st.session_state["hair_gender"],
                is_hair_topic=is_hair_loss_topic(current_topic) if current_topic else False
            )
            lid = get_layout_id(layout)
            st.session_state["base_prompt"]    = built
            st.session_state["hair_label"]     = hl
            st.session_state["lighting_label"] = ll
            st.session_state["pose_label"]     = pl
            st.session_state["layout_id"]      = lid
            st.session_state["skeleton_square"]= generate_skeleton_preview(lid, title, subtext, cta, "square", pose_label=pl)
            st.session_state["skeleton_story"] = generate_skeleton_preview(lid, title, subtext, cta, "story", pose_label=pl)

        if regenerate_prompt_clicked:
            current_topic = topic if topic else st.session_state.get("last_topic", "healthcare")
            st.session_state["hair_gender"] = pick_hair_gender()
            st.session_state["generation_seed"] = random.randint(1, 999999)
            with st.spinner("Getting new visual style from Groq..."):
                try:
                    new_data   = call_groq(st.session_state["groq_key"], current_topic)
                    new_style  = new_data.get("visual_style", "")
                    new_layout = new_data.get("layout", LAYOUTS[0]["groq"])
                    if new_style:
                        st.session_state["ad_data"]["visual_style"] = new_style
                        st.session_state["ad_data"]["layout"]       = new_layout
                        build_and_store(new_style, edited_title, edited_subtext, edited_cta, font_prompt, new_layout)
                        st.rerun()
                    else:
                        st.error("Groq returned empty visual style.")
                except Exception as e:
                    st.error(f"Error: {e}")

        if generate_prompt_clicked:
            base_style  = st.session_state["ad_data"].get("visual_style", "")
            base_layout = st.session_state["ad_data"].get("layout", LAYOUTS[0]["groq"])
            build_and_store(base_style, edited_title, edited_subtext, edited_cta, font_prompt, base_layout)

        # SKELETON PREVIEWS
        if st.session_state["skeleton_square"] and st.session_state["skeleton_story"]:
            st.markdown("---")
            st.markdown("##### 🗂 Layout Preview")
            lid   = st.session_state["layout_id"]
            lname = next((l["name"] for l in LAYOUTS if l["id"] == lid), "")
            st.caption(f"**{lid}** — {lname}")
            sk1, sk2 = st.columns(2)
            with sk1:
                st.caption("📱 Feed 1080×1080")
                st.image(st.session_state["skeleton_square"], width=220)
            with sk2:
                st.caption("📲 Story 1080×1920")
                st.image(st.session_state["skeleton_story"], width=130)

            # Character details below skeleton
            hg_p = st.session_state.get("hair_gender")
            hl_p = st.session_state.get("hair_label")
            ll_p = st.session_state.get("lighting_label")
            pl_p = st.session_state.get("pose_label")
            if hg_p and hl_p:
                gender_icon = "👨" if hg_p == "male" else "👩"
                gender_word = "Male" if hg_p == "male" else "Female"
                st.markdown(
                    f"<div style='background:#f0f4ff;border:1px solid #c0ceff;border-radius:10px;"
                    f"padding:12px 16px;font-size:13px;color:#333;margin-top:10px'>"
                    f"<b>🎭 Character Details</b><br>"
                    f"&nbsp;&nbsp;{gender_icon} <b>Gender:</b> {gender_word}<br>"
                    f"&nbsp;&nbsp;💇 <b>Hair Style:</b> {hl_p}<br>"
                    f"&nbsp;&nbsp;💡 <b>Lighting:</b> {ll_p}<br>"
                    f"&nbsp;&nbsp;🤸 <b>Pose:</b> {pl_p}<br>"
                    f"&nbsp;&nbsp;🎬 <b>Style:</b> {'Raw Emotional Documentary' if hair_detected else 'Candid Lifestyle'}"
                    f"</div>",
                    unsafe_allow_html=True
                )

        if st.session_state["base_prompt"]:
            st.markdown("---")

            hg   = st.session_state["hair_gender"]
            hl   = st.session_state["hair_label"]
            ll   = st.session_state["lighting_label"]
            pl   = st.session_state.get("pose_label", "")
            seed = st.session_state.get("generation_seed", 42)

            if hg and hl:
                gw = "Male" if hg == "male" else "Female"
                bc = "#1a73e8" if hg == "male" else "#d81b60"
                pose_text = f" · Pose: <b>{pl}</b>" if pl else ""
                st.markdown(
                    f"<span style='background:{bc}15;color:{bc};border-radius:6px;padding:4px 10px;font-size:12px'>"
                    f"✅ {gw} · Hair: <b>{hl}</b> · Lighting: <b>{ll}</b>{pose_text} · 🎞 Raw Emotional</span>",
                    unsafe_allow_html=True
                )

            st.markdown(
                f"<span style='background:#f0f0f0;color:#666;border-radius:6px;"
                f"padding:3px 10px;font-size:11px;margin-left:6px'>"
                f"🌱 Seed: <b>{seed}</b></span>",
                unsafe_allow_html=True
            )
            st.markdown("")

            col_both, col_feed = st.columns(2)
            gen_both = col_both.button("✦ Generate Both (Feed + Story)")
            gen_feed = col_feed.button("✦ Feed Only (1080x1080)")

            if gen_feed:
                if not st.session_state.get("fal_key"):
                    st.error("Save your fal.ai API key in the sidebar.")
                else:
                    base = st.session_state["base_prompt"]
                    with st.status("Generating Feed...", expanded=True) as status:
                        try:
                            sq_prompt = (
                                "Square 1:1 format 1080x1080. "
                                "Compose for Instagram feed post — balanced square composition. "
                                "Person half-body or close-up, headline and CTA clearly visible. "
                                + base
                            )
                            sq_bytes = generate_and_stamp(sq_prompt, 1080, 1080, seed)
                            st.session_state["image_square"] = sq_bytes
                            st.session_state["image_story"] = None
                            status.update(label="Feed ready! ✅", state="complete")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            if gen_both:
                if not st.session_state.get("fal_key"):
                    st.error("Save your fal.ai API key in the sidebar.")
                else:
                    base = st.session_state["base_prompt"]
                    with st.status("Generating both formats...", expanded=True) as status:
                        try:
                            # ── Feed 1080×1080 ──
                            st.write(f"◈ Generating 1080×1080 Feed (seed: {seed})...")
                            sq_prompt = (
                                "Square 1:1 format 1080x1080. "
                                "Compose for Instagram feed post — balanced square composition. "
                                "Person half-body or close-up, headline and CTA clearly visible. "
                                + base
                            )
                            sq_bytes = generate_and_stamp(sq_prompt, 1080, 1080, seed)
                            st.session_state["image_square"] = sq_bytes
                            st.write("✅ Feed done!")

                            # ── Story 1080×1920 ──
                            # TEST: Same exact prompt, same seed, different dimensions only
                            # st.write(f"◈ Generating 1080×1920 Story (seed: {seed})...")
                            # st_bytes = generate_and_stamp(sq_prompt, 1080, 1920, seed)
                            # st.session_state["image_story"] = st_bytes
                            st.write(f"◈ Generating 1080×1920 Story (seed: {seed})...")

                            story_prompt = (
    "Vertical 9:16 format 1080x1920 FULL FRAME composition. "
    "The image MUST fill the entire frame edge-to-edge. "
    "NO empty space, NO borders, NO small centered image. "

    "Compose for Instagram Story/Reels — premium full-screen ad. "

    "STRICT COMPOSITION: "
    "Top 25% = headline area. "
    "Middle 50% = person. "
    "Bottom 25% = CTA area. "

    "Person must be large and dominant in frame, slightly lower positioned. "
    "Zoom appropriately so subject fills the frame naturally. "
    "NO small subject, NO distant framing. "

    "Person waist-up or full body, NOT cropped, face clearly visible. "

    "Face and hands must be high detail and perfectly formed. "
    "No distortion, no warped fingers, no artifacts. "

    "Headline large and bold at top with margin. "
    "Subtext below headline. "

    "CTA button fixed at bottom center with margin. "

    "Maintain full vertical coverage with strong composition hierarchy. "
    + base
)

                            st_bytes = generate_and_stamp(story_prompt, 1080, 1920, seed)
                            st.session_state["image_story"] = st_bytes
                            st.write("✅ Story done!")

                            status.update(label="Both images ready! ✅", state="complete")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    if st.session_state["image_square"] or st.session_state["image_story"]:
        st.markdown("---")
        st.markdown("##### 🖼 Generated Ads")
        seed = st.session_state.get("generation_seed", "?")
        st.caption(f"🌱 Both generated with seed **{seed}** — same person, same style")

        col_sq, col_st = st.columns(2)
        with col_sq:
            if st.session_state["image_square"]:
                st.caption("📱 Feed Post — 1080×1080")
                st.image(st.session_state["image_square"], width=300)
                st.download_button("⬇ Download Feed (1080×1080)",
                    data=st.session_state["image_square"],
                    file_name="meta_feed_1080x1080.jpg", mime="image/jpeg", key="dl_square")
        with col_st:
            if st.session_state["image_story"]:
                st.caption("📲 Story / Reels — 1080×1920")
                st.image(st.session_state["image_story"], width=170)
                st.download_button("⬇ Download Story (1080×1920)",
                    data=st.session_state["image_story"],
                    file_name="meta_story_1080x1920.jpg", mime="image/jpeg", key="dl_story")


# =============================================
# RIGHT — Chat
# =============================================
with right_col:
    st.markdown("### 💬 Creative Chat")
    st.markdown("<p style='color:#666;font-size:12px'>Paste a prompt, ask for edits, or describe what you want.</p>", unsafe_allow_html=True)

    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state["chat_messages"]:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-msg-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f"<div class='chat-msg-ai'>✦ {msg['content']}</div>", unsafe_allow_html=True)
            elif msg["role"] == "image":
                st.image(msg["content"], width=300)

    chat_input = st.text_input("Message", placeholder="e.g. 'generate an ad for hair fall'...",
                                key="chat_input", label_visibility="collapsed")
    col_send, col_gen = st.columns(2)
    send_clicked  = col_send.button("💬 Send")
    gen_from_chat = col_gen.button("✦ Generate from Chat")

    CHAT_SYSTEM = (
        "You are a creative assistant for Dr Batra's healthcare ad campaigns. "
        "App generates BOTH 1080x1080 (Feed) and 1080x1920 (Story) using SAME SEED. "
        "Clothing rule: always kurta or plain t-shirt — NO towel, NO revealing clothing. "
        "For HAIR LOSS: RAW EMOTIONAL DOCUMENTARY style. "
        "Male (50%): Norwood Stage 2, crown thinning. Female (50%): parting thinning. "
        "Always: Indian age 25-45, no medicine, photorealistic, no Meta text."
    )

    if send_clicked and chat_input:
        st.session_state["chat_messages"].append({"role": "user", "content": chat_input})
        if st.session_state.get("groq_key"):
            groq_messages = [{"role": "system", "content": CHAT_SYSTEM}]
            for msg in st.session_state["chat_messages"]:
                if msg["role"] in ["user", "assistant"]:
                    groq_messages.append({"role": msg["role"], "content": msg["content"]})
            with st.spinner("Thinking..."):
                try:
                    reply = call_groq_chat(st.session_state["groq_key"], groq_messages)
                    st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
                    st.session_state["chat_prompt"] = reply
                except Exception as e:
                    st.session_state["chat_messages"].append({"role": "assistant", "content": f"Error: {e}"})
            st.rerun()
        else:
            st.error("Save your Groq API key first.")

    if gen_from_chat:
        prompt_to_use = st.session_state.get("chat_prompt", "")
        if not prompt_to_use:
            for msg in reversed(st.session_state["chat_messages"]):
                if msg["role"] == "assistant":
                    prompt_to_use = msg["content"]
                    break
        if prompt_to_use and st.session_state.get("fal_key"):
            seed = random.randint(1, 999999)
            with st.spinner("Generating from chat..."):
                try:
                    img_bytes = generate_and_stamp(prompt_to_use, 1080, 1080, seed)
                    st.session_state["chat_messages"].append({"role": "image", "content": img_bytes})
                    st.session_state["image_square"] = img_bytes
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        elif not prompt_to_use:
            st.error("Send a message first to get a prompt.")
        else:
            st.error("Save your fal.ai API key first.")

    if st.button("🗑 Clear Chat", key="clear_chat"):
        st.session_state["chat_messages"] = []
        st.session_state["chat_prompt"] = ""
        st.rerun()


        # here the ouput hands n all getting chnaged
        