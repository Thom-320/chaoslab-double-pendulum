from __future__ import annotations

from pathlib import Path
import shutil
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.physics import DoublePendulumParams, simulate, positions
from chaoslab.visuals import BG, FG, CYAN, MAGENTA, GOLD, GREEN

OUT = ROOT / "animations" / "manim_style_geometry.mp4"
MUTED = "#9a9aac"


def setup(ax):
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)
    ax.set_xlim(-2.6, 2.8)
    ax.set_ylim(-2.7, 1.35)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def alpha_phase(now, start, duration=1.0):
    return float(np.clip((now - start) / duration, 0.0, 1.0))


def main() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required to render animations/manim_style_geometry.mp4")

    OUT.parent.mkdir(exist_ok=True)
    params = DoublePendulumParams()
    y0 = np.array([np.radians(110), 0.0, np.radians(-35), 0.0])
    t, y = simulate(y0, params, t_max=8.0, n=480)
    x1, y1, x2, y2 = positions(y, params)
    theta1 = np.arctan2(x1, -y1)
    theta2 = np.arctan2(x2 - x1, -(y2 - y1))

    fps = 30
    duration = 18
    frames = fps * duration
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    writer = FFMpegWriter(fps=fps, bitrate=3500, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-preset", "medium"])

    with writer.saving(fig, str(OUT), dpi=100):
        for frame in range(frames):
            now = frame / fps
            fig.clf()
            fig.patch.set_facecolor(BG)
            ax = fig.add_subplot(111)
            setup(ax)

            k = min(len(t) - 1, int((now / duration) * (len(t) - 1)))
            px1, py1, px2, py2 = x1[k], y1[k], x2[k], y2[k]

            ax.text(-2.45, 1.08, "De ángulos a coordenadas", color=FG, fontsize=25, weight="bold")
            ax.text(-2.45, 0.86, "escena opcional estilo 3Blue1Brown / Manim", color=MUTED, fontsize=12)

            ax.plot([0, 0], [0, -1.35], color=MUTED, lw=1.0, ls="--", alpha=0.65)
            ax.plot([px1, px1], [py1, py1 - 1.0], color=MUTED, lw=1.0, ls="--", alpha=0.45)
            ax.plot([0, px1, px2], [0, py1, py2], color=FG, lw=3.2, alpha=0.92)
            ax.scatter([px1, px2], [py1, py2], s=[62, 88], color=[MAGENTA, GOLD], zorder=5)
            ax.text(0.13, -0.20, r"$\theta_1$", color=CYAN, fontsize=17)
            ax.text(px1 + 0.08, py1 - 0.18, r"$\theta_2$", color=GOLD, fontsize=17)

            a = alpha_phase(now, 3.0, 1.0)
            if a > 0:
                ax.plot([0, px1], [py1, py1], color=CYAN, lw=2.0, ls="--", alpha=a)
                ax.text(-2.45, 0.35, r"$x_1=L_1\sin\theta_1$", color=CYAN, fontsize=18, alpha=a)
            a = alpha_phase(now, 4.4, 1.0)
            if a > 0:
                ax.plot([0, 0], [0, py1], color=MAGENTA, lw=2.0, ls="--", alpha=a)
                ax.text(-2.45, 0.07, r"$y_1=-L_1\cos\theta_1$", color=MAGENTA, fontsize=18, alpha=a)
            a = alpha_phase(now, 5.8, 1.0)
            if a > 0:
                ax.plot([px1, px2], [py2, py2], color=GOLD, lw=2.0, ls="--", alpha=a)
                ax.text(-2.45, -0.21, r"$x_2=x_1+L_2\sin\theta_2$", color=GOLD, fontsize=18, alpha=a)
            a = alpha_phase(now, 7.2, 1.0)
            if a > 0:
                ax.plot([px1, px1], [py1, py2], color=GREEN, lw=2.0, ls="--", alpha=a)
                ax.text(-2.45, -0.49, r"$y_2=y_1-L_2\cos\theta_2$", color=GREEN, fontsize=18, alpha=a)

            a = alpha_phase(now, 9.0, 1.2)
            if a > 0:
                # Draw a small angle-space inset.
                left, bottom, size = 0.78, -2.25, 1.45
                ax.add_patch(plt.Rectangle((left, bottom), size, size, fill=False, ec="#333344", lw=1.1, alpha=a))
                ax.axvline(left + size / 2, ymin=(bottom + 2.7) / 4.05, ymax=(bottom + size + 2.7) / 4.05, color="#66667a", lw=0.7, alpha=0.6 * a)
                ax.axhline(bottom + size / 2, xmin=(left + 2.6) / 5.4, xmax=(left + size + 2.6) / 5.4, color="#66667a", lw=0.7, alpha=0.6 * a)
                n = max(3, min(k, len(theta1) - 1))
                xs = left + ((theta1[:n] + np.pi) / (2 * np.pi)) * size
                ys = bottom + ((theta2[:n] + np.pi) / (2 * np.pi)) * size
                ax.plot(xs, ys, color=CYAN, lw=1.7, alpha=a)
                ax.scatter([xs[-1]], [ys[-1]], s=28, color=GOLD, alpha=a)
                ax.text(left, bottom + size + 0.12, r"huella angular: $\theta_1(t)$ vs $\theta_2(t)$", color=FG, fontsize=13, alpha=a)
                ax.text(left + size * 0.38, bottom - 0.18, r"$\theta_1$", color=MUTED, fontsize=11, alpha=a)
                ax.text(left - 0.23, bottom + size * 0.45, r"$\theta_2$", color=MUTED, fontsize=11, alpha=a)

            a = alpha_phase(now, 13.0, 1.0)
            if a > 0:
                ax.text(-2.45, -2.28, r"Una ley local produce una trayectoria global.", color=FG, fontsize=19, weight="bold", alpha=a)
                ax.text(-2.45, -2.52, r"Y miles de trayectorias producen el mapa final.", color=GOLD, fontsize=14, alpha=a)

            writer.grab_frame()

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
