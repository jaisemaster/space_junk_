"""Shared styling for the sub-pages (3D model, tracking, team)."""
import base64
from pathlib import Path

import streamlit as st

BACKGROUND = Path(__file__).parent / "assets" / "background.png"


def html(block: str) -> str:
    """Strip blank lines + indentation so Markdown doesn't turn HTML into a code block."""
    return "\n".join(line.strip() for line in block.splitlines() if line.strip())


def apply_theme(extra_css: str = "") -> None:
    bg = base64.b64encode(BACKGROUND.read_bytes()).decode()
    st.markdown(
        f"""
<style>
@import url("https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800&family=Rajdhani:wght@500;600;700&display=swap");
.stApp {{
    background-image:
        linear-gradient(rgba(1,7,24,.35), rgba(1,7,24,.70)),
        url("data:image/png;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
html, body, [class*="css"] {{ font-family: "Rajdhani", sans-serif; }}
h1, h2, h3 {{ font-family: "Orbitron", sans-serif !important; }}
header {{ background: transparent !important; }}
{extra_css}
</style>
""",
        unsafe_allow_html=True,
    )
