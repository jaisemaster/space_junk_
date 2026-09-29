import streamlit as st
from pathlib import Path
import base64


# ============================================================
# HTML HELPER
# ============================================================
# Streamlit runs st.markdown() through a Markdown parser. A blank line
# or 4+ spaces of indentation inside HTML makes it print the tags as
# a code block instead of rendering them. This strips both.

def html(block: str) -> str:
    return "\n".join(
        line.strip() for line in block.splitlines() if line.strip()
    )

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SPACE JUNK",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# LOAD BACKGROUND IMAGE
# ============================================================

BASE_DIR = Path(__file__).parent
BACKGROUND = BASE_DIR / "assets" / "background.png"

with open(BACKGROUND, "rb") as image_file:
    background_base64 = base64.b64encode(
        image_file.read()
    ).decode()

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       IMPORT FUTURISTIC FONTS
       ====================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap'
    );

    /* ======================================================
       GLOBAL
       ====================================================== */

    html,
    body,
    [class*="css"] {{
        font-family: 'Rajdhani', sans-serif;
    }}

    .stApp {{
        min-height: 100vh;

        background-image:
            linear-gradient(
                rgba(1, 5, 20, 0.40),
                rgba(1, 5, 20, 0.72)
            ),
            url("data:image/png;base64,{background_base64}");

        background-size: cover;
        background-position: center center;
        background-attachment: fixed;

        color: white;
    }}

    /* Remove Streamlit default padding */

    .block-container {{
        padding-top: 0.8rem;
        padding-left: 4%;
        padding-right: 4%;
        max-width: 1500px;
    }}

    /* Hide Streamlit branding */

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        background: transparent !important;
    }}

    /* ======================================================
       TOP NAVBAR
       ====================================================== */

    .navbar {{
        height: 64px;

        display: flex;
        align-items: center;

        border-bottom: 1px solid rgba(0, 220, 255, 0.15);

        background:
            rgba(3, 9, 26, 0.72);

        backdrop-filter: blur(14px);

        margin-bottom: 20px;

        padding: 0 18px;

        border-radius: 0 0 14px 14px;

        box-shadow:
            0 8px 30px rgba(0,0,0,0.25);
    }}

    .brand {{
        display: flex;
        align-items: center;

        gap: 10px;

        font-family: 'Orbitron', sans-serif;

        font-size: 19px;

        font-weight: 800;

        color: #f4f8ff;

        letter-spacing: 0.5px;
    }}

    .rocket {{
        width: 34px;
        height: 34px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            rgba(0, 200, 255, 0.12);

        border: 1px solid rgba(0, 220, 255, 0.45);

        border-radius: 9px;

        font-size: 19px;

        box-shadow:
            0 0 18px rgba(0, 200, 255, 0.25);
    }}

    /* ======================================================
       HERO
       ====================================================== */

    .hero-wrapper {{
        min-height: 650px;

        display: flex;

        align-items: center;

        padding-top: 25px;
        padding-bottom: 40px;
    }}

    .hero-left {{
        padding: 25px 15px 25px 20px;
    }}

    /* ======================================================
       BADGE
       ====================================================== */

    .badge {{
        display: inline-flex;

        align-items: center;

        gap: 8px;

        padding: 8px 17px;

        border-radius: 30px;

        border: 1px solid rgba(0, 220, 255, 0.45);

        background:
            rgba(0, 190, 255, 0.08);

        color: #62eaff;

        font-family: 'Rajdhani', sans-serif;

        font-size: 14px;

        font-weight: 700;

        letter-spacing: 1.5px;

        box-shadow:
            0 0 20px rgba(0, 200, 255, 0.12);
    }}

    /* ======================================================
       MAIN TITLE
       ====================================================== */

    .main-title {{
        margin-top: 25px;

        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(64px, 8.5vw, 118px);
        line-height: 1;
        font-weight: 700;
        font-style: italic;
        text-transform: uppercase;
        letter-spacing: 1px;
        transform: skewX(-10deg);
        transform-origin: left center;
        color: #f5f8ff;
        text-shadow: 0 0 22px rgba(160, 210, 255, 0.25);
    }}

    /* Razor-cut lettering: each word is sliced by a sharp diagonal
       and the top half is pushed sideways, like the reference image */
    .main-title .razor {{
        position: relative;
        display: inline-block;
        color: transparent;
        -webkit-text-fill-color: transparent;
    }}

    .main-title .razor::before,
    .main-title .razor::after {{
        content: attr(data-text);
        position: absolute;
        left: 0;
        top: 0;
        white-space: nowrap;
        background: var(--fill);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .main-title .razor::before {{
        clip-path: polygon(0 0, 100% 0, 100% 44%, 0 58%);
        transform: translateX(14px);
    }}

    .main-title .razor::after {{
        clip-path: polygon(0 61%, 100% 47%, 100% 100%, 0 100%);
    }}

    .main-title .white {{
        --fill: linear-gradient(180deg, #ffffff 20%, #aebfe0 100%);
    }}

    .main-title .blue {{
        --fill: linear-gradient(180deg, #4de4ff 10%, #0a9dff 100%);
        filter: drop-shadow(0 0 14px rgba(0, 200, 255, 0.55));
    }}

    .main-title .streak {{
        display: inline-block;
        width: 90px;
        height: 4px;
        margin-left: 14px;
        vertical-align: middle;
        background: linear-gradient(90deg, rgba(0,220,255,.9), transparent);
        box-shadow: 0 0 12px rgba(0,220,255,.6);
    }}

    /* ======================================================
       DESCRIPTION
       ====================================================== */

    .w-text {{
        margin-top: 24px;

        color: #b9d2e9;

        font-family: 'Rajdhani', sans-serif;

        font-size: 19px;

        line-height: 1.45;

        font-weight: 500;

        max-width: 720px;

        letter-spacing: 0.4px;
    }}

    .r-text {{
        margin-top: 5px;

        color: #65e7ff;

        font-family: 'Rajdhani', sans-serif;

        font-size: 17px;

        line-height: 1.45;

        font-weight: 600;

        max-width: 720px;

        letter-spacing: 0.6px;
    }}

    /* ======================================================
       BUTTON AREA
       ====================================================== */

    .button-space {{
        margin-top: 32px;
    }}

    /* Streamlit buttons */

    .stButton > button {{
        width: 100%;

        min-height: 52px;

        border-radius: 10px !important;

        border: 1px solid rgba(0, 225, 255, 0.75) !important;

        background:
            linear-gradient(
                135deg,
                rgba(0, 196, 255, 0.92),
                rgba(20, 70, 220, 0.95)
            ) !important;

        color: white !important;

        font-family: 'Orbitron', sans-serif !important;

        font-size: 13px !important;

        font-weight: 700 !important;

        letter-spacing: 0.8px !important;

        box-shadow:
            0 0 18px rgba(0, 200, 255, 0.20);

        transition:
            all 0.25s ease !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);

        border-color: #5cecff !important;

        box-shadow:
            0 0 30px rgba(0, 220, 255, 0.45);

        background:
            linear-gradient(
                135deg,
                #00d9ff,
                #2558ff
            ) !important;
    }}

    /* ======================================================
       INFO ROW
       ====================================================== */

    .info-row {{
        display: flex;

        gap: 35px;

        margin-top: 25px;

        color: #a9bdd6;

        font-family: 'Rajdhani', sans-serif;

        font-size: 15px;

        font-weight: 600;
    }}

    .info-item {{
        display: flex;

        align-items: center;

        gap: 8px;
    }}

    .info-dot {{
        color: #00eaff;

        text-shadow:
            0 0 10px #00eaff;
    }}

    /* ======================================================
       RIGHT VISUAL PANEL
       ====================================================== */

    .visual-container {{
        position: relative;

        height: 550px;

        display: flex;

        align-items: center;

        justify-content: center;
    }}

    .orbital-glow {{
        position: absolute;

        width: 430px;
        height: 430px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(0, 220, 255, 0.15) 0%,
                rgba(0, 100, 255, 0.07) 35%,
                transparent 70%
            );

        filter: blur(5px);
    }}

    .orbit {{
        position: absolute;

        width: 390px;
        height: 175px;

        border: 1px solid rgba(0, 220, 255, 0.35);

        border-radius: 50%;

        transform: rotate(-25deg);

        box-shadow:
            0 0 25px rgba(0, 210, 255, 0.10);
    }}

    .orbit.two {{
        width: 430px;
        height: 210px;

        transform:
            rotate(25deg);

        border-color:
            rgba(50, 130, 255, 0.22);
    }}

    .core {{
        position: absolute;

        width: 230px;
        height: 230px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 35% 30%,
                #1b74a8,
                #082552 45%,
                #020918 75%
            );

        border:
            1px solid rgba(0, 225, 255, 0.55);

        box-shadow:
            0 0 30px rgba(0, 200, 255, 0.30),
            inset 0 0 40px rgba(0, 200, 255, 0.20);

        display: flex;

        align-items: center;

        justify-content: center;

        z-index: 3;
    }}

    .core-text {{
        text-align: center;

        font-family: 'Orbitron', sans-serif;

        color: #8defff;

        font-size: 18px;

        font-weight: 800;

        letter-spacing: 2px;

        text-shadow:
            0 0 15px rgba(0, 230, 255, 0.65);
    }}

    .satellite {{
        position: absolute;

        font-size: 34px;

        z-index: 5;

        filter:
            drop-shadow(
                0 0 10px rgba(0,220,255,0.65)
            );
    }}

    .sat-1 {{
        top: 90px;
        right: 100px;
        transform: rotate(25deg);
    }}

    .sat-2 {{
        bottom: 105px;
        left: 95px;
        transform: rotate(-20deg);
    }}

    .sat-3 {{
        top: 155px;
        left: 60px;
        font-size: 25px;
    }}

    .sat-4 {{
        bottom: 120px;
        right: 70px;
        font-size: 25px;
    }}

    /* ======================================================
       RIGHT PANEL
       ====================================================== */

    .system-card {{
        position: absolute;

        right: 0;

        bottom: 20px;

        width: 270px;

        padding: 18px;

        border-radius: 14px;

        background:
            rgba(2, 12, 32, 0.78);

        border:
            1px solid rgba(0, 220, 255, 0.30);

        backdrop-filter:
            blur(15px);

        box-shadow:
            0 15px 40px rgba(0,0,0,0.35),
            0 0 25px rgba(0,180,255,0.08);
    }}

    .system-title {{
        font-family: 'Orbitron', sans-serif;

        font-size: 13px;

        font-weight: 700;

        color: #eaf8ff;

        letter-spacing: 1px;

        margin-bottom: 12px;
    }}

    .online {{
        color: #39f6bb;

        font-size: 13px;

        font-weight: 700;

        letter-spacing: 1px;
    }}

    .system-line {{
        height: 1px;

        margin: 13px 0;

        background:
            rgba(0, 220, 255, 0.15);
    }}

    .system-small {{
        color: #8da8c7;

        font-size: 13px;
    }}

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {{
        margin-top: 15px;

        padding: 20px;

        text-align: center;

        color: #718aa8;

        font-family: 'Rajdhani', sans-serif;

        font-size: 13px;

        letter-spacing: 1px;

        border-top:
            1px solid rgba(0, 220, 255, 0.12);
    }}

    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {{

        .visual-container {{
            height: 430px;
        }}

        .main-title {{
            font-size: 50px;
        }}

        .system-card {{
            right: 5%;
        }}

        .info-row {{
            flex-wrap: wrap;
        }}

    }}

    /* ---- button variants (3D MODEL = filled, DEBRIS REMOVAL TOOL = outline) ---- */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"] {{
        background: rgba(3, 12, 34, 0.35) !important;
        border: 1px solid rgba(0, 225, 255, 0.55) !important;
        box-shadow: none;
    }}
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover {{
        background: rgba(0, 200, 255, 0.18) !important;
    }}

    .info-sep {{
        width: 1px;
        height: 26px;
        background: rgba(0, 220, 255, 0.45);
    }}

    .info-row {{ align-items: center; }}

    .badge .b-icon {{ font-size: 17px; }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# NAVBAR (shared with Team Information page)
# ============================================================

from nav import render_navbar

render_navbar("home")

# ============================================================
# HERO SECTION
# ============================================================

left, _spacer = st.columns([1.5, 0.5], gap="large")

with left:

    # Badge

    st.markdown(
        html("""
        <div class="badge">
            <span class="b-icon">🚀</span> Based on FY-1C
        </div>
        """),
        unsafe_allow_html=True
    )

    # Main heading

    st.markdown(
        html("""
        <div class="main-title">
            <span class="razor white" data-text="SPACE">SPACE</span> <span class="razor blue" data-text="JUNK">JUNK</span><span class="streak"></span>
        </div>
        """),
        unsafe_allow_html=True
    )

    # W text

    st.markdown(
        html("""
        <div class="w-text">
        Explore the debris cloud left behind by the FY-1C satellite breakup, see it in 3D, and understand how it threatens working satellites.
        </div>
        """),
        unsafe_allow_html=True
    )

    # R text

    st.markdown(
        html("""
        <div class="r-text">
        Live orbit data  •  Close-approach risk  •  Debris hotspots
        </div>
        """),
        unsafe_allow_html=True
    )

    # Buttons

    st.markdown('<div class="button-space"></div>', unsafe_allow_html=True)

    button1, button2, _b3 = st.columns([1, 1.15, 0.85], gap="medium")

    with button1:
        if st.button("🧊  3D MODEL  →", type="primary", use_container_width=True):
            st.switch_page("pages/3d_model.py")

    with button2:
        if st.button("▶️  DEBRIS REMOVAL TOOL", type="secondary", use_container_width=True):
            st.switch_page("pages/removal.py")

    # Info row

    st.markdown(
        html("""
        <div class="info-row">
            <div class="info-item">
                <span>🌐</span>
                FENGYUN SATELLITE
            </div>
            <div class="info-sep"></div>
            <div class="info-item">
                <span>❤️</span>
                BUILD WITH LOVE
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    html("""
    <div class="footer">
        SPACE JUNK &nbsp; • &nbsp;
        BASED ON FY-1C &nbsp; • &nbsp;
        BUILT WITH LOVE ❤️ &nbsp; • &nbsp;
        TATCRACKER'S
    </div>
    """),
    unsafe_allow_html=True
)
