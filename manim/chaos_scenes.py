"""Optional Manim sketch.

This is not required for the project to run. It is included as a visual direction
if you later want a more 3Blue1Brown-style explainer. Install Manim Community
and run something like:
    manim -pqh manim/chaos_scenes.py OpeningScene
"""
from manim import *

class OpeningScene(Scene):
    def construct(self):
        title = Text("ChaosLab", font_size=72)
        subtitle = Text("Del péndulo simple al caos", font_size=34).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle, shift=UP))
        self.wait(1)
        eq = MathTex(r"\Delta(0) = 10^{-6}\ \mathrm{rad}", r"\quad\Longrightarrow\quad", r"\Delta(t)\ \text{crece}")
        self.play(Transform(VGroup(title, subtitle), eq))
        self.wait(2)
