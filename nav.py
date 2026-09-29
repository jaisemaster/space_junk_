"""Shared top navbar for Home + Team Information pages.

Kept in its own file so theme.py (used by the 3D model and removal-tool pages)
is not touched at all.
"""
import streamlit as st

NAV_CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap");

/* remove Streamlit toolbar (deploy / menu / profile-style icon) and sidebar */
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"], #MainMenu, footer { display: none !important; visibility: hidden !important; }
header { background: transparent !important; }

.block-container { padding-top: 0.8rem !important; padding-left: 4% !important; padding-right: 4% !important; max-width: 1500px !important; }

/* navbar bar */
div[data-testid="stHorizontalBlock"]:has(.nav-brand) {
    align-items: center !important;
    min-height: 64px;
    padding: 0 18px;
    margin-bottom: 20px;
    gap: 0.8rem !important;
    border-bottom: 1px solid rgba(0, 220, 255, 0.15);
    background: rgba(3, 9, 26, 0.72);
    backdrop-filter: blur(14px);
    border-radius: 0 0 14px 14px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}
.nav-brand {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Orbitron', sans-serif; font-size: 19px; font-weight: 800;
    color: #f4f8ff; letter-spacing: 0.5px; white-space: nowrap;
}
.nav-rocket { font-size: 26px; filter: drop-shadow(0 0 8px rgba(0,200,255,.6)); }

/* pill links */
div[data-testid="stHorizontalBlock"]:has(.nav-brand) a {
    display: flex; justify-content: center; align-items: center; white-space: nowrap;
    padding: 0.45rem 1.1rem; border-radius: 999px;
    border: 1px solid rgba(0, 220, 255, 0.30);
    background: rgba(3, 12, 34, 0.55);
    color: #eaf6ff !important; text-decoration: none !important;
    font-family: 'Rajdhani', sans-serif; font-size: 16px; font-weight: 600; letter-spacing: .4px;
    transition: all .25s ease;
}
div[data-testid="stHorizontalBlock"]:has(.nav-brand) a p { margin: 0; font-family: 'Rajdhani', sans-serif; font-weight: 600; font-size: 16px; }
div[data-testid="stHorizontalBlock"]:has(.nav-brand) a:hover { border-color: #5cecff; box-shadow: 0 0 18px rgba(0,220,255,.35); }
NAV_ACTIVE_RULE
</style>
"""

ACTIVE_RULE = """
div[data-testid="stHorizontalBlock"]:has(.nav-brand) > div:nth-child(%d) a {
    background: linear-gradient(135deg, rgba(0,120,255,.55), rgba(0,60,180,.55));
    border-color: #2f8bff;
    box-shadow: 0 0 18px rgba(30,120,255,.55), inset 0 0 12px rgba(0,160,255,.25);
}
"""


def render_navbar(active: str) -> None:
    """active = 'home' or 'team'."""
    n = 2 if active == "home" else 3
    st.markdown(NAV_CSS.replace("NAV_ACTIVE_RULE", ACTIVE_RULE % n), unsafe_allow_html=True)

    c1, c2, c3, _ = st.columns([2.6, 1.1, 2.1, 7], gap="small")
    with c1:
        st.markdown(
            '<div class="nav-brand"><span class="nav-rocket">🚀</span><span>TATCRACKER\'S</span></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.page_link("main.py", label="🏠 Home", use_container_width=True)
    with c3:
        st.page_link("pages/team.py", label="⚙️ Team Information", use_container_width=True)
