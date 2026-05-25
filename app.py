"""Streamlit app for ChaosLab.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

try:
    import streamlit as st
except ImportError as exc:
    raise SystemExit("Install streamlit first: pip install -r requirements.txt") from exc

from chaoslab.physics import DoublePendulumParams, simulate, positions, energy, divergence, estimate_lyapunov_slope

st.set_page_config(page_title="ChaosLab", layout="wide")
st.title("ChaosLab: del péndulo simple al péndulo doble caótico")
st.caption("Mecánica clásica + ecuaciones diferenciales + visualización estilo 2swap/3Blue1Brown.")

PRESETS = {
    "Caótico": dict(th1=120.0, th2=-10.0, w1=0.0, w2=0.0, L1=1.0, L2=1.0, m1=1.0, m2=1.0),
    "Regular": dict(th1=18.0, th2=12.0, w1=0.0, w2=0.0, L1=1.0, L2=1.0, m1=1.0, m2=1.0),
    "Isla estable": dict(th1=92.0, th2=-96.0, w1=0.0, w2=0.0, L1=1.0, L2=1.0, m1=1.0, m2=1.0),
    "Alta energía": dict(th1=170.0, th2=-150.0, w1=0.0, w2=0.0, L1=1.0, L2=1.0, m1=1.0, m2=1.0),
}


@st.cache_data(show_spinner=False)
def run_case(m1, m2, L1, L2, th1, th2, w1, w2, eps, tmax):
    params = DoublePendulumParams(m1=m1, m2=m2, L1=L1, L2=L2)
    y0 = np.array([np.radians(th1), w1, np.radians(th2), w2])
    t, y = simulate(y0, params, t_max=tmax, n=1800)
    y0b = y0.copy()
    y0b[2] += eps
    _, yb = simulate(y0b, params, t_max=tmax, n=1800)
    d = divergence(y, yb)
    slope = estimate_lyapunov_slope(t, d, fit_window=(1.0, min(7.0, tmax)))
    T, V, E = energy(y, params)
    rel_drift = np.max(np.abs((E - E[0]) / max(abs(E[0]), 1e-12)))
    x1, yy1, x2, yy2 = positions(y, params)
    return t, y, d, slope, T, V, E, rel_drift, x1, yy1, x2, yy2

with st.sidebar:
    st.header("Modo presentación")
    preset_name = st.selectbox("Escena base", list(PRESETS), index=0)
    preset = PRESETS[preset_name]
    st.write("Usa los presets para una demo estable; luego ajusta parámetros si quieres explorar.")

    st.header("Parámetros")
    L1 = st.slider("L1 [m]", 0.2, 2.0, preset["L1"], 0.05)
    L2 = st.slider("L2 [m]", 0.2, 2.0, preset["L2"], 0.05)
    m1 = st.slider("m1 [kg]", 0.1, 5.0, preset["m1"], 0.1)
    m2 = st.slider("m2 [kg]", 0.1, 5.0, preset["m2"], 0.1)
    th1 = st.slider("theta1(0) [deg]", -180.0, 180.0, preset["th1"], 1.0)
    th2 = st.slider("theta2(0) [deg]", -180.0, 180.0, preset["th2"], 1.0)
    w1 = st.slider("omega1(0) [rad/s]", -5.0, 5.0, preset["w1"], 0.1)
    w2 = st.slider("omega2(0) [rad/s]", -5.0, 5.0, preset["w2"], 0.1)
    eps = st.select_slider("Perturbación epsilon en theta2", options=[1e-8, 1e-7, 1e-6, 1e-5, 1e-4], value=1e-6)
    tmax = st.slider("Tiempo de simulación [s]", 5.0, 40.0, 20.0, 1.0)

params = DoublePendulumParams(m1=m1, m2=m2, L1=L1, L2=L2)
with st.spinner("Integrando el sistema..."):
    t, y, d, slope, T, V, E, rel_drift, x1, yy1, x2, yy2 = run_case(
        m1, m2, L1, L2, th1, th2, w1, w2, eps, tmax
    )

tab_demo, tab_assets, tab_methods = st.tabs(["Laboratorio interactivo", "Pitch visual", "Método"])

with tab_demo:
    col1, col2 = st.columns([1.05, 1.0])
    with col1:
        st.subheader(f"Escena: {preset_name}")
        st.write("La línea cian es la trayectoria de la segunda masa; la magenta, la primera.")
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120)
        ax.set_facecolor("#05050a"); fig.set_facecolor("#05050a")
        ax.plot(x2, yy2, color="#42e8f5", lw=1.2)
        ax.plot(x1, yy1, color="#ff2bd6", lw=0.8, alpha=0.7)
        k = -1
        ax.plot([0, x1[k], x2[k]], [0, yy1[k], yy2[k]], color="#eeeeee", lw=2)
        ax.scatter([x1[k], x2[k]], [yy1[k], yy2[k]], s=55, color="#ffcf33")
        lim = L1 + L2 + 0.25
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
        ax.set_title("Trayectoria", color="#f2f2f2")
        ax.tick_params(colors="#bbbbcc")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 3.4), dpi=120)
        ax.set_facecolor("#05050a"); fig.set_facecolor("#05050a")
        ax.plot(t, T, color="#42e8f5", label="Cinética")
        ax.plot(t, V, color="#ff2bd6", label="Potencial")
        ax.plot(t, E, color="#ffcf33", label="Total")
        ax.set_title("Energía mecánica", color="#f2f2f2")
        ax.tick_params(colors="#bbbbcc")
        ax.legend(facecolor="#05050a", labelcolor="#f2f2f2")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(7, 3.4), dpi=120)
        ax.set_facecolor("#05050a"); fig.set_facecolor("#05050a")
        ax.semilogy(t, np.maximum(d, 1e-16), color="#82ff7a")
        ax.set_title("Divergencia entre trayectorias", color="#f2f2f2")
        ax.tick_params(colors="#bbbbcc")
        st.pyplot(fig)

    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("Deriva relativa máxima de energía", f"{rel_drift:.2e}")
    mcol2.metric("Perturbación inicial", f"{eps:.0e} rad")
    mcol3.metric("Pendiente temprana de log(Delta)", f"{slope:.3g} 1/s")
    st.info("La pendiente no se presenta como exponente de Lyapunov formal, sino como indicador cuantitativo de sensibilidad a condiciones iniciales.")

with tab_assets:
    st.subheader("Activos listos para la exposición")
    teaser = ROOT / "animations" / "chaoslab_teaser.mp4"
    gif = ROOT / "animations" / "double_pendulum.gif"
    fmap = ROOT / "figures" / "flip_time_fractal_map.png"
    pitch = ROOT / "animations" / "chaoslab_pitch_5min.mp4"
    if pitch.exists():
        st.video(str(pitch))
    elif teaser.exists():
        st.video(str(teaser))
    cols = st.columns(2)
    if gif.exists():
        cols[0].image(str(gif), caption="Animación del péndulo doble")
    if fmap.exists():
        cols[1].image(str(fmap), caption="Mapa de condiciones iniciales")

with tab_methods:
    st.subheader("Cómo leer la demo")
    st.markdown(
        """
        - El estado del sistema es `[theta1, omega1, theta2, omega2]`.
        - Las velocidades angulares son derivadas de los ángulos: `omega = dtheta/dt`.
        - La energía total `E = T + V` funciona como prueba de calidad numérica.
        - La divergencia compara dos sistemas con una diferencia inicial microscópica.
        - El mapa de condiciones iniciales es exploratorio: cada pixel integra un caso y colorea el tiempo hasta el primer flip.
        """
    )
