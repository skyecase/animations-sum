from manim import *
from modules.custom_mobjects import CheckMark
from modules.helpers import highlight_animation
from modules.interpolation import cubic_out


class FlattenOut(Scene):
    def construct(self):
        text_1 = Tex("$f(x) \\to 0\ $ as $\ x \\to \\infty$.").move_to(UP)
        text_2 = Tex("$f(x)$", " flattens out ", "as $x \\to \\infty$.").move_to(DOWN)
        
        text_1.shift(RIGHT * (text_2.get_left() - text_1.get_left()))


        self.play(Write(text_1))

        check_mark = CheckMark(text_1.get_left())

        self.play(check_mark.create_animation())

        self.play(Write(text_2))


        self.play(
            highlight_animation(text_2[1], RED)
        )
