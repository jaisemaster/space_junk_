"""
Debris data + risk engine
--------------------------
Shared by pages/3d_model.py (and, later, the removal tool page) so the
TLE propagation and close-approach search only run once per session.

Needs debris.txt in the SAME FOLDER as main.py.
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.spatial import cKDTree
from skyfield.api import load

# ---------------- settings ----------------
TLE_FILE = "debris.txt"
EARTH_RADIUS = 6371        # km
HOURS = 1
STEP_S = 10
THRESHOLD_KM = 50
ALERT_KM = 500
FRAME_SKIP = 3
TOP_PAIRS = 25
TOP_TARGETS = 5
MAX_DEBRIS_SHOWN = 3000


@st.cache_resource
def load_and_compute():
    """Loads the TLEs, propagates every object once, and finds close approaches + risk.
    Cached so it only runs once per server process, not once per page visit."""
    ts = load.timescale()
    satellites = load.tle_file(TLE_FILE)
    labels = [f"{s.name} [{s.model.satnum}]" for s in satellites]  # catalog number keeps duplicate names apart

    now = ts.now()
    n_steps = int(HOURS * 3600 / STEP_S)
    times = ts.tt_jd(now.tt + np.arange(n_steps) * STEP_S / 86400)

    pos = np.empty((len(satellites), 3, n_steps))
    vel = np.empty_like(pos)
    for s, sat in enumerate(satellites):
        g = sat.at(times)
        pos[s], vel[s] = g.position.km, g.velocity.km_per_s

    closest = {}
    for k in range(n_steps):
        snap = pos[:, :, k]
        valid = np.where(~np.isnan(snap).any(axis=1))[0]
        if len(valid) < 2:
            continue
        for i, j in cKDTree(snap[valid]).query_pairs(THRESHOLD_KM):
            a, b = int(valid[i]), int(valid[j])
            d = float(np.linalg.norm(snap[a] - snap[b]))
            if (a, b) not in closest or d < closest[(a, b)]["distance_km"]:
                closest[(a, b)] = {
                    "a": a, "b": b, "object_a": labels[a], "object_b": labels[b],
                    "distance_km": round(d, 1),
                    "relative_speed_kms": round(float(np.linalg.norm(vel[a, :, k] - vel[b, :, k])), 2),
                    "seconds_from_now": k * STEP_S,
                    "altitude_km": round(float(np.linalg.norm(snap[a])) - EARTH_RADIUS),
                }

    def risk_score(distance_km, rel_speed):
        closeness = 1 - distance_km / THRESHOLD_KM
        speed = min(rel_speed / 14, 1)
        return round(100 * closeness * speed, 1)

    pairs = list(closest.values())
    for r in pairs:
        r["risk"] = risk_score(r["distance_km"], r["relative_speed_kms"])
    pairs.sort(key=lambda r: r["risk"], reverse=True)

    obj_risk = {}
    for r in pairs:
        for i in (r["a"], r["b"]):
            obj_risk[i] = obj_risk.get(i, 0) + r["risk"]
    ranked = sorted(obj_risk.items(), key=lambda x: -x[1])
    targets = [i for i, _ in ranked[:TOP_TARGETS]]

    now_alt = {i: round(float(np.linalg.norm(pos[i, :, 0])) - EARTH_RADIUS) for i in range(len(satellites))}

    return dict(satellites=satellites, labels=labels, pos=pos, vel=vel, n_steps=n_steps,
                pairs=pairs, targets=targets, now_alt=now_alt, obj_risk=obj_risk)


def build_globe_figure(data):
    labels, pos = data["labels"], data["pos"]
    pairs, targets = data["pairs"], data["targets"]
    n_steps = data["n_steps"]

    shown = pairs[:TOP_PAIRS]
    targets_idx = np.array(targets, dtype=int)
    risky = np.array(sorted({r["a"] for r in shown} | {r["b"] for r in shown} | set(targets)), dtype=int)
    risky_only = np.setdiff1d(risky, targets_idx)
    ok = np.where(~np.isnan(pos).any(axis=(1, 2)))[0]
    others = np.setdiff1d(ok, risky)
    if len(others) > MAX_DEBRIS_SHOWN:
        others = np.sort(np.random.default_rng(0).choice(others, MAX_DEBRIS_SHOWN, replace=False))

    def state(k):
        p = np.nan_to_num(pos[:, :, k])

        def xyz(idx):
            q = np.rint(p[idx]).astype(int)
            return q[:, 0].tolist(), q[:, 1].tolist(), q[:, 2].tolist()

        alt = (np.linalg.norm(p[others], axis=1) - EARTH_RADIUS).round().astype(int).tolist()
        lx, ly, lz = [], [], []
        for r in shown:
            a, b = r["a"], r["b"]
            if np.linalg.norm(p[a] - p[b]) <= ALERT_KM:
                for q in (p[a], p[b]):
                    lx.append(int(q[0])); ly.append(int(q[1])); lz.append(int(q[2]))
                lx.append(None); ly.append(None); lz.append(None)
        return xyz(others), alt, xyz(risky_only), (lx, ly, lz), xyz(targets_idx)

    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 40)
    ex = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    ey = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    ez = EARTH_RADIUS * np.outer(np.ones_like(u), np.cos(v))

    (dx, dy, dz), alt, (rx, ry, rz), (lx, ly, lz), (tx, ty, tz) = state(0)
    cmin, cmax = (min(alt), max(alt)) if alt else (0, 2000)

    fig = go.Figure()
    # Earth sphere, colored to match the site's cyan/navy brand
    fig.add_trace(go.Surface(x=ex, y=ey, z=ez, showscale=False, hoverinfo="skip",
                             colorscale=[[0, "#010714"], [1, "#0d3a66"]], opacity=0.97))
    fig.add_trace(go.Scatter3d(x=dx, y=dy, z=dz, mode="markers", name="Debris",
                               text=[labels[i] for i in others], customdata=alt,
                               hovertemplate="<b>%{text}</b><br>Altitude: %{customdata} km<extra></extra>",
                               marker=dict(size=2, color=alt, colorscale="Turbo", cmin=cmin, cmax=cmax,
                                           showscale=True, colorbar=dict(title="Altitude (km)"))))
    fig.add_trace(go.Scatter3d(x=rx, y=ry, z=rz, mode="markers", name="Objects in close pairs",
                               text=[labels[i] for i in risky_only], hovertemplate="<b>%{text}</b><extra></extra>",
                               marker=dict(size=4, color="orange")))
    fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz, mode="lines", name=f"Pair within {ALERT_KM} km",
                               hoverinfo="skip", line=dict(color="#ff3b3b", width=5)))
    fig.add_trace(go.Scatter3d(x=tx, y=ty, z=tz, mode="markers+text", name="Removal priority",
                               text=[labels[i] for i in targets_idx], textposition="top center",
                               textfont=dict(size=10, color="gold"), hovertemplate="<b>%{text}</b><extra></extra>",
                               marker=dict(size=7, color="gold", symbol="diamond")))

    frames = []
    for k in range(0, n_steps, FRAME_SKIP):
        (dx, dy, dz), alt, (rx, ry, rz), (lx, ly, lz), (tx, ty, tz) = state(k)
        frames.append(go.Frame(name=str(k), traces=[1, 2, 3, 4], data=[
            go.Scatter3d(x=dx, y=dy, z=dz, customdata=alt),
            go.Scatter3d(x=rx, y=ry, z=rz),
            go.Scatter3d(x=lx, y=ly, z=lz),
            go.Scatter3d(x=tx, y=ty, z=tz)]))
    fig.frames = frames

    fig.update_layout(
        template="plotly_dark", height=700,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=f"{len(data['satellites'])} objects tracked \u00b7 {len(pairs)} close pairs in the next {HOURS} h",
        font=dict(family="Rajdhani, sans-serif", color="#eaf8ff"),
        scene=dict(aspectmode="data", bgcolor="rgba(0,0,0,0)",
                  xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),
        legend=dict(x=0.02, y=0.98), margin=dict(l=0, r=0, t=50, b=0),
        updatemenus=[{"type": "buttons", "direction": "left", "x": 0.02, "y": 0.0, "showactive": False,
                      "buttons": [
                          {"label": "Play", "method": "animate",
                           "args": [None, {"frame": {"duration": 60, "redraw": True}, "fromcurrent": True}]},
                          {"label": "Pause", "method": "animate",
                           "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]}]}],
        sliders=[{"x": 0.2, "len": 0.7, "y": 0.0, "currentvalue": {"prefix": "T+ ", "suffix": " min"},
                  "steps": [{"method": "animate", "label": f"{int(f.name) * STEP_S / 60:.1f}",
                             "args": [[f.name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]}
                            for f in frames]}],
    )
    return fig
