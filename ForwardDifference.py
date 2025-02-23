from manim import *
from modules.custom_mobjects import CheckMark, CustomArrow, DottedLine, FullscreenAxes, create_axes
from modules.helpers import create_double_arrow, create_updater_container, fade_and_shift_in, fade_and_shift_out, grow_between, highlight, highlight_animation, morph_text, normalize_point_speed, rotate_points
from modules.interpolation import bounce, cubic_out, sin_smooth_in, cubic_in, cubic_in_out


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




class ForwardDifferenceIntroduction(Scene):
    def construct(self):
        DOT_SPREAD = 1.5
        DOT_Y = -1

        text = Tex("$\\displaystyle \\lim_{x \\to \\infty} f(x)$ = 0").move_to(UP)

        dot_0 = Dot(LEFT * 3 + UP*DOT_Y, 0.12, color=BLUE)
        neg_dots = [Dot(dot_0.get_center() + RIGHT*DOT_SPREAD*i, 0.12, color=BLUE) for i in range(-2, 0)]
        pos_dots = [Dot(dot_0.get_center() + RIGHT*DOT_SPREAD*i, 0.12, color=BLUE) for i in range(1, 8)]

        s_n_text = MathTex("S(n)").move_to(dot_0.get_center() + DOWN, UP)
        arrow = Arrow(s_n_text.get_top(), dot_0.get_center(), buff=0.2)

        for obj in [dot_0, s_n_text, arrow] + neg_dots + pos_dots: obj.set_z_index(2)

        
        self.play(
            fade_and_shift_in(text, UP),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in neg_dots + [dot_0]],
                fade_and_shift_in(VGroup(s_n_text, arrow), UP),
                lag_ratio = 0.3
            )
        )


        arrows = [CustomArrow(dot_0.get_center() + i*DOT_SPREAD*RIGHT, dot_0.get_center() + (i+1)*DOT_SPREAD*RIGHT, angle=PI/2*(1-2*(i%2))) for i in range(0, 7)]
        self.add(*arrows)
        for i in range(0, len(arrows)):
            f_text = MathTex("+ f(n + " + str(i+1) + ")").scale(0.8)
            pretty_much_text = Tex("(Pretty much 0)").scale(0.5).move_to(f_text.get_bottom() + DOWN*0.1, UP)
            group = VGroup(f_text, pretty_much_text)

            dir = UP if i%2 == 0 else DOWN
            group.move_to(dir * 0.2, -dir)
            arrows[i].set_text(group)
        
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        arrows[i].animation,
                        FadeIn(pos_dots[i], scale = 3, rate_func=bounce())
                    ) for i in range(0, len(arrows))
                ],
                lag_ratio = 0.25
            ),
        )
        self.remove(*arrows)


        new_text = Tex("$S(x)$ flattens out if ", "$\\displaystyle \\lim_{x \\to \\infty} f(x) = 0$", ".").move_to(UP)
        self.play(
            Transform(text[0], new_text[1]),
            FadeIn(new_text[0], shift = RIGHT * 3),
            grow_between(new_text[2], text)
        )

        
        self.play(
            LaggedStart(
                *[fade_and_shift_out(dot, DOWN) for dot in neg_dots],
                fade_and_shift_out(VGroup(dot_0, arrow, s_n_text), DOWN),
                *[fade_and_shift_out(dot, DOWN) for dot in pos_dots],
                lag_ratio = 0.05
            )
        )
        

        recursive_text = MathTex("S(x+1)", "=", "S(x)", "+", "f(x+1)").move_to(DOWN)

        self.play(fade_and_shift_in(recursive_text, UP))

        new_recursive_text = MathTex("S(x+1)", "-", "S(x)", "=", "f(x+1)").move_to(DOWN)

        self.play(
            morph_text(recursive_text, new_recursive_text, [0, 3, 2, 1, 4], path_arc=PI*3/4)
        )

        self.remove(*recursive_text)
        recursive_text = MathTex("S(x+1) - S(x)", "=", "f(x+1)").move_to(DOWN)
        new_recursive_text = MathTex("\\lim_{x \\to \\infty} (", "S(x+1) - S(x)", ") = 0", "\\iff", "\\lim_{x \\to \\infty}", "f(x + 1)", "= 0").move_to(DOWN)
        # Unnecessary hacky stuff to make the equals morph really fancy
        equals_top = recursive_text[1][0]
        equals_bottom = recursive_text[1][0].copy()
        equals_top.points = equals_top.points[:24]
        equals_bottom.points = equals_bottom.points[24:]
        rotate_points(equals_bottom, 16)
        recursive_text.submobjects[1] = VGroup(equals_top, equals_bottom)
        self.play(
            morph_text(recursive_text, new_recursive_text, [1, 3, 5]),
        )

        self.remove(*recursive_text, *new_recursive_text, *new_recursive_text[1])
        recursive_text = MathTex("\\lim_{x \\to \\infty} (S(x+1) - S(x)) = 0 \\iff", "\\lim_{x \\to \\infty} f(x", "+ 1", ") = 0").move_to(DOWN)
        self.add(recursive_text)
        self.play(
            highlight_animation(recursive_text[2], BLUE),
            recursive_text[0].animate.set_color(GRAY)
        )

        new_recursive_text = MathTex("\\lim_{x \\to \\infty} (S(x+1) - S(x)) = 0 \\iff", "\\lim_{x \\to \\infty} f(x", ") = 0").move_to(DOWN)
        self.play(morph_text(recursive_text, new_recursive_text, [0, 1, None, 2]))


        self.remove(*text, *new_text)
        text = Tex("$S(x)$ flattens out if ", "$\\displaystyle \\lim_{x \\to \\infty} f(x) = 0$", ".").move_to(UP)
        equation_part = MathTex("\\lim_{x\\to\\infty}", "f(x)", "= 0").move_to(text[1])
        text.submobjects[1] = equation_part
        new_text = Tex("$S(x)$ flattens out if ", "$\\displaystyle \\lim_{x \\to \\infty} (S(x+1) - S(x)) = 0$", ".").move_to(UP)
        equation_part = MathTex("\\lim_{x\\to\\infty}", "(S(x+1) - S(x))", "= 0").move_to(new_text[1])
        new_text.submobjects[1] = equation_part
        self.play(Transform(text, new_text))

        self.remove(*text, *new_text, *recursive_text)
        text = Tex("$S(x)$ flattens out if ", "$\\displaystyle \\lim_{x \\to \\infty} (S(x+1) - S(x)) = 0$", ".").move_to(UP)
        recursive_text = MathTex("\\lim_{x \\to \\infty} (S(x+1) - S(x)) = 0 \\iff \\lim_{x \\to \\infty} f(x) = 0").move_to(DOWN)
        self.play(
            FadeOut(recursive_text, shift = DOWN * 2),
            text.animate.move_to(ORIGIN)
        )

        new_text = Tex("$f(x)$ flattens out if ", "$\\displaystyle \\lim_{x \\to \\infty} (f(x+1) - f(x)) = 0$", ".")
        self.play(Transform(text, new_text))
        equation_part = MathTex("\\lim_{x \\to \\infty}", "(", "f(x+1) -", "f(x)", ")", "= 0").move_to(text[1])
        text.submobjects[1] = equation_part
        self.add(text)


        fd_text = equation_part[2:4].copy()
        equation_part[2:4].set_color(DARK_GRAY)

        self.play(
            text.animate.shift(UP * 2.5),
            fd_text.animate.move_to(DOWN).scale(1.2)
        )


        fd_title = Tex("The Forward Difference of $f$")
        self.play(Write(fd_title))

        new_fd_text = MathTex("\\Delta f(x) =", "f(x+1) -", "f(x)").scale(1.2).move_to(DOWN)
        self.play(
            Transform(fd_text, new_fd_text[1:]),
            FadeIn(new_fd_text[0], shift = RIGHT * 2)
        )

        new_text = Tex("$f(x)$ flattens out if ", "$\\displaystyle \\lim_{x \\to \\infty} \\Delta f(x) = 0$", ".").move_to(UP * 2.5)
        equation_part = MathTex("\\lim_{x \\to \\infty}", "\\Delta", "f(x)", "= 0").move_to(new_text[1])
        new_text.submobjects[1] = equation_part
        self.play(
            Transform(text[0], new_text[0]),
            Transform(text[2], new_text[2]),
            morph_text(text[1], new_text[1], [0, None, 1, 2, None, 3])
        )


        self.remove(*text, *new_text, *text[1], *new_text[1], *fd_text)
        text = Tex("$f(x)$ flattens out if $\\displaystyle \\lim_{x \\to \\infty} \\Delta f(x) = 0$.").move_to(UP * 2.5)

        self.play(
            text.animate.shift(UP * 2),
            VGroup(new_fd_text, fd_title).animate.move_to(ORIGIN)
        )



class DiscreteContinuous(Scene):
    def construct(self):

        DIST_FROM_CENTER = 2.5

        discrete_header = Tex("Discrete").move_to(LEFT*DIST_FROM_CENTER + UP*2.5)
        continuous_header = Tex("Continuous").move_to(RIGHT*DIST_FROM_CENTER + UP*2.5)

        discrete_underline = Line(discrete_header.get_corner(DOWN + LEFT), discrete_header.get_corner(DOWN + RIGHT), stroke_width=3).shift(DOWN * 0.1)
        continuous_underline = Line(continuous_header.get_corner(DOWN + LEFT), continuous_header.get_corner(DOWN + RIGHT), stroke_width=3).shift(DOWN * 0.1)

        sum = MathTex("\\sum").move_to(LEFT*DIST_FROM_CENTER + UP*1/2).scale(1.25)
        integral = MathTex("\\int").move_to(RIGHT*DIST_FROM_CENTER + UP*1/2).scale(1.25)

        arrow_1 = create_double_arrow(UP*1/2 + LEFT*1.5, UP*1/2 + RIGHT*1.5, tip_length=0.3)
        arrow_1.save_state()
        arrow_1.scale(0).set_stroke(width=0).set_color(BLACK)

        self.play(
            arrow_1.animate.restore(),
            FadeIn(sum, scale=0),
            FadeIn(integral, scale=0),
            LaggedStart(
                Write(discrete_header),
                Create(discrete_underline, rate_func=cubic_out),
                Write(continuous_header),
                Create(continuous_underline, rate_func=cubic_out),
                lag_ratio = 0.2
            )
        )

        delta = MathTex("\\Delta").move_to(LEFT*DIST_FROM_CENTER + DOWN*1.5).scale(2)
        derivative = MathTex("\\frac d{dx}").move_to(RIGHT*DIST_FROM_CENTER + DOWN*1.5).scale(1.25)

        arrow_2 = arrow_1.copy().move_to(DOWN*1.5)
        arrow_2.save_state()
        arrow_2.scale(0).set_stroke(width=0).set_color(BLACK)

        self.play(
            arrow_2.animate.restore(),
            FadeIn(delta, scale=0),
            FadeIn(derivative, scale=0)
        )


        RIGHT_CENTER_H = 3.5

        recursive_text = MathTex("S(x+1) -", "S(x) = f(x+1)").move_to(RIGHT*RIGHT_CENTER_H + UP*1.5)

        self.play(
            VGroup(discrete_header, discrete_underline, sum, delta).animate.shift(LEFT * 3),
            VGroup(continuous_header, continuous_underline, integral, derivative).animate.shift(LEFT * 4.5),
            arrow_1.animate.become(create_double_arrow(UP*1/2 + LEFT*4.5, UP*1/2 + LEFT*3, tip_length=0.3)),
            arrow_2.animate.become(create_double_arrow(DOWN*1.5 + LEFT*4.5, DOWN*1.5 + LEFT*3, tip_length=0.3)),
            FadeIn(recursive_text, shift=LEFT*5)
        )


        self.play(Transform(recursive_text, MathTex("\\Delta", "S(x) = f(x+1)").move_to(RIGHT*RIGHT_CENTER_H + UP*1.5)))



        f = MathTex("f").move_to(DOWN*1.25 + RIGHT*(RIGHT_CENTER_H - 1.25)).scale(1.25)
        s = MathTex("S").move_to(DOWN*1.25 + RIGHT*(RIGHT_CENTER_H + 1.25)).scale(1.25)


        self.play(fade_and_shift_in(f, UP))

        right_arrow = CustomArrow(f.get_center(), s.get_center(), buff=0.4)
        self.add(right_arrow)

        arrow_sigma = MathTex("\\Sigma").move_to((f.get_center() + s.get_center())/2 + UP)

        self.play(
            right_arrow.end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(arrow_sigma, scale=0, shift=UP*0.5, rate_func=cubic_out),
            FadeIn(s, scale=0)
        )


        left_arrow = CustomArrow(s.get_center(), f.get_center(), buff=0.4)
        self.add(left_arrow)

        arrow_delta = MathTex("\\Delta").move_to((f.get_center() + s.get_center())/2 + DOWN)

        self.play(
            left_arrow.end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(arrow_delta, scale=0, shift=DOWN*0.5, rate_func=cubic_out),
        )

        right_arrow.remove_arrow_updater()
        left_arrow.remove_arrow_updater()

        final_text = MathTex("\\Delta f(x) = f(x+1) - f(x)")
        final_text.save_state()
        final_text.scale(0)

        self.play(
            LaggedStart(
                VGroup(discrete_header, discrete_underline, sum, delta, arrow_1, arrow_2, continuous_underline, continuous_header, integral, derivative).animate(rate_func=cubic_in).shift(LEFT * 7.5),
                VGroup(recursive_text, arrow_delta, arrow_sigma, f, s, right_arrow, left_arrow).animate(rate_func=cubic_in).shift(RIGHT * 7.5),
                final_text.animate(scale=0, run_time=1.5, rate_func=cubic_in_out).restore()
            )
        )



class SuperRecursive(Scene):
    def construct(self):

        text = MathTex("\\Delta f(x) = f(x+1)", "-", "f(x)")
        self.add(text)
        new_text = MathTex("f(x)", "+", "\\Delta f(x) = f(x+1)")
        self.play(morph_text(text, new_text, [[2, {"path_arc":0}], 1, 0], path_arc=PI*0.85))

        self.remove(*text, *new_text)
        text = MathTex("f(x) + \\Delta f(x)", "=", "f(x+1)")
        new_text = MathTex("f(x+1)", "=", "f(x) + \\Delta f(x)")
        self.play(morph_text(text, new_text, [2, [1, {"path_arc": 0}], 0], path_arc=PI*0.85))


        def f(x):
            return x**3 / 30 - x/3
        
        SCALE = 1.8
        
        invisible_axes = FullscreenAxes(self, DOWN*1.5, [SCALE, SCALE])

        right_side = invisible_axes.point_to_coords((self.camera.frame_width/2 + 0.1) * RIGHT)[0]

        curve = ParametricFunction(lambda t: invisible_axes.coords_to_point(t, f(t)), [-right_side, right_side], color=RED)

        self.play(
            LaggedStart(
                text.animate.move_to(UP * 2.5),
                Create(curve, rate_func = linear),
                lag_ratio=0.25
            )
        )


        dot_0 = Dot(invisible_axes.coords_to_point(-3, f(-3)), 0.12, color=BLUE).scale(1.5)
        f_a_text = MathTex("f(a)").move_to(dot_0.get_center() + DOWN * 0.5, UP)

        self.play(
            FadeIn(dot_0, scale=3, rate_func=bounce()),
            fade_and_shift_in(f_a_text, UP)
        )

        dot_6 = Dot(invisible_axes.coords_to_point(3, f(3)), 0.12, color=BLUE).scale(1.5)
        f_a_b_text = MathTex("f(a+b)").move_to(dot_6.get_center() + DOWN * 0.5, UP)

        self.play(
            FadeIn(dot_6, scale=3, rate_func=bounce()),
            fade_and_shift_in(f_a_b_text, UP)
        )


        dots = [dot_0] + [Dot(invisible_axes.coords_to_point(i, f(i)), 0.12, color=BLUE) for i in range(-2, 3)] + [dot_6]

        arrows = [CustomArrow(dots[i].get_center(), dots[i+1].get_center(), PI*0.6, buff=0.2) for i in range(0, 6)]
        self.add(*arrows)

        arrow_text_0 = MathTex("+\,\\Delta f(a)").scale(0.8).move_to((dots[0].get_center()+dots[1].get_center())/2 + UP + LEFT*0.3 + LEFT*0.3)

        self.play(
            arrows[0].end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(arrow_text_0, scale=0, shift=UP*0.75, rate_func=cubic_out),
            FadeIn(dots[1], scale=3, rate_func=bounce())
        )

        arrow_text_1 = MathTex("+\,\\Delta f(a+1)").scale(0.8).move_to((dots[1].get_center()+dots[2].get_center())/2 + UP + LEFT*0.3)

        self.play(
            arrows[1].end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(arrow_text_1, scale=0, shift=UP*0.75, rate_func=cubic_out),
            FadeIn(dots[2], scale=3, rate_func=bounce())
        )

        arrow_text_2 = MathTex("+\,\\Delta f(a+2)").scale(0.8).move_to((dots[2].get_center()+dots[3].get_center())/2 + UP + LEFT*0.3 + RIGHT*0.4)

        self.play(
            arrows[2].end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(arrow_text_2, scale=0, shift=UP*0.75, rate_func=cubic_out),
            FadeIn(dots[3], scale=3, rate_func=bounce())
        )

        arrow_text_5 = MathTex("+\,\\Delta f(a+b-1)").scale(0.8).move_to((dots[5].get_center()+dots[6].get_center())/2 + UP + LEFT*0.3)

        self.play(
            LaggedStart(
                AnimationGroup(
                    arrows[3].end_vt.animate(rate_func=cubic_out).set_value(1),
                    FadeIn(dots[4], scale=3, rate_func=bounce())
                ),
                AnimationGroup(
                    arrows[4].end_vt.animate(rate_func=cubic_out).set_value(1),
                    FadeIn(dots[5], scale=3, rate_func=bounce())
                ),
                AnimationGroup(
                    arrows[5].end_vt.animate(rate_func=cubic_out).set_value(1),
                    FadeIn(arrow_text_5, scale=0, shift=UP*0.75, rate_func=cubic_out)
                ),
                lag_ratio=0.5
            )
        )


        long_text = MathTex("f(a)", "+ \\Delta f(a)", "+ \\Delta f(a+1)", "+ \\Delta f(a+2)", "+ \\cdots", "+ \\Delta f(a+b-1)", "=", "f(a+b)").scale(0.8).move_to(UP)

        self.play(
            Transform(f_a_text[0], long_text[0]),
            Transform(arrow_text_0[0], long_text[1]),
            Transform(arrow_text_1[0], long_text[2]),
            Transform(arrow_text_2[0], long_text[3]),
            grow_between(long_text[4], arrow_text_2, arrow_text_5),
            Transform(arrow_text_5[0], long_text[5]),
            grow_between(long_text[6], arrow_text_5, f_a_b_text),
            Transform(f_a_b_text[0], long_text[7])
        )

        for a in arrows: a.remove_arrow_updater()


        self.remove(*f_a_text, *f_a_b_text, *arrow_text_0, *arrow_text_1, *arrow_text_2, *arrow_text_5, *long_text)

        self.add(long_text)

        new_long_text = MathTex("f(a) +", "\\Delta f(a) + \\Delta f(a+1) + \\Delta f(a+2) + \\cdots + \\Delta f(a+b-1)", "= f(a+b)").scale(0.8)
        brace = Brace(new_long_text[1])
        brace_text = MathTex("\\sum_{k=0}^{b-1} \\Delta f(a+k)").move_to(brace.get_bottom() + DOWN * 0.2, UP)

        self.play(
            VGroup(curve, *arrows, *dots).animate.shift(DOWN*4),
            long_text.animate.move_to(ORIGIN),
            FadeIn(brace, shift=DOWN/2)
        )
        self.remove(curve, *arrows, *dots)

        self.play(
            fade_and_shift_in(brace_text, UP)
        )

        self.remove(*long_text)
        long_text = new_long_text
        self.add(long_text)

        new_long_text = MathTex("f(a) +", "\\sum_{k=0}^{b-1} \\Delta f(a+k)", "= f(a+b)")

        shift = new_long_text[1].get_center() - brace_text.get_center()

        self.play(
            LaggedStart(
                AnimationGroup(
                    brace_text.animate.shift(shift),
                    FadeOut(VGroup(brace, long_text[1]), shift=shift),
                ),
                AnimationGroup(
                    Transform(long_text[0], new_long_text[0], rate_func = bounce()),
                    Transform(long_text[2], new_long_text[2], rate_func = bounce()),
                    run_time = 1.5
                ),
                lag_ratio=0.5
            )
        )

        self.remove(*long_text, *new_long_text, brace_text)
        long_text = MathTex("f(a) + \\sum_{k=0}^{b-1} \\Delta f(a+k)", "=", "f(a+b)")
        new_long_text = MathTex("f(a+b)", "=", "f(a) + \\sum_{k=0}^{b-1} \\Delta f(a+k)")
        self.play(morph_text(long_text, new_long_text, [2, 1, 0], path_arc=-PI*0.8))

        bottom_text = Tex("This is the discrete version of $\\displaystyle\\ f(a+b) = f(a) + \\int_0^b f'(a+t) dt$").scale(0.7).move_to(DOWN*2.5)

        self.play(FadeIn(bottom_text))
        self.play(FadeOut(bottom_text))
        self.wait()