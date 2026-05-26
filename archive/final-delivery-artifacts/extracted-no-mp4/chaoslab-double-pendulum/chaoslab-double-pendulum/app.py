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
st.caption("Mecánica clásica + ecuaciones diferenciales + visualización estilo 2swap/3Blue1Brown, sin sacrificios humanos al WiFi.")

with st.sidebar:
    st.header("Parámetros")
    L1 = st.slider("L1 [m]", 0.2, 2.0, 1.0, 0.05)
    L2 = st.slider("L2 [m]", 0.2, 2.0, 1.0, 0.05)
    m1 = st.slider("m1 [kg]", 0.1, 5.0, 1.0, 0.1)
    m2 = st.slider("m2 [kg]", 0.1, 5.0, 1.0, 0.1)
    th1 = st.slider("theta1(0) [deg]", -180.0, 180.0, 120.0, 1.0)
    th2 = st.slider("theta2(0) [deg]", -180.0, 180.0, -10.0, 1.0)
    w1 = st.slider("omega1(0) [rad/s]", -5.0, 5.0, 0.0, 0.1)
    w2 = st.slider("omega2(0) [rad/s]", -5.0, 5.0, 0.0, 0.1)
    eps = st.select_slider("Perturbación epsilon en theta2", options=[1e-8, 1e-7, 1e-6, 1e-5, 1e-4], value=1e-6)
    tmax = st.slider("Tiempo de simulación [s]", 5.0, 40.0, 20.0, 1.0)

params = DoublePendulumParams(m1=m1, m2=m2, L1=L1, L2=L2)
y0 = np.array([np.radians(th1), w1, np.radians(th2), w2])
t, y = simulate(y0, params, t_max=tmax, n=1800)
y0b = y0.copy(); y0b[2] += eps
tb, yb = simulate(y0b, params, t_max=tmax, n=1800)
d = divergence(y, yb)
slope = estimate_lyapunov_slope(t, d, fit_window=(1.0, min(7.0, tmax)))
T, V, E = energy(y, params)
rel_drift = np.max(np.abs((E - E[0]) / max(abs(E[0]), 1e-12)))
x1, yy1, x2, yy2 = positions(y, params)

col1, col2 = st.columns([1.05, 1.0])
with col1:
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
    ax.plot(t, T, color="#42e8f5", label="T")
    ax.plot(t, V, color="#ff2bd6", label="V")
    ax.plot(t, E, color="#ffcf33", label="E")
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

st.metric("Deriva relativa máxima de energía", f"{rel_drift:.2e}")
st.metric("Pendiente temprana de log(Delta)", f"{slope:.3g} 1/s")
st.info("La pendiente no se presenta como exponente de Lyapunov formal, sino como indicador cuantitativo de sensibilidad a condiciones iniciales.")
