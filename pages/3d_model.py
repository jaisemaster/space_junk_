import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from theme import apply_theme, html
from bg import apply_page_bg
from debris_data import load_and_compute, build_globe_figure

st.set_page_config(page_title="3D Model | SPACE JUNK", page_icon="🧊", layout="wide")
apply_theme()
apply_page_bg("3d")

st.page_link("main.py", label="← Back to Home")
st.title("🧊 3D MODEL")
st.caption("Interactive space-debris viewer — live orbit propagation + close-approach risk")

with st.spinner("Propagating orbits and scanning for close approaches..."):
    data = load_and_compute()

fig = build_globe_figure(data)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    html(f"""
    <div class="r-text">
    Orange dots and red lines mark the {min(25, len(data["pairs"]))} closest tracked pairs in the next hour.
    Gold diamonds are the top removal-priority objects, ranked by total risk across all their close approaches.
    </div>
    """),
    unsafe_allow_html=True,
)
