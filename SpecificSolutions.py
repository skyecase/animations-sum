from manim import *

from modules.helpers import fade_and_shift_in, highlight, morph_text, shrink_between


class OrderZero(Scene):
    def construct(self):


        text = MathTex("S(x) = \\lim_{n \\to \\infty}", "\\left(", "\\sum_{k=1}^n (f(k) - f(x + k))", "+", "\\sum_{k=1}^x", "f(n + k)", "\\right)", stroke_width=0)
        self.add(text)

        top_text = MathTex("\\lim_{x \\to \\infty} f(x) = 0").move_to(UP*2.5)

        self.play(Write(top_text))

        brace = Brace(text[5], buff=0.4, color=BLUE)
        brace_text = MathTex("\\to 0", color=BLUE).move_to(brace.get_bottom() + DOWN*0.1, UP)

        self.play(
            highlight(text[5], BLUE),
            fade_and_shift_in(VGroup(brace_text, brace), UP*0.5)
        )


        new_brace = Brace(VGroup(text[4], text[5]), color=BLUE)
        new_brace_text = MathTex("\\to 0", color=BLUE).move_to(new_brace.get_bottom() + DOWN*0.1, UP)

        self.play(
            highlight(text[4], BLUE),
            brace.animate.become(new_brace),
            brace_text.animate.become(new_brace_text)
        )


        new_text = MathTex("S(x) = \\lim_{n \\to \\infty}", "\\sum_{k=1}^n (f(k) - f(x + k))")
        self.play(
            morph_text(text, new_text, [0, None, 1]),
            shrink_between(VGroup(brace, brace_text), new_text[1])
        )

        self.wait()