from __future__ import annotations

from pathlib import Path
import sys
import shutil

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.physics import DoublePendulumParams, simulate, positions, energy, divergence
from chaoslab.visuals import BG, FG, CYAN, MAGENTA, GOLD, GREEN


OUT = ROOT / "animations" / "chaoslab_pitch_5min.mp4"
MUTED = "#b8b8c8"


def _style(ax):
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)
    ax.tick_params(colors="#b8b8c8")
    for spine in ax.spines.values():
        spine.set_color("#333344")
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)


def _text(ax, text, x, y, size=24, color=FG, ha="left", weight="normal"):
    ax.text(x, y, text, transform=ax.transAxes, color=color, fontsize=size, ha=ha, va="center", weight=weight)


def _draw_pendulum(ax, x1, y1, x2, y2, k, trail=120, label=None, color=CYAN):
    start = max(0, k - trail)
    ax.plot(x2[start : k + 1], y2[start : k + 1], color=color, lw=1.25, alpha=0.9)
    ax.plot([0, x1[k], x2[k]], [0, y1[k], y2[k]], color=FG, lw=2.1, alpha=0.85)
    ax.scatter([x1[k], x2[k]], [y1[k], y2[k]], s=[30, 48], color=[MAGENTA, GOLD])
    if label:
        ax.text(0.04, 0.92, label, transform=ax.transAxes, color=color, fontsize=15)


def main() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required to render animations/chaoslab_pitch_5min.mp4")

    OUT.parent.mkdir(exist_ok=True)
    params = DoublePendulumParams()
    y0 = np.array([np.radians(120.0), 0.0, np.radians(-10.0), 0.0])
    y0b = y0.copy()
    y0b[2] += 1e-6
    t, y = simulate(y0, params, t_max=30.0, n=3600)
    _, yb = simulate(y0b, params, t_max=30.0, n=3600)
    x1, yy1, x2, yy2 = positions(y, params)
    xb1, yb1, xb2, yb2 = positions(yb, params)
    d = divergence(y, yb)
    T, V, E = energy(y, params)

    regular_t = np.linspace(0, 30, 1800)
    theta = 0.55 * np.cos(np.sqrt(params.g / params.L1) * regular_t)
    sx = params.L1 * np.sin(theta)
    sy = -params.L1 * np.cos(theta)

    map_path = ROOT / "figures" / "flip_time_fractal_map.png"
    map_img = plt.imread(map_path) if map_path.exists() else None

    fps = 8
    duration = 298
    frames = fps * duration
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    writer = FFMpegWriter(fps=fps, bitrate=2400)

    with writer.saving(fig, str(OUT), dpi=100):
        for frame in range(frames):
            now = frame / fps
            fig.clf()
            fig.patch.set_facecolor(BG)

            if now < 25:
                ax = fig.add_subplot(111)
                _style(ax)
                ax.set_xlim(-2.3, 2.3)
                ax.set_ylim(-2.25, 1.25)
                ax.set_aspect("equal")
                ax.set_xticks([])
                ax.set_yticks([])
                k = min(len(t) - 1, int((now / 25) * (len(t) - 1)))
                _draw_pendulum(ax, x1, yy1, x2, yy2, k, trail=90, label="Sistema A", color=CYAN)
                _draw_pendulum(ax, xb1, yb1, xb2, yb2, k, trail=90, label=None, color=GREEN)
                _text(ax, "Mismas leyes, futuros distintos", 0.5, 0.94, size=34, color=FG, ha="center", weight="bold")
                _text(ax, r"$\Delta(0)=10^{-6}$ rad", 0.5, 0.86, size=24, color=GOLD, ha="center")

            elif now < 55:
                ax = fig.add_subplot(111)
                _style(ax)
                ax.set_xlim(-1.35, 1.35)
                ax.set_ylim(-1.25, 0.45)
                ax.set_aspect("equal")
                ax.set_xticks([])
                ax.set_yticks([])
                frac = (now - 25) / 30
                k = min(len(regular_t) - 1, int(frac * (len(regular_t) - 1)))
                ax.plot([0, sx[k]], [0, sy[k]], color=FG, lw=3)
                ax.scatter([sx[k]], [sy[k]], s=80, color=GOLD)
                ax.plot(sx[max(0, k - 220) : k + 1], sy[max(0, k - 220) : k + 1], color=CYAN, lw=1.4)
                _text(ax, "Pendulo simple: el caso ordenado", 0.5, 0.94, 34, FG, "center", "bold")
                _text(ax, r"$\omega=\frac{d\theta}{dt}$", 0.08, 0.22, 26, CYAN)
                _text(ax, r"$\sin(\theta)\approx\theta$ para angulos pequenos", 0.08, 0.13, 22, FG)

            elif now < 85:
                ax = fig.add_subplot(111)
                ax.axis("off")
                ax.set_facecolor(BG)
                _text(ax, "Agregamos una segunda masa", 0.5, 0.76, 40, FG, "center", "bold")
                _text(ax, "El estado ya no es una posicion.", 0.5, 0.58, 26, MUTED, "center")
                _text(ax, r"$s(t)=[\theta_1,\omega_1,\theta_2,\omega_2]$", 0.5, 0.43, 34, CYAN, "center")
                _text(ax, "Dos grados de libertad. Ecuaciones acopladas. No linealidad.", 0.5, 0.28, 23, GOLD, "center")

            elif now < 125:
                ax = fig.add_subplot(111)
                _style(ax)
                ax.set_xlim(-2.3, 2.3)
                ax.set_ylim(-2.25, 1.25)
                ax.set_aspect("equal")
                ax.set_xticks([])
                ax.set_yticks([])
                frac = (now - 85) / 40
                k = min(len(t) - 1, int(frac * (len(t) - 1)))
                _draw_pendulum(ax, x1, yy1, x2, yy2, k, trail=190, label=None, color=CYAN)
                _text(ax, "Simulacion numerica", 0.5, 0.94, 34, FG, "center", "bold")
                _text(ax, "solve_ivp integra el sistema paso a paso", 0.5, 0.86, 21, GOLD, "center")

            elif now < 165:
                ax = fig.add_subplot(111)
                _style(ax)
                frac = (now - 125) / 40
                k = max(5, min(len(t), int(frac * len(t))))
                ax.plot(t[:k], T[:k], color=CYAN, lw=1.6, label="Cinetica")
                ax.plot(t[:k], V[:k], color=MAGENTA, lw=1.6, label="Potencial")
                ax.plot(t[:k], E[:k], color=GOLD, lw=2.1, label="Total")
                ax.set_xlim(0, 30)
                ax.set_ylim(min(V) * 1.08, max(T) * 1.08)
                ax.set_xlabel("t [s]")
                ax.set_ylabel("Energia [J]")
                ax.set_title("Energia como prueba de calidad numerica", fontsize=28)
                ax.legend(facecolor=BG, edgecolor="#333344", labelcolor=FG, loc="upper right")

            elif now < 215:
                ax = fig.add_subplot(111)
                _style(ax)
                frac = (now - 165) / 50
                k = max(5, min(len(t), int(frac * len(t))))
                ax.semilogy(t[:k], np.maximum(d[:k], 1e-16), color=GREEN, lw=2.2)
                ax.set_xlim(0, 30)
                ax.set_ylim(1e-7, max(20, np.max(d) * 1.2))
                ax.set_xlabel("t [s]")
                ax.set_ylabel(r"$\Delta(t)$")
                ax.set_title("Sensibilidad a condiciones iniciales", fontsize=28)
                _text(ax, "Una diferencia invisible se vuelve macroscopica", 0.07, 0.16, 20, FG)

            elif now < 275:
                ax = fig.add_subplot(111)
                ax.set_facecolor(BG)
                ax.axis("off")
                if map_img is not None:
                    zoom = 1.0 + 0.08 * ((now - 215) / 60)
                    ax.imshow(map_img, extent=[-zoom, zoom, -zoom, zoom])
                _text(ax, "Cada pixel es un experimento", 0.5, 0.93, 34, FG, "center", "bold")
                _text(ax, "color = tiempo hasta el primer flip", 0.5, 0.08, 24, GOLD, "center")

            else:
                ax = fig.add_subplot(111)
                ax.axis("off")
                ax.set_facecolor(BG)
                _text(ax, "Deterministico no significa predecible", 0.5, 0.62, 40, CYAN, "center", "bold")
                _text(ax, "La fisica da reglas locales.", 0.5, 0.45, 26, FG, "center")
                _text(ax, "La computacion revela consecuencias globales.", 0.5, 0.34, 26, GOLD, "center")
                _text(ax, "ChaosLab - Fisica I", 0.5, 0.18, 20, FG, "center")

            writer.grab_frame(facecolor=BG)

    print(OUT)


if __name__ == "__main__":
    main()
