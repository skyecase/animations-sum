from manim import *
from modules.custom_mobjects import FullscreenAxes, create_arrow, create_axes, CustomArrow
from modules.helpers import fade_and_shift_out, normalize_point_speed, fade_and_shift_in, create_updater_container
from modules.interpolation import bounce, cubic_out


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
        pos_dots = [Dot(dot_0.get_center() + RIGHT*DOT_SPREAD*i, 0.12, color=BLUE) for i in range(1, 8)]

        s_n_text = MathTex("S(n)").move_to(dot_0.get_center() + DOWN, UP)
        arrow = Arrow(s_n_text.get_top(), dot_0.get_center(), buff=0.2)
        really_big_text = Tex("($n$ is a really big whole number.)").scale(0.75).move_to(DOWN * 2.5)

        for obj in [dot_0, s_n_text, arrow, really_big_text] + neg_dots + pos_dots: obj.set_z_index(2)


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
                    fade_and_shift_in(really_big_text, UP),
                    lag_ratio = 0.2
                ),
                lag_ratio=0.5
            )
        )

        self.remove(*axes[0], *axes[1], left_curve, right_curve, text, black_fade)



        arrows = [CustomArrow(dot_0.get_center() + i*DOT_SPREAD*RIGHT, dot_0.get_center() + (i+1)*DOT_SPREAD*RIGHT, angle=PI/2*(1-2*(i%2))) for i in range(0, 7)] # TODO: Remove i%2 part
        self.add(*arrows)

        np1_text = MathTex("+ f(n + 1)").scale(0.8).move_to((dot_0.get_center() + pos_dots[0].get_center())/2 + 0.6*UP, DOWN)

        self.play(
            arrows[0].end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(np1_text, scale=0, shift=UP*0.5, rate_func=cubic_out),
            FadeIn(pos_dots[0], scale=3, rate_func=bounce())
        )

        pretty_much_0_text = Tex("(Pretty much 0)").scale(0.5).move_to(np1_text.get_bottom())
        self.play(
            FadeIn(pretty_much_0_text, scale=0, shift = UP * pretty_much_0_text.height/2),
            np1_text.animate.shift(UP * (pretty_much_0_text.height/2 + 0.1))
        )


        for i in range(1, len(arrows)):
            f_text = MathTex("+ f(n + " + str(i+1) + ")").scale(0.8)
            pretty_much_text = Tex("(Pretty much 0)").scale(0.5).move_to(f_text.get_bottom() + DOWN*0.1, UP)
            group = VGroup(f_text, pretty_much_text)

            dir = UP if i%2 == 0 else DOWN
            group.move_to(dir * 0.2, -dir)
            arrows[i].set_text(group)
        
        self.play(
            LaggedStart(
                AnimationGroup(
                    arrows[0].start_vt.animate(rate_func=cubic_out).set_value(1),
                    fade_and_shift_out(VGroup(np1_text, pretty_much_0_text), UP)
                ),
                LaggedStart(
                    *[
                        AnimationGroup(
                            arrows[i].animation,
                            FadeIn(pos_dots[i], scale = 3, rate_func=bounce())
                        ) for i in range(1, len(arrows))
                    ],
                    lag_ratio = 0.25
                ),
                lag_ratio = 0.4
            )
        )


        line = Line(8*LEFT, 8*RIGHT).set_color(YELLOW)
        line.set_z_index(-1)
        self.play(Create(line), rate_func=cubic_out)