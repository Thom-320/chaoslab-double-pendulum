from __future__ import annotations

from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.physics import DoublePendulumParams, simulate, positions, divergence
from chaoslab.visuals import BG, FG, CYAN, MAGENTA, GOLD, GREEN


def draw_text(ax, text, y=0.5, size=32, color=FG, alpha=1.0):
    ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", color=color, fontsize=size, alpha=alpha, family="DejaVu Sans")


def main():
    params = DoublePendulumParams()
    y0 = np.array([np.radians(120), 0.0, np.radians(-10), 0.0])
    y0b = y0.copy(); y0b[2] += 1e-6
    t, y = simulate(y0, params, t_max=18, n=2200)
    tb, yb = simulate(y0b, params, t_max=18, n=2200)
    x1, yy1, x2, yy2 = positions(y, params)
    d = divergence(y, yb)

    map_data = np.load(ROOT / "data" / "flip_time_map_120.npz")
    th1 = map_data["theta1"]; th2 = map_data["theta2"]; flips = map_data["flip_times"]
    masked = np.ma.masked_where(flips >= flips.max() * 0.999, flips)

    out = ROOT / "animations" / "chaoslab_teaser.mp4"
    fps = 24
    duration = 16
    frames = fps * duration

    fig = plt.figure(figsize=(12.8, 7.2), dpi=120)
    writer = FFMpegWriter(fps=fps, bitrate=3200)

    with writer.saving(fig, str(out), dpi=120):
        for f in range(frames):
            time = f / fps
            fig.clf()
            fig.patch.set_facecolor(BG)

            if time < 2.5:
                ax = fig.add_subplot(111)
                ax.set_facecolor(BG); ax.axis("off")
                draw_text(ax, "ChaosLab", y=0.58, size=64, color=CYAN)
                draw_text(ax, "mismas leyes, futuros distintos", y=0.45, size=26, color=FG)
                draw_text(ax, r"$\Delta(0)=10^{-6}\ \mathrm{rad}$", y=0.34, size=30, color=GOLD)
            elif time < 8.0:
                ax = fig.add_subplot(111)
                ax.set_facecolor(BG)
                ax.set_xlim(-2.25, 2.25); ax.set_ylim(-2.25, 1.25); ax.set_aspect("equal")
                ax.set_xticks([]); ax.set_yticks([])
                for sp in ax.spines.values(): sp.set_visible(False)
                frac = (time - 2.5) / 5.5
                k = int(frac * (len(t) - 1))
                start = max(0, k - 170)
                ax.plot(x2[start:k+1], yy2[start:k+1], color=CYAN, lw=1.4, alpha=0.9)
                ax.plot([0, x1[k], x2[k]], [0, yy1[k], yy2[k]], color=FG, lw=2.8, alpha=0.85)
                ax.scatter([x1[k], x2[k]], [yy1[k], yy2[k]], s=[55, 85], color=[MAGENTA, GOLD])
                ax.text(0.03, 0.92, "1. Simular el sistema", transform=ax.transAxes, color=FG, fontsize=24)
                ax.text(0.03, 0.85, "ángulos → velocidades → aceleraciones", transform=ax.transAxes, color="#bfc0d0", fontsize=17)
            elif time < 11.5:
                ax = fig.add_subplot(111)
                ax.set_facecolor(BG)
                for sp in ax.spines.values(): sp.set_color("#333344")
                ax.tick_params(colors="#bbbbcc")
                frac = (time - 8.0) / 3.5
                k = max(10, int(frac * (len(t) - 1)))
                ax.semilogy(t[:k], np.maximum(d[:k], 1e-16), color=GREEN, lw=2.4)
                ax.set_xlim(0, 18); ax.set_ylim(1e-8, max(5, np.nanmax(d)*1.2))
                ax.set_xlabel("t [s]", color=FG); ax.set_ylabel(r"$\Delta(t)$", color=FG)
                ax.set_title("2. Medir divergencia", color=FG, fontsize=28)
                ax.text(0.05, 0.12, "una diferencia invisible se vuelve macroscópica", transform=ax.transAxes, color="#bfc0d0", fontsize=18)
            else:
                ax = fig.add_subplot(111)
                ax.set_facecolor(BG)
                im = ax.imshow(masked, extent=[-np.pi, np.pi, -np.pi, np.pi], origin="lower", cmap="turbo", interpolation="bilinear")
                ax.set_xlabel(r"$\theta_1(0)$", color=FG); ax.set_ylabel(r"$\theta_2(0)$", color=FG)
                ax.tick_params(colors="#bbbbcc")
                for sp in ax.spines.values(): sp.set_color("#333344")
                ax.set_title("3. Cada pixel es un experimento", color=FG, fontsize=28)
                ax.text(0.05, 0.08, "color = tiempo hasta el primer flip", transform=ax.transAxes, color=FG, fontsize=18, bbox=dict(facecolor=BG, alpha=0.6, edgecolor="#333344"))

            writer.grab_frame(facecolor=BG)
    print(out)


if __name__ == "__main__":
    main()
