from manim import *
from modules.custom_mobjects import CheckMark, FullscreenAxes
from modules.helpers import fade_and_shift_out, highlight, highlight_animation
from modules.interpolation import cubic_out


class FlattenOut(Scene):
    def construct(self):
        text_1 = Tex("$f(x) \\to 0\ $ as $\ x \\to \\infty$.").move_to(UP)
        text_2 = Tex("$f(x)$", " flattens out ", "as $x \\to \\infty$.").move_to(DOWN).shift(RIGHT*0.5)
        
        text_1.shift(RIGHT * (text_2.get_left() - text_1.get_left()))


        self.play(Write(text_1))

        check_mark = CheckMark(text_1.get_left())

        self.play(check_mark.create_animation())

        self.play(Write(text_2))

        new_flattens_out = text_2[1].copy().set_color(RED).shift(UP*0.75)

        arrow = MathTex("\\uparrow").move_to(new_flattens_out.get_bottom() + DOWN*0.3, UP)
        arrow_text = Tex("What does this mean?").scale(0.9).move_to(arrow.get_bottom() + DOWN*0.3, UP)


        self.play(
            VGroup(text_1, check_mark).animate.shift(UP * 0.5),
            Transform(text_2[1], new_flattens_out),
            VGroup(text_2[0], text_2[2]).animate.shift(UP*0.75),
            FadeIn(VGroup(arrow, arrow_text), shift = UP * 2)
        )


        self.play(fade_and_shift_out(VGroup(text_1, text_2, arrow, arrow_text, check_mark), UP))