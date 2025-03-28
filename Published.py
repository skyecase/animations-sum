import math
from manim import *

from modules.custom_mobjects import DottedLine, FullscreenAxes, create_axes
from modules.helpers import create_updater_container, fade_and_shift_in, fade_and_shift_out, fade_and_shift_out_color, highlight_animation, morph_text, rotate_points
from modules.interpolation import cubic_out, sin_smooth_in_out


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

        u.add_updater(lambda _: axes.become(make_axes()))
        u.add_updater(lambda _: curve.become(create_curve()))
        u.add_updater(lambda _: line.become(create_line()))

        self.play(axis_space_center_vt.animate.set_value(27), run_time=3, rate_func=sin_smooth_in_out(0.1))

        u.remove_updater_index(-1)


        dot_1 = Dot(axes.coords_to_point(math.e**PI, PI), 0.1, color=YELLOW)
        dot_1.save_state(); dot_1.scale(0)
        # dotted_line_1 = DottedLine(dot_1.get_center(), axes.coords_to_point(math.e**PI, 0), color=BLUE)
        # dotted_line_1.set_z_index(-1)

        line_2 = Line(axes.coords_to_point(31 - 3, math.log(31)), axes.coords_to_point(31 + 3, math.log(31)), color=BLUE)
        line_2.save_state(); line_2.scale(0)
        dot_2 = Dot(axes.coords_to_point(31, math.log(31)), 0.1, color=YELLOW)
        dot_2.save_state(); dot_2.scale(0)
        # dotted_line_2 = DottedLine(dot_2.get_center(), axes.coords_to_point(math.e**PI, 0), color=GREEN)
        # dotted_line_2.set_z_index(-1)

        self.play(
            LaggedStart(
                AnimationGroup(
                    Transform(line, Line(axes.coords_to_point(math.e**PI - 3, PI), axes.coords_to_point(math.e**PI + 3, PI), color=BLUE), rate_func=cubic_out),
                    dot_1.animate(rate_func=cubic_out).restore(),
                    # FadeIn(dot_1, scale=0, rate_func=cubic_out),
                    # Create(dotted_line_1),
                ),
                AnimationGroup(
                    line_2.animate(rate_func=cubic_out).restore(),
                    dot_2.animate(rate_func=cubic_out).restore(),
                    # FadeIn(dot_2, scale=0, rate_func=cubic_out),
                    # Create(dotted_line_2),
                ),
                lag_ratio = 0.5,
                run_time = 1
            )
        )