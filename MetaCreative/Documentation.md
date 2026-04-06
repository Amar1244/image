# Meta Creative Generator — Project Documentation

## Project Overview
An AI-powered static ad creative generator for Dr Batra's healthcare brand. The tool generates complete, ready-to-post Meta (Facebook/Instagram) ad creatives from a single topic input.

**Built by:** Amar  
**Tech Stack:** Python, Streamlit, Groq (LLaMA 3.3 70B), Flux 2 Pro (fal.ai), Pillow

---

## Architecture & Flow

```
USER enters topic (e.g. "PCOS treatment")
        |
        v
GROQ (LLaMA 3.3 70B) generates:
  - Title (punchy headline)
  - Subtext (supporting line)
  - CTA (call to action)
  - Visual Style (image description prompt)
        |
        v
USER reviews & edits all fields
        |
        v
PROMPT BUILDER combines:
  edited title + subtext + CTA + visual style + font + rules
        |
        v
FLUX 2 PRO renders the COMPLETE ad image
  (text, layout, person, background — all in one shot)
        |
        v
PILLOW stamps Dr Batra logo (top-right corner)
        |
        v
FINAL OUTPUT: 1080x1080 JPG ready to post
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| One-click generation | Enter topic, click generate, get complete ad |
| Editable ad copy | Title, subtext, CTA can be edited before image generation |
| Prompt review | User can review and edit the Flux prompt before generating |
| 18 font styles | Roboto, Impact, Playfair, Montserrat, Poppins, Arial Black, Oswald, Bebas Neue, Lato, Raleway, Open Sans, Merriweather, DM Serif, Futura, Abril Fatface, Nunito Sans, Josefin Sans, Handwritten Script |
| 35 text placement styles | Curved, angled, stacked, diagonal, centered, overlapping, banner, speech bubble, etc. |
| Auto logo stamping | Dr Batra logo.png stamped on every image automatically |
| Indian audience focus | All people in images are Indian, age 25-45 |
| Emotion matching | Expressions match the topic (frustration for problems, hope for solutions, confidence for results) |
| Bright color palettes | 12 vibrant color combinations for eye-catching ads |
| Design flair | Geometric shapes, gradients, dot patterns, glow effects for premium feel |

---

## Issues Faced & Solutions

### Issue 1: Generic/Boring Prompts
**Problem:** Initial prompts were too vague — "professional photo of person in clinic". Flux generated bland, repetitive images.

**Solution:** Built a detailed system prompt with specific instructions for:
- Subject description (age, ethnicity, clothing, expression)
- Lighting setup (golden hour, studio, natural light)
- Camera gear references (Canon R5, Sony A7IV)
- Composition rules (safe zones for text overlays)
- Negative instructions (no text, no watermarks)

**Result:** Much more varied, detailed, and professional images every time.

---

### Issue 2: Flux Rendering Text ON Photos (Overlay Approach)
**Problem:** Initially tried generating a plain photo with Flux, then overlaying text with Pillow (dark bars + headline + CTA). This looked like a basic 2015 Facebook ad — not like a real static creative.

**Solution:** Studied real Dr Batra static creatives and identified the actual design patterns:
- Split layouts (text top, photo bottom)
- Colored panels, not dark overlays
- Circular/rounded photo frames
- Decorative elements (dots, blobs, curves)

Built 8 Pillow templates matching real ad designs:
1. Circle Frame
2. Curved Split
3. Rounded Card
4. Side Blob
5. Border Frame
6. Photo Top + Text Bottom
7. Text Left + Photo Right
8. Photo Full + Overlay

**Result:** Better looking ads but still not matching the quality of real designs.

---

### Issue 3: Pillow Templates vs Flux Direct
**Problem:** Pillow templates were rigid and couldn't match the dynamic, organic feel of real static creatives. Too many edge cases, positioning issues, and font rendering limitations.

**Discovery:** Tested Flux 2 Pro with simple, direct prompts like:
```
"Struggling with irregular cycles?
Balance Hormones, Naturally Heal PCOS
add 2 girls and one cta make static creative"
```
Flux generated a COMPLETE, professional-looking ad creative in one shot — layout, text, person, CTA, everything.

**Solution:** Abandoned the Pillow overlay approach. Let Flux handle ALL text rendering and layout. Pillow only stamps the logo.

**Result:** Much better quality, more dynamic layouts, closer to real ad creatives.

---

### Issue 4: Text Spelling Errors
**Problem:** Flux sometimes misspells words, especially:
- Long words like "homeopathy" → "homeopatyraytry"
- CTA buttons → garbled text like "Püp peratrit Geu rarm"

**Solution:** 
- Added "clean sharp text rendering, no spelling errors" to prompt
- Repeated the exact CTA text in the prompt for emphasis
- Kept text short and simple (max 8 words headline, max 4 words CTA)

**Status:** Partially solved. Flux text rendering is ~80% accurate. Short text works better than long text.

---

### Issue 5: Duplicate CTA Buttons
**Problem:** CTA button ("Get Help") appeared TWICE in the generated image.

**Root Cause:** The prompt mentioned CTA 3 times — Flux interpreted this as "render it multiple times."

**Solution:** Reduced CTA mention to once with explicit instruction: "only ONE button, do not duplicate it."

**Result:** Fixed.

---

### Issue 6: Edited Text Not Matching Prompt
**Problem:** When user edited the title/CTA in the UI, the visual_style from Groq still contained the OLD text. So Flux saw two different headlines and rendered both.

**Example:**
- Groq generated visual_style with "Knee Pain Gone" inside it
- User changed title to "Get Rid Knee Pain"
- Prompt had both → Flux rendered both headlines

**Solution:** 
- Told Groq to NEVER include headline/CTA text inside visual_style
- visual_style now only describes the visual scene (people, lighting, setting)
- Text content is added separately from the edited fields

**Result:** Fixed. Edited text now always matches the generated image.

---

### Issue 7: Flux Adding "Meta" Text
**Problem:** Flux literally wrote "Meta" in the image because the prompt said "Meta ad creative."

**Solution:** Changed "Meta ad creative" to "social media ad creative" and added "Do not write the word Meta anywhere in the image."

**Result:** Fixed.

---

### Issue 8: Flux Adding Fake Copyright Text
**Problem:** Flux generated random copyright text at the bottom like "© Thdheirtion Sanvce Ean Enise."

**Solution:** Added "No copyright text, no watermark, no fake attribution text, no small print at bottom" to the prompt.

**Result:** Fixed.

---

### Issue 9: Logo White Background
**Problem:** Dr Batra logo.png has a white rectangular background that shows up on the image.

**Current Status:** Logo is stamped by Pillow. Needs a transparent PNG version of the logo for clean rendering.

**Recommendation:** Replace logo.png with a version that has a transparent background.

---

### Issue 10: Flux Adding Logo in Image + Pillow Adding Logo
**Problem:** Both Groq prompt and Pillow were adding logos — Groq told Flux to render "Dr Batra's logo at top-right" AND Pillow stamped the real logo. Result: double logo or AI-generated ugly logo.

**Solution:** Removed logo instruction from Groq prompt. Changed to "Leave top-right corner empty/clean (logo will be added separately)." Only Pillow stamps the real logo.

**Result:** Fixed. Clean logo placement every time.

---

### Issue 11: Non-Indian Faces
**Problem:** Flux was generating Caucasian/Western faces instead of Indian faces.

**Solution:** Added "All people MUST be Indian, age 25-45, with realistic skin texture" to both the Groq system prompt AND the Flux prompt.

**Result:** Fixed. All generated people are Indian.

---

### Issue 12: Medicine/Pills in Images
**Problem:** Flux was adding medicine bottles, pills, and medical equipment in healthcare ad images.

**Solution:** Added strict rule: "No medicine bottles, no pills, no tablets, no medical products, no syringes, no drugs in the image" to both Groq and Flux prompts.

**Result:** Fixed.

---

### Issue 13: American English / Formal Language
**Problem:** Groq generated overly formal American marketing language like "Unlock Your Path to Radiant Skin" — not relatable for Indian audience.

**Solution:** Added language instruction: "Write in simple, conversational Indian English — the way educated urban Indians speak. Avoid overly formal or American marketing jargon."

**Result:** Titles now sound natural and Indian — e.g. "Dandruff Won't Go?" instead of "Discover Your Journey to a Flake-Free Scalp."

---

### Issue 14: Same Layout Every Time
**Problem:** Flux kept generating the same text placement (headline top, CTA bottom) every time.

**Solution:** Added 35 text placement variations to the system prompt — curved, angled, stacked, diagonal, left-aligned, center, overlapping, banner, speech bubble, etc.

**Result:** Each generation now has a different layout. Much more variety.

---

### Issue 15: Dull/Muted Colors
**Problem:** Images had muted beige/brown tones — looked "premium" but boring in a social media feed.

**Solution:** Added 12 bright color palette options to the system prompt — bright pink, teal, coral, orange, purple + gold, sky blue, lavender, etc. Groq picks the right colors based on the topic mood.

**Result:** More vibrant, eye-catching ads that stand out in the feed.

---

## File Structure

```
MetaCreative/
├── main.py              <- Main app (all latest features)
├── app.py               <- Original backup (untouched)
├── logo.png             <- Dr Batra logo
├── requirements.txt     <- Python dependencies
└── Documentation.md     <- This file
```

---

## How to Run

```bash
cd MetaCreative
pip install -r requirements.txt
streamlit run main.py
```

---

## Dependencies

- streamlit
- requests
- Pillow
- fal-client
- python-dotenv

---

## API Keys Required

| Service | Purpose | Cost |
|---------|---------|------|
| Groq | LLM for ad copy generation (LLaMA 3.3 70B) | Free |
| fal.ai | Image generation (Flux 2 Pro) | ~$0.03/image |

---

## Complete Rules & System Prompt Breakdown

### 1. BRAND
- Brand: Dr Batra's healthcare
- Logo: Pillow stamps `logo.png` at top-right corner (not rendered by Flux)
- Flux is told to leave top-right corner empty/clean for logo placement

### 2. LANGUAGE
- Simple, conversational Indian English
- The way educated urban Indians speak
- No American marketing jargon
- Relatable and natural (e.g. "Dandruff Won't Go?" not "Unlock Your Flake-Free Journey")

### 3. AD COPY RULES
| Field | Max Length | Rule |
|-------|-----------|------|
| Title | 8 words | Punchy, emotional, highlights problem or benefit |
| Subtext | 15 words | Builds trust/curiosity, can reference homeopathy |
| CTA | 4 words | Action-driven, conversion-focused |

### 4. PEOPLE IN IMAGE
- All people must be **Indian, age 25-45**
- Realistic skin texture
- Expressions match the topic:
  - **Problem topics** (acne, hair loss) → frustration, concern, insecurity
  - **Solution topics** (treatment) → hope, relief, slight smile
  - **Result topics** (success) → confidence, happiness, direct eye contact
- Expressions must be natural, subtle, and instantly understandable

### 5. FRAMING / SUBJECT VARIATION
- Rotate between (DO NOT always use close-up):
  - **Half-body** (chest up — shows body language + face + outfit)
  - **Full-body** (person standing/sitting in environment, lifestyle context)
  - **Medium shot** (waist up, balanced between face and setting)
  - **Two-person shot** (doctor + patient, or friends together)
  - **Environmental portrait** (person small in frame, setting is prominent)
  - **Close-up** (face fills frame — USE RARELY)
- Number of people: 1 or 2 (varies)
- Face always clearly visible — never hidden behind objects
- Natural, candid composition — NOT stock photo feel

### 6. TEXT PLACEMENT (35 unique styles)
Examples of placements used:
- Headline curved at top-left, CTA pill button bottom-center
- Headline centered, CTA bottom-right
- Headline in diagonal banner, CTA pill bottom
- Headline large top-center, CTA floating bottom-left
- Headline curved arc above person's head, CTA with colored ribbon
- Headline stacked vertically on left side
- Headline bold at bottom-left overlapping image
- Headline inside colored circle/badge
- Headline on frosted glass overlay box
- Headline in speech bubble near person
- Headline on solid colored panel (left 40%), person on right
- Headline on white/beige card section at bottom
- Headline with vertical accent strip beside it
- Headline in two sizes (small question + BIG answer)
- ...and 20+ more variations
- **NEVER repeats the same placement twice**

### 7. DESIGN FLAIR (Scroll-stopping elements)
- Colored geometric shapes / abstract blobs in background
- Soft gradient overlays or color washes
- Decorative dot patterns / line accents
- Bold color contrast between text and background
- Depth / layered feel with foreground and background separation
- Glossy or polished finish, not flat or boring
- Warm glow or light leak effects for emotional warmth
- Must feel like a premium brand campaign

### 8. COLOR PALETTE (12 vibrant combinations)
| Colors | Mood | Best For |
|--------|------|----------|
| Bright pink/magenta + white | Bold, feminine | PCOS, skin, women's health |
| Teal/turquoise + white | Fresh, trustworthy | Hair care, wellness |
| Orange/coral + cream | Warm, energetic | CTA-focused ads |
| Deep purple + gold | Premium, luxury | Anti-aging, premium treatments |
| Bright green + white | Natural, fresh | Homeopathy, natural remedies |
| Red + white | Urgent, attention | Problem-focused ads |
| Sky blue + white | Clean, clinical trust | Doctor, clinic ads |
| Peach + cream | Soft, feminine, warm | Women's health |
| Coral + teal | Trendy, vibrant | Instagram-focused |
| Lavender + soft white | Gentle, soothing | Wellness, stress |
| Sunset orange + warm yellow | Optimistic, hopeful | Success stories |
| Navy blue + gold | Authority, premium | Specialist ads |

- **AVOID** dull, flat, or muted colors

### 9. STRICT RULES
- No medicine bottles, pills, tablets, syringes, or medical equipment
- No exaggerated claims or unrealistic results
- No copyright text, watermarks, or fake attribution
- No "Meta" text in image
- Text in image must be minimal (headline + CTA only)
- CTA: only ONE button — no duplicates
- Keep visuals authentic and trustworthy

### 10. STYLE VARIATION
Must use a different style each time:
- Lifestyle photography
- Minimalist clinic
- Bold typography
- Luxury dark theme
- Pastel wellness
- Editorial magazine
- Vibrant gradient
- Candid real-life moment
- **Never repeat styles**

### 11. FONT OPTIONS (18 styles)
| Font | Style |
|------|-------|
| Roboto | Clean modern sans-serif |
| Impact | Bold thick headlines |
| Playfair Display | Elegant serif |
| Montserrat | Thin minimal |
| Poppins | Rounded friendly |
| Arial Black | Classic bold |
| Handwritten Script | Calligraphy |
| Oswald | Condensed uppercase |
| Bebas Neue | Tall narrow all-caps |
| Lato | Professional lightweight |
| Raleway | Thin elegant |
| Open Sans | Universal readable |
| Merriweather | Warm trustworthy serif |
| DM Serif Display | Bold editorial |
| Futura | Geometric modern |
| Abril Fatface | Dramatic attention-grabbing |
| Nunito Sans | Soft approachable |
| Josefin Sans | Stylish geometric thin |

### 12. TECHNICAL SPECS
- Output size: 1080x1080 (Meta feed format)
- 100% photorealistic — real human faces, real photography
- Not AI-looking
- Clean sharp text rendering
- No spelling errors

---

## System Prompt Components Summary

| Component | Purpose |
|-----------|---------|
| EMOTION LOGIC | Matches facial expressions to topic mood |
| LAYOUT LOGIC | Dynamic text placement, not fixed positions |
| TEXT PLACEMENT VARIATION | 35 unique text/CTA placement styles |
| SUBJECT VARIATION | 1-2 people, half-body/full-body/medium/close-up framing |
| DESIGN FLAIR | Geometric shapes, gradients, dot patterns, glow effects |
| COLOR PALETTE | 12 bright, vibrant color combinations |
| LANGUAGE | Simple conversational Indian English |
| STRICT RULES | No medicine, no Meta text, no copyright, no watermarks |
| FONT OPTIONS | 18 font styles user can choose from |

---

## App Features

### Left Side — Ad Workflow
1. **Generate Ideas** — Groq generates title, subtext, CTA, visual style from topic
2. **Edit Ad Copy** — User can modify title, subtext, CTA before generating
3. **Font Selection** — 18 font styles to choose from
4. **Generate Prompt / New Style** — Build prompt or regenerate with completely new visual style
5. **Review Prompt** — User can review and manually edit the full Flux prompt
6. **Generate Image** — Flux 2 Pro renders the complete ad
7. **Logo Stamping** — Pillow adds Dr Batra logo at top-right
8. **Download** — Save as JPG

### Right Side — Creative Chat
1. **Direct prompt generation** — "generate an ad for hair fall" → AI writes Flux prompt
2. **Edit instructions** — "make it more vibrant" → AI updates the prompt
3. **Describe image** — "how will the image look?" → AI describes in simple words
4. **Prompt analysis** — Paste a prompt → AI suggests improvements
5. **Generate from Chat** — Use AI's response as a Flux prompt directly
6. **Chat history** — Full conversation preserved

---

## Known Limitations

1. **Text Spelling:** Flux 2 Pro sometimes misspells words (~80% accuracy). Short text works better than long text.
2. **Logo Transparency:** Current logo.png has white background. Needs transparent PNG for clean rendering.
3. **CTA Consistency:** CTA button sometimes doesn't render or gets duplicated. Reduced by limiting CTA mention to once in prompt.
4. **Font Control:** Flux approximates font styles but can't load actual font files. Font hints guide the style but aren't pixel-perfect.
5. **No Edit Without Regeneration:** Changing text requires full image regeneration. Flux 2 Pro Edit endpoint exists but not yet integrated.
6. **Same Image Different Size:** Cannot generate the exact same image in a different size. Each generation is unique.
7. **Local Language Scripts:** Hindi (Devanagari), Tamil, Bengali scripts cannot be rendered by Flux. Would need Pillow hybrid approach.

---

## Future Improvements

- [ ] Transparent logo support (auto-remove white background)
- [ ] Flux 2 Pro Edit integration for post-generation text edits
- [ ] Multiple image variations in one click
- [ ] A/B testing support (generate 2 versions side by side)
- [ ] Hindi/regional language text support via Pillow overlay
- [ ] Template library (save and reuse successful layouts)
- [ ] Image resize/reformat (1080x1080 → 1080x1920 story format)
- [ ] Image history / gallery of past generations
- [ ] Batch generation (multiple topics at once)
- [ ] Edit text on existing images

---

## Iterations Summary

| Version | Approach | Outcome |
|---------|----------|---------|
| V1 | Flux photo + Pillow dark overlay text | Basic, looked amateur |
| V2 | Flux photo + Pillow split templates (8 layouts) | Better but rigid, didn't match real ad designs |
| V3 | Flux generates EVERYTHING + Pillow logo only (current) | Best quality, most dynamic, closest to real ads |
| V3.1 | Added chat assistant, editable ad copy, regenerate style | Full creative workflow with AI chat support |

---

*Document created: April 2, 2026*
*Last updated: April 2, 2026*
