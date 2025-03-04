from manim import *

from modules.custom_mobjects import CheckMark
from modules.helpers import fade_and_shift_in, fade_and_shift_out


class OtherVideos1(Scene):
    def construct(self):
        title = Tex("\\underline{Tricks From Previous Videos}").scale(1.2).move_to(UP*2.5)

        self.play(fade_and_shift_in(title, UP))

        text = Tex("The Recursive Formula").move_to(UP)

        self.play(fade_and_shift_in(text, UP))

        self.play(fade_and_shift_out(VGroup(title, text), UP))


class OtherVideos2(Scene):
    def construct(self):
        title = Tex("\\underline{Tricks From Previous Videos}").scale(1.2).move_to(UP*2.5)

        text_1 = Tex("The Recursive Formula").move_to(UP)
        check = CheckMark(text_1.get_left()).scale(0.8)
        VGroup(text_1, check).shift(RIGHT * (text_1.get_center() - VGroup(text_1, check).get_center())/2)

        self.play(fade_and_shift_in(VGroup(title, text_1, check), UP))

        text_2 = Tex("Going to the Right").move_to(DOWN * 0.5)

        self.play(fade_and_shift_in(text_2, UP))


        self.play(fade_and_shift_out(VGroup(title, text_1, check, text_2), UP))


class OtherVideos3(Scene):
    def construct(self):
        title = Tex("\\underline{Tricks From Previous Videos}").scale(1.2).move_to(UP*2.5)

        text_1 = Tex("The Recursive Formula")
        check_1 = CheckMark(text_1.get_left()).scale(0.8)
        VGroup(text_1, check_1).move_to(UP)

        text_2 = Tex("Going to the Right")
        check_2 = CheckMark(text_2.get_left()).scale(0.8)
        VGroup(text_2, check_2).move_to(DOWN * 0.5)

        self.play(fade_and_shift_in(VGroup(text_2, check_2, text_1, check_1, title), UP))
        self.play(fade_and_shift_out(VGroup(text_2, check_2, text_1, check_1, title), UP))