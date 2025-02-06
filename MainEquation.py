from manim import *
from modules.custom_mobjects import DottedLine, FullscreenAxes, create_axes
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
        rect = Rectangle(height=3, width=self.camera.frame_width).move_to(UP * self.camera.frame_height/2, UP)

        axes = FullscreenAxes(self, UP*1.5 + LEFT*6, [1/2, 1/2], 0.15, stroke_width=3, rect=rect)
        axes.y_line.set_cap_style(CapStyleType.SQUARE)

        dots = [Dot(axes.coords_to_point(i, s(i)), color=BLUE) for i in range(-2, 27)]
        for dot in dots: dot.set_z_index(2)

        n_text = MathTex("n").move_to(axes.coords_to_point(21, 0) + DOWN * 0.35, UP).set_color(RED)
        n_line = DottedLine(n_text.get_top() + UP*0.1, axes.coords_to_point(21, s(21)), stroke_width=3).set_color(RED)

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






        text_1 = Tex("\\textbf{Step 1:} Compute $S(n)$.").move_to(LEFT * 6, LEFT)
        text_2 = Tex("\\textbf{Step 2:} Move forward $x$ units.").move_to(DOWN*1.5 + LEFT * 6, LEFT)
        text_3 = Tex("\\textbf{Step 3:} Step backward $n$ units.").move_to(DOWN*3 + LEFT*6, LEFT)
        
        self.add(text_1, text_2, text_3)
        self.wait()