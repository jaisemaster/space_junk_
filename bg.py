"""Per-page background override for the 3D model and removal-tool pages.

Only swaps the background image. Call it right after apply_theme().
"""
import base64
from pathlib import Path

import streamlit as st

ASSETS = Path(__file__).parent / "assets"
FILES = {"3d": "bg_3d_model.jpg", "removal": "bg_removal.jpg"}


def apply_page_bg(name: str) -> None:
    data = base64.b64encode((ASSETS / FILES[name]).read_bytes()).decode()
    st.markdown(
        f"""
<style>
.stApp {{
    background-image:
        linear-gradient(rgba(1,7,24,.15), rgba(1,7,24,.45)),
        url("data:image/jpeg;base64,{data}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )
