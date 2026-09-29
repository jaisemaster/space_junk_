import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from theme import apply_theme, html
from bg import apply_page_bg
from debris_data import load_and_compute, HOURS

st.set_page_config(page_title="Removal Tool | SPACE JUNK", page_icon="🛠️", layout="wide")
apply_theme()
apply_page_bg("removal")

# ---------------- removal method constants ----------------
ASSUMED_MASS_KG = 50  # same mass assumed for every object, kept simple on purpose

# cost = base_cost + (mass * cost_per_kg) + (altitude_km * cost_per_km)
# time = base_time_days + (altitude_km / speed_factor)
METHODS = {
    "Net capture": dict(base_cost=30_000_000, cost_per_kg=50_000, cost_per_km=10_000,
                        base_time=30, speed_factor=20,
                        note="Net launched from a chaser satellite, drags debris down to burn up. (ESA RemoveDEBRIS, 2018)"),
    "Robotic arm": dict(base_cost=60_000_000, cost_per_kg=80_000, cost_per_km=15_000,
                        base_time=45, speed_factor=15,
                        note="Servicing satellite grips the object directly. (Astroscale ELSA-d approach)"),
    "Laser ablation": dict(base_cost=15_000_000, cost_per_kg=5_000, cost_per_km=20_000,
                           base_time=90, speed_factor=40,
                           note="Laser nudges debris out of orbit over time. Still mostly experimental."),
}


def estimate(method: dict, altitude: float):
    cost = method["base_cost"] + ASSUMED_MASS_KG * method["cost_per_kg"] + altitude * method["cost_per_km"]
    days = method["base_time"] + altitude / method["speed_factor"]
    return cost, days


st.page_link("main.py", label="← Back to Home")
st.title("🛠️ DEBRIS REMOVAL TOOL")
st.caption(f"Cost and time are illustrative estimates. Every object assumes a mass of {ASSUMED_MASS_KG} kg.")

with st.spinner("Loading orbital data..."):
    data = load_and_compute()

labels, pairs, obj_risk, now_alt = data["labels"], data["pairs"], data["obj_risk"], data["now_alt"]

ranked = sorted(obj_risk.items(), key=lambda x: -x[1])[:20]
if not ranked:
    st.info("No close approaches found in the current window, so there is nothing to remove.")
    st.stop()

options = [f"{labels[i]} (risk {round(v, 1)})" for i, v in ranked]
idx_lookup = [i for i, _ in ranked]

choice = st.selectbox("Select a debris object", options)
chosen = idx_lookup[options.index(choice)]
altitude = now_alt[chosen]
risk = round(obj_risk[chosen], 1)

involved = [p for p in pairs if chosen in (p["a"], p["b"])]
total_risk = sum(p["risk"] for p in pairs) or 1
share = sum(p["risk"] for p in involved) / total_risk

a, b, c = st.columns(3)
a.metric("Altitude", f"{altitude:,} km")
b.metric("Total risk score", f"{risk}")
c.metric(f"Risk removed (next {HOURS} h)", f"{100 * share:.1f}%")

method_name = st.selectbox("Select a removal method", list(METHODS.keys()))
m = METHODS[method_name]
cost, days = estimate(m, altitude)

c1, c2 = st.columns(2)
c1.metric("Estimated cost", f"${cost:,.0f}")
c2.metric("Estimated time", f"{days:.0f} days")
st.caption(m["note"])

st.subheader("Compare all methods for this object")
st.dataframe(
    pd.DataFrame([
        {"Method": name,
         "Estimated cost": f"${estimate(md, altitude)[0]:,.0f}",
         "Estimated time (days)": round(estimate(md, altitude)[1])}
        for name, md in METHODS.items()
    ]),
    hide_index=True, use_container_width=True,
)

st.markdown(
    html("""
    <div class="r-text">
    Costs scale with object mass and altitude; time scales with altitude. These are rough planning numbers
    based on published demonstration missions, not quotes.
    </div>
    """),
    unsafe_allow_html=True,
)
