from manim import *

from modules.helpers import fade_and_shift_in, grow_between, highlight, highlight_animation, morph_text, shrink_between


class OrderZero(Scene):
    def construct(self):


        text = MathTex("S(x) = \\lim_{n \\to \\infty}", "\\left(", "\\sum_{k=1}^n (f(k) - f(x + k))", "+", "\\sum_{k=1}^x", "f(n + k)", "\\right)")
        self.add(text)

        top_text = MathTex("\\lim_{x \\to \\infty} f(x) = 0").move_to(UP*2.5)

        self.play(Write(top_text))

        brace = Brace(text[5], buff=0.4, color=BLUE)
        brace_text = MathTex("\\to 0", color=BLUE).move_to(brace.get_bottom() + DOWN*0.1, UP)

        self.play(
            highlight_animation(text[5], BLUE),
            fade_and_shift_in(VGroup(brace_text, brace), UP*0.5)
        )


        new_brace = Brace(VGroup(text[4], text[5]), color=BLUE)
        new_brace_text = MathTex("\\to 0", color=BLUE).move_to(new_brace.get_bottom() + DOWN*0.1, UP)

        self.play(
            highlight_animation(text[4], BLUE),
            brace.animate.become(new_brace),
            brace_text.animate.become(new_brace_text)
        )


        new_text = MathTex("S(x) = \\lim_{n \\to \\infty}", "\\sum_{k=1}^n (f(k) - f(x + k))")
        self.play(
            morph_text(text, new_text, [0, None, 1]),
            shrink_between(VGroup(brace, brace_text), new_text[1])
        )

        self.wait()


class OrderOne(Scene):
    def construct(self):

        top_text = MathTex("\\lim_{x \\to \\infty} \\Delta f(x) = 0")
        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) +", "\\sum_{k=1}^x", "f(n + k", ")", "\\right)")

        self.play(Write(top_text))

        self.play(
            FadeIn(text, shift=UP*2),
            top_text.animate.shift(UP*2)
        )

        text[1].save_state()

        self.play(highlight_animation(text[1], RED))
        self.play(
            highlight_animation(text[2:4], BLUE),
            text[1].animate.restore()
        )

        equation = MathTex("f(a + b) = f(a) +", "\\sum_{k=0}^{b-1}", "\\Delta f(a + k", ")").move_to(DOWN*1.5)

        self.play(
            top_text.animate.scale(0.8).move_to(UP*3),
            text.animate.shift(UP),
            FadeIn(equation, shift=UP)
        )


        self.play(
            highlight_animation(text[2][-1], RED),
            highlight_animation(text[1][2], RED),
            highlight_animation(equation[2][-1], RED),
            highlight_animation(equation[1][4], RED),
        )

        new_text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) +", "\\sum_{k_1=1}^x", "f(n + k_", "1", ")", "\\right)").move_to(UP)
        highlight(new_text[2:5], BLUE)
        self.play(
            morph_text(text, new_text, [0, None, 2, 4, 5], ignore_1=[1], ignore_2=[1]),
            Transform(text[1][0:3], new_text[1][0:3]),
            Transform(text[1][3:], new_text[1][4:]),
            grow_between(new_text[1][3], text[1][2], text[1][3])
        )

        new_equation = MathTex("f(a + b) = f(a) +", "\\sum_{k_2=0}^{b-1}", "\\Delta f(a + k_", "2", ")").move_to(DOWN*1.5)
        self.play(
            morph_text(equation, new_equation, [0, None, 2, 4], ignore_1=[1], ignore_2=[1]),
            Transform(equation[1][0:5], new_equation[1][0:5]),
            Transform(equation[1][5:], new_equation[1][6:]),
            grow_between(new_equation[1][5], equation[1][4], equation[1][5])
        )


        self.remove(*text, *new_text, *text[1], *new_text[1], *equation, *new_equation, *equation[1], *new_equation[1])

        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) +", "\\sum_{k_1=1}^x", "f(n + k_1)", "\\right)").move_to(UP)
        highlight(text[2], BLUE)
        equation = MathTex("f(", "a", "+ b) = f(", "a", ") + \\sum_{k_2=0}^{b-1} \\Delta f(", "a", "+ k_2)").move_to(DOWN*1.5)
        self.add(text, equation)

        self.play(highlight_animation(VGroup(equation[1], equation[3], equation[5]), YELLOW))
        new_equation = MathTex("f(", "n", "+ b) = f(", "n", ") + \\sum_{k_2=0}^{b-1} \\Delta f(", "n", "+ k_2)").move_to(DOWN*1.5)
        self.play(Transform(equation, new_equation))

        self.remove(equation)
        equation = MathTex("f(n +", "b", ") = f(n) +", "\\sum_{k_2=0}^{b-1}", "\\Delta f(n + k_2)").move_to(DOWN*1.5)
        self.add(equation)

        new_equation = MathTex("f(n +", "k_1", ") = f(n) +", "\\sum_{k_2=0}^{k_1-1}", "\\Delta f(n + k_2)").move_to(DOWN*1.5)
        self.play(highlight_animation(VGroup(equation[1], equation[3][0]), YELLOW))
        highlight(VGroup(new_equation[0:2], new_equation[2][0]), BLUE)

        self.play(
            morph_text(equation, new_equation, [0, 1, 2, None, 4], ignore_1=[3], ignore_2=[3]),
            Transform(equation[3][0], new_equation[3][0:2]),
            Transform(equation[3][1:], new_equation[3][2:]),
        )

        self.play(highlight_animation(text[1], BLUE))

        self.remove(*equation, *new_equation, *equation[3])
        equation = MathTex("f(n + k_1)", "=", "f(n) + \\sum_{k_2=0}^{k_1-1} \\Delta f(n + k_2)").move_to(DOWN*1.5)
        highlight(equation[0], BLUE)
        self.add(equation)

        new_equation = MathTex("\\sum_{k_1=1}^x", "f(n + k_1)", "=", "\\sum_{k_1=1}^x \\left(", "f(n) + \\sum_{k_2=0}^{k_1-1} \\Delta f(n + k_2)", "\\right)").move_to(DOWN*1.5)
        highlight(new_equation[0:2], color=BLUE)
        new_equation[0].save_state()
        new_equation[0].scale(0).set_color(BLACK).set_stroke(width=0).move_to(equation[0].get_left())
        self.play(
            morph_text(equation, new_equation, [1, 2, 4], ignore_2=[0]),
            new_equation[0].animate.restore()
        )

        self.remove(*new_equation, *equation)
        equation = MathTex("\\sum_{k_1=1}^x f(n + k_1)", "=", "\\sum_{k_1=1}^x", "\\left(", "f(n) +", "\\sum_{k_2=0}^{k_1-1} \\Delta f(n + k_2)", "\\right)").move_to(DOWN*1.5)
        new_equation = MathTex("\\sum_{k_1=1}^x f(n + k_1)", "=", "\\sum_{k_1=1}^x", "f(n) +", "\\sum_{k_1=1}^x", "\\sum_{k_2=0}^{k_1-1} \\Delta f(n + k_2)").move_to(DOWN*1.5)
        highlight(VGroup(new_equation[0], equation[0]), color=BLUE)
        self.add(equation)

        sum_copy = equation[2].copy()

        self.play(
            morph_text(equation, new_equation, [0, 1, 2, None, 3, 5], ignore_2=[4]),
            sum_copy.animate(path_arc=PI*3/4).become(new_equation[4])
        )

        self.remove(*equation, *new_equation, sum_copy)
        equation = MathTex("\\sum_{k_1=1}^x f(n + k_1)", "=", "\\sum_{k_1=1}^x f(n) + \\sum_{k_1=1}^x \\sum_{k_2=0}^{k_1-1} \\Delta f(n + k_2)").move_to(DOWN*1.5)
        highlight(equation[0], BLUE)
        self.add(equation)
        new_text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) +", "\\sum_{k_1=1}^x f(n) + \\sum_{k_1=1}^x \\sum_{k_2=0}^{k_1-1} \\Delta f(n + k_2)", "\\right)").scale(0.85)


        self.play(
            Transform(text[0], new_text[0]),
            Transform(text[3], new_text[2]),
            Transform(equation[2], new_text[1]),
            text[1:3].animate.shift(UP*0.75).set_color(BLACK),
            equation[0:2].animate.shift(DOWN).set_color(BLACK),
        )

        self.remove(*text, *equation)
        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) + \\sum_{k_1=1}^x f(n)", "+", "\\sum_{k_1=1}^x \\sum_{k_2=0}^{k_1-1}", "\\Delta f(n + k_2)", "\\right)").scale(0.85)
        self.add(text)

        self.play(top_text.animate.scale(1/0.8).shift(DOWN * 0.5))

        brace = Brace(text[3], buff=0.4, color=BLUE)
        brace_text = MathTex("\\to 0", color=BLUE).move_to(brace.get_bottom() + DOWN*0.1, UP)

        self.play(
            highlight_animation(text[3], color=BLUE),
            fade_and_shift_in(VGroup(brace, brace_text), UP*0.5)
        )


        new_brace = Brace(VGroup(text[2:4]), color=BLUE)
        new_brace_text = MathTex("\\to 0", color=BLUE).move_to(new_brace.get_bottom() + DOWN*0.1, UP)


        self.play(
            Transform(brace, new_brace),
            Transform(brace_text, new_brace_text),
            highlight_animation(text[2], color=BLUE)
        )


        new_text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) + \\sum_{k_1=1}^x f(n)", "\\right)")
        self.play(
            morph_text(text, new_text, [0, None, None, None, 1]),
            shrink_between(VGroup(brace, brace_text), new_text[0], new_text[1])
        )

        self.remove(*new_text, *text)

        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) +", "\\sum_{k_1=1}^x f(n)", "\\right)")
        self.add(text)

        sum_copy = text[1].copy()
        text[1].set_color(DARK_GRAY)

        self.play(
            sum_copy.animate.move_to(DOWN * 2),
            text.animate.shift(UP * 0.5)
        )

        new_equation = MathTex("\\sum_{k_1=1}^x f(n)", "=", "x f(n)").move_to(DOWN * 2)
        self.play(
            Transform(sum_copy, new_equation[0]),
            FadeIn(new_equation[1:], shift = LEFT * 2)
        )

        new_text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n (f(k) - f(x + k)) +", "xf(n)", "\\right)").move_to(UP * 0.5)

        self.play(Transform(text, new_text))

        self.play(
            text.animate.move_to(ORIGIN),
            FadeOut(VGroup(new_equation[1:], sum_copy), shift = DOWN)
        )