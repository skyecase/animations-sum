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

        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) + \\sum_{k=0}^{x-1}", "f(n + k)\\right)")
        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) + \\sum_{k=0}^{x-1}", "\\Delta^0", "f(n + k)\\right)")
        self.play(morph_text(text, new_text, [0, 2]))

        self.remove(*text, *new_text)
        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=0}^{x-1}", "\\Delta^0 f(n + k", ")\\right)")
        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n + k_", "1", ")\\right)")
        self.add(text)
        self.play(
            morph_text(text, new_text, [0, None, 2, 4], ignore_1=[1], ignore_2=[1]),
            Transform(text[1][:5], new_text[1][:5]),
            Transform(text[1][5:], new_text[1][6:]),
            grow_between(new_text[1][5], text[1][4], text[1][5])
        )


        self.wait()



class SuperRecursive2(Scene):
    def construct(self):
        text = MathTex("f(a + b) =", "f(a) + \\sum_{k=0}^{b-1} \\Delta", "f(a + k)")
        self.play(Write(text))

        new_text = MathTex("\\Delta^0", "f(a + b) =", "\\Delta^0", "f(a) + \\sum_{k=0}^{b-1} \\Delta^", "1", "f(a + k)")
        self.play(morph_text(text, new_text, [1, 3, 5]))

        self.remove(*text, *new_text)
        text = new_text
        self.add(text)


        text_2 = MathTex("\\Delta^1 f(a + b) = \\Delta^1 f(a) + \\sum_{k=0}^{b-1} \\Delta^2 f(a + k)").move_to(DOWN*1.5)
        self.play(
            text.animate.shift(UP*1.5),
            FadeIn(text_2, shift=UP*1.5)
        )

        self.play(Transform(text_2, MathTex("\\Delta^2 f(a + b) = \\Delta^2 f(a) + \\sum_{k=0}^{b-1} \\Delta^3 f(a + k)").move_to(DOWN*1.5)))
        self.play(Transform(text_2, MathTex("\\Delta^3 f(a + b) = \\Delta^3 f(a) + \\sum_{k=0}^{b-1} \\Delta^4 f(a + k)").move_to(DOWN*1.5)))

        self.remove(text_2)
        text_2 = MathTex("\\Delta^3 f(a + b) = \\Delta^3 f(a) + \\sum_{k=0}^{b-1} \\Delta^", "4", "f(a + k)").move_to(DOWN*1.5)
        self.add(text_2)
        new_text_2 = MathTex("\\Delta^n f(a + b) = \\Delta^n f(a) + \\sum_{k=0}^{b-1} \\Delta^", "{n+1}", "f(a + k)").move_to(DOWN*1.5)

        self.play(Transform(text_2, new_text_2))

        self.wait()




class BigSolution(Scene):
    def construct(self):
        lim_text = MathTex("\\lim_{x \\to \\infty} \\Delta^3 f(x) = 0").scale(0.8).move_to(UP * 3)
        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n + k_1)", "\\right)")

        self.add(text, lim_text)

        self.play(highlight_animation(text[2], BLUE))


        low_text = MathTex("\\Delta^0 f(", "a", "+ b) = \\Delta^0 f(", "a", ") + \\sum_{k_2=0}^{b-1} \\Delta^1 f(", "a", "+ k_2)").move_to(DOWN * 2)

        self.play(
            text.animate.shift(UP),
            FadeIn(low_text, shift=UP)
        )

        self.play(highlight_animation(VGroup(low_text[1], low_text[3], low_text[5]), YELLOW), run_time=0.5)

        new_low_text = MathTex("\\Delta^0 f(", "n", "+ b) = \\Delta^0 f(", "n", ") + \\sum_{k_2=0}^{b-1} \\Delta^1 f(", "n", "+ k_2)").move_to(DOWN * 2)
        self.play(Transform(low_text, new_low_text))

        self.remove(*low_text, *new_low_text)
        low_text = MathTex("\\Delta^0 f(n +", "b", ") = \\Delta^0 f(n) +", "\\sum_{k_2=0}^{b-1}", "\\Delta^1 f(n + k_2)").move_to(DOWN * 2)
        self.add(low_text)
        self.play(highlight_animation(VGroup(low_text[1], low_text[3][0]), YELLOW), run_time=0.5)

        new_low_text = MathTex("\\Delta^0 f(n +", "k_1", ") = \\Delta^0 f(n) +", "\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n + k_2)").move_to(DOWN * 2)
        self.play(
            Transform(low_text[0:3], new_low_text[0:3]),
            Transform(low_text[4:], new_low_text[4:]),
            Transform(low_text[3][1:], new_low_text[3][2:]),
            Transform(low_text[3][0], new_low_text[3][0:2]),
        )

        self.remove(*new_low_text, *low_text, *new_low_text[3], *low_text[3])
        low_text = MathTex("\\Delta^0 f(n + k_1)", "=", "\\Delta^0 f(n) + \\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)").move_to(DOWN * 2)
        new_low_text = MathTex("\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n + k_1)", "=", "\\sum_{k_1=0}^{x-1} \\left(", "\\Delta^0 f(n) + \\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)", "\\right)").move_to(DOWN * 2)
        highlight(new_low_text[0:2], BLUE)
        new_low_text[0].save_state()
        new_low_text[0].set_stroke(width=0).set_color(BLACK).scale(0).move_to(low_text[0].get_left())
        self.play(
            morph_text(low_text, new_low_text, [1, 2, 4], ignore_2=[0]),
            new_low_text[0].animate.restore(),
            highlight_animation(text[1], BLUE)
        )

        self.remove(*low_text, *new_low_text)
        low_text = MathTex("\\sum_{k_1=0}^{x-1} \\Delta^0 f(n + k_1)", "=", "\\sum_{k_1=0}^{x-1}", "\\left(", "\\Delta^0 f(n) +", "\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)", "\\right)").move_to(DOWN * 2)
        self.add(low_text)
        new_low_text = MathTex("\\sum_{k_1=0}^{x-1} \\Delta^0 f(n + k_1)", "=", "\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n) +", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)").move_to(DOWN * 2)
        highlight(low_text[0], BLUE)
        highlight(new_low_text[0], BLUE)
        sum_copy = low_text[2].copy()
        self.play(
            morph_text(low_text, new_low_text, [0, 1, 2, None, 3, 5], ignore_2=[4]),
            Transform(sum_copy, new_low_text[4], path_arc=PI*3/4)
        )

        self.remove(*low_text, *new_low_text, sum_copy)
        low_text = MathTex("\\sum_{k_1=0}^{x-1} \\Delta^0 f(n + k_1)", "=", "\\sum_{k_1=0}^{x-1} \\Delta^0 f(n)", "+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)").move_to(DOWN * 2)
        highlight(low_text[0], BLUE)
        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+", "\\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\",
            "&+ \\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta^1 f(n + k_2)", "\\right)"
        ).scale(0.9)

        self.play(
            Transform(text[0], new_text[0]),
            text[1:3].animate(remover=True).scale(0).move_to(new_text[1].get_top()).set_stroke(width=0).set_color(BLACK),
            Transform(text[3], new_text[3]),
            Transform(low_text[2], new_text[1]),
            Transform(low_text[3], new_text[2]),
            low_text[0:2].animate(remover=True).shift(DOWN).set_stroke(width=0).set_color(BLACK),
        )



        # =====================================
        # SECOND ITERATION
        # =====================================

        self.remove(*text, *new_text, *low_text)
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\",
            "&+ \\left.", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n + k_2)", "\\right)"
        ).scale(0.9)
        self.add(text)

        self.play(highlight_animation(text[3], BLUE))


        low_text = MathTex("\\Delta^1 f(", "a", "+ b) = \\Delta^1 f(", "a", ") + \\sum_{k_3=0}^{b-1} \\Delta^2 f(", "a", "+ k_3)").scale(0.9).move_to(DOWN * 2)

        self.play(
            text.animate.move_to(2.5*UP, UP),
            lim_text.animate.move_to(3.25*UP),
            FadeIn(low_text, shift=UP)
        )

        self.play(highlight_animation(VGroup(low_text[1], low_text[3], low_text[5]), YELLOW), run_time=0.5)

        new_low_text = MathTex("\\Delta^1 f(", "n", "+ b) = \\Delta^1 f(", "n", ") + \\sum_{k_3=0}^{b-1} \\Delta^2 f(", "n", "+ k_3)").scale(0.9).move_to(DOWN * 2)
        self.play(Transform(low_text, new_low_text))

        self.remove(*low_text, *new_low_text)
        low_text = MathTex("\\Delta^1 f(n +", "b", ") = \\Delta^1 f(n) +", "\\sum_{k_3=0}^{b-1}", "\\Delta^2 f(n + k_3)").scale(0.9).move_to(DOWN * 2)
        self.add(low_text)
        self.play(highlight_animation(VGroup(low_text[1], low_text[3][0]), YELLOW), run_time=0.5)

        new_low_text = MathTex("\\Delta^1 f(n +", "k_2", ") = \\Delta^1 f(n) +", "\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n + k_3)").scale(0.9).move_to(DOWN * 2)
        self.play(
            Transform(low_text[0:3], new_low_text[0:3]),
            Transform(low_text[4:], new_low_text[4:]),
            Transform(low_text[3][1:], new_low_text[3][2:]),
            Transform(low_text[3][0], new_low_text[3][0:2]),
        )

        self.play(highlight_animation(text[2], BLUE))

        self.remove(*low_text, *new_low_text, *low_text[3], *new_low_text[3])
        low_text = MathTex("\\Delta^1 f(n + k_2)", "=", "\\Delta^1 f(n) + \\sum_{k_3=0}^{k_2-1}\\Delta^2 f(n + k_3)").scale(0.9).move_to(DOWN * 2)
        new_low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n + k_2)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\left(", "\\Delta^1 f(n) + \\sum_{k_3=0}^{k_2-1}\\Delta^2 f(n + k_3)", "\\right)").scale(0.85).move_to(DOWN * 2)
        highlight(new_low_text[0:2], BLUE)
        new_low_text[0].save_state()
        new_low_text[0].set_stroke(width=0).set_color(BLACK).scale(0).move_to(low_text[0].get_left())
        self.play(
            morph_text(low_text, new_low_text, [1, 2, 4], ignore_2=[0]),
            new_low_text[0].animate.restore()
        )

        self.remove(*low_text, *new_low_text)
        low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\left(", "\\Delta^1 f(n) +", "\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)", "\\right)").scale(0.85).move_to(DOWN * 2)
        self.add(low_text)
        new_low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n) +", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)").scale(0.82).move_to(DOWN * 2)
        highlight(low_text[0], BLUE)
        highlight(new_low_text[0], BLUE)
        sum_copy = low_text[2].copy()
        self.play(
            morph_text(low_text, new_low_text, [0, 1, 2, None, 3, 5], ignore_2=[4]),
            Transform(sum_copy, new_low_text[4], path_arc=PI*3/4)
        )

        self.remove(*low_text, *new_low_text, *sum_copy)
        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\",
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n) \\\\",
            "&+ \\left. \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)", "\\right)"
        ).scale(0.85)
        low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n)", "+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)").scale(0.82).move_to(DOWN * 2)
        highlight(low_text[0], BLUE)
        self.add(low_text)
        self.play(
            Transform(text[0], new_text[0]),
            Transform(text[1], new_text[1]),
            text[2:4].animate(remover=True).scale(0).move_to(new_text[2].get_top()).set_stroke(width=0).set_color(BLACK),
            Transform(low_text[2], new_text[2]),
            Transform(low_text[3], new_text[3]),
            low_text[0:2].animate(remover=True).shift(DOWN).set_stroke(width=0).set_color(BLACK),
            Transform(text[-1], new_text[-1])
        )