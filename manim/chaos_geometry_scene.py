"""Optional Manim scene for the ChaosLab presentation.

This file is intentionally not part of the required runtime. The main project
runs with NumPy/SciPy/Matplotlib/Streamlit. Use this scene only if Manim is
already available locally and you want a short 3Blue1Brown-style clip for the
geometric model.

Run from the repository root:

    pip install -r requirements-manim.txt
    manim -pqh manim/chaos_geometry_scene.py ChaosGeometryScene

The output can be inserted as a backup clip, not as a dependency for the live
presentation.
"""

from __future__ import annotations

from manim import *
import numpy as np


class ChaosGeometryScene(Scene):
    def construct(self):
        self.camera.background_color = "#05050a"
        cyan = "#42e8f5"
        gold = "#ffcf33"
        magenta = "#ff2bd6"
        green = "#82ff7a"
        fg = "#f2f2f2"
        muted = "#8f90a3"

        title = Text("De ángulos a coordenadas", font_size=44, weight=BOLD, color=fg)
        title.to_edge(UP)
        subtitle = Text("la animación sale del modelo físico", font_size=24, color=muted)
        subtitle.next_to(title, DOWN, buff=0.18)
        self.play(Write(title), FadeIn(subtitle, shift=0.2 * DOWN), run_time=1.2)

        pivot = np.array([-2.4, 1.15, 0.0])
        L1 = 1.6
        L2 = 1.35
        theta1 = 0.78
        theta2 = -0.56
        p1 = pivot + np.array([L1 * np.sin(theta1), -L1 * np.cos(theta1), 0])
        p2 = p1 + np.array([L2 * np.sin(theta2), -L2 * np.cos(theta2), 0])

        vertical_1 = DashedLine(pivot, pivot + np.array([0, -1.9, 0]), color=muted, stroke_opacity=0.55)
        vertical_2 = DashedLine(p1, p1 + np.array([0, -1.45, 0]), color=muted, stroke_opacity=0.45)
        rod1 = Line(pivot, p1, color=fg, stroke_width=6)
        rod2 = Line(p1, p2, color=fg, stroke_width=6)
        bob1 = Dot(p1, radius=0.09, color=magenta)
        bob2 = Dot(p2, radius=0.11, color=gold)
        arc1 = Arc(radius=0.42, start_angle=-PI / 2, angle=theta1, color=cyan).shift(pivot)
        arc2 = Arc(radius=0.34, start_angle=-PI / 2, angle=theta2, color=gold).shift(p1)
        label1 = MathTex(r"\theta_1", color=cyan, font_size=34).move_to(pivot + np.array([0.42, -0.55, 0]))
        label2 = MathTex(r"\theta_2", color=gold, font_size=34).move_to(p1 + np.array([-0.35, -0.44, 0]))

        self.play(Create(vertical_1), Create(vertical_2), Create(rod1), Create(rod2), FadeIn(bob1), FadeIn(bob2), run_time=1.6)
        self.play(Create(arc1), Create(arc2), FadeIn(label1), FadeIn(label2), run_time=1.0)

        eqs = VGroup(
            MathTex(r"x_1=L_1\sin\theta_1", color=cyan, font_size=34),
            MathTex(r"y_1=-L_1\cos\theta_1", color=magenta, font_size=34),
            MathTex(r"x_2=x_1+L_2\sin\theta_2", color=gold, font_size=34),
            MathTex(r"y_2=y_1-L_2\cos\theta_2", color=green, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        eqs.to_corner(RIGHT + DOWN).shift(0.25 * UP)

        guides = VGroup(
            DashedLine([pivot[0], p1[1], 0], p1, color=cyan),
            DashedLine(pivot, [pivot[0], p1[1], 0], color=magenta),
            DashedLine([p1[0], p2[1], 0], p2, color=gold),
            DashedLine(p1, [p1[0], p2[1], 0], color=green),
        )
        self.play(Create(guides[0]), Write(eqs[0]), run_time=0.9)
        self.play(Create(guides[1]), Write(eqs[1]), run_time=0.9)
        self.play(Create(guides[2]), Write(eqs[2]), run_time=0.9)
        self.play(Create(guides[3]), Write(eqs[3]), run_time=0.9)

        state = MathTex(r"s(t)=[\theta_1,\omega_1,\theta_2,\omega_2]", color=fg, font_size=38)
        state.next_to(subtitle, DOWN, buff=0.45)
        box = SurroundingRectangle(state, color=cyan, buff=0.16)
        self.play(FadeIn(state, shift=0.2 * UP), Create(box), run_time=1.1)
        self.wait(0.8)

        closing = Text("una ley local → una trayectoria global", font_size=34, color=gold)
        closing.to_edge(DOWN)
        self.play(FadeIn(closing), run_time=1.0)
        self.wait(1.2)
