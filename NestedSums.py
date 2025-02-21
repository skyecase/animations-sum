from manim import *
from modules.helpers import create_single_arrow, fade_and_shift_in, fade_and_shift_out, grow_between, highlight, highlight_animation, morph_text, shrink_between
from modules.interpolation import cubic_in_out, cubic_out


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
        self.add(low_text)
        self.play(highlight_animation(low_text[0], BLUE))
        self.play(highlight_animation(text[1], BLUE))

        new_low_text = MathTex("\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n + k_1)", "=", "\\sum_{k_1=0}^{x-1} \\left(", "\\Delta^0 f(n) + \\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n + k_2)", "\\right)").move_to(DOWN * 2)
        highlight(new_low_text[0:2], BLUE)
        new_low_text[0].save_state()
        new_low_text[0].set_stroke(width=0).set_color(BLACK).scale(0).move_to(low_text[0].get_left())
        self.play(
            morph_text(low_text, new_low_text, [1, 2, 4], ignore_2=[0]),
            new_low_text[0].animate.restore()
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
            "&+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta^1 f(n + k_2)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
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
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n + k_2)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
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
        low_text = MathTex("\\Delta^1 f(n +", "b", ")", "= \\Delta^1 f(n) +", "\\sum_{k_3=0}^{b-1}", "\\Delta^2 f(n + k_3)").scale(0.9).move_to(DOWN * 2)
        self.add(low_text)
        self.play(highlight_animation(VGroup(low_text[1], low_text[4][0]), YELLOW), run_time=0.5)

        new_low_text = MathTex("\\Delta^1 f(n +", "k_2", ")", "= \\Delta^1 f(n) +", "\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n + k_3)").scale(0.9).move_to(DOWN * 2)
        highlight(new_low_text[0:3], BLUE)
        self.play(
            Transform(low_text[0:4], new_low_text[0:4]),
            Transform(low_text[5:], new_low_text[5:]),
            Transform(low_text[4][1:], new_low_text[4][2:]),
            Transform(low_text[4][0], new_low_text[4][0:2]),
        )

        self.play(highlight_animation(text[2], BLUE))

        self.remove(*low_text, *new_low_text, *low_text[4], *new_low_text[4])
        low_text = MathTex("\\Delta^1 f(n + k_2)", "=", "\\Delta^1 f(n) + \\sum_{k_3=0}^{k_2-1}\\Delta^2 f(n + k_3)").scale(0.9).move_to(DOWN * 2)
        highlight(low_text[0], BLUE)
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
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
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




        # =====================================
        # THIRD ITERATION
        # =====================================

        self.remove(*text, *new_text, *low_text)
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n + k_3)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.85)
        self.add(text)

        self.play(highlight_animation(text[2], BLUE))

        low_text = MathTex("\\Delta^2 f(n + k_3)", "=", "\\Delta^2 f(n) + \\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n + k_4)").scale(0.8).move_to(DOWN * 2.5)
        highlight(low_text[0], BLUE).save_state()
        low_text[0].shift(DOWN).set_color(BLACK)

        self.play(
            lim_text.animate.scale(1/0.8 * 0.7).move_to(UP*3.5),
            text.animate.scale(1/0.85 * 0.8).move_to(UP*3, UP),
            FadeIn(low_text[1:], shift=UP),
            low_text[0].animate.restore()
        )

        self.play(highlight_animation(text[1], BLUE))

        new_low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n + k_3)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\left(", "\\Delta^2 f(n) + \\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n + k_4)", "\\right)").scale(0.75).move_to(DOWN * 2.5)
        highlight(new_low_text[1], BLUE)
        highlight(new_low_text[0], BLUE).save_state()
        new_low_text[0].scale(0).move_to(low_text[0].get_left()).set_color(BLACK).set_stroke(width=0)
        self.play(
            morph_text(low_text, new_low_text, [1, 2, 4], ignore_2=[0]),
            new_low_text[0].animate.restore()
        )

        self.remove(*low_text, *new_low_text)
        low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "\\left(", "\\Delta^2 f(n) +", "\\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n + k_4)", "\\right)").scale(0.75).move_to(DOWN * 2.5)
        self.add(low_text)
        new_low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n) +", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "\\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n + k_4)").scale(0.7).move_to(DOWN * 2.5)
        highlight(low_text[0], BLUE)
        highlight(new_low_text[0], BLUE)
        sum_copy = low_text[2].copy()
        self.play(
            morph_text(low_text, new_low_text, [0, 1, 2, None, 3, 5], ignore_2=[4]),
            Transform(sum_copy, new_low_text[4], path_arc=PI/2)
        )

        self.remove(*low_text, *new_low_text, *sum_copy)
        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n) \\\\",
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}\\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n + k_4)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.8)
        low_text = MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + k_3)", "=", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n)", "+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}\\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n + k_4)").scale(0.7).move_to(DOWN * 2.5)
        highlight(low_text[0], BLUE)
        self.add(low_text)
        self.play(
            Transform(text[0], new_text[0]),
            text[1:3].animate(remover=True).scale(0).move_to(new_text[2].get_top()).set_stroke(width=0).set_color(BLACK),
            Transform(low_text[2], new_text[1]),
            Transform(low_text[3], new_text[2]),
            low_text[0:2].animate(remover=True).shift(DOWN).set_stroke(width=0).set_color(BLACK),
            Transform(text[-1], new_text[-1])
        )



        # =====================================
        # LIMIT
        # =====================================

        self.remove(*text, *new_text, *low_text)

        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n) \\\\",
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}\\sum_{k_4=0}^{k_3-1}", "\\Delta^3 f(n + k_4)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.8)
        self.add(text)

        brace = Brace(text[3], color=BLUE).shift(DOWN * 0.1)
        brace_text = MathTex("\\to 0", color=BLUE).move_to(brace.get_bottom() + DOWN * 0.1, UP).scale(0.8)

        lim_text.set_stroke(width=0)
        self.play(lim_text.animate.scale(0.8/0.7).shift(DOWN*0.15).set_color(YELLOW).set_stroke(width=1))

        self.play(
            FadeIn(VGroup(brace, brace_text), shift = UP*0.5),
            highlight_animation(text[3], BLUE)
        )

        highlighted_sum = highlight(text[2].copy(), BLUE)

        self.play(highlight_animation(text[2][0], GREEN, scale=1.2))

        new_brace = Brace(text[2:4], color=BLUE).shift(UP*0.1)

        self.play(
            brace_text.animate.move_to(new_brace.get_bottom() + DOWN*0.1, UP),
            Transform(brace, new_brace),
            Transform(text[2], highlighted_sum)
        )

        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} \\Delta^1 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95).move_to(DOWN * 0.25)

        approach_0_group = VGroup(text[1:4], brace, brace_text)

        self.play(
            Transform(text[0], new_text[0]),
            approach_0_group.animate(remover=True).scale(0).set_color(BLACK).set_stroke(width=0).move_to(UP * new_text.get_bottom() + DOWN*0.1 + RIGHT * approach_0_group.get_center()),
            Transform(text[-1], new_text[-1]),
            lim_text.animate.set_color(WHITE).set_stroke(width=0)
        )

        self.remove(*text, *new_text)

        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+", "\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n) \\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95).move_to(DOWN * 0.25)
        self.add(text)
        
        sums = [text[1], text[3], text[4], text[6], text[7], text[8]]
        self.play(
            LaggedStart(
                *[highlight_animation(sum, RED, rate_func = lambda x: 4*x*(1-x)) for sum in sums],
                lag_ratio=0.15
            )
        )

        self.wait()


class UhOh(Scene):
    def construct(self):
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+", "\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n) \\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95).move_to(DOWN * 0.25)
        self.add(text)

        text.save_state()

        lim_text = MathTex("\\lim_{x \\to \\infty} \\Delta^", "3", "f(x) = 0").scale(0.8).move_to(UP * 3.25)
        self.add(lim_text)

        self.play(
            text[0:6].animate.set_color(DARK_GREY),
            text[9:].animate.set_color(DARK_GREY),
            lim_text.animate.set_color(DARK_GRAY),
        )

        self.play(
            highlight_animation(text[8][0:2], YELLOW),
            highlight_animation(text[7][5:7], YELLOW),
        )

        self.play(
            highlight_animation(text[7][0:2], ORANGE),
            highlight_animation(text[6][4:6], ORANGE),
        )

        self.play(
            highlight_animation(text[6][0], RED, scale=1.2)
        )

        self.play(
            text.animate.restore(),
            lim_text.animate.set_color(WHITE),
        )

        self.remove(*text)
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+", "\\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\",
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\Delta^1 f(n) \\\\",
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95).move_to(DOWN * 0.25)
        self.add(text)

        text[1].save_state()
        self.play(highlight_animation(text[1], GREEN))

        text[3].save_state()
        self.play(
            text[1].animate.restore(),
            highlight_animation(text[3], BLUE)
        )

        text[5].save_state()
        self.play(
            text[3].animate.restore(),
            highlight_animation(text[5], RED)
        )

        self.play(text[5].animate.restore())

        new_lim_text = MathTex("\\lim_{x \\to \\infty} \\Delta^", "{10}", "f(x) = 0").scale(0.8).move_to(UP * 3.25)
        self.play(Transform(lim_text, new_lim_text))

        parenthesis = text[-1]
        self.remove(*text)

        texts = [
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\Delta^1 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n)"
        ]

        for i in range(3, 10):
            current_text = "\\\\ &+ \\sum_{k_1=0}^{x-1}"
            for j in range(1, i+1):
                current_text += f"\\sum_{{k_{{{j+1}}}=0}}^{{k_{{{j}}}-1}}"
            current_text += f"\\Delta^{{{i}}} f(n)"
            texts.append(current_text)
        texts.append("\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)")

        text = MathTex(
            *texts
        ).scale(0.95).move_to(text.get_corner(UP+LEFT), UP+LEFT)
        self.add(text[0])

        self.play(
            Write(text[1], run_time = 1.5),
            parenthesis.animate.move_to(text[-1])
        )

        self.add(text)
        self.remove(parenthesis)
        
        scale = 12 / text[-2:].width

        text_copy = text.copy()
        text_copy.scale(scale)

        self.play(
            text.animate.scale(scale).shift(-text_copy[-2:].get_center()),
            lim_text.animate(remover=True).scale(scale).shift(-text_copy[-2:].get_center()),
            run_time = 3,
            rate_func = cubic_in_out
        )

        self.play(text.animate(run_time = 2, rate_func = cubic_in_out).scale(7 / text.height).move_to(ORIGIN))


        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\sum_{k_1=0}^{x-1} \\Delta^0 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\Delta^1 f(n) \\\\"
            "&+ \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95)

        self.play(
            Transform(text[0], new_text[0]),
            Transform(text[-1], new_text[-1]),
            FadeOut(text[1:-1], shift = DOWN*6),
            rate_func=cubic_in_out,
            run_time = 2
        )

        self.remove(*text)

        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+", "\\sum_{k_1=0}^{x-1}", "\\Delta^0 f(n) \\\\",
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "\\Delta^1 f(n) \\\\",
            "&+", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "\\Delta^2 f(n)", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95)
        self.add(text)

        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+", "\\Delta^0 f(n)", "\\sum_{k_1=0}^{x-1}", "1 \\\\",
            "&+", "\\Delta^1 f(n)", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}", "1 \\\\",
            "&+", "\\Delta^2 f(n)", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}", "1", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95)

        self.play(
            highlight_animation(VGroup(text[2], text[5], text[8]), GREEN)
        )

        self.play(
            morph_text(text, new_text, [0, 2, [1, {"path_arc": PI*3/4}], 4, 6, [5, {"path_arc": PI*3/4}], 8, 10, [9, {"path_arc": PI*3/4}], 12])
        )

        self.remove(*text, *new_text)
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\Delta^0 f(n) \\sum_{k_1=0}^{x-1} 1 \\\\"
            "&+ \\Delta^1 f(n) \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} 1 \\\\"
            "&+ \\Delta^2 f(n)", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} 1", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95)

        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\Delta^0 f(n) \\sum_{k_1=0}^{x-1} 1 \\\\"
            "&+ \\Delta^1 f(n) \\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} 1 \\\\"
            "&+ \\Delta^2 f(n)", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} 1", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(1.2)
        new_text.shift(-new_text[1].get_center())
        VGroup(new_text[0], new_text[2]).set_fill(opacity=0)

        self.play(
            Transform(text, new_text),
            rate_func=cubic_in_out,
            run_time = 1.5
        )

        self.wait()


class Optimization(Scene):
    def construct(self):

        V_OFFSET = 1.75

        text = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1").scale(1.2)
        self.add(text)

        sum = MathTex("\\sum_{k_3=0}^{k_2-1}").scale(1.2).move_to(DOWN*V_OFFSET + RIGHT*text[2].get_center())
        zero_text = MathTex("k_2 = 0").move_to(sum.get_center() * [-1, 1, 1])
        arrow = create_single_arrow(text[2].get_bottom() + UP*V_OFFSET, sum.get_top()).set_color(BLUE)
        arrow.save_state()
        arrow.shift(DOWN*V_OFFSET).set_color(BLACK)

        self.play(
            FadeIn(VGroup(sum, zero_text), shift=UP*V_OFFSET),
            VGroup(text[0:2], text[3]).animate.shift(UP*V_OFFSET).set_color(DARK_GRAY),
            text[2].animate.shift(UP * V_OFFSET),
            arrow.animate.restore()
        )
        
        new_sum = MathTex("\\sum_{k_3=0}^{-1}").scale(1.2)
        new_sum.shift(sum[0][4].get_center() - new_sum[0][2].get_center())

        self.play(
            shrink_between(sum[0][0:2], right=new_sum[0][0]),
            Transform(sum[0][2:], new_sum[0])
        )


        def create_x(center):
            return VGroup(
                Line(center + (LEFT+UP)*0.6, center + (RIGHT+DOWN)*0.6),
                Line(center + (RIGHT+UP)*0.6, center + (LEFT+DOWN)*0.6),
            ).set_color(RED).set_stroke(width=10)

        x = create_x(new_sum.get_center())

        self.play(
            Create(x, run_time=0.5)
        )

        self.play(
            text[0].animate.set_color(WHITE),
            text[1][:-4].animate.set_color(WHITE),
            text[3].animate.set_color(WHITE),
            highlight_animation(text[1][-4:], BLUE)
        )

        new_text = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=1}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1").scale(1.2).move_to(UP*V_OFFSET)
        new_text.save_state()
        highlight(new_text[1][-4:], BLUE)
        self.play(Transform(text, new_text))

        self.remove(*sum, *sum[0])
        sum = new_sum
        self.add(sum)

        self.play(
            Transform(text, new_text.restore()),
            VGroup(sum, zero_text, x, arrow).animate(remover=True).shift(DOWN).set_color(BLACK)
        )


        sum_1 = MathTex("\\sum_{k_2=1}^{k_1-1}").scale(1.2).move_to(DOWN*V_OFFSET + RIGHT*text[0].get_center())
        sum_2 = MathTex("\\sum_{k_2=1}^{k_1-1}").scale(1.2).move_to(DOWN*V_OFFSET + RIGHT*text[2].get_center())
        arrow_1 = create_single_arrow(text[1].get_bottom(), sum_1.get_top())
        arrow_2 = create_single_arrow(text[1].get_bottom(), sum_2.get_top())
        arrows = VGroup(arrow_1, arrow_2).set_color(BLUE)
        arrows.save_state().shift(DOWN/2).set_color(BLACK)
        zero_text = MathTex("k_1 = 0").move_to(sum_1.get_left() + LEFT * 0.5, RIGHT)
        one_text = MathTex("k_1 = 1").move_to(sum_2.get_right() + RIGHT * 0.5, LEFT)
        
        self.play(
            arrows.animate.restore(),
            FadeIn(VGroup(sum_1, sum_2, zero_text, one_text), shift=UP),
            VGroup(text[0], text[2:]).animate.set_color(DARK_GRAY)
        )


        new_sum_1 = MathTex("\\sum_{k_2=1}^{-1}").scale(1.2)
        new_sum_2 = MathTex("\\sum_{k_2=1}^{0}").scale(1.2)
        new_sum_1.shift(sum_1[0][4].get_center() - new_sum_1[0][2].get_center())
        new_sum_2.shift(sum_2[0][4].get_center() - new_sum_2[0][1].get_center())

        self.play(
            LaggedStart(
                AnimationGroup(
                    Transform(sum_1[0][2:], new_sum_1[0][:]),
                    shrink_between(sum_1[0][:2], right=new_sum_1[0][0])
                ),
                AnimationGroup(
                    Transform(sum_2[0][4:], new_sum_2[0][1:]),
                    Transform(sum_2[0][:4], new_sum_2[0][:1])
                ),
                lag_ratio=0.5
            )
        )

        x_1 = create_x(new_sum_1.get_center())
        x_2 = create_x(new_sum_2.get_center())

        self.play(
                Create(x_1, run_time=0.5),
        )
        self.play(
                Create(x_2, run_time=0.5),
        )

        self.play(
            text[0][:-4].animate.set_color(WHITE),
            text[1:].animate.set_color(WHITE),
            highlight_animation(text[0][-4:], BLUE)
        )

        new_text = MathTex("\\sum_{k_1=2}^{x-1}", "\\sum_{k_2=1}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1").scale(1.2).move_to(UP*V_OFFSET)
        new_text.save_state()
        highlight(new_text[0][-4:], BLUE)
        self.play(Transform(text, new_text))

        self.remove(*sum_1[0])
        self.add(new_sum_1)

        self.play(
            Transform(text, new_text.restore()),
            VGroup(new_sum_1, sum_2, zero_text, one_text, x_1, x_2, arrow_1, arrow_2).animate(remover=True).shift(DOWN).set_color(BLACK)
        )


        six_sums = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "\\sum_{k_4=0}^{k_3-1}", "\\sum_{k_5=0}^{k_4-1}", "\\sum_{k_6=0}^{k_5-1}", "1")\
            .move_to(DOWN*V_OFFSET)
        
        self.play(
            LaggedStart(
                *[fade_and_shift_in(s, LEFT) for s in six_sums],
                lag_ratio = 0.15
            )
        )

        new_six_sums = MathTex("\\sum_{k_1=5}^{x-1}", "\\sum_{k_2=4}^{k_1-1}", "\\sum_{k_3=3}^{k_2-1}", "\\sum_{k_4=2}^{k_3-1}", "\\sum_{k_5=1}^{k_4-1}", "\\sum_{k_6=0}^{k_5-1}", "1")\
            .move_to(DOWN*V_OFFSET)
        for s in new_six_sums[:-1]:
            highlight(s[-1], YELLOW)
        
        self.play(
            LaggedStart(
                *[Transform(six_sums[i], new_six_sums[i]) for i in reversed(range(len(new_six_sums) - 1))],
                lag_ratio=0.3
            )
        )

        self.play(
            six_sums.animate(remover=True).shift(DOWN).set_color(BLACK)
        )