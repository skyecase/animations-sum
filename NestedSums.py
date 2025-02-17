from manim import *
import numpy as np
import math
from modules.helpers import fade_and_shift_in, fade_and_shift_out, grow_between, highlight, highlight_animation, morph_text


class Transformation(Scene):
    def construct(self):
        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(", "\\sum_{k=1}^n", "(f(k) - f(x+k)) + \\sum_{k=1}^x f(n", "+k)\\right)")
        sub_text = MathTex("n", "\\to", "n - 1").move_to(DOWN * 1.5)

        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(", "\\sum_{k=1}^{n-1}", "(f(k) - f(x+k)) + \\sum_{k=1}^x f(n", "-1", "+k)\\right)")

        self.add(text)

        self.play(
            LaggedStart(
                *[fade_and_shift_in(t, LEFT * 0.5, run_time=0.5) for t in sub_text],
                lag_ratio=0.25
            )
        )

        self.play(
            morph_text(text, new_text, [0, 1, 2, 4], ignore_1=[1], ignore_2=[1]),
            grow_between(new_text[1][1:3], text[1][0]),
            Transform(text[1], VGroup(new_text[1][0], *new_text[1][3:]))
        )

        self.remove(*text, *new_text, *text[1], *new_text[1])

        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=1}^x f(n", "- 1", "+ k", ")", "\\right)")
        self.add(text)

        self.play(
            fade_and_shift_out(sub_text, DOWN)
        )

        sum = MathTex("\\sum_{k=0}^{x-1} f(n + k)").move_to(text[1:5].get_center() + DOWN)

        self.play(highlight_animation(text[1:5], BLUE))


        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=1}^x f(n", "+ k", "- 1", ")", "\\right)")
        highlight(new_text[1:5], BLUE)

        self.play(
            morph_text(text, new_text, [0, 1, 3, 2, 4, 5], path_arc = PI*0.8)
        )

        equals = MathTex("=").rotate(PI/2).move_to(RIGHT * sum.get_center())

        self.play(
            text.animate.shift(UP),
            FadeIn(sum, shift = UP),
            FadeIn(equals, shift = UP, scale = 0)
        )

        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=0}^{x-1} f(n + k)", "\\right)")

        self.play(
            Transform(text[0], new_text[0]),
            Transform(text[5], new_text[2]),
            text[1:5].animate.set_color(BLACK).shift(UP).scale(0.5),
            FadeOut(equals, shift=UP, scale=0),
            Transform(sum[0], new_text[1])
        )

        self.remove(*text, *new_text, sum)
        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=0}^{x-1}", "f(n + k", ")\\right)")
        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k_1=0}^{x-1}", "f(n + k_", "1", ")\\right)")
        self.add(text)
        self.play(
            morph_text(text, new_text, [0, None, 2, 4], ignore_1=[1], ignore_2=[1]),
            Transform(text[1][:5], new_text[1][:5]),
            Transform(text[1][5:], new_text[1][6:]),
            grow_between(new_text[1][5], text[1][4], text[1][5])
        )


        self.wait()


class Bsdf(Scene):
    def construct(self):
        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+", "\\left. \\sum_{k_1=0}^{x-1} f(n + 1 + k_1)", "\\right)")
        text.scale(0.8)

        self.add(text)


        focus_text = text[1].copy()
        self.add(focus_text)
        text[1].set_color(DARK_GRAY)
        self.play(
            focus_text.animate.move_to(DOWN),
            text[0].animate.shift(UP * 2),
            text[1].animate.shift(UP * 2),
            text[2].animate.shift(UP * 2),
        )


        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1)", "= \\sum_{k_1=0}^{x-1} \\left(f(n + 1) + \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)\\right)")
        new_focus_text.move_to(DOWN).scale(0.8)

        self.play(morph_text(VGroup(focus_text), new_focus_text, [0]))

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1) = \\sum_{k_1=0}^{x-1}", "\\left(", "f(n + 1) +", "\\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "\\right)")
        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1) = \\sum_{k_1=0}^{x-1}", "f(n + 1) +", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)")
        focus_text.move_to(DOWN).scale(0.8)
        new_focus_text.move_to(DOWN).scale(0.8)
        self.play(morph_text(focus_text, new_focus_text, [0, None, 1, 3]))

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1) =", "\\sum_{k_1=0}^{x-1} f(n + 1)", "+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)")
        focus_text.move_to(DOWN).scale(0.8)
        new_text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+", "\\sum_{k_1=0}^{x-1} f(n + 1) \\\\",
            "&+ \\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "\\right)"
        ).move_to(UP).scale(0.8)
        self.add(focus_text)

        self.play(
            Transform(text[0], new_text[0]),
            Transform(focus_text[1], new_text[1]),
            Transform(focus_text[2], new_text[2]),
            Transform(text[2], new_text[3]),
            FadeOut(text[1], shift = UP),
            FadeOut(focus_text[0], shift = LEFT),
        )


        self.remove(*text, *new_text, *focus_text)

        text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+ \\sum_{k_1=0}^{x-1} f(n + 1) \\\\"
            "&+", "\\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "\\right)"
        ).move_to(UP).scale(0.8)
        focus_text = text[1].copy()
        text[1].set_color(DARK_GRAY)

        self.play(
            text.animate.move_to(UP * 1.5),
            focus_text.animate.move_to(DOWN * 1.5)
        )

        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "= \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\left(\\Delta f(n + 1) + \\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)\\right)")
        new_focus_text.move_to(DOWN * 1.5).scale(0.8)
        self.play(
            focus_text.animate.move_to(new_focus_text[0]),
            FadeIn(new_focus_text[1], shift = LEFT * 5)
        )

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2) = \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}", "\\left(", "\\Delta f(n + 1) +", "\\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)", "\\right)")
        focus_text.move_to(DOWN * 1.5).scale(0.8)
        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2) = \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}", "\\Delta f(n + 1) +", "\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)")
        new_focus_text.move_to(DOWN * 1.5).scale(0.75)
        self.play(morph_text(focus_text, new_focus_text, [0, None, 1, 3]))

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2) =", "\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\Delta f(n + 1)", "+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)")
        focus_text.move_to(DOWN * 1.5).scale(0.75)
        new_text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+ \\sum_{k_1=0}^{x-1} f(n + 1) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\Delta f(n + 1) \\\\",
            "&+ \\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + 1 + k_3)", "\\right)"
        ).scale(0.8)
        self.add(focus_text)

        self.play(
            Transform(text[0], new_text[0]),
            Transform(focus_text[1], new_text[1]),
            Transform(focus_text[2], new_text[2]),
            Transform(text[2], new_text[3]),
            FadeOut(text[1], shift = new_text[1].get_top() - text[1].get_center(), scale = 0),
            FadeOut(focus_text[0], shift = LEFT),
        )




        self.remove(*text, *new_text, *focus_text)

        text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+ \\sum_{k_1=0}^{x-1} f(n + 1) \\\\"
            "&+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\Delta f(n + 1) \\\\"
            "&+", "\\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + 1 + k_3)", "\\right)"
        ).scale(0.8)
        self.add(text)



        self.wait()
