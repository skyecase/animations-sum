from manim import *
from modules.custom_mobjects import FullscreenAxes
from modules.interpolation import bounce
from modules.helpers import fade_and_shift_in, grow_between

class Recursive(Scene):
    def construct(self):
        text = MathTex("S(x+1)").scale(1.25)

        self.play(Write(text))


        new_text = MathTex("S(x+1)", "=", "f(1)", "+", "f(2)", "+", "f(3)", "+", "\\cdots", "+", "f(x)", "+", "f(x+1)")

        self.play(
            Transform(text[0], new_text[0]),
            FadeIn(new_text[1], scale=1.25, shift = new_text[0].get_right() - text[0].get_right() + LEFT*(new_text[1].width * (1.25 - 1)/2)),
        )

        self.play(
            LaggedStart(
                # Transform(text[0], new_text[0]),
                *[fade_and_shift_in(sub, shift = LEFT * 2) for sub in new_text[2:8]],
                *[fade_and_shift_in(sub, shift = LEFT * 2) for sub in new_text[8]],
                *[fade_and_shift_in(sub, shift = LEFT * 2) for sub in new_text[9:]],
                lag_ratio = 0.3
            )
        )


        self.remove(*text, *new_text, *new_text[8])
        text = MathTex("S(x+1) =", "f(1) + f(2) + f(3) + \\cdots + f(x)", "+ f(x+1)")
        self.add(text)


        brace = Brace(text[1], DOWN)
        self.play(fade_and_shift_in(brace, UP))

        s_x_text = MathTex("S(x)").move_to(brace.get_bottom() + DOWN * 0.2, UP)
        self.play(Write(s_x_text))


        new_text = MathTex("S(x+1) =", "S(x)", "+ f(x+1)")
        shift = new_text[1].get_center() - s_x_text.get_center()

        self.play(
            LaggedStart(
                AnimationGroup(
                    VGroup(s_x_text).animate.shift(shift),
                    FadeOut(VGroup(brace, text[1]), shift=shift),
                ),
                AnimationGroup(
                    Transform(text[0], new_text[0], rate_func = bounce()),
                    Transform(text[2], new_text[2], rate_func = bounce()),
                    run_time = 1.5
                ),
                lag_ratio=0.5
            )
        )

        self.remove(*text, *new_text, s_x_text)
        text = MathTex("S(x+1) = S(x) + f(x+1)")
        self.add(text)

        self.play(text.animate.scale(1.25))
