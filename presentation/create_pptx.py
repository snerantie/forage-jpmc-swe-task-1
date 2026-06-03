"""
AI Tutor South Africa - PowerPoint Presentation Generator
=========================================================
Generates a visually attractive .pptx file for hackathon finals.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
import os

# Brand colors
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)       # Deep navy
ACCENT_BLUE = RGBColor(0x16, 0x21, 0x3E)    # Dark blue
BRIGHT_BLUE = RGBColor(0x0F, 0x3D, 0x6B)    # Medium blue
GREEN = RGBColor(0x00, 0xB4, 0x5A)          # SA green
GOLD = RGBColor(0xFF, 0xB8, 0x1C)           # SA gold
RED = RGBColor(0xDE, 0x35, 0x31)            # SA red
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xE8, 0xE8, 0xE8)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
TEAL = RGBColor(0x00, 0x89, 0x9B)
PURPLE = RGBColor(0x6C, 0x5C, 0xE7)
ORANGE = RGBColor(0xFF, 0x6B, 0x35)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)



def add_bg(slide, color=DARK_BG):
    """Set slide background color"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, left, top, width, height, color, opacity=1.0):
    """Add a colored rectangle shape"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18,
                 color=WHITE, bold=False, align=PP_ALIGN.LEFT, font_name='Segoe UI'):
    """Add a text box with styling"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_paragraph(text_frame, text, font_size=16, color=WHITE, bold=False,
                  align=PP_ALIGN.LEFT, space_before=Pt(6)):
    """Add a paragraph to existing text frame"""
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = 'Segoe UI'
    p.alignment = align
    p.space_before = space_before
    return p



# ============================================================
# SLIDE 1: TITLE SLIDE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_bg(slide, DARK_BG)

# Gradient accent bar at top
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

# Title
add_text_box(slide, Inches(1), Inches(1.5), Inches(11), Inches(1.2),
             "AI TUTOR SOUTH AFRICA", font_size=54, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER)

# SA Flag emoji + tagline
add_text_box(slide, Inches(1), Inches(2.8), Inches(11), Inches(0.8),
             "Teaching Students HOW to Think, Not WHAT to Think",
             font_size=28, color=GOLD, align=PP_ALIGN.CENTER)

# Subjects line
add_text_box(slide, Inches(1), Inches(4.0), Inches(11), Inches(0.6),
             "Mathematics  |  Physics  |  Accounting",
             font_size=20, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Grade + Curriculum
add_text_box(slide, Inches(1), Inches(4.6), Inches(11), Inches(0.6),
             "Grades 1-12  |  CAPS & IEB Curriculum",
             font_size=18, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Channels
add_text_box(slide, Inches(1), Inches(5.2), Inches(11), Inches(0.6),
             "WhatsApp + USSD  |  Zero-Rated on Vodacom",
             font_size=18, color=GREEN, align=PP_ALIGN.CENTER)

# Bottom bar
add_shape_bg(slide, Inches(0), Inches(7.0), Inches(13.333), Inches(0.5), ACCENT_BLUE)
add_text_box(slide, Inches(1), Inches(7.05), Inches(11), Inches(0.4),
             "Hackathon Finals Presentation",
             font_size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 2: THE PROBLEM
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), RED)

add_text_box(slide, Inches(0.5), Inches(0.4), Inches(12), Inches(0.8),
             "THE PROBLEM", font_size=40, color=RED, bold=True, align=PP_ALIGN.LEFT)

add_text_box(slide, Inches(0.5), Inches(1.2), Inches(12), Inches(0.6),
             "South Africa's Mathematics Education Crisis",
             font_size=24, color=GOLD, align=PP_ALIGN.LEFT)

# Stats in boxes
stats = [
    ("Only 37%", "of Grade 9 learners\npassed mathematics", RED),
    ("40:1", "Learner-to-teacher\nratio in many schools", ORANGE),
    ("R200-R500/hr", "Cost of private\ntutoring", GOLD),
    ("60%+", "Learners can't afford\ndata for online learning", TEAL),
]

for i, (stat, desc, color) in enumerate(stats):
    left = Inches(0.5 + i * 3.2)
    top = Inches(2.2)
    # Card background
    card = add_shape_bg(slide, left, top, Inches(2.9), Inches(2.8), ACCENT_BLUE)
    card.shadow.inherit = False
    # Stat number
    add_text_box(slide, left + Inches(0.2), top + Inches(0.3), Inches(2.5), Inches(0.8),
                 stat, font_size=32, color=color, bold=True, align=PP_ALIGN.CENTER)
    # Description
    add_text_box(slide, left + Inches(0.2), top + Inches(1.3), Inches(2.5), Inches(1.2),
                 desc, font_size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Bottom question
add_text_box(slide, Inches(0.5), Inches(5.5), Inches(12), Inches(0.8),
             "How do we provide QUALITY tutoring to EVERY learner?",
             font_size=24, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

# Additional context
add_text_box(slide, Inches(0.5), Inches(6.3), Inches(12), Inches(0.6),
             "Language barriers  |  Rural access  |  Device limitations  |  Data costs",
             font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 3: OUR SOLUTION
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

add_text_box(slide, Inches(0.5), Inches(0.4), Inches(12), Inches(0.8),
             "OUR SOLUTION", font_size=40, color=GREEN, bold=True)

# Comparison
add_shape_bg(slide, Inches(0.5), Inches(1.5), Inches(5.8), Inches(2.0), RGBColor(0x3D, 0x15, 0x15))
add_text_box(slide, Inches(0.7), Inches(1.6), Inches(5.4), Inches(0.5),
             "TRADITIONAL AI TUTORS", font_size=16, color=RED, bold=True)
add_text_box(slide, Inches(0.7), Inches(2.1), Inches(5.4), Inches(1.2),
             '"The answer is x = 4"\n\nJust gives the answer. Learner doesn\'t\nunderstand WHY or HOW.',
             font_size=14, color=LIGHT_GRAY)

add_shape_bg(slide, Inches(7), Inches(1.5), Inches(5.8), Inches(2.0), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(7.2), Inches(1.6), Inches(5.4), Inches(0.5),
             "AI TUTOR SOUTH AFRICA", font_size=16, color=GREEN, bold=True)
add_text_box(slide, Inches(7.2), Inches(2.1), Inches(5.4), Inches(1.2),
             '"Interesting approach! Think of it like a\nbalance scale. What\'s in the way of x?"\n\nGuides learner to DISCOVER the answer.',
             font_size=14, color=LIGHT_GRAY)

# Three pillars
pillars = [
    ("REASONING\nANALYSIS", "Analyzes HOW\nlearners think", TEAL),
    ("PERSONALIZED\nHINTS", "Progressive guidance\ntailored to level", PURPLE),
    ("PROGRESS\nTRACKING", "Track improvement\nover time", GOLD),
]

for i, (title, desc, color) in enumerate(pillars):
    left = Inches(0.5 + i * 4.3)
    top = Inches(4.0)
    card = add_shape_bg(slide, left, top, Inches(3.8), Inches(2.5), ACCENT_BLUE)
    add_text_box(slide, left + Inches(0.3), top + Inches(0.3), Inches(3.2), Inches(1.0),
                 title, font_size=18, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text_box(slide, left + Inches(0.3), top + Inches(1.4), Inches(3.2), Inches(1.0),
                 desc, font_size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text_box(slide, Inches(0.5), Inches(6.7), Inches(12), Inches(0.5),
             "We analyze HOW learners think, not just WHAT they answer",
             font_size=18, color=WHITE, bold=True, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 4: THE INNOVATION - REASONING ANALYSIS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), TEAL)

add_text_box(slide, Inches(0.5), Inches(0.4), Inches(12), Inches(0.8),
             "THE INNOVATION: Reasoning Analysis", font_size=36, color=TEAL, bold=True)

# Problem box
add_shape_bg(slide, Inches(0.5), Inches(1.4), Inches(5.5), Inches(0.7), BRIGHT_BLUE)
add_text_box(slide, Inches(0.7), Inches(1.45), Inches(5.1), Inches(0.6),
             "PROBLEM:  2x + 5 = 13", font_size=20, color=WHITE, bold=True)

# Learner response
add_shape_bg(slide, Inches(0.5), Inches(2.3), Inches(5.5), Inches(1.0), RGBColor(0x3D, 0x15, 0x15))
add_text_box(slide, Inches(0.7), Inches(2.35), Inches(5.1), Inches(0.4),
             "LEARNER SAYS:", font_size=12, color=RED, bold=True)
add_text_box(slide, Inches(0.7), Inches(2.7), Inches(5.1), Inches(0.5),
             '"I think I should add 13 and 5 together"', font_size=15, color=WHITE)

# Analysis box
add_shape_bg(slide, Inches(0.5), Inches(3.6), Inches(5.5), Inches(3.2), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(3.7), Inches(5.1), Inches(0.4),
             "AI REASONING ANALYSIS:", font_size=12, color=TEAL, bold=True)

txBox = slide.shapes.add_textbox(Inches(0.7), Inches(4.1), Inches(5.1), Inches(2.6))
tf = txBox.text_frame
tf.word_wrap = True
analysis_items = [
    ("Misconception:", "inverse_operation_confusion", GOLD),
    ("Reasoning Gap:", "Treating equation as L-to-R calculation", WHITE),
    ("Severity:", "foundational", RED),
    ("Confidence:", "85%", GREEN),
    ("Concepts:", "equation_balance, inverse_operations", LIGHT_GRAY),
]
for label, value, color in analysis_items:
    p = tf.add_paragraph()
    p.text = f"{label}  {value}"
    p.font.size = Pt(13)
    p.font.color.rgb = color
    p.font.name = 'Segoe UI'
    p.space_before = Pt(8)

# Right side - AI Response
add_shape_bg(slide, Inches(6.5), Inches(1.4), Inches(6.3), Inches(5.4), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(6.7), Inches(1.5), Inches(5.9), Inches(0.4),
             "AI TUTOR RESPONDS (Socratic Method):", font_size=12, color=GREEN, bold=True)

txBox2 = slide.shapes.add_textbox(Inches(6.7), Inches(2.0), Inches(5.9), Inches(4.5))
tf2 = txBox2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = '"Interesting thinking! Let me help you see this differently.'
p.font.size = Pt(15)
p.font.color.rgb = WHITE
p.font.name = 'Segoe UI'
add_paragraph(tf2, '', font_size=8)
add_paragraph(tf2, 'An equation is like a balance scale.', font_size=15, color=WHITE)
add_paragraph(tf2, 'You have 2x + 5 on the left, and 13 on the right.', font_size=15, color=WHITE)
add_paragraph(tf2, '', font_size=8)
add_paragraph(tf2, 'If you add 13 and 5, which side would change?', font_size=15, color=GOLD)
add_paragraph(tf2, '', font_size=8)
add_paragraph(tf2, 'Think about it: We want to get x by itself.', font_size=15, color=WHITE)
add_paragraph(tf2, "What's 'in the way' of x?", font_size=15, color=GREEN, bold=True)

add_text_box(slide, Inches(0.5), Inches(7.0), Inches(12), Inches(0.4),
             "We guide learners to DISCOVER answers through questions - never giving solutions directly",
             font_size=14, color=GOLD, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 5: SYSTEM ARCHITECTURE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), PURPLE)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "SYSTEM ARCHITECTURE", font_size=36, color=PURPLE, bold=True)

# Layer 1 - Interaction
add_shape_bg(slide, Inches(0.5), Inches(1.2), Inches(12.3), Inches(1.2), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(1.25), Inches(4), Inches(0.4),
             "LEARNER INTERACTION LAYER", font_size=11, color=TEAL, bold=True)
add_text_box(slide, Inches(1.5), Inches(1.65), Inches(4), Inches(0.6),
             "WhatsApp Channel\n(Smartphones, rich media)", font_size=13, color=WHITE)
add_text_box(slide, Inches(7.5), Inches(1.65), Inches(4), Inches(0.6),
             "USSD Channel\n(Any phone, text-only)", font_size=13, color=WHITE)

# Layer 2 - API
add_shape_bg(slide, Inches(3), Inches(2.6), Inches(7.3), Inches(0.7), BRIGHT_BLUE)
add_text_box(slide, Inches(3.2), Inches(2.65), Inches(7), Inches(0.6),
             "API GATEWAY  (Zero-Rated Endpoints on Vodacom)",
             font_size=13, color=GREEN, bold=True, align=PP_ALIGN.CENTER)

# Layer 3 - Engine
add_shape_bg(slide, Inches(0.5), Inches(3.5), Inches(12.3), Inches(1.6), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(3.55), Inches(4), Inches(0.4),
             "AI TUTOR ENGINE (AWS Lambda)", font_size=11, color=TEAL, bold=True)

engine_items = [
    ("Reasoning\nAnalyzer", TEAL),
    ("Hint\nEngine", PURPLE),
    ("Progress\nTracker", GOLD),
    ("Session\nManager", ORANGE),
]
for i, (name, color) in enumerate(engine_items):
    left = Inches(1.0 + i * 3.0)
    add_shape_bg(slide, left, Inches(4.0), Inches(2.5), Inches(0.9), color)
    add_text_box(slide, left + Inches(0.1), Inches(4.02), Inches(2.3), Inches(0.85),
                 name, font_size=12, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

# Layer 4 - Bedrock
add_shape_bg(slide, Inches(0.5), Inches(5.3), Inches(12.3), Inches(1.0), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(5.35), Inches(4), Inches(0.4),
             "AWS BEDROCK", font_size=11, color=GOLD, bold=True)

bedrock_items = [
    ("Claude 3.5 Sonnet\n(Primary AI)", GREEN),
    ("Knowledge Base\n(CAPS/IEB Curriculum)", TEAL),
    ("Guardrails\n(Content Safety)", RED),
]
for i, (name, color) in enumerate(bedrock_items):
    left = Inches(1.0 + i * 4.0)
    add_shape_bg(slide, left, Inches(5.75), Inches(3.5), Inches(0.45), color)
    add_text_box(slide, left + Inches(0.1), Inches(5.76), Inches(3.3), Inches(0.4),
                 name, font_size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

# Layer 5 - Data
add_shape_bg(slide, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.8), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(6.55), Inches(3), Inches(0.4),
             "DATA LAYER", font_size=11, color=GOLD, bold=True)
add_text_box(slide, Inches(1.5), Inches(6.82), Inches(5), Inches(0.4),
             "DynamoDB (Learner Profiles & Progress)", font_size=12, color=WHITE)
add_text_box(slide, Inches(7.5), Inches(6.82), Inches(5), Inches(0.4),
             "S3 (Curriculum Resources)", font_size=12, color=WHITE)



# ============================================================
# SLIDE 6: WHATSAPP DEMO FLOW
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "WHATSAPP EXPERIENCE", font_size=36, color=GREEN, bold=True)

# Chat bubbles - left side (learner) and right side (tutor)
chats = [
    ("learner", "Hi", Inches(1.2)),
    ("tutor", "Hello Thabo! Welcome to AI Tutor!\nWhat would you like help with today?", Inches(1.8)),
    ("learner", "Help me solve: 2x + 5 = 13", Inches(3.0)),
    ("tutor", "Great question! Tell me: What do you think\nis the first step?", Inches(3.6)),
    ("learner", "I think I should add 13 and 5 together", Inches(4.8)),
    ("tutor", "Interesting thinking! Think of it like a\nbalance scale. What's 'in the way' of x?", Inches(5.4)),
]

for sender, text, top in chats:
    if sender == "learner":
        left = Inches(0.5)
        bg_color = BRIGHT_BLUE
        add_shape_bg(slide, left, top, Inches(5.5), Inches(0.55) if '\n' not in text else Inches(0.9), bg_color)
        add_text_box(slide, left + Inches(0.2), top + Inches(0.02), Inches(5.1), Inches(0.5),
                     f"Learner: {text}", font_size=12, color=WHITE)
    else:
        left = Inches(6.5)
        bg_color = RGBColor(0x0A, 0x3D, 0x1A)
        h = Inches(0.55) if '\n' not in text else Inches(0.9)
        add_shape_bg(slide, left, top, Inches(6.3), h, bg_color)
        add_text_box(slide, left + Inches(0.2), top + Inches(0.02), Inches(5.9), h,
                     f"AI Tutor: {text}", font_size=12, color=WHITE)

# Key insight box
add_shape_bg(slide, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.8), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(6.6), Inches(11.9), Inches(0.6),
             "KEY: The AI detected a misconception and guided the learner with a question - NEVER giving the answer directly!",
             font_size=15, color=GOLD, bold=True, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 7: USSD DEMO FLOW
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), ORANGE)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "USSD EXPERIENCE - Works on ANY Phone", font_size=36, color=ORANGE, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "Dial: *120*TUTOR#    |    No smartphone needed    |    No data needed",
             font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# USSD screens
screens = [
    ("Welcome to AI Tutor!\n1. Mathematics\n2. Help\n3. My Progress", "User dials *120*TUTOR#"),
    ("Select your grade:\n1. Gr 1-3\n2. Gr 4-6\n3. Gr 7-9\n4. Gr 10-12", "User inputs: 1"),
    ("Topic:\n1. Algebra\n2. Calculus\n3. Trigonometry\n4. Functions", "User inputs: 4"),
    ("Practice:\nSolve: 2x = 10\nWhat is x?\n\nReply with number:", "User inputs: 1"),
]

for i, (screen_text, action) in enumerate(screens):
    left = Inches(0.3 + i * 3.3)
    top = Inches(1.8)
    # Phone frame
    add_shape_bg(slide, left, top, Inches(3.0), Inches(3.8), RGBColor(0x2A, 0x2A, 0x2A))
    # Screen
    add_shape_bg(slide, left + Inches(0.15), top + Inches(0.15), Inches(2.7), Inches(3.0), RGBColor(0x0A, 0x0A, 0x0A))
    # Screen text
    add_text_box(slide, left + Inches(0.25), top + Inches(0.3), Inches(2.5), Inches(2.7),
                 screen_text, font_size=11, color=GREEN)
    # Action label
    add_text_box(slide, left, top + Inches(3.25), Inches(3.0), Inches(0.4),
                 action, font_size=10, color=GOLD, align=PP_ALIGN.CENTER)

# Bottom highlights
add_shape_bg(slide, Inches(0.5), Inches(6.2), Inches(5.8), Inches(1.0), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(6.3), Inches(5.4), Inches(0.8),
             "Works on Nokia 3310, Samsung feature phones,\nand ANY device that supports USSD",
             font_size=14, color=WHITE, align=PP_ALIGN.CENTER)

add_shape_bg(slide, Inches(7.0), Inches(6.2), Inches(5.8), Inches(1.0), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(7.2), Inches(6.3), Inches(5.4), Inches(0.8),
             "Zero-rated on Vodacom network\nNo data deducted from learner's balance!",
             font_size=14, color=GREEN, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 8: PROGRESSIVE HINT SYSTEM
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), PURPLE)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "PROGRESSIVE HINT SYSTEM", font_size=36, color=PURPLE, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "Hints get MORE specific as learner needs more help - but NEVER give the answer",
             font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Four levels
levels = [
    ("LEVEL 1", "Probing Question", '"What do you think is\nthe first step?"', TEAL, "Understand thinking"),
    ("LEVEL 2", "Conceptual Hint", '"Think of a balance scale.\nWhat\'s in the way of x?"', PURPLE, "Provide mental model"),
    ("LEVEL 3", "Procedural Hint", '"Try subtracting 5 from\nBOTH sides. What do you get?"', GOLD, "Guide specific action"),
    ("LEVEL 4", "Worked Example", '"Let me show a similar problem:\n3x + 7 = 19 ..."', ORANGE, "Model the process"),
]

for i, (level, title, example, color, goal) in enumerate(levels):
    top = Inches(1.7 + i * 1.35)
    # Level indicator
    add_shape_bg(slide, Inches(0.5), top, Inches(1.5), Inches(1.1), color)
    add_text_box(slide, Inches(0.55), top + Inches(0.1), Inches(1.4), Inches(0.5),
                 level, font_size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(0.55), top + Inches(0.55), Inches(1.4), Inches(0.5),
                 title, font_size=10, color=WHITE, align=PP_ALIGN.CENTER)
    # Example
    add_shape_bg(slide, Inches(2.2), top, Inches(7.0), Inches(1.1), ACCENT_BLUE)
    add_text_box(slide, Inches(2.4), top + Inches(0.15), Inches(6.6), Inches(0.9),
                 example, font_size=13, color=WHITE)
    # Goal
    add_shape_bg(slide, Inches(9.5), top, Inches(3.3), Inches(1.1), BRIGHT_BLUE)
    add_text_box(slide, Inches(9.7), top + Inches(0.25), Inches(2.9), Inches(0.6),
                 f"Goal: {goal}", font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Arrow indicators between levels
for i in range(3):
    top = Inches(2.85 + i * 1.35)
    add_text_box(slide, Inches(1.0), top, Inches(0.5), Inches(0.3),
                 "v", font_size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text_box(slide, Inches(0.5), Inches(7.0), Inches(12), Inches(0.4),
             "Learners EARN the answer through guided discovery - building real understanding",
             font_size=15, color=GOLD, bold=True, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 9: PROGRESS TRACKING
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GOLD)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "PROGRESS TRACKING & GAMIFICATION", font_size=36, color=GOLD, bold=True)

# Left side - Progress report
add_shape_bg(slide, Inches(0.5), Inches(1.3), Inches(6.0), Inches(5.8), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(1.4), Inches(5.6), Inches(0.5),
             "Your Progress Report", font_size=18, color=WHITE, bold=True)

progress_items = [
    ("Problems Attempted:", "12", WHITE),
    ("Problems Solved:", "9", GREEN),
    ("Accuracy:", "75%", GOLD),
    ("Current Streak:", "3 correct!", ORANGE),
    ("", "", WHITE),
    ("Topics Covered:", "", TEAL),
    ("  - Linear Equations", "80%", GREEN),
    ("  - Fractions", "60%", GOLD),
    ("  - Algebra", "40%", ORANGE),
    ("", "", WHITE),
    ("Keep Practicing:", "Word Problems", RED),
]

txBox = slide.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.2), Inches(4.8))
tf = txBox.text_frame
tf.word_wrap = True
for label, value, color in progress_items:
    p = tf.add_paragraph()
    p.text = f"{label}  {value}" if value else label
    p.font.size = Pt(14)
    p.font.color.rgb = color
    p.font.name = 'Segoe UI'
    p.space_before = Pt(4)

# Right side - Achievements
add_shape_bg(slide, Inches(7.0), Inches(1.3), Inches(5.8), Inches(2.5), ACCENT_BLUE)
add_text_box(slide, Inches(7.2), Inches(1.4), Inches(5.4), Inches(0.5),
             "ACHIEVEMENTS", font_size=18, color=GOLD, bold=True)

achievements = [
    ("First Step", "Solved first problem", GREEN),
    ("Getting Started", "Attempted 10 problems", TEAL),
    ("On Fire!", "5 correct in a row", ORANGE),
    ("Unstoppable!", "10 correct in a row", RED),
]
for i, (title, desc, color) in enumerate(achievements):
    top = Inches(2.0 + i * 0.45)
    add_text_box(slide, Inches(7.4), top, Inches(2.5), Inches(0.4),
                 title, font_size=13, color=color, bold=True)
    add_text_box(slide, Inches(9.9), top, Inches(2.7), Inches(0.4),
                 desc, font_size=12, color=LIGHT_GRAY)

# Features box
add_shape_bg(slide, Inches(7.0), Inches(4.0), Inches(5.8), Inches(3.1), ACCENT_BLUE)
add_text_box(slide, Inches(7.2), Inches(4.1), Inches(5.4), Inches(0.5),
             "SMART FEATURES", font_size=18, color=TEAL, bold=True)

features = [
    "Identifies weak areas automatically",
    "Adapts difficulty based on performance",
    "Celebrates milestones and streaks",
    "Weekly parent/guardian progress reports",
    "Teacher dashboard (planned)",
]
txBox2 = slide.shapes.add_textbox(Inches(7.4), Inches(4.6), Inches(5.2), Inches(2.4))
tf2 = txBox2.text_frame
tf2.word_wrap = True
for feat in features:
    p = tf2.add_paragraph()
    p.text = f"  {feat}"
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(6)



# ============================================================
# SLIDE 10: MULTI-LANGUAGE SUPPORT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), TEAL)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "MULTI-LANGUAGE SUPPORT", font_size=36, color=TEAL, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "AI Tutor speaks the learner's home language!",
             font_size=18, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Language examples
languages = [
    ("English", '"What do you think is the first step?"', GREEN),
    ("IsiZulu", '"Ucabanga ukuthi yisiphi isinyathelo sokuqala?"', GOLD),
    ("IsiXhosa", '"Ucinga ukuba yeyiphi inyathelo lokuqala?"', TEAL),
    ("Afrikaans", '"Wat dink jy is die eerste stap?"', ORANGE),
    ("Sepedi", '"O nagana gore ke mohato ofe wa pele?"', PURPLE),
    ("Setswana", '"O akanya gore ke kgato efe ya ntlha?"', RED),
]

for i, (lang, text, color) in enumerate(languages):
    top = Inches(1.7 + i * 0.85)
    # Language label
    add_shape_bg(slide, Inches(0.5), top, Inches(2.0), Inches(0.65), color)
    add_text_box(slide, Inches(0.6), top + Inches(0.1), Inches(1.8), Inches(0.5),
                 lang, font_size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    # Text example
    add_shape_bg(slide, Inches(2.7), top, Inches(10.1), Inches(0.65), ACCENT_BLUE)
    add_text_box(slide, Inches(2.9), top + Inches(0.1), Inches(9.7), Inches(0.5),
                 text, font_size=14, color=WHITE)

# Bottom insight
add_shape_bg(slide, Inches(1.0), Inches(6.8), Inches(11.3), Inches(0.5), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(1.2), Inches(6.85), Inches(10.9), Inches(0.4),
             "Research shows: Learning in mother tongue improves comprehension by 40%",
             font_size=15, color=GREEN, bold=True, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 11: ZERO-RATING
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "ZERO-RATED ON VODACOM", font_size=36, color=GREEN, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "NO DATA COSTS for Vodacom users - completely FREE to access!",
             font_size=20, color=GOLD, align=PP_ALIGN.CENTER)

# Before vs After
add_shape_bg(slide, Inches(0.5), Inches(1.8), Inches(5.8), Inches(3.5), RGBColor(0x3D, 0x15, 0x15))
add_text_box(slide, Inches(0.7), Inches(1.9), Inches(5.4), Inches(0.5),
             "BEFORE (Other platforms)", font_size=16, color=RED, bold=True)

before_items = [
    "R50-R200/month data costs",
    "Data runs out mid-lesson",
    "Can't afford data = can't learn",
    "Only accessible with WiFi",
    "Smartphone required",
]
txBox = slide.shapes.add_textbox(Inches(0.9), Inches(2.5), Inches(5.2), Inches(2.5))
tf = txBox.text_frame
tf.word_wrap = True
for item in before_items:
    p = tf.add_paragraph()
    p.text = f"  {item}"
    p.font.size = Pt(14)
    p.font.color.rgb = LIGHT_GRAY
    p.font.name = 'Segoe UI'
    p.space_before = Pt(8)

add_shape_bg(slide, Inches(7.0), Inches(1.8), Inches(5.8), Inches(3.5), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(7.2), Inches(1.9), Inches(5.4), Inches(0.5),
             "AFTER (AI Tutor SA)", font_size=16, color=GREEN, bold=True)

after_items = [
    "R0/month - completely FREE",
    "Always available, never runs out",
    "Every learner can access",
    "Works with R0 airtime balance",
    "Works on ANY phone (USSD)",
]
txBox = slide.shapes.add_textbox(Inches(7.4), Inches(2.5), Inches(5.2), Inches(2.5))
tf = txBox.text_frame
tf.word_wrap = True
for item in after_items:
    p = tf.add_paragraph()
    p.text = f"  {item}"
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(8)

# How it works
add_shape_bg(slide, Inches(0.5), Inches(5.6), Inches(12.3), Inches(1.7), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(5.7), Inches(11.9), Inches(0.4),
             "HOW ZERO-RATING WORKS:", font_size=14, color=TEAL, bold=True)

how_items = [
    "1. Our API endpoints are registered and whitelisted by Vodacom",
    "2. Requests from Vodacom network are identified and routed free of charge",
    "3. No data is deducted from the learner's balance",
    "4. 43 million Vodacom subscribers can access for FREE",
]
txBox = slide.shapes.add_textbox(Inches(0.9), Inches(6.1), Inches(11.5), Inches(1.1))
tf = txBox.text_frame
tf.word_wrap = True
for item in how_items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(3)



# ============================================================
# SLIDE 12: CURRICULUM ALIGNMENT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GOLD)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "CURRICULUM ALIGNMENT", font_size=36, color=GOLD, bold=True)

# CAPS and IEB boxes
add_shape_bg(slide, Inches(0.5), Inches(1.3), Inches(6.0), Inches(1.2), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(1.4), Inches(5.6), Inches(0.5),
             "CAPS", font_size=20, color=GREEN, bold=True)
add_text_box(slide, Inches(0.7), Inches(1.9), Inches(5.6), Inches(0.5),
             "Curriculum and Assessment Policy Statement", font_size=13, color=LIGHT_GRAY)

add_shape_bg(slide, Inches(7.0), Inches(1.3), Inches(5.8), Inches(1.2), ACCENT_BLUE)
add_text_box(slide, Inches(7.2), Inches(1.4), Inches(5.4), Inches(0.5),
             "IEB", font_size=20, color=GREEN, bold=True)
add_text_box(slide, Inches(7.2), Inches(1.9), Inches(5.4), Inches(0.5),
             "Independent Examinations Board", font_size=13, color=LIGHT_GRAY)

# Subjects
add_text_box(slide, Inches(0.5), Inches(2.8), Inches(12), Inches(0.5),
             "SUBJECTS:", font_size=16, color=WHITE, bold=True)

subjects = [
    ("Mathematics", "Grades 1-12 (All)", GREEN, "Pilot"),
    ("Physical Sciences", "Grades 10-12 (FET)", TEAL, "Planned"),
    ("Accounting", "Grades 10-12 (FET)", PURPLE, "Planned"),
]

for i, (subj, grades, color, status) in enumerate(subjects):
    left = Inches(0.5 + i * 4.3)
    add_shape_bg(slide, left, Inches(3.3), Inches(3.8), Inches(1.2), color)
    add_text_box(slide, left + Inches(0.2), Inches(3.4), Inches(3.4), Inches(0.5),
                 subj, font_size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text_box(slide, left + Inches(0.2), Inches(3.9), Inches(3.4), Inches(0.5),
                 f"{grades}\nStatus: {status}", font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Grade breakdown
add_text_box(slide, Inches(0.5), Inches(4.8), Inches(12), Inches(0.4),
             "MATHEMATICS TOPICS BY PHASE:", font_size=14, color=WHITE, bold=True)

phases = [
    ("Foundation (Gr 1-3)", "Counting, Addition, Subtraction, Patterns, Shapes", GREEN),
    ("Intermediate (Gr 4-6)", "Fractions, Decimals, Geometry, Data Handling, Measurement", TEAL),
    ("Senior (Gr 7-9)", "Algebra, Equations, Functions, Geometry, Statistics", PURPLE),
    ("FET (Gr 10-12)", "Calculus, Trigonometry, Functions, Statistics, Probability", GOLD),
]

for i, (phase, topics, color) in enumerate(phases):
    top = Inches(5.3 + i * 0.5)
    add_text_box(slide, Inches(0.7), top, Inches(3.5), Inches(0.4),
                 phase, font_size=12, color=color, bold=True)
    add_text_box(slide, Inches(4.2), top, Inches(8.5), Inches(0.4),
                 topics, font_size=12, color=LIGHT_GRAY)



# ============================================================
# SLIDE 13: TECH STACK
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), BRIGHT_BLUE)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "TECHNOLOGY STACK", font_size=36, color=RGBColor(0x4E, 0xA8, 0xDE), bold=True)

# Tech stack table
tech_items = [
    ("AI / LLM", "AWS Bedrock (Claude 3.5 Sonnet)", TEAL),
    ("Backend", "AWS Lambda (Serverless)", GREEN),
    ("API", "API Gateway (Zero-rated endpoints)", PURPLE),
    ("Database", "DynamoDB (Learner profiles & progress)", GOLD),
    ("Storage", "S3 (Curriculum resources)", ORANGE),
    ("WhatsApp", "WhatsApp Business API", GREEN),
    ("USSD", "USSD Gateway Provider (Vodacom)", ORANGE),
    ("Infrastructure", "AWS CDK (Infrastructure as Code)", TEAL),
]

for i, (component, tech, color) in enumerate(tech_items):
    top = Inches(1.2 + i * 0.6)
    # Component label
    add_shape_bg(slide, Inches(0.5), top, Inches(2.5), Inches(0.5), color)
    add_text_box(slide, Inches(0.6), top + Inches(0.05), Inches(2.3), Inches(0.4),
                 component, font_size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    # Tech value
    add_shape_bg(slide, Inches(3.2), top, Inches(5.5), Inches(0.5), ACCENT_BLUE)
    add_text_box(slide, Inches(3.4), top + Inches(0.05), Inches(5.1), Inches(0.4),
                 tech, font_size=13, color=WHITE)

# Cost estimate box
add_shape_bg(slide, Inches(9.2), Inches(1.2), Inches(3.6), Inches(5.5), ACCENT_BLUE)
add_text_box(slide, Inches(9.4), Inches(1.3), Inches(3.2), Inches(0.5),
             "COST ESTIMATE", font_size=14, color=GOLD, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, Inches(9.4), Inches(1.8), Inches(3.2), Inches(0.4),
             "(10,000 learners/month)", font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

costs = [
    ("Lambda", "$50"),
    ("API Gateway", "$30"),
    ("DynamoDB", "$25"),
    ("Bedrock", "$200"),
    ("", ""),
    ("TOTAL", "~$305/mo"),
    ("", ""),
    ("Per Learner", "R0.58/mo"),
]
txBox = slide.shapes.add_textbox(Inches(9.4), Inches(2.3), Inches(3.2), Inches(4.0))
tf = txBox.text_frame
tf.word_wrap = True
for label, cost in costs:
    p = tf.add_paragraph()
    if label == "TOTAL":
        p.text = f"{label}:  {cost}"
        p.font.bold = True
        p.font.color.rgb = GREEN
    elif label == "Per Learner":
        p.text = f"{label}:  {cost}"
        p.font.bold = True
        p.font.color.rgb = GOLD
    elif label:
        p.text = f"{label}:  {cost}"
        p.font.color.rgb = WHITE
    p.font.size = Pt(12)
    p.font.name = 'Segoe UI'
    p.space_before = Pt(4)



# ============================================================
# SLIDE 14: IMAGE RECOGNITION FEATURE (NEW!)
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), TEAL)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "📸 IMAGE RECOGNITION FEATURE", font_size=36, color=TEAL, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "Upload photos of your work - AI spots mistakes and guides you!",
             font_size=18, color=GOLD, align=PP_ALIGN.CENTER)

# Left side - How it works
add_shape_bg(slide, Inches(0.5), Inches(1.7), Inches(5.8), Inches(5.2), ACCENT_BLUE)
add_text_box(slide, Inches(0.7), Inches(1.8), Inches(5.4), Inches(0.5),
             "HOW IT WORKS:", font_size=16, color=GREEN, bold=True)

steps = [
    ("1. 📷", "Take photo of your work", GREEN),
    ("2. 📤", "Upload via WhatsApp", TEAL),
    ("3. 🔍", "AI reads handwriting (AWS Textract)", PURPLE),
    ("4. 👁️", "AI understands math (Claude Vision)", GOLD),
    ("5. 🎯", "AI spots exact mistake", ORANGE),
    ("6. 💡", "AI provides Socratic guidance", GREEN),
]

for i, (icon, desc, color) in enumerate(steps):
    top = Inches(2.4 + i * 0.7)
    add_text_box(slide, Inches(0.9), top, Inches(0.8), Inches(0.5),
                 icon, font_size=16, color=color, bold=True)
    add_text_box(slide, Inches(1.8), top, Inches(4.2), Inches(0.5),
                 desc, font_size=14, color=WHITE)

# Right side - Example
add_shape_bg(slide, Inches(7.0), Inches(1.7), Inches(5.8), Inches(5.2), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(7.2), Inches(1.8), Inches(5.4), Inches(0.5),
             "EXAMPLE:", font_size=16, color=GOLD, bold=True)

# Mock handwritten work
add_shape_bg(slide, Inches(7.4), Inches(2.4), Inches(5.0), Inches(1.8), RGBColor(0x2A, 0x2A, 0x2A))
add_text_box(slide, Inches(7.6), Inches(2.5), Inches(4.6), Inches(1.6),
             """Problem: 2x + 5 = 13

Learner wrote:
  Step 1: 2x + 5 + 13 = 18  ❌
  Step 2: 2x = 18
  Step 3: x = 9""",
             font_size=13, color=RGBColor(0xFF, 0xFF, 0xDD))

# AI feedback
add_text_box(slide, Inches(7.2), Inches(4.4), Inches(5.4), Inches(0.4),
             "AI FEEDBACK:", font_size=14, color=TEAL, bold=True)
add_text_box(slide, Inches(7.4), Inches(4.9), Inches(5.0), Inches(1.8),
             """I see you added 13 and 5! 

Think: What's 'in the way' of x?
It's that +5.

To remove +5, do we add more
or use the opposite operation?""",
             font_size=13, color=WHITE)

# Bottom benefits
add_shape_bg(slide, Inches(0.5), Inches(6.9), Inches(12.3), Inches(0.5), BRIGHT_BLUE)
add_text_box(slide, Inches(0.7), Inches(6.95), Inches(11.9), Inches(0.4),
             "✅ No typing needed  |  ✅ Works with exam papers, homework  |  ✅ Sees actual work context  |  ✅ Available 24/7",
             font_size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 15: LIVE DEMO SLIDE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, RGBColor(0x0A, 0x0A, 0x1A))
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

add_text_box(slide, Inches(1), Inches(2.0), Inches(11), Inches(1.0),
             "LIVE DEMO", font_size=64, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1), Inches(3.3), Inches(11), Inches(0.8),
             "Watch the AI Tutor in Action", font_size=28, color=GOLD, align=PP_ALIGN.CENTER)

# What we'll see
add_shape_bg(slide, Inches(3), Inches(4.3), Inches(7.3), Inches(2.5), ACCENT_BLUE)
txBox = slide.shapes.add_textbox(Inches(3.3), Inches(4.4), Inches(6.7), Inches(2.3))
tf = txBox.text_frame
tf.word_wrap = True
demo_steps = [
    "Learner asks for help with a math problem",
    "AI detects misconception in real-time",
    "AI guides learner using Socratic method",
    "Learner solves problem themselves!",
]
for step in demo_steps:
    p = tf.add_paragraph()
    p.text = f"  {step}"
    p.font.size = Pt(16)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(10)

# ============================================================
# SLIDE 15: LIVE DEMO SLIDE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, RGBColor(0x0A, 0x0A, 0x1A))
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

add_text_box(slide, Inches(1), Inches(2.0), Inches(11), Inches(1.0),
             "LIVE DEMO", font_size=64, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1), Inches(3.3), Inches(11), Inches(0.8),
             "Watch the AI Tutor in Action", font_size=28, color=GOLD, align=PP_ALIGN.CENTER)

# What we'll see
add_shape_bg(slide, Inches(3), Inches(4.3), Inches(7.3), Inches(2.5), ACCENT_BLUE)
txBox = slide.shapes.add_textbox(Inches(3.3), Inches(4.4), Inches(6.7), Inches(2.3))
tf = txBox.text_frame
tf.word_wrap = True
demo_steps = [
    "Learner asks for help with a math problem",
    "AI detects misconception in real-time",
    "AI guides learner using Socratic method",
    "Learner solves problem themselves!",
]
for step in demo_steps:
    p = tf.add_paragraph()
    p.text = f"  {step}"
    p.font.size = Pt(16)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(10)

# ============================================================
# SLIDE 16: IMPACT & METRICS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "IMPACT & TARGET METRICS", font_size=36, color=GREEN, bold=True)

# 6-month targets
targets = [
    ("10,000", "Active\nLearners", GREEN),
    ("100,000", "Problems\nSolved", TEAL),
    ("+20%", "Accuracy\nImprovement", GOLD),
    (">70%", "Session\nCompletion", PURPLE),
    ("4.0/5.0", "User\nSatisfaction", ORANGE),
]

for i, (number, label, color) in enumerate(targets):
    left = Inches(0.3 + i * 2.6)
    top = Inches(1.3)
    add_shape_bg(slide, left, top, Inches(2.4), Inches(2.0), ACCENT_BLUE)
    add_text_box(slide, left + Inches(0.1), top + Inches(0.2), Inches(2.2), Inches(0.7),
                 number, font_size=28, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text_box(slide, left + Inches(0.1), top + Inches(1.1), Inches(2.2), Inches(0.8),
                 label, font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Addressing challenges
add_text_box(slide, Inches(0.5), Inches(3.6), Inches(12), Inches(0.5),
             "ADDRESSING SOUTH AFRICAN EDUCATION CHALLENGES:", font_size=16, color=WHITE, bold=True)

challenges = [
    ("High learner-teacher ratios (40:1)", "Personal AI tutor for every learner", RED, GREEN),
    ("Expensive private tutoring (R200-500/hr)", "FREE, accessible via WhatsApp/USSD", RED, GREEN),
    ("Data costs block online learning", "Zero-rated on Vodacom network", RED, GREEN),
    ("Language barriers in education", "Multi-language support (11 languages)", RED, GREEN),
    ("Rural access limitations", "USSD works on any phone, anywhere", RED, GREEN),
]

for i, (problem, solution, p_color, s_color) in enumerate(challenges):
    top = Inches(4.2 + i * 0.55)
    add_text_box(slide, Inches(0.7), top, Inches(5.8), Inches(0.45),
                 f"  {problem}", font_size=12, color=p_color)
    add_text_box(slide, Inches(6.8), top, Inches(5.8), Inches(0.45),
                 f"  {solution}", font_size=12, color=s_color)



# ============================================================
# SLIDE 16: COMPETITIVE ADVANTAGE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GOLD)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "COMPETITIVE ADVANTAGE", font_size=36, color=GOLD, bold=True)

# Comparison table header
headers = [("Feature", 2.5), ("Traditional AI Tutors", 4.5), ("AI Tutor South Africa", 4.5)]
left_pos = Inches(0.7)
for title, width in headers:
    add_shape_bg(slide, left_pos, Inches(1.2), Inches(width), Inches(0.5), BRIGHT_BLUE)
    add_text_box(slide, left_pos + Inches(0.1), Inches(1.22), Inches(width - 0.2), Inches(0.45),
                 title, font_size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    left_pos += Inches(width + 0.1)

# Table rows
rows = [
    ("Reasoning Analysis", "Checks answer only", "Analyzes WHY learner thinks"),
    ("Teaching Method", "Gives answers directly", "Socratic method - guides discovery"),
    ("Data Access", "Requires data/internet", "Zero-rated on Vodacom"),
    ("Device Support", "Smartphone only", "ANY phone (USSD + WhatsApp)"),
    ("Language", "English only", "11 official SA languages"),
    ("Curriculum", "Generic / US curriculum", "CAPS & IEB aligned"),
    ("Context", "Generic examples", "South African context"),
    ("Personalization", "One-size-fits-all", "Adaptive to learner level"),
]

for i, (feature, trad, ours) in enumerate(rows):
    top = Inches(1.85 + i * 0.58)
    bg = ACCENT_BLUE if i % 2 == 0 else RGBColor(0x12, 0x18, 0x30)
    # Feature
    add_shape_bg(slide, Inches(0.7), top, Inches(2.5), Inches(0.5), bg)
    add_text_box(slide, Inches(0.8), top + Inches(0.05), Inches(2.3), Inches(0.4),
                 feature, font_size=11, color=WHITE, bold=True)
    # Traditional
    add_shape_bg(slide, Inches(3.3), top, Inches(4.5), Inches(0.5), bg)
    add_text_box(slide, Inches(3.4), top + Inches(0.05), Inches(4.3), Inches(0.4),
                 f"  {trad}", font_size=11, color=RED)
    # Ours
    add_shape_bg(slide, Inches(7.9), top, Inches(4.5), Inches(0.5), bg)
    add_text_box(slide, Inches(8.0), top + Inches(0.05), Inches(4.3), Inches(0.4),
                 f"  {ours}", font_size=11, color=GREEN)

add_shape_bg(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.6), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(1.7), Inches(6.75), Inches(9.9), Inches(0.5),
             "We're not just another AI tutor - we're built specifically for South African learners!",
             font_size=15, color=GREEN, bold=True, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 17: ROADMAP
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), TEAL)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "ROADMAP", font_size=36, color=TEAL, bold=True)

# Phase 1
add_shape_bg(slide, Inches(0.5), Inches(1.3), Inches(3.8), Inches(5.0), ACCENT_BLUE)
add_shape_bg(slide, Inches(0.5), Inches(1.3), Inches(3.8), Inches(0.6), GREEN)
add_text_box(slide, Inches(0.7), Inches(1.35), Inches(3.4), Inches(0.5),
             "PHASE 1: Launch", font_size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.7), Inches(1.85), Inches(3.4), Inches(0.3),
             "Months 1-3", font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

phase1 = ["WhatsApp integration", "Mathematics (Gr 8-12)", "English + IsiZulu",
           "Vodacom zero-rating\npartnership", "10,000 learners target"]
txBox = slide.shapes.add_textbox(Inches(0.7), Inches(2.3), Inches(3.4), Inches(3.5))
tf = txBox.text_frame
tf.word_wrap = True
for item in phase1:
    p = tf.add_paragraph()
    p.text = f"  {item}"
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(10)

# Phase 2
add_shape_bg(slide, Inches(4.7), Inches(1.3), Inches(3.8), Inches(5.0), ACCENT_BLUE)
add_shape_bg(slide, Inches(4.7), Inches(1.3), Inches(3.8), Inches(0.6), GOLD)
add_text_box(slide, Inches(4.9), Inches(1.35), Inches(3.4), Inches(0.5),
             "PHASE 2: Expand", font_size=16, color=DARK_BG, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, Inches(4.9), Inches(1.85), Inches(3.4), Inches(0.3),
             "Months 4-6", font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

phase2 = ["USSD channel launch", "All grades (1-12)", "All 11 official languages",
           "Image recognition\n(snap photo of problem)", "Voice message support"]
txBox = slide.shapes.add_textbox(Inches(4.9), Inches(2.3), Inches(3.4), Inches(3.5))
tf = txBox.text_frame
tf.word_wrap = True
for item in phase2:
    p = tf.add_paragraph()
    p.text = f"  {item}"
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(10)

# Phase 3
add_shape_bg(slide, Inches(8.9), Inches(1.3), Inches(3.8), Inches(5.0), ACCENT_BLUE)
add_shape_bg(slide, Inches(8.9), Inches(1.3), Inches(3.8), Inches(0.6), PURPLE)
add_text_box(slide, Inches(9.1), Inches(1.35), Inches(3.4), Inches(0.5),
             "PHASE 3: Scale", font_size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, Inches(9.1), Inches(1.85), Inches(3.4), Inches(0.3),
             "Months 7-12", font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

phase3 = ["Physical Sciences", "Accounting subject", "Parent/guardian reports",
           "School dashboard\nfor teachers", "100,000 learners target"]
txBox = slide.shapes.add_textbox(Inches(9.1), Inches(2.3), Inches(3.4), Inches(3.5))
tf = txBox.text_frame
tf.word_wrap = True
for item in phase3:
    p = tf.add_paragraph()
    p.text = f"  {item}"
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.name = 'Segoe UI'
    p.space_before = Pt(10)

# Bottom vision
add_shape_bg(slide, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.7), RGBColor(0x0A, 0x3D, 0x1A))
add_text_box(slide, Inches(0.7), Inches(6.7), Inches(11.9), Inches(0.5),
             "VISION: A personal AI tutor for every South African learner, accessible anywhere, anytime, for free",
             font_size=14, color=GREEN, bold=True, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 18: TEAM
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), PURPLE)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "THE TEAM", font_size=36, color=PURPLE, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "South Africans building for South African learners",
             font_size=18, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Team member placeholders
team_colors = [GREEN, TEAL, PURPLE, GOLD]
for i in range(4):
    left = Inches(0.7 + i * 3.2)
    top = Inches(2.0)
    add_shape_bg(slide, left, top, Inches(2.9), Inches(3.8), ACCENT_BLUE)
    # Avatar circle placeholder
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.7), top + Inches(0.3),
                                     Inches(1.5), Inches(1.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = team_colors[i]
    circle.line.fill.background()
    # Name placeholder
    add_text_box(slide, left + Inches(0.2), top + Inches(2.0), Inches(2.5), Inches(0.5),
                 f"[Team Member {i+1}]", font_size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    # Role placeholder
    add_text_box(slide, left + Inches(0.2), top + Inches(2.5), Inches(2.5), Inches(0.4),
                 "[Role]", font_size=12, color=team_colors[i], align=PP_ALIGN.CENTER)
    # Skills
    add_text_box(slide, left + Inches(0.2), top + Inches(2.9), Inches(2.5), Inches(0.6),
                 "[Expertise area]", font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_shape_bg(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.9), ACCENT_BLUE)
add_text_box(slide, Inches(1.7), Inches(6.4), Inches(9.9), Inches(0.7),
             "We understand the education challenges in SA because we've lived them.\nOur mission: Quality education for EVERY learner, regardless of circumstances.",
             font_size=14, color=WHITE, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 19: THE ASK
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GOLD)

add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7),
             "THE ASK", font_size=36, color=GOLD, bold=True)

add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5),
             "What we need to make this a reality:",
             font_size=20, color=WHITE, align=PP_ALIGN.CENTER)

asks = [
    ("FUNDING", "Scale to 100,000 learners in year 1", GREEN, "$50,000 seed funding"),
    ("PARTNERSHIP", "Vodacom zero-rating partnership", TEAL, "API endpoint whitelisting"),
    ("CURRICULUM", "Content experts for CAPS/IEB alignment", PURPLE, "Subject matter experts"),
    ("PILOT SCHOOLS", "5-10 schools for beta testing", GOLD, "Feedback & validation"),
]

for i, (title, desc, color, detail) in enumerate(asks):
    top = Inches(1.8 + i * 1.2)
    add_shape_bg(slide, Inches(0.5), top, Inches(12.3), Inches(1.0), ACCENT_BLUE)
    # Number
    add_shape_bg(slide, Inches(0.7), top + Inches(0.15), Inches(0.7), Inches(0.7), color)
    add_text_box(slide, Inches(0.7), top + Inches(0.2), Inches(0.7), Inches(0.6),
                 str(i+1), font_size=22, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    # Title and desc
    add_text_box(slide, Inches(1.7), top + Inches(0.1), Inches(4), Inches(0.5),
                 title, font_size=16, color=color, bold=True)
    add_text_box(slide, Inches(1.7), top + Inches(0.55), Inches(5), Inches(0.4),
                 desc, font_size=13, color=WHITE)
    # Detail
    add_text_box(slide, Inches(8), top + Inches(0.3), Inches(4.5), Inches(0.4),
                 detail, font_size=13, color=LIGHT_GRAY)

# Contact
add_shape_bg(slide, Inches(3), Inches(6.5), Inches(7.3), Inches(0.8), ACCENT_BLUE)
add_text_box(slide, Inches(3.2), Inches(6.55), Inches(6.9), Inches(0.7),
             "Contact:  team@aitutor.co.za  |  +27 XX XXX XXXX  |  www.aitutor.co.za",
             font_size=14, color=GOLD, align=PP_ALIGN.CENTER)



# ============================================================
# SLIDE 20: THANK YOU
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.15), GREEN)
add_shape_bg(slide, Inches(0), Inches(7.35), Inches(13.333), Inches(0.15), GOLD)

add_text_box(slide, Inches(1), Inches(1.5), Inches(11), Inches(1.0),
             "THANK YOU!", font_size=54, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1), Inches(2.7), Inches(11), Inches(0.8),
             "AI TUTOR SOUTH AFRICA", font_size=32, color=GREEN, bold=True, align=PP_ALIGN.CENTER)

# Quote box
add_shape_bg(slide, Inches(2.5), Inches(3.8), Inches(8.3), Inches(1.5), ACCENT_BLUE)
add_text_box(slide, Inches(2.7), Inches(4.0), Inches(7.9), Inches(1.2),
             '"Traditional AI tutors give answers.\nWe build thinkers."',
             font_size=24, color=GOLD, align=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1), Inches(5.6), Inches(11), Inches(0.6),
             "Teaching Students HOW to Think, Not WHAT to Think",
             font_size=18, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Bottom info
add_text_box(slide, Inches(1), Inches(6.5), Inches(11), Inches(0.5),
             "Questions? Let's chat!",
             font_size=18, color=WHITE, align=PP_ALIGN.CENTER)

# ============================================================
# SAVE FILE
# ============================================================
output_path = "/projects/sandbox/forage-jpmc-swe-task-1/presentation/AI_Tutor_SA_Presentation.pptx"
prs.save(output_path)
print(f"\nPresentation saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
print("\nSlide order:")
slide_titles = [
    "1. Title Slide",
    "2. The Problem",
    "3. Our Solution",
    "4. The Innovation - Reasoning Analysis",
    "5. System Architecture",
    "6. WhatsApp Experience",
    "7. USSD Experience",
    "8. Progressive Hint System",
    "9. Progress Tracking & Gamification",
    "10. Multi-Language Support",
    "11. Zero-Rated on Vodacom",
    "12. Curriculum Alignment",
    "13. Technology Stack",
    "14. Live Demo",
    "15. Impact & Metrics",
    "16. Competitive Advantage",
    "17. Roadmap",
    "18. The Team",
    "19. The Ask",
    "20. Thank You",
]
for title in slide_titles:
    print(f"  {title}")
