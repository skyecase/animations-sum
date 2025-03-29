import math
from manim import *

from modules.custom_mobjects import DottedLine, FullscreenAxes, create_axes
from modules.helpers import create_time_getter, create_updater_container, fade_and_shift_in, fade_and_shift_out, fade_and_shift_out_color, highlight, highlight_animation, morph_text, rotate_points
from modules.interpolation import cubic_out, cubic_in, sin_smooth_in, sin_smooth_in_out, cubic_in_out


# Adds the arrow on a sigma
def make_notation(text: SVGMobject):
    arrow = MathTex("\\rightarrow")
    arrow.move_to(text.get_center() + LEFT*0.0825)
    return arrow

def fade_with_color_change(mobj: VMobject):
    mobj.save_state()
    mobj.scale(0).set_color(BLACK).set_stroke(width=0)
    return mobj.animate.restore()


class Formulas(Scene):
    def construct(self):
        text = MathTex("\\sum_{n=x}^y f(n)")
        arrow = make_notation(text[0][1])

        text = VGroup(text, arrow)

        text.scale(1.5)

        self.play(
            fade_with_color_change(text)
        )


        id_1 = MathTex("\\sum_{n=-x}^x \\frac1n = \\pi \\cot(\\pi x)").move_to(LEFT*2.5)
        id_1 = VGroup(id_1, make_notation(id_1[0][1]))

        id_2 = MathTex("\\sum_{n=1}^{-\\frac12} n^x = (2 - 2^x)\\zeta(x)").move_to(LEFT*3.5 + DOWN*2)
        id_2 = VGroup(id_2, make_notation(id_2[0][4]))

        id_3 = MathTex("\\sum_{n=1}^{-\\frac12} \\frac1n = -2\\ln2").move_to(RIGHT*3)
        id_3 = VGroup(id_3, make_notation(id_3[0][4]))

        id_4 = MathTex("\\sum_{n=1}^{-\\frac12} n\\ln(n) = -\\frac{\\ln(2)}{24} - \\frac32 \\zeta'(-1)").scale(0.9).move_to(RIGHT*3 + DOWN*2)
        id_4 = VGroup(id_4, make_notation(id_4[0][4]))

        self.play(
            LaggedStart(
                text.animate.shift(UP*2.5).scale(1.25/1.5),
                LaggedStart(
                    fade_with_color_change(id_1),
                    fade_with_color_change(id_2),
                    fade_with_color_change(id_3),
                    fade_with_color_change(id_4),
                    lag_ratio=0.1
                ),
                lag_ratio = 0.2
            )
        )

        self.play(
            LaggedStart(
                fade_and_shift_out_color(id_2, DOWN),
                fade_and_shift_out_color(id_4, DOWN),
                fade_and_shift_out_color(id_1, DOWN),
                fade_and_shift_out_color(id_3, DOWN),
                fade_and_shift_out_color(text, DOWN),
                lag_ratio=0.1
            )
        )

        text = MathTex("S(x) = \\lim_{n \\to \\infty}\\left(\\sum_{k=1}^n (f(k) - f(x+k)) + \\sum_{k=1}^x f(n+k)\\right)")
        self.play(fade_and_shift_in(text, UP))


        forward_difference = MathTex("\\Delta^n f(k)").move_to(DOWN * 1.5 + LEFT*3).set_color(RED)

        self.play(
            FadeIn(forward_difference, shift=UP*1.5),
            text.animate.shift(UP)
        )

        bcoef = MathTex("\\binom nk").move_to(DOWN*1.5 + RIGHT*3).set_color(RED)
        self.play(FadeIn(bcoef, shift=UP))


        polynomials = Tex("Polynomials").scale(1.25)

        self.play(
            FadeOut(text, shift=UP),
            FadeOut(VGroup(forward_difference, bcoef), shift=DOWN),
            FadeIn(polynomials, scale=0)
        )


class Polynomials(Scene):
    def construct(self):
        
        title = Tex("Polynomials").scale(1.25)

        text = MathTex("x^3 - 3x^2 - 2x + 4")

        self.play(
            FadeIn(text, shift=UP),
            title.animate.shift(UP*2.5)
        )

        new_text = MathTex("\\sum_{k=1}^x (", "k^3 - 3k^2 - 2k + 4", ")")
        for letter in [new_text[1][0], new_text[1][4], new_text[1][8]]:
            rotate_points(letter, 72+36-16)
            # letter.reverse_points()
        self.play(morph_text(text, new_text, [1]))

        self.remove(*text, *new_text)
        text = MathTex("\\sum_{k=1}^x (k^3 - 3k^2 - 2k + 4)")
        new_text = MathTex("\\sum_{k=1}^x (k^3 - 3k^2 - 2k + 4)", "= \\frac14x^4-\\frac12x^3-\\frac94x^2+\\frac52x")
        self.add(text)

        self.play(
            Transform(text[0], new_text[0]),
            FadeIn(new_text[1], shift = LEFT*4)
        )

        self.remove(*text, *new_text)
        text = MathTex("\\sum_{k=1}^x (k^", "3", "- 3k^2 - 2k + 4) = \\frac14x^", "4", "-\\frac12x^3-\\frac94x^2+\\frac52x")
        self.add(text)
        self.play(highlight_animation(VGroup(text[1], text[3]), BLUE))

        self.play(fade_and_shift_out_color(text, UP))


        f_text = Tex("If $f(x)$", " behaves like a polynomial ", "as $x \\to \\infty$,").move_to(UP*0.5)
        s_text = Tex("then $S(x)$", " behaves like a polynomial ", "as $x \\to \\infty$.").move_to(DOWN)

        self.play(fade_and_shift_in(f_text, UP))
        self.play(fade_and_shift_in(s_text, UP))

        self.play(
            VGroup(f_text[1], s_text[1]).animate.set_color(RED)
        )

        self.play(
            fade_and_shift_out(title, UP),
            fade_and_shift_out(VGroup(f_text, s_text), DOWN)
        )



class Constant(Scene):
    def construct(self):
        u = create_updater_container(self)

        AXIS_SCALE = 0.8
        axis_space_center_vt = ValueTracker(5) # X coordinate in the axes that is at the screen origin

        def make_axes():
            center_x = axis_space_center_vt.get_value()
            return FullscreenAxes(self, LEFT*AXIS_SCALE*center_x + DOWN*AXIS_SCALE*math.log(center_x), [0.8, 0.8], major_tick_every=[10, None])
        axes = make_axes()


        def create_curve(): 
            return ParametricFunction(lambda t: axes.coords_to_point(t, math.log(t)), [max(0.01, axes.point_to_coords(LEFT*7.5)[0]), axes.point_to_coords(RIGHT*7.5)[0]], color=RED)
        curve = create_curve()

        def create_line():
            return Line(LEFT*7.5 + UP*axes.coords_to_point(0, PI), RIGHT*7.5 + UP*axes.coords_to_point(0, PI), color=BLUE)
        line = create_line()


        self.play(
            LaggedStart(
                create_axes(self, axes),
                Create(curve),
                Create(line),
                lag_ratio=0.25
            )
        )
        self.add(axes)
        self.add(curve)
        self.add(line)

        def axis_updater(_): axes.become(make_axes())
        u.add_updater(axis_updater)
        u.add_updater(lambda _: curve.become(create_curve()))
        u.add_updater(lambda _: line.become(create_line()))

        self.play(axis_space_center_vt.animate.set_value(27), run_time=3, rate_func=sin_smooth_in_out(0.1))

        u.remove_updater_index(-1)
        line.save_state()

        dot = Dot(axes.coords_to_point(math.e**PI, PI), 0.1, color=YELLOW)
        dot.save_state(); dot.scale(0)

        line_2 = Line(axes.coords_to_point(31 - 3, math.log(31)), axes.coords_to_point(31 + 3, math.log(31)), color=BLUE)
        line_2.save_state(); line_2.scale(0)
        dot_2 = Dot(axes.coords_to_point(31, math.log(31)), 0.1, color=YELLOW)
        dot_2.save_state(); dot_2.scale(0)

        self.play(
            LaggedStart(
                AnimationGroup(
                    Transform(line, Line(axes.coords_to_point(math.e**PI - 3, PI), axes.coords_to_point(math.e**PI + 3, PI), color=BLUE), rate_func=cubic_out),
                    dot.animate(rate_func=cubic_out).restore(),
                ),
                AnimationGroup(
                    line_2.animate(rate_func=cubic_out).restore(),
                    dot_2.animate(rate_func=cubic_out).restore(),
                ),
                lag_ratio = 0.5,
                run_time = 1
            )
        )

        self.play(
            LaggedStart(
                AnimationGroup(
                    line_2.animate(rate_func=cubic_in).scale(0),
                    dot_2.animate(rate_func=cubic_in).scale(0),
                ),
                AnimationGroup(
                    line.animate(rate_func=cubic_in).restore(),
                    dot.animate.scale(1) # noop to prevent z order from getting messed up (no clue why that happens)
                ),
                lag_ratio = 0.5,
                run_time = 1
            )
        )



        point_x_vt = ValueTracker(math.e**PI)
        def line_and_dot_updater(_):
            line.move_to(UP*axes.coords_to_point(0, math.log(point_x_vt.get_value())))
            dot.move_to(axes.coords_to_point(point_x_vt.get_value(), math.log(point_x_vt.get_value())))
        u.add_updater(line_and_dot_updater)

        self.play(point_x_vt.animate.set_value(34), rate_func=sin_smooth_in_out())
        self.play(point_x_vt.animate.set_value(20), rate_func=sin_smooth_in_out())
        self.play(point_x_vt.animate.set_value(axis_space_center_vt.get_value()), rate_func=sin_smooth_in_out())

        u.remove_updater(line_and_dot_updater)

        self.play(
            axis_space_center_vt.animate.set_value(300),
            point_x_vt.animate.set_value(300),
            rate_func=sin_smooth_in(0.5),
            run_time=15
        )


        #=========================#
        # Done going to the right #
        #=========================#

        axis_space_center_vt.set_value(5)
        axes.become(make_axes()) # Force update
        self.remove(line)
        self.remove(dot)

        dotted_line = DottedLine(axes.coords_to_point(5, 0) + DOWN*0.4, axes.coords_to_point(5, math.log(5))).set_color(YELLOW)
        dot.set_z_index(1)
        n_text = MathTex("n").move_to(axes.coords_to_point(5, 0) + DOWN*0.55, UP).set_color(YELLOW)

        self.play(
            Create(dotted_line, rate_func=cubic_out),
            FadeIn(dot, scale=0, rate_func=cubic_out),
            fade_and_shift_in(n_text, UP*0.5)
        )


        c_text = MathTex("c_n").move_to(axes.coords_to_point(5, math.log(5)) + UP*0.25 + LEFT*1.5, DOWN+RIGHT).set_color(BLUE)
        self.play(
            Create(line, rate_func=cubic_out),
            fade_and_shift_in(c_text, RIGHT)
        )


        def set_objects(n: int):
            dot.move_to(axes.coords_to_point(n, math.log(n)))
            line.move_to(UP*axes.coords_to_point(n, math.log(n)))
            dotted_line.become(DottedLine(axes.coords_to_point(n, 0) + DOWN*0.4, axes.coords_to_point(n, math.log(n))).set_color(YELLOW))
            n_text.become(MathTex(n).move_to(axes.coords_to_point(n, 0) + DOWN*0.55, UP).set_color(YELLOW))
            c_text.become(MathTex(f"c_{{{n}}}").move_to(axes.coords_to_point((n**0.75)/2, math.log(n)) + UP*0.25, DOWN).set_color(BLUE))

        opacity_vt = ValueTracker(1)

        self.wait()

        set_objects(1)
        self.wait()
        set_objects(2)
        self.wait()
        set_objects(3)
        self.wait()

        point_x_vt.set_value(4)
        def updater(_):
            set_objects(math.floor(point_x_vt.get_value()))
            VGroup(line, c_text).set_opacity(opacity_vt.get_value())
        u.add_updater(updater)

        self.play(
            LaggedStart(
                point_x_vt.animate(rate_func=sin_smooth_in(0.6), run_time=4).set_value(35),
                opacity_vt.animate(rate_func=linear).set_value(0),
                lag_ratio=3/4
            )
        )

        u.remove_updater(updater)
        VGroup(line, c_text).set_opacity(1)


        set_objects(5)
        self.remove(dotted_line, c_text, n_text)
        n_equals_text = MathTex("n =", "5", color=YELLOW).move_to(axes.coords_to_point(5, 0) + DOWN*0.55, UP).set_color(YELLOW)
        dot.save_state(); dot.scale(0)

        self.play(
            dot.animate(rate_func=cubic_out).restore(),
            Create(line, rate_func=cubic_out),
            Create(dotted_line, rate_func=cubic_out),
            fade_and_shift_in(n_equals_text, UP),
        )


        green_color = '#53ff55'


        n_plus_one_half_line = DottedLine(axes.coords_to_point(5 + 1/2, 0) + UP*0.06, axes.coords_to_point(5 + 1/2, 2.75)).set_color(green_color)
        n_plus_one_half_text = MathTex("n + \\tfrac12").set_color(green_color).move_to(axes.coords_to_point(5 + 1/2, 3.25))
        self.play(
            Create(n_plus_one_half_line, rate_func=cubic_out),
            fade_and_shift_in(n_plus_one_half_text, DOWN),
            run_time = 0.75
        )


        n_minus_pi_line = DottedLine(axes.coords_to_point(5 - PI, 0) + UP*0.06, axes.coords_to_point(5 - PI, 2.75)).set_color(green_color)
        n_minus_pi_text = MathTex("n - \\pi").set_color(green_color).move_to(axes.coords_to_point(5 - PI, 3.25))
        self.play(
            Create(n_minus_pi_line, rate_func=cubic_out),
            fade_and_shift_in(n_minus_pi_text, DOWN),
            run_time = 0.75
        )

        n_plus_5_line = DottedLine(axes.coords_to_point(5 + 5, 0) + UP*0.26, axes.coords_to_point(5 + 5, 2.75)).set_color(green_color)
        n_plus_5_text = MathTex("n + 5").set_color(green_color).move_to(axes.coords_to_point(5 + 5, 3.25))
        self.play(
            Create(n_plus_5_line, rate_func=cubic_out),
            fade_and_shift_in(n_plus_5_text, DOWN),
            run_time = 0.75
        )


        def create_stuff(val, const=5):
            const_dot = Dot(axes.coords_to_point(val, math.log(const)), color=green_color)
            curve_dot = Dot(axes.coords_to_point(val, math.log(val)), color=green_color)
            line = Line(const_dot.get_center(), curve_dot.get_center(), color=green_color)
            return VGroup(const_dot, curve_dot, line)
        

        n_minus_pi_stuff = create_stuff(5 - PI)
        n_minus_pi_stuff.save_state()
        n_minus_pi_stuff[0].scale(0); n_minus_pi_stuff[1].scale(0); n_minus_pi_stuff[2].set_stroke(width=0)

        n_plus_one_half_stuff = create_stuff(5 + 1/2)
        n_plus_one_half_stuff.save_state()
        n_plus_one_half_stuff[0].scale(0); n_plus_one_half_stuff[1].scale(0); n_plus_one_half_stuff[2].set_stroke(width=0)

        n_plus_5_stuff = create_stuff(5 + 5)
        n_plus_5_stuff.save_state()
        n_plus_5_stuff[0].scale(0); n_plus_5_stuff[1].scale(0); n_plus_5_stuff[2].set_stroke(width=0)

        invisible_text = MathTex("n =", "0").move_to(DOWN*0.6)

        dotted_line.reverse_direction()

        self.play(
            n_minus_pi_stuff.animate(rate_func=cubic_out).restore(),
            n_plus_one_half_stuff.animate(rate_func=cubic_out).restore(),
            n_plus_5_stuff.animate(rate_func=cubic_out).restore(),
            n_minus_pi_line.animate(rate_func=cubic_out, run_time=0.5, remover=True).set_stroke(width=0),
            n_plus_one_half_line.animate(rate_func=cubic_out, run_time=0.5, remover=True).set_stroke(width=0),
            n_plus_5_line.animate(rate_func=cubic_out, run_time=0.5, remover=True).set_stroke(width=0),

            Uncreate(dotted_line),
            n_equals_text.animate.shift(invisible_text[0].get_center() - n_equals_text[0].get_center()),
            
            n_minus_pi_text.animate.move_to(RIGHT*n_minus_pi_text.get_center() + UP*0.6),
            n_plus_one_half_text.animate.move_to(axes.coords_to_point(5 + 1/2, math.log(5 + 1/2)) + UP*0.6),
            n_plus_5_text.animate.move_to(axes.coords_to_point(5 + 5, math.log(5 + 5)) + UP*0.6)
        )
        invisible_text.shift(DOWN*0.75)



        def stuff_updater(_):
            n = point_x_vt.get_value()

            n_minus_pi_stuff.become(create_stuff(n - PI, n))
            n_plus_one_half_stuff.become(create_stuff(n + 1/2, n))
            n_plus_5_stuff.become(create_stuff(n + 5, n))

            n_minus_pi_text.move_to(axes.coords_to_point(n - PI, math.log(n)) + UP*0.6)
            n_plus_one_half_text.move_to(axes.coords_to_point(n + 1/2, math.log(n + 1/2)) + UP*0.6)
            n_plus_5_text.move_to(axes.coords_to_point(n + 5, math.log(n + 5)) + UP*0.6)

            dot.move_to(axes.coords_to_point(n, math.log(n)))
            line.move_to(UP*axes.coords_to_point(n, math.log(n)))

            digits = int(math.log10(n)) + 1
            invisible_text.become(MathTex("n =", "0" * digits)).move_to(axes.coords_to_point(n, math.log(n)) + DOWN*0.6)
            n_equals_text.become(MathTex("n =", int(n), color=YELLOW))
            n_equals_text.shift(invisible_text[0].get_center() - n_equals_text[0].get_center())
        
        u.add_updater(stuff_updater)





        v_offset_vt = ValueTracker(0)

        u.remove_updater(axis_updater)
        def make_axes():
            center_x = axis_space_center_vt.get_value()
            return FullscreenAxes(self, LEFT*AXIS_SCALE*center_x + DOWN*(v_offset_vt.get_value() + AXIS_SCALE*math.log(center_x)), [0.8, 0.8], major_tick_every=[10, None])
        u.add_updater(lambda _: axes.become(make_axes()), 0)

        get_time = create_time_getter(self)
        
        def round_updater(_):
            A = 30 # Higher = slower ease
            x = math.sqrt((18*get_time())**2 + A**2) - A + 5
            point_x_vt.set_value(round(x))
            axis_space_center_vt.set_value(round(x))
        u.add_updater(round_updater, 0)


        self.wait(5)

        text = MathTex("\\lim_{n \\to \\infty} (f(n + x) - c_n) = 0").move_to(UP)
        top_text = Tex("For every $x$,").move_to(text.get_top() + UP*0.5, DOWN)
        text.set_z_index(3)
        top_text.set_z_index(3)

        self.play(
            LaggedStart(
                v_offset_vt.animate(run_time=1.5).set_value(2),
                Write(top_text),
                Write(text),
                lag_ratio=0.5
            )
        )

        self.wait(5)



        black_fade = Square(16, color=BLACK, fill_opacity=1)
        black_fade.set_z_index(2)

        def_text = Tex(
            "$f(x)$ behaves like a constant if \\\\",
            "there is a sequence of constants \\\\",
            "$c_1, c_2, c_3 \\dots$ such that ", "for every $x$,"
        )
        for t in def_text[:2] + [def_text[2:]]:
            t.shift(RIGHT*(-t.get_left()))
        def_text.move_to(RIGHT*0.2 + UP).set_z_index(3)

        rotate_points(def_text[3][0], 28)

        new_text = MathTex("\\lim_{n \\to \\infty} (f(n + x) - c_n) = 0", ".").move_to(DOWN)
        new_text.set_z_index(3)

        self.play(
            LaggedStart(
                FadeIn(black_fade, rate_func=linear),
                AnimationGroup(
                    FadeIn(def_text[:3], shift=def_text[3].get_center() - top_text.get_center()),
                    Transform(top_text[0], def_text[3]),
                    morph_text(text, new_text, [0])
                ),
                lag_ratio=0.5
            )
        )



class Definition(Scene):
    def construct(self):
        def_text = Tex(
            "$f(x)$ behaves like a ", "constant ", "if \\\\",
            "there is a sequence of ", "constants \\\\",
            "$c_1, c_2, c_3 \\dots$ ", "such that for every $x$,"
        )
        for t in [def_text[0:3], def_text[3:5], def_text[5:]]:
            t.shift(RIGHT*(-t.get_left()))
        def_text.move_to(RIGHT*0.2 + UP)

        text = MathTex("\\lim_{n \\to \\infty} (f(n + x) -", "c_", "n", ") = 0.").move_to(DOWN)

        self.add(text, def_text)

        self.play(
            highlight_animation(def_text[1], BLUE),
            highlight_animation(def_text[4], BLUE),
        )


        new_def_text = Tex(
            "$f(x)$ behaves like a ", "degree $0$ polynomial ", "if \\\\",
            "there is a sequence of ", "degree $0$ polynomials \\\\",
            "$c_1, c_2, c_3\\dots$ ", "such that for every $x$,"
        )
        for t in [new_def_text[0:3], new_def_text[3:5], new_def_text[5:]]:
            t.shift(RIGHT*(-t.get_left()))
        new_def_text.move_to(UP)

        self.play(Transform(def_text, new_def_text))

        self.remove(*def_text, *new_def_text)


        def_text = Tex(
            "$f(x)$ behaves like a degree $0$ polynomial if \\\\",
            "there is a sequence of degree $0$ polynomials \\\\",
            "$c_1, c_2, c_3\\dots$ such that for every $x$,"
        )
        for t in def_text:
            t.shift(RIGHT*(-t.get_left()))
        def_text.move_to(UP)
        self.add(def_text)

        self.play(
            highlight_animation(VGroup(def_text[2][0], def_text[2][3], def_text[2][6]), RED),
            highlight_animation(text[1], RED)
        )


        new_def_text = Tex(
            "$f(x)$ behaves like a degree $0$ polynomial if \\\\",
            "there is a sequence of degree $0$ polynomials \\\\",
            "$p_1, p_2, p_3\\dots$ such that for every $x$,"
        )
        for t in [new_def_text[0], new_def_text[1], new_def_text[2:]]:
            t.shift(RIGHT*(-t.get_left()))
        new_def_text.move_to(UP)

        new_text = MathTex("\\lim_{n \\to \\infty} (f(n + x) -", "p_", "n", "(n + x)", ") = 0.").move_to(DOWN)

        self.play(
            Transform(def_text, new_def_text),
            morph_text(text, new_text, [0, 1, 2, 4])
        )
        


        self.remove(*def_text, *new_def_text)
        def_text = Tex(
            "$f(x)$ behaves like a degree ", "$0$ ", "polynomial if \\\\",
            "there is a sequence of degree ", "$0$ ", "polynomials \\\\",
            "$p_1, p_2, p_3\\dots$ such that for every $x$,"
        )
        for t in [def_text[0:3], def_text[3:6], def_text[6:]]:
            t.shift(RIGHT*(-t.get_left()))
        def_text.move_to(UP)
        self.add(def_text)

        new_def_text = Tex(
            "$f(x)$ behaves like a degree ", "$m$ ", "polynomial if \\\\",
            "there is a sequence of degree ", "$m$ ", "polynomials \\\\",
            "$p_1, p_2, p_3\\dots$ such that for every $x$,"
        )
        for t in [new_def_text[0:3], new_def_text[3:6], new_def_text[6:]]:
            t.shift(RIGHT*(-t.get_left()))
        new_def_text.move_to(UP)

        self.play(
            highlight_animation(VGroup(def_text[1], def_text[4]), BLUE)
        )

        self.play(Transform(def_text, new_def_text))

        
        self.remove(*text, *new_text)
        text = MathTex("\\lim_{n \\to \\infty} (f(n + x) - p_n(n + x)) = 0", ".").move_to(DOWN)
        self.add(text)

        new_text = MathTex("\\lim_{n \\to \\infty} (f(n + x) - p_n(n + x)) = 0").move_to(UP*2.5)
        s_def_text = MathTex("S(x) = \\lim_{n\\to\\infty} \\left( \\sum_{k=1}^n (f(k) - f(x+k)) + \\sum_{k=1}^x", "f(n+k)", "\\right)")

        self.play(
            LaggedStart(
                AnimationGroup(
                    def_text.animate(remover=True, rate_func=cubic_in).move_to(UP*4, DOWN),
                    morph_text(text, new_text, [0], run_time=2, rate_func=cubic_in_out)
                ),
                Write(s_def_text),
                lag_ratio = 0.5
            )
        )

        self.remove(*text, *new_text)
        text = new_text
        self.add(text)

        self.play(
            highlight_animation(s_def_text[1], BLUE)
        )

        new_s_def_text = MathTex("S(x) = \\lim_{n\\to\\infty} \\left( \\sum_{k=1}^n (f(k) - f(x+k)) + \\sum_{k=1}^x", "p_n(n+k)", "\\right)")

        self.play(Transform(s_def_text, new_s_def_text))

        
        self.remove(s_def_text)
        s_def_text = MathTex("S(x) = \\lim_{n\\to\\infty} \\left( \\sum_{k=1}^n (f(k) - f(x+k)) +", "\\sum_{k=1}^x p_n(n+k)", "\\right)")
        self.add(s_def_text)

        polynomial_text = Tex("This is a polynomial!").move_to(s_def_text[1].get_bottom() + DOWN*0.5, UP).set_color(BLUE)

        self.play(
            highlight_animation(s_def_text[1], BLUE),
            FadeIn(polynomial_text, shift=UP)
        )


        p_text = MathTex("P_n(x) = \\sum_{k=1}^x p_n(n + k)").move_to(DOWN*2)

        self.play(
            FadeIn(p_text, shift=UP),
            FadeOut(polynomial_text, scale=0, shift = UP*0.25)
        )


        new_s_def_text = MathTex("S(x) = \\lim_{n\\to\\infty} \\left( \\sum_{k=1}^n (f(k) - f(x+k)) +", "P_n(x)", "\\right)")
        self.play(Transform(s_def_text, new_s_def_text))

        self.wait()