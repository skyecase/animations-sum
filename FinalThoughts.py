import math
from manim import *

from modules.custom_mobjects import FullscreenAxes, create_axes
from modules.helpers import fade_and_shift_in, fade_and_shift_out, grow_between, highlight_animation, morph_text


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

        
        counterexample = Tex("It doesn't converge for $\\displaystyle f(x) = \\frac{\\sin(2\\pi x)}{2\\pi x}$.").scale(0.8).move_to(DOWN*2).set_color(RED)

        self.play(
            FadeIn(counterexample, shift=UP),
            VGroup(text, arrow, description).animate.shift(UP),
            lim_text.animate.shift(UP*0.5)
        )

        self.play(
            text.animate.restore().move_to(text),
            fade_and_shift_out(VGroup(description, arrow, counterexample), DOWN)
        )


        example_1 = MathTex("\\frac{x^2-3x+2}{x^2+3}").set_color(BLUE).move_to(DOWN*2 + LEFT*3)
        example_2 = MathTex("\\ln(x)").set_color(BLUE).move_to(DOWN*2)
        example_3 = MathTex("\\sqrt{x}").set_color(BLUE).move_to(DOWN*2 + RIGHT*3)

        self.play(
            LaggedStart(
                fade_and_shift_in(example_1, UP),
                fade_and_shift_in(example_2, UP),
                fade_and_shift_in(example_3, UP),
                lag_ratio=0.7
            )
        )

        self.play(
            fade_and_shift_out(VGroup(lim_text, text), UP),
            fade_and_shift_out(VGroup(example_1, example_2, example_3), DOWN)
        )



def binomial_coefficient(n, k):
    total = 1
    for i in range(k):
        total *= (n - i) / (i + 1)
    return total



def forward_difference(f, x, n):
    """
    f: function
    x: input value
    n: order
    """
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



class Graphs(Scene):
    def construct(self):


        def f(x):
            if (x >= 0): return math.sqrt(x) * math.sin(math.sqrt(x))
            return -math.sqrt(-x) * math.sinh(math.sqrt(-x))
        
        axes = FullscreenAxes(self, LEFT*3 + DOWN*2, [0.7, 0.7])

        def create_curve(function):
            left = axes.point_to_coords(LEFT*7.12)[0]
            right = axes.point_to_coords(RIGHT*7.12)[0]
            return ParametricFunction(lambda t: axes.coords_to_point(t, function(t)), [left, right])


        curve = create_curve(f)

        self.play(
            create_axes(self, axes)
        )

        self.play(Create(curve))

        curve_2 = create_curve(get_s(f, 4, 100))

        self.play(Create(curve_2))