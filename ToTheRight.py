from manim import *
from modules.custom_mobjects import FullscreenAxes, create_axes
from modules.helpers import normalize_point_speed, fade_and_shift_in, create_updater_container
from modules.interpolation import sin_smooth_in, bounce


class Reciprocal(MovingCameraScene):
    def construct(self):

        axes = FullscreenAxes(self, LEFT * 4.5 + DOWN, [0.8, 0.8])


        left_curve = ParametricFunction(lambda t: axes.coords_to_point(t, max(1/t, -5)), [-3.5, -0.1], color=RED)
        left_curve.set_points(normalize_point_speed(left_curve.points))

        right_curve = ParametricFunction(lambda t: axes.coords_to_point(t, min(1/t, 6.5)), [0.1, 15], color=RED)
        right_curve.set_points(normalize_point_speed(right_curve.points))


        text = MathTex("f(x) = \\frac 1x").move_to(UP * 2)


        self.play(
            LaggedStart(
                Write(text),
                create_axes(self, axes),
                LaggedStart(
                    Create(left_curve, rate_func=linear),
                    Create(right_curve, rate_func=linear, run_time = right_curve.get_arc_length() / left_curve.get_arc_length()),
                    lag_ratio = 0.7,
                    run_time = 1
                ),
                lag_ratio=0.25
            )
        )

        lim_text = MathTex("\\lim_{x \\to \\infty} f(x) = 0").scale(0.8).move_to(RIGHT*(self.camera.frame.get_right() - 1) + DOWN * 0.2, RIGHT)
        lim_text.set_z_index(2)
        self.play(Write(lim_text))


        DOT_SPREAD = 1.5

        dot_0 = Dot(LEFT * 3, 0.12, color=BLUE)
        neg_dots = [Dot(dot_0.get_center() + RIGHT*DOT_SPREAD*i, 0.12, color=BLUE) for i in range(-2, 0)]
        pos_dots = [Dot(dot_0.get_center() + RIGHT*DOT_SPREAD*i, 0.12, color=BLUE) for i in range(1, 5)]

        s_n_text = MathTex("S(n)").move_to(dot_0.get_center() + DOWN, UP)
        arrow = Arrow(s_n_text.get_top(), dot_0.get_center(), buff=0.2)

        for obj in [dot_0, s_n_text, arrow] + neg_dots + pos_dots: obj.set_z_index(2)


        black_fade = Square(20, color=BLACK, fill_opacity=1)
        black_fade.set_z_index(1)
        self.play(
            LaggedStart(
                FadeIn(black_fade, rate_func=linear),
                lim_text.animate.become(MathTex("\\lim_{x \\to \\infty} f(x) = 0").move_to(UP * 3)),
                LaggedStart(
                    *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in neg_dots],
                    FadeIn(dot_0, scale=3, rate_func=bounce()),
                    fade_and_shift_in(VGroup(s_n_text, arrow), UP),
                    lag_ratio = 0.2
                ),
                lag_ratio=0.5
            )
        )

        self.remove(*axes[0], *axes[1], left_curve, right_curve, text, black_fade)



        