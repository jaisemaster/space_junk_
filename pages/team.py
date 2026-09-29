import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from theme import apply_theme, html
from nav import render_navbar

st.set_page_config(page_title="Team Information | SPACE JUNK", page_icon="⚙️", layout="wide", initial_sidebar_state="collapsed")

TEAM_CSS = """
.team-title { font-family:'Orbitron',sans-serif; font-style:italic; font-weight:800; font-size:clamp(30px,4vw,44px);
    letter-spacing:1px; margin:4px 0 6px 0; background:linear-gradient(90deg,#ffffff,#7fd8ff);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.our-team { font-family:'Rajdhani',sans-serif; font-weight:600; font-size:24px; color:#f2f7ff; margin:0 0 18px 0; }
.card { padding:26px 14px 20px 14px; border:1px solid rgba(0,220,255,.35); border-radius:16px;
    background:rgba(2,12,34,.70); text-align:center; box-shadow:0 0 22px rgba(0,160,255,.08); }
.avatar { width:76px; height:76px; margin:0 auto 14px auto; border-radius:50%;
    background:linear-gradient(180deg,#3d8fe0,#1a5fb4); display:flex; align-items:flex-end; justify-content:center;
    overflow:hidden; box-shadow:0 0 18px rgba(0,160,255,.45); }
.avatar svg { width:60px; height:60px; }
.m-name { font-family:'Rajdhani',sans-serif; font-weight:700; font-size:21px; color:#fff; letter-spacing:.5px; }
.m-role { font-family:'Rajdhani',sans-serif; font-weight:600; font-size:16px; color:#38c4ff; margin-bottom:14px; }
.m-links { display:flex; justify-content:center; align-items:center; gap:14px; }
.m-links a { text-decoration:none; display:flex; align-items:center; justify-content:center; }
.li { width:22px; height:22px; border-radius:4px; background:#0a66c2; color:#fff; font-family:Arial,sans-serif;
    font-weight:700; font-size:13px; }
.about-text { font-family:'Rajdhani',sans-serif; font-weight:500; font-size:19px; line-height:1.5; color:#c4d6ea;
    max-width:760px; letter-spacing:.4px; }
.team-footer { margin-top:40px; padding:16px 4px; border-top:1px solid rgba(0,220,255,.15);
    font-family:'Rajdhani',sans-serif; font-size:15px; letter-spacing:1px; color:#9fb6d0; }
"""
apply_theme(TEAM_CSS)
render_navbar("team")

st.page_link("main.py", label="← Back to Home")
st.markdown('<div class="team-title">TEAM INFORMATION</div>', unsafe_allow_html=True)
st.markdown('<div class="our-team">Our Team</div>', unsafe_allow_html=True)

AVATAR = ('<svg viewBox="0 0 64 64"><circle cx="32" cy="24" r="12" fill="#eaf4ff"/>'
          '<path d="M8 64c0-16 10-26 24-26s24 10 24 26z" fill="#eaf4ff"/></svg>')
GITHUB = ('<svg width="22" height="22" viewBox="0 0 16 16" fill="#ffffff"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 '
          '5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53'
          '.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2'
          '-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12'
          '.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 '
          '0016 8c0-4.42-3.58-8-8-8z"/></svg>')

team = [
    ("M.ARMAAN", "Frontend Developer"),
    ("JAISE.B.THOMAS", "Backend Developer"),
    ("NIHITH AKSHAY", "ML / AI Engineer"),
    ("ATUL SHRIVASTAVA", "UI/UX Designer"),
]

cols = st.columns(4, gap="medium")
for col, (name, role) in zip(cols, team):
    with col:
        st.markdown(
            html(f"""
            <div class="card">
                <div class="avatar">{AVATAR}</div>
                <div class="m-name">{name}</div>
                <div class="m-role">{role}</div>
                <div class="m-links">
                    <a href="#" title="GitHub">{GITHUB}</a>
                    <a href="#" title="LinkedIn"><span class="li">in</span></a>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
st.subheader("About Our Project")
st.markdown(
    '<div class="about-text">SPACE JUNK IS A REAL TIME DEMONSTRATION OF SPACE DEBRIS TRACKING AND ANALYSIS. '
    'OUR MISSION IS TO COLLECT DATA AND PRESENT HERE.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="team-footer">SPACE JUNK &nbsp;|&nbsp; Built with love ❤️</div>', unsafe_allow_html=True)
