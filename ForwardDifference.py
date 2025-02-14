from manim import *
from modules.custom_mobjects import CheckMark, DottedLine, FullscreenAxes, create_axes
from modules.helpers import create_updater_container, fade_and_shift_in, fade_and_shift_out, highlight, highlight_animation, normalize_point_speed
from modules.interpolation import bounce, cubic_out, sin_smooth_in


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



class LogarithmConstant(MovingCameraScene):
    def construct(self):
        u = create_updater_container(self)

        AXIS_SCALE = 0.8
        axis_start = ValueTracker(-5.5) # screen space position of axis origin x coordinate

        def make_axes():
            vertical_offset = -np.log((7 + 5.5)/AXIS_SCALE) * AXIS_SCALE
            return FullscreenAxes(self, axis_start.get_value()*RIGHT + vertical_offset*UP, [AXIS_SCALE, AXIS_SCALE])
        
        axes = make_axes()


        curve = ParametricFunction(lambda t: axes.coords_to_point(t, max(np.log(t), -3.5)), [0.01, 17.1]).set_color(RED)
        curve.set_points(normalize_point_speed(curve.points))


        TEXT_POS = (3, 2)

        text = MathTex("\\ln(x)").move_to(axes.coords_to_point(*TEXT_POS))

        self.play(
            LaggedStart(
                create_axes(self, axes),
                Create(curve, rate_func=lambda t: (t + t**2)/2),
                Write(text),
                lag_ratio=0.3
            )
        )
        self.add(axes) # This is important!
        self.add(curve) # Fixes wrong ordering caused by previous line.


        CONSTANT = 3.5

        dotted_line = DottedLine(axes.coords_to_point(-2, CONSTANT), axes.coords_to_point(16, CONSTANT), 0.3, 0.15, color=BLUE)

        self.play(Create(dotted_line), rate_func=linear)


        def updater(_):
            axes.become(make_axes())
            left_bound = max(0.01, axes.point_to_coords(LEFT * 7.5)[0])
            right_bound = axes.point_to_coords(RIGHT * 7.5)[0]
            curve.become(ParametricFunction(lambda t: axes.coords_to_point(t, np.log(t)), [left_bound, right_bound]).set_color(RED))
            text.move_to(axes.coords_to_point(*TEXT_POS))
            dotted_line.become(DottedLine(axes.coords_to_point(-2, CONSTANT), axes.coords_to_point(right_bound, CONSTANT), 0.3, 0.15, color=BLUE))
        u.add_updater(updater)



        black_fade = Square(20, color=BLACK, fill_opacity=1)
        black_fade.set_z_index(1)


        dot_1 = Dot(DOWN * 3, 0.12, color=BLUE)
        dot_1.set_z_index(2)

        s_text = MathTex("S(n)").move_to(dot_1.get_center() + RIGHT, LEFT)
        s_text.set_z_index(2)

        s_arrow = Arrow(s_text.get_left(), dot_1.get_center())
        s_arrow.set_z_index(2)


        self.play(
            axis_start.animate(run_time = 8, rate_func = sin_smooth_in(0.8)).set_value(-40),
        )
