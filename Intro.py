from manim import *

from modules.helpers import create_double_arrow, fade_and_shift_in, highlight_animation
from modules.interpolation import cubic_out, cubic_in



class Intro(Scene):
    def construct(self):
        # text_1 = MathTex("1", "+", "2", "+", "3", "+ \\cdots +", "x", "=\\quad \\frac{x(x+1)}2").move_to(UP*2)
        # text_2 = MathTex("r^1", "+", "r^2", "+", "r^3", "+ \\cdots +", "r^x", "=\\quad r\\frac{1-r^x}{1-r}")
        # text_3 = MathTex("f(1)", "+", "f(2)", "+", "f(3)", "+ \\cdots +", "f(x)", "=\\quad ???").move_to(DOWN*2)

        # for i in range(len(text_3[:-1])):
        #     text_1[i].move_to(text_1[i].get_center()*UP + text_3[i].get_center()*RIGHT)
        #     text_2[i].move_to(text_2[i].get_center()*UP + text_3[i].get_center()*RIGHT)
        # text_1[-1].move_to(text_1[-1].get_center()*UP + text_3[-1].get_left()*RIGHT, LEFT)
        # text_2[-1].move_to(text_2[-1].get_center()*UP + text_3[-1].get_left()*RIGHT, LEFT)

        # self.add(text_1)
        # self.add(text_2)
        # self.add(text_3)

        text_1 = MathTex("\\sum_{k=1}^x k =", "1 + 2 + 3 + \\cdots + x", "=", "\\frac{x(x+1)}2")

        self.play(Write(text_1[0]))

        self.play(
            LaggedStart(
                *[fade_and_shift_in(t, LEFT) for t in text_1[1]],
                lag_ratio=0.25
            )
        )

        self.play(Write(text_1[2:]))

        text_2 = MathTex("\\sum_{k=1}^x r^k =", "r^1", "+", "r^2", "+", "r^3", "+ \\cdots +", "r^x", "=", "r\\frac{1-r^x}{1-r}").move_to(DOWN)

        self.play(
            text_1.animate.move_to(UP),
            FadeIn(text_2[0], shift=UP)
        )

        self.play(
            LaggedStart(
                *[fade_and_shift_in(t, LEFT) for t in text_2[1:6].submobjects + text_2[6].submobjects + text_2[7:8].submobjects],
                lag_ratio=0.15
            )
        )

        self.play(Write(text_2[-2:]))


        text_1[-1].save_state()
        text_2[-1].save_state()

        self.play(
            highlight_animation(text_1[-1], scale=1),
            highlight_animation(text_2[-1], scale=1),
            text_1[:-1].animate.set_color(GREY),
            text_2[:-1].animate.set_color(GREY),
        )






class Integral(Scene):
    def construct(self):
        prerequisite_text = Tex("Prerequisites:", joint_type=LineJointType.ROUND).scale(1.5).move_to(UP*2)
        black_text = prerequisite_text.copy().set_stroke(width=10).set_color(BLACK)
        prerequisite_text.set_z_index(1); black_text.set_z_index(1)
        self.add(black_text)

        underline = Underline(prerequisite_text).shift(UP*0.12)

        self.play(
            Write(prerequisite_text),
            Create(underline)
        )


        point_1 = Tex("$\\bullet$", " Summation Notation ", "(lots of it)")
        point_2 = Tex("$\\bullet$", " Limits")

        point_1.shift(LEFT*3.5 + UP*0.5 - point_1[0].get_center())
        point_2.shift(LEFT*3.5 + DOWN*0.5 - point_2[0].get_center())

        self.play(
            Write(point_1[:2], run_time=1)
        )

        self.play(
            fade_and_shift_in(point_1[2], LEFT)
        )

        self.play(
            Write(point_2)
        )


        integral = MathTex("\\int")

        self.play(
            FadeOut(VGroup(underline, point_1, point_2, prerequisite_text), shift=UP),
            black_text.animate(remover=True).shift(UP),
            FadeIn(integral, shift=UP)
        )

        text = MathTex("\\int \\ \\ ", "\\approx \\ \\ ", "\\sum")
        text.move_to(-text[1].get_center())
        self.play(
            Transform(integral, text[0][:]),
            FadeIn(text[1:], shift=LEFT*1.5)
        )


        DIST_FROM_CENTER = 2.25

        continuous_header = Tex("Continuous").move_to(LEFT*DIST_FROM_CENTER + UP*1.5)
        discrete_header = Tex("Discrete").move_to(RIGHT*DIST_FROM_CENTER + UP*1.5)

        continuous_underline = Line(continuous_header.get_corner(DOWN + LEFT), continuous_header.get_corner(DOWN + RIGHT), stroke_width=3).shift(DOWN * 0.1)
        discrete_underline = Line(discrete_header.get_corner(DOWN + LEFT), discrete_header.get_corner(DOWN + RIGHT), stroke_width=3).shift(DOWN * 0.1)

        arrow_1 = create_double_arrow(LEFT, RIGHT, tip_length=0.3)
        arrow_1.save_state()
        arrow_1.scale(0).set_stroke(width=0).set_color(BLACK)


        sum = text[2]
        self.play(
            arrow_1.animate.restore(),
            integral.animate.move_to(LEFT*DIST_FROM_CENTER),
            sum.animate.move_to(RIGHT*DIST_FROM_CENTER),
            FadeOut(text[1], scale=0),
            LaggedStart(
                Write(continuous_header),
                Create(continuous_underline, rate_func=cubic_out),
                Write(discrete_header),
                Create(discrete_underline, rate_func=cubic_out),
                lag_ratio = 0.2
            )
        )


        derivative = MathTex("\\frac d{dx}").move_to(LEFT*DIST_FROM_CENTER + DOWN*0.25)
        delta = MathTex("\\Delta").scale(1.5).move_to(RIGHT*DIST_FROM_CENTER + DOWN*0.25)
        arrow_2 = create_double_arrow(LEFT, RIGHT, tip_length=0.3).move_to(DOWN*0.25)
        arrow_2.save_state()
        arrow_2.shift(DOWN*1.5).set_color(BLACK)


        taylor = MathTex("\\sum_{n=0}^\\infty \\frac{x^n}{n!} f^{(n)}(0)").scale(0.8).move_to(LEFT*1.25 + DOWN*2, RIGHT)
        newton = MathTex("\\sum_{n=0}^\\infty \\binom xn \\Delta^n f(0)").scale(0.8).move_to(RIGHT*1.25 + DOWN*2, LEFT)

        arrow_3 = create_double_arrow(LEFT, RIGHT, tip_length=0.3).move_to(DOWN*2)
        arrow_3.save_state()
        arrow_3.shift(DOWN*1.5).set_color(BLACK)


        self.play(
            LaggedStart(
                AnimationGroup(
                    VGroup(continuous_header, continuous_underline, discrete_header, discrete_underline, integral, arrow_1, sum).animate.shift(UP*1.5),
                    FadeIn(VGroup(derivative, delta), shift=UP*1.5),
                    arrow_2.animate.restore()
                ),
                AnimationGroup(
                    FadeIn(VGroup(taylor, newton), shift=UP*1.5),
                    arrow_3.animate.restore()
                ),
                lag_ratio=0.25
            )
        )

        self.play(
            VGroup(continuous_header, continuous_underline, integral, derivative, taylor).animate(rate_func=cubic_in).shift(LEFT*7),
            VGroup(discrete_header, discrete_underline, sum, delta, newton).animate(rate_func=cubic_in).shift(RIGHT*7),
            *[arrow.animate.scale(0) for arrow in [arrow_1, arrow_2, arrow_3]]
        )