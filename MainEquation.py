from manim import *
from modules.custom_mobjects import CustomArrow, DottedLine, FullscreenAxes, create_axes
from modules.interpolation import cubic_out
from modules.helpers import fade_and_shift_in
import math

from modules.interpolation import bounce


def s_not_touching_origin(x):
    a = 7
    b = 5.33
    c = 0.2
    return b/math.sqrt(1 + c**2 * (x - a)**2) + x**2 / 150

def s(x):
    return s_not_touching_origin(x) - s_not_touching_origin(0)


class ThreeSteps(Scene):
    def construct(self):
        rect = Rectangle(height=3.5, width=self.camera.frame_width).move_to(UP * self.camera.frame_height/2, UP)

        axes = FullscreenAxes(self, UP*1 + LEFT*6, [1/2, 1/2], 0.15, stroke_width=3, rect=rect)
        axes.y_line.set_cap_style(CapStyleType.SQUARE)

        dots = [Dot(axes.coords_to_point(i, s(i)), color=BLUE) for i in range(-2, 27)]
        for dot in dots: dot.set_z_index(2)

        n_text = MathTex("n").move_to(axes.coords_to_point(21, 0) + DOWN * 0.35, UP).set_color(RED)
        n_line = DottedLine(n_text.get_top() + UP*0.1, axes.coords_to_point(21, 6), stroke_width=3).set_color(RED)

        curve = ParametricFunction(lambda t: axes.coords_to_point(t, s(t)), [20, 26.5], stroke_width=3, color=YELLOW)

        self.play(
            LaggedStart(
                LaggedStart(
                    create_axes(self, axes, x_axis_time=1),
                    LaggedStart(
                        *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                        lag_ratio = 0.05,
                        # rate_func = lambda t: t*(3 - t)/2
                    ),
                    lag_ratio = 0.05
                ),
                LaggedStart(
                    Create(curve),
                    fade_and_shift_in(n_text, UP),
                    Create(n_line, rate_func=cubic_out),
                    lag_ratio=0.3
                ),
                lag_ratio=0.65
            )
        )


        x_text = MathTex("x").move_to(axes.coords_to_point(2.5, 0) + DOWN * 0.35, UP).set_color(GREEN)
        x_line = DottedLine(x_text.get_top() + UP*0.1, axes.coords_to_point(2.5, 6), stroke_width=3).set_color(GREEN)

        self.play(
            LaggedStart(
                fade_and_shift_in(x_text, UP),
                Create(x_line, rate_func=cubic_out),
                lag_ratio=0.3
            ),
        )


        n_dot = dots[23]
        s_n_text = MathTex("S(n)").scale(0.8).move_to(n_dot.get_center() + (UP+LEFT)*0.75, DOWN+RIGHT)
        s_n_arrow = CustomArrow(s_n_text.get_corner(DOWN+RIGHT), n_dot.get_center(), 0, stroke_width=3)
        self.add(s_n_arrow)

        text_1 = Tex("\\textbf{Step 1:} ", "Compute $S(n)$.").move_to(LEFT * 5 + DOWN*0.5, LEFT)

        
        self.play(fade_and_shift_in(text_1[0], LEFT*0.5, run_time = 0.5))
        self.play(
            Write(text_1[1]),
            n_dot.animate.scale(1.5),
            s_n_arrow.end_vt.animate.set_value(1),
            fade_and_shift_in(s_n_text, (DOWN+RIGHT)/2, run_time=0.75)
        )


        arrow = CustomArrow(n_dot.get_center(), axes.coords_to_point(21 + 2.5, s(21 + 2.5)), PI*3/4, stroke_width=3)
        self.add(arrow)

        npx_dot = Dot(axes.coords_to_point(21 + 2.5, s(21 + 2.5)), color=RED).scale(1.5)
        npx_dot.save_state()
        npx_dot.scale(0)

        text_2 = Tex("\\textbf{Step 2:} ", "Move forward $x$ units.").move_to(DOWN*1.75 + LEFT * 5, LEFT)

        self.play(fade_and_shift_in(text_2[0], LEFT * 0.5, run_time=0.5))
        self.play(
            n_dot.animate(rate_func=bounce()).scale(1/1.5),
            Write(text_2[1]),
            arrow.end_vt.animate(rate_func=cubic_out).set_value(1),
            npx_dot.animate.restore()
        )


        s_npx_text = MathTex("S(n + x)").scale(0.8).move_to(npx_dot.get_center() + UP)
        s_npx_arrow = CustomArrow(s_npx_text.get_bottom(), npx_dot.get_center(), 0, stroke_width=3)
        self.add(s_npx_arrow)

        self.play(
            fade_and_shift_in(s_npx_text, DOWN * 0.5),
            s_npx_arrow.end_vt.animate.set_value(1)
        )

        text_3 = Tex("\\textbf{Step 3:} ", "Step backward $n$ units.").move_to(DOWN*3 + LEFT*5, LEFT)

        self.play(fade_and_shift_in(text_3[0], LEFT * 0.5, run_time=0.5))



        arrows = [CustomArrow(axes.coords_to_point(i+2.5+1, s(i+2.5+1)), axes.coords_to_point(i+2.5, s(i+2.5)), PI*3/4, buff=0.07, tip_size=0.125, stroke_width=3) for i in range(0, 21)]
        for arrow in arrows: self.add(arrow)

        offset_dots = [Dot(axes.coords_to_point(i+2.5, s(i+2.5)), 0.06, color=RED) for i in range(0, 21)]
        for dot in offset_dots:
            dot.save_state()
            dot.scale(0)

        self.play(
            Write(text_3[1]),
            LaggedStart(
                *[
                    LaggedStart(
                        arrows[i].end_vt.animate(rate_func=cubic_out, run_time=0.5).set_value(1),
                        offset_dots[i].animate(rate_func=cubic_out, run_time=0.5).restore(),
                        lag_ratio = 0.25
                    ) for i in reversed(range(0, 21))
                ],
                lag_ratio = 1/2.5
            )
        )