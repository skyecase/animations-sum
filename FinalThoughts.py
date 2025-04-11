import math
from manim import *

from modules.custom_mobjects import FullscreenAxes, create_axes
from modules.helpers import create_updater_container, fade_and_shift_in, fade_and_shift_out, grow_between, highlight_animation, morph_text, normalize_point_speed
from modules.interpolation import bounce, cubic_in



class Decree(Scene):
    def construct(self):
        title = Tex("\\underline{Where We Made ``Decrees\"}").scale(1.2).move_to(UP*3)
        self.play(fade_and_shift_in(title, UP))

        recursive = MathTex("S(x+1) = S(x) + f(x+1)").move_to(UP*1.75)
        self.play(fade_and_shift_in(recursive, UP))

        binomial = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3=0}^{k_2-1} 1 = \\binom x3 = \\frac{x(x-1)(x-2)}{3!}", ",").move_to(UP*0)
        etc_1 = Tex("etc...").scale(0.75).move_to(binomial.get_right() + RIGHT*0.75, LEFT)
        self.play(
            LaggedStart(
                fade_and_shift_in(binomial[0], UP),
                LaggedStart(
                    *[fade_and_shift_in(element, shift=LEFT*0.3, run_time = 0.5) for element in [binomial[1], *etc_1[0]]],
                    lag_ratio = 0.125
                ),
                lag_ratio=0.666
            )
        )

        approach_zero = MathTex("\\lim_{n\\to\\infty} \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3=0}^{k_2-1} \\sum_{k_4=0}^{k_3-1} \\Delta^3 f(n+k_4) = 0", ",").move_to(DOWN*2.25)
        etc_2 = Tex("etc...").scale(0.75).move_to(approach_zero.get_right() + RIGHT*0.75, LEFT)
        self.play(
            LaggedStart(
                fade_and_shift_in(approach_zero[0], UP),
                LaggedStart(
                    *[fade_and_shift_in(element, shift=LEFT*0.3, run_time = 0.5) for element in [approach_zero[1], *etc_2[0]]],
                    lag_ratio = 0.125
                ),
                lag_ratio=0.666
            )
        )

        self.play(
            fade_and_shift_out(VGroup(title, recursive, binomial, approach_zero, etc_1, etc_2), UP)
        )

        lim_text = MathTex("\\lim_{x\\to\\infty} \\Delta^m f(x", ") = 0").move_to(UP*2)
        text = MathTex("S(x", ") = \\lim_{n\\to\\infty}\\left( \\sum_{k=1}^{n-1}(f(k) - f(x", "+k)) + \\sum_{k=1}^m", "\\binom xk", "\\Delta^{k-1}f(n) \\right)")

        self.play(
            fade_and_shift_in(VGroup(lim_text, text), UP)
        )




class FinalThoughts(Scene):
    def construct(self):
        lim_text = MathTex("\\lim_{x\\to\\infty} \\Delta^m f(x", ") = 0").move_to(UP*2)
        text = MathTex("S(x", ") = \\lim_{n\\to\\infty}\\left( \\sum_{k=1}^{n-1}(f(k) - f(x", "+k)) + \\sum_{k=1}^m", "\\binom xk", "\\Delta^{k-1}f(n) \\right)")

        self.add(lim_text, text)

        new_text = MathTex("S(x", "+ iy", ") = \\lim_{n\\to\\infty}\\left( \\sum_{k=1}^{n-1}(f(k) - f(x", "+ iy", "+k)) + \\sum_{k=1}^m", "\\binom{x+iy}k", "\\Delta^{k-1}f(n) \\right)").scale(0.8)
        new_lim_text = MathTex("\\lim_{x\\to\\infty} \\Delta^m f(x", "+ iy", ") = 0").move_to(UP*2).scale(0.8)

        self.play(
            morph_text(lim_text, new_lim_text, [0, 2]),
            morph_text(text, new_text, [0, 2, 4, 5, 6], ignore_1=[3], ignore_2=[5]),
            Transform(text[3][:2], new_text[5][:2]),
            Transform(text[3][2:], new_text[5][5:]),
            grow_between(new_text[5][2:5], text[3][1])
        )

        self.wait()

        self.remove(*text, *new_text, *lim_text, *new_lim_text, *text[3], *new_text[5])
        lim_text = MathTex("\\lim_{x\\to\\infty} \\Delta^m f(x", ") = 0").move_to(UP*2)
        text = MathTex("S(x) =", "\\lim_{n\\to\\infty}\\left( \\sum_{k=1}^{n-1}(f(k) - f(x+k)) + \\sum_{k=1}^m \\binom{x}k \\Delta^{k-1}f(n) \\right)")
        self.add(text, lim_text)

        text.save_state()
        lim_text.save_state()

        self.play(highlight_animation(lim_text, BLUE))
        
        description = Tex("This needs to actually converge").scale(0.8)
        arrow = MathTex("\\uparrow").move_to(description.get_top() + UP*0.2, DOWN)
        VGroup(description, arrow).move_to(text[1].get_bottom() + DOWN*0.2, UP)

        self.play(
            lim_text.animate.restore(),
            highlight_animation(text[1]),
            FadeIn(VGroup(description, arrow), shift=UP)
        )

        self.play(
            text.animate.restore().move_to(text),
            fade_and_shift_out(VGroup(description, arrow), DOWN)
        )


        example_1 = MathTex("\\frac{x^2-3x+2}{x^2+3}").set_color(BLUE).move_to(DOWN*2 + LEFT*3)
        example_2 = MathTex("\\ln(x)").set_color(BLUE).move_to(DOWN*2)
        examples_3 = VGroup(
            MathTex("\\sqrt{x}").set_color(BLUE).move_to(DOWN*1.6 + RIGHT*2.8),
            MathTex("x^\\pi").set_color(BLUE).move_to(DOWN*2.2 + RIGHT*3.7),
            MathTex("x^{\\sqrt2}").set_color(BLUE).move_to(DOWN*2.6 + RIGHT*2.6),
        )

        self.play(
            LaggedStart(
                fade_and_shift_in(example_1, UP),
                fade_and_shift_in(example_2, UP),
                fade_and_shift_in(examples_3, UP),
                lag_ratio=0.7
            )
        )

        self.play(
            fade_and_shift_out(VGroup(lim_text, text), UP),
            fade_and_shift_out(VGroup(example_1, example_2, examples_3), DOWN)
        )



def binomial_coefficient(n, k):
    total = 1
    for i in range(k):
        total *= (n - i) / (i + 1)
    return total



def forward_difference(f, x, n):
    total = 0
    for k in range(n + 1):
        total += (1 if k%2 == 0 else -1) * binomial_coefficient(n, k) * f(x + n - k)
    return total
        


def get_s(f, m, n):
    def s(x):
        floor_x = math.floor(x)

        total = 0
        if (x > 0):
            for k in range(1, floor_x + 1):
                total += f(k)
        else:
            for k in range(floor_x + 1, 1):
                total -= f(k)
        for k in range(1, n):
            total += f(k + floor_x) - f(x + k)
        for k in range(1, m + 1):
            total += binomial_coefficient(x - floor_x, k) * forward_difference(f, n + floor_x, k-1)
        return total
    return s


# Gauss Pi function (the Gamma function if it was good)
def pi(x, n = 100):
    total = 1
    for i in range(1, n-1):
        total *= i/(x + i)
    total *= n**x
    total *= ((n+1)/n)**(x*(x-1)/2)
    return total

# Zeta function for values > -2. Computed by eta function + 2 iterations of Euler summation
def zeta_positive(x, n = 100):
    total = 0
    sign = 1
    for i in range(1, n):
        total += sign / (i**x)
        sign *= -1
    total += 0.75 * sign / ((n+1)**x)
    total -= 0.25 * sign / ((n+2)**x)
    return total / (1 - 2**(1-x))

def zeta(x, n = 100):
    if x > 0: return zeta_positive(x, n)
    return zeta_positive(1 - x, n) * 2*pi(-x, n)/(TAU**(1-x)) * math.sin(PI * x/2)




class Graphs(Scene):
    def construct(self):
        u = create_updater_container(self)

        scale_vt = ValueTracker(1)
        graph_origin = Dot(LEFT*4 + DOWN*2.5, 0, 0, 0)

        def make_axes():
            return FullscreenAxes(self, graph_origin.get_center(), [scale_vt.get_value()]*2, 0.25 * math.sqrt(scale_vt.get_value()))
        
        axes = make_axes()

        def create_f_curve(function, left = None, right = None):
            if left is None: left = axes.point_to_coords(LEFT*7.12)[0]
            if right is None: right = axes.point_to_coords(RIGHT*7.12)[0]
            return ParametricFunction(lambda t: axes.coords_to_point(t, function(t)), [left, right], color=RED)
        
        def create_s_curve(function, left = None, right = None, t_step = 0.01):
            if left is None: left = axes.point_to_coords(LEFT*7.12)[0]
            if right is None: right = axes.point_to_coords(RIGHT*7.12)[0]
            return ParametricFunction(lambda t: axes.coords_to_point(t, function(t)), [left, right, t_step], color=YELLOW)

        def create_dots(function, num):
            dots = []
            total = 0
            for i in range(1, num):
                total += function(i)
                dot = Dot(axes.coords_to_point(i, total), max(0.08, 0.12 * scale_vt.get_value()), color=BLUE)
                dot.set_z_index(1)
                dots.append(dot)
            return dots



        self.play(
            create_axes(self, axes)
        )
        self.remove(axes)
        self.add(axes)

        u.add_updater(lambda _: axes.become(make_axes()))

        

        def f(x): return math.sqrt(x)

        text = MathTex("f(x) =", "\\sqrt x").move_to(RIGHT*3 + UP)
        dots = create_dots(f, 5)
        curve_f = create_f_curve(f, 0)
        curve_s = create_s_curve(get_s(f, 4, 100), -1, 4.5)

        self.play(
            Create(curve_f),
            Write(text),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.1
            )
        )
        self.play(Create(curve_s))


        new_text = MathTex("f(x) =", "\\frac1x").move_to(RIGHT*4)

        curve_f.reverse_direction()
        curve_s.reverse_direction()
        self.play(
            LaggedStart(
                AnimationGroup(
                    Uncreate(curve_f),
                    Uncreate(curve_s),
                    LaggedStart(
                        *[FadeOut(dot, scale=0, rate_func=cubic_in, run_time=0.5) for dot in dots],
                        lag_ratio = 0.2
                    ),
                    LaggedStart(
                        *[fade_and_shift_out(letter, RIGHT*0.5, run_time=0.5) for letter in reversed(text[1])]
                    )
                ),
                AnimationGroup(
                    graph_origin.animate.move_to(LEFT*2 + DOWN),
                    text[0].animate.move_to(new_text[0]),
                ),
                lag_ratio=0.5
            )
        )

        # ===========================================================
        

        def f(x): return 1/x if x != 0 else 0
        s = get_s(f, 4, 100)
        def s_adjusted(x): return min(5.5, max(-3.5, s(x)))
        dots = create_dots(f, 10)
        curve_f = VGroup(create_f_curve(f, right=-0.01), create_f_curve(f, 0.01))
        curve_s = VGroup(
            *[create_s_curve(s_adjusted, i+0.001, i+0.999) for i in range(-5, -1)],
            create_s_curve(s_adjusted, -1 + 0.01)
        )
        for curve in curve_s:
            curve.set_points(normalize_point_speed(curve.points))

        self.play(
            Create(curve_f),
            Write(new_text[1]),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.1
            )
        )
        self.play(
            LaggedStart(
                *[Create(curve) for curve in curve_s],
                lag_ratio = 0.1
            )
        )


        for curve in curve_f.submobjects + curve_s.submobjects:
            curve.reverse_direction()
        
        left_text = new_text[1]
        new_text = MathTex("f(x) =", "\\ln(|x|)").move_to(RIGHT*4.5 + DOWN*0.25)
        self.play(
            LaggedStart(
                AnimationGroup(
                    Uncreate(curve_f),
                    LaggedStart(
                        *[Uncreate(curve) for curve in curve_s],
                        lag_ratio = 0.1
                    ),
                    LaggedStart(
                        *[FadeOut(dot, scale=0, rate_func=cubic_in, run_time=0.5) for dot in dots],
                        lag_ratio = 0.2
                    ),
                    LaggedStart(
                        *[fade_and_shift_out(letter, RIGHT*0.5, run_time=0.5) for letter in reversed(left_text)]
                    )
                ),
                AnimationGroup(
                    graph_origin.animate.move_to(LEFT + DOWN),
                    text[0].animate.move_to(new_text[0]),
                ),
                lag_ratio = 0.5
            )
        )


        # ===========================================================

        def f(x): return math.log(abs(x)) if x != 0 else 0
        s = get_s(f, 4, 100)
        def s_adjusted(x): return min(5.5, max(-3.5, s(x)))
        dots = create_dots(f, 6)
        curve_f = VGroup(create_f_curve(f, right=-0.01), create_f_curve(f, 0.01))
        curve_s = VGroup(
            *[create_s_curve(s_adjusted, i+0.00001, i+0.99999) for i in range(-7, -1)],
            create_s_curve(s_adjusted, -1 + 0.001, 5.5)
        )
        for curve in curve_s:
            curve.set_points(normalize_point_speed(curve.points, 0.01))

        self.play(
            Create(curve_f),
            Write(new_text[1]),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.1
            )
        )
        self.play(
            LaggedStart(
                *[Create(curve) for curve in curve_s],
                lag_ratio = 0.1
            )
        )


        for curve in curve_f.submobjects + curve_s.submobjects:
            curve.reverse_direction()
        
        left_text = new_text[1]
        new_text = MathTex("f(x) =", "\\frac{\\sin(\\pi x)}{\\pi x}").move_to(RIGHT*3.5 + UP*1.5)
        self.play(
            LaggedStart(
                AnimationGroup(
                    Uncreate(curve_f),
                    LaggedStart(
                        *[Uncreate(curve) for curve in curve_s],
                        lag_ratio = 0.1
                    ),
                    LaggedStart(
                        *[FadeOut(dot, scale=0, rate_func=cubic_in, run_time=0.5) for dot in dots],
                        lag_ratio = 0.2
                    ),
                    LaggedStart(
                        *[fade_and_shift_out(letter, RIGHT*0.5, run_time=0.5) for letter in reversed(left_text)]
                    )
                ),
                AnimationGroup(
                    graph_origin.animate.move_to(ORIGIN),
                    text[0].animate.move_to(new_text[0]),
                    scale_vt.animate.set_value(1.2)
                ),
                lag_ratio = 0.7
            )
        )


        # ===========================================================

        def f(x): return math.sin(PI*x)/(PI*x) if x != 0 else 1
        dots = create_dots(f, 8)
        curve_f = create_f_curve(f)
        curve_s = create_s_curve(get_s(f, 0, 1000))

        self.play(
            Create(curve_f, rate_func=linear),
            Write(new_text[1]),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.1
            )
        )
        self.play(
            Create(curve_s, rate_func=linear)
        )


        curve_f.reverse_direction()
        curve_s.reverse_direction()
        
        left_text = new_text[1]
        new_text = MathTex("f(x) =", "\\sqrt x \\sin(\\sqrt x)").move_to(LEFT*0.5 + DOWN*0.5)
        self.play(
            LaggedStart(
                AnimationGroup(
                    LaggedStart(
                        Uncreate(curve_f, rate_func=linear, run_time=0.7),
                        Uncreate(curve_s, rate_func=linear, run_time=0.7),
                        lag_ratio = 0.2
                    ),
                    LaggedStart(
                        *[FadeOut(dot, scale=0, rate_func=cubic_in, run_time=0.5) for dot in dots],
                        lag_ratio = 0.2
                    ),
                    LaggedStart(
                        *[fade_and_shift_out(letter, RIGHT*0.5, run_time=0.5) for letter in reversed(left_text)]
                    )
                ),
                AnimationGroup(
                    graph_origin.animate.move_to(LEFT*4.5 + DOWN*2),
                    scale_vt.animate.set_value(0.45),
                    text[0].animate.move_to(new_text[0]),
                ),
                lag_ratio = 0.8
            )
        )



        # ===========================================================

        def f(x):
            if (x >= 0): return math.sqrt(x) * math.sin(math.sqrt(x))
            return -math.sqrt(-x) * math.sinh(math.sqrt(-x))
        
        dots = create_dots(f, 18)
        curve_f = create_f_curve(f)
        curve_s = create_s_curve(get_s(f, 4, 100), right=19)

        self.play(
            Create(curve_f, rate_func=linear),
            Write(new_text[1]),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.05
            )
        )
        self.play(
            Create(curve_s, rate_func=linear)
        )


        curve_f.reverse_direction()
        curve_s.reverse_direction()
        
        left_text = new_text[1]
        new_text = MathTex("f(x) =", "\\zeta(x + 1)").move_to(RIGHT*4 + DOWN*0.5)
        self.play(
            LaggedStart(
                AnimationGroup(
                    LaggedStart(
                        Uncreate(curve_f, rate_func=linear),
                        Uncreate(curve_s, rate_func=linear),
                        lag_ratio = 0.25
                    ),
                    LaggedStart(
                        *[FadeOut(dot, scale=0, rate_func=cubic_in, run_time=0.5) for dot in dots],
                        lag_ratio = 0.075
                    ),
                    LaggedStart(
                        *[fade_and_shift_out(letter, RIGHT*0.5, run_time=0.5) for letter in reversed(left_text)]
                    )
                ),
                AnimationGroup(
                    graph_origin.animate.move_to(LEFT*2 + DOWN*2.5),
                    scale_vt.animate.set_value(0.7),
                    text[0].animate.move_to(new_text[0]),
                ),
                lag_ratio = 0.7
            )
        )

        # ===========================

        def f(x): return 0 if x == 0 or x == -1 else zeta(x + 1, 25)

        s = get_s(f, 4, 25)
        def s_adjusted(x): return min(9.5, max(-2.5, s(x)))
        dots = create_dots(f, 9)
        curve_f = VGroup(create_f_curve(f, right=-0.01), create_f_curve(f, 0.01))
        curve_s = VGroup(
            *[create_s_curve(s_adjusted, i+0.001, i+0.999) for i in range(-7, -1)],
            create_s_curve(s_adjusted, -1 + 0.01, 8.5)
        )
        for curve in curve_s:
            curve.set_points(normalize_point_speed(curve.points))

        self.play(
            Create(curve_f),
            Write(new_text[1]),
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.1
            )
        )
        self.play(
            LaggedStart(
                *[Create(curve) for curve in curve_s],
                lag_ratio = 0.1
            )
        )


        self.remove(*text, *new_text)
        text = new_text
        self.add(text)

        new_text = MathTex("f(x) =", "\\sum_{k=1}^x", "\\zeta(k + 1)").move_to(text)

        for curve in curve_f.submobjects:
            curve.reverse_direction()
        
        self.play(
            Uncreate(curve_f),
            morph_text(text, new_text, [0, 2]),
            curve_s.animate.set_color(RED),
            LaggedStart(
                *[FadeOut(dot, scale=0, rate_func=cubic_in, run_time=0.5) for dot in dots],
                lag_ratio = 0.2
            )
        )




        f = s
        dots = create_dots(f, 4)
        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=3, rate_func=bounce()) for dot in dots],
                lag_ratio= 0.1
            )
        )

        # Insanely inefficient, but it does the job
        s = get_s(f, 4, 25)
        def s_adjusted(x):
            print(x)
            return min(10, max(-2.5, s(x)))
        curve_f = curve_s
        curve_s = VGroup(
            *[create_s_curve(s_adjusted, i+0.001, i+0.999, 0.025) for i in range(-7, -2)],
            create_s_curve(s_adjusted, -2 + 0.01, 3.5, 0.05)
        )

        for curve in curve_s:
            curve.set_points(normalize_point_speed(curve.points, 0.05))

        self.play(
            LaggedStart(
                *[Create(curve) for curve in curve_s],
                lag_ratio = 0.1
            )
        )


        # self.remove(*text, new_text)
        # self.add(new_text)

        # for curve in curve_s + curve_f:
        #     curve.reverse_direction()
        # new_text.submobjects.reverse()
        # for t in new_text.submobjects:
        #     t.submobjects.reverse()
        #     for tt in t.submobjects:
        #         t.reverse_direction()


        # self.play(
        #     LaggedStart(
        #         *[Uncreate(curve) for curve in curve_f],
        #         lag_ratio = 0.1
        #     ),
        #     LaggedStart(
        #         *[Uncreate(curve) for curve in curve_s],
        #         lag_ratio = 0.1
        #     ),
        #     LaggedStart(
        #         *[FadeOut(dot, scale=0) for dot in dots],
        #         lag_ratio=0.2
        #     ),
        #     Unwrite(new_text, run_time = 1.5)
        # )