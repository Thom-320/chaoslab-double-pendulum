from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

from .physics import DoublePendulumParams, positions, energy

BG = "#05050a"
FG = "#f2f2f2"
CYAN = "#42e8f5"
MAGENTA = "#ff2bd6"
GOLD = "#ffcf33"
VIOLET = "#8c6cff"
GREEN = "#82ff7a"


def set_dark(ax):
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)
    ax.tick_params(colors="#b8b8c8")
    for spine in ax.spines.values():
        spine.set_color("#333344")
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)
    return ax


def save_trajectory(t, y, out: str | Path, params: DoublePendulumParams = DoublePendulumParams()):
    out = Path(out)
    x1, y1, x2, y2 = positions(y, params)
    fig, ax = plt.subplots(figsize=(7, 7), dpi=180)
    set_dark(ax)
    ax.plot(x2, y2, color=CYAN, lw=1.3, alpha=0.9)
    ax.plot(x1, y1, color=MAGENTA, lw=0.8, alpha=0.65)
    ax.scatter([x2[0]], [y2[0]], s=25, color=GOLD, label="inicio")
    ax.scatter([x2[-1]], [y2[-1]], s=25, color=GREEN, label="final")
    lim = params.L1 + params.L2 + 0.1
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Trayectoria de la segunda masa: orden local, caos global")
    ax.legend(facecolor=BG, edgecolor="#333344", labelcolor=FG, loc="upper right")
    fig.tight_layout()
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def save_energy(t, y, out: str | Path, params: DoublePendulumParams = DoublePendulumParams()):
    out = Path(out)
    T, V, E = energy(y, params)
    rel = (E - E[0]) / max(1e-12, abs(E[0]))
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=180)
    set_dark(ax)
    ax.plot(t, T, color=CYAN, lw=1.4, label="Cinética")
    ax.plot(t, V, color=MAGENTA, lw=1.4, label="Potencial")
    ax.plot(t, E, color=GOLD, lw=1.8, label="Total")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("Energía [J]")
    ax.set_title("Conservación de energía como prueba de calidad numérica")
    ax.legend(facecolor=BG, edgecolor="#333344", labelcolor=FG)
    fig.tight_layout()
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)

    rel_out = out.with_name(out.stem + "_relative_error.png")
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=180)
    set_dark(ax)
    ax.plot(t, rel, color=GREEN, lw=1.4)
    ax.axhline(0, color="#777777", lw=0.8)
    ax.set_xlabel("t [s]")
    ax.set_ylabel("(E(t)-E(0))/|E(0)|")
    ax.set_title("Deriva relativa de energía")
    fig.tight_layout()
    fig.savefig(rel_out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def save_divergence(t, delta, out: str | Path):
    out = Path(out)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=180)
    set_dark(ax)
    ax.semilogy(t, np.maximum(delta, 1e-16), color=CYAN, lw=1.8)
    ax.set_xlabel("t [s]")
    ax.set_ylabel(r"$\Delta(t)$")
    ax.set_title("Sensibilidad a condiciones iniciales: una diferencia microscópica crece")
    fig.tight_layout()
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def save_fractal_map(theta1, theta2, flip_times, out: str | Path, t_max: float):
    out = Path(out)
    data = np.ma.masked_where(flip_times >= t_max * 0.999, flip_times)
    fig, ax = plt.subplots(figsize=(7.2, 6.2), dpi=180)
    set_dark(ax)
    im = ax.imshow(
        data,
        extent=[theta1.min(), theta1.max(), theta2.min(), theta2.max()],
        origin="lower",
        cmap="turbo",
        interpolation="bilinear",
        aspect="equal",
    )
    ax.contour(theta1, theta2, flip_times >= t_max * 0.999, levels=[0.5], colors=[FG], linewidths=0.45, alpha=0.9)
    ax.set_xlabel(r"$\theta_1(0)$ [rad]")
    ax.set_ylabel(r"$\theta_2(0)$ [rad]")
    ax.set_title("Mapa de condiciones iniciales: tiempo hasta el primer flip")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("tiempo hasta flip [s]", color=FG)
    cbar.ax.yaxis.set_tick_params(color=FG)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=FG)
    fig.tight_layout()
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def animate_double_pendulum(t, y, out: str | Path, params: DoublePendulumParams = DoublePendulumParams(), fps: int = 30, seconds: float = 8.0):
    out = Path(out)
    x1, yy1, x2, yy2 = positions(y, params)
    total_frames = max(2, int(fps * seconds))
    idx = np.linspace(0, len(t) - 1, total_frames).astype(int)

    fig, ax = plt.subplots(figsize=(6, 6), dpi=140)
    set_dark(ax)
    lim = params.L1 + params.L2 + 0.25
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("ChaosLab: double pendulum", color=FG, pad=12)

    rod_line, = ax.plot([], [], color=FG, lw=2.0, alpha=0.75)
    bob_line, = ax.plot([], [], "o", color=GOLD, markersize=6)
    trail_line, = ax.plot([], [], color=CYAN, lw=1.0, alpha=0.9)
    time_text = ax.text(0.03, 0.96, "", transform=ax.transAxes, color="#bbbbcc", ha="left", va="top")

    trail = 120

    def update(frame_number):
        k = idx[frame_number]
        rod_line.set_data([0, x1[k], x2[k]], [0, yy1[k], yy2[k]])
        bob_line.set_data([x1[k], x2[k]], [yy1[k], yy2[k]])
        start = max(0, k - trail)
        trail_line.set_data(x2[start:k+1], yy2[start:k+1])
        time_text.set_text(f"t = {t[k]:.2f} s")
        return rod_line, bob_line, trail_line, time_text

    ani = FuncAnimation(fig, update, frames=total_frames, blit=True)
    if out.suffix.lower() == ".gif":
        ani.save(out, writer=PillowWriter(fps=fps))
    else:
        ani.save(out, writer=FFMpegWriter(fps=fps, bitrate=1800))
    plt.close(fig)
