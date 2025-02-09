from manim import *
from modules.custom_mobjects import CustomArrow, DottedLine, FullscreenAxes, create_arrow, create_axes
from modules.interpolation import cubic_out
from modules.helpers import CustomLaggedStart, create_updater_container, fade_and_shift_in, fade_and_shift_out, morph_text
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
        u = create_updater_container(self)

        X_START = 2.5
        X_COLOR = RED
        N_COLOR = GREEN

        rect = Rectangle(height=3.5, width=self.camera.frame_width).move_to(UP * self.camera.frame_height/2, UP)

        axes = FullscreenAxes(self, UP*1 + LEFT*6, [1/2, 1/2], 0.15, stroke_width=3, rect=rect)
        axes.y_line.set_cap_style(CapStyleType.SQUARE)

        dots = [Dot(axes.coords_to_point(i, s(i)), color=BLUE) for i in range(-2, 27)]
        for dot in dots: dot.set_z_index(2)

        n_text = MathTex("n").move_to(axes.coords_to_point(21, 0) + DOWN * 0.35, UP).set_color(N_COLOR)
        n_line = DottedLine(n_text.get_top() + UP*0.1, axes.coords_to_point(21, 6), stroke_width=3).set_color(N_COLOR)

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


        x_text = MathTex("x").move_to(axes.coords_to_point(X_START, 0) + DOWN * 0.35, UP).set_color(X_COLOR)
        x_line = DottedLine(x_text.get_top() + UP*0.1, axes.coords_to_point(X_START, 6), stroke_width=3).set_color(X_COLOR)

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
            Write(text_1[1], run_time = 1),
            n_dot.animate.scale(1.5),
            s_n_arrow.end_vt.animate.set_value(1),
            fade_and_shift_in(s_n_text, (DOWN+RIGHT)/2, run_time=0.75)
        )


        arrow = CustomArrow(n_dot.get_center(), axes.coords_to_point(21 + X_START, s(21 + X_START)), PI*3/4, stroke_width=3)
        self.add(arrow)

        npx_dot = Dot(axes.coords_to_point(21 + X_START, s(21 + X_START)), color=X_COLOR).scale(1.5)
        npx_dot.set_z_index(2)
        npx_dot.save_state()
        npx_dot.scale(0)

        text_2 = Tex("\\textbf{Step 2:} ", "Move forward $x$ units.").move_to(DOWN*1.75 + LEFT * 5, LEFT)

        self.play(fade_and_shift_in(text_2[0], LEFT * 0.5, run_time=0.5))
        self.play(
            n_dot.animate(rate_func=bounce()).scale(1/1.5),
            Write(text_2[1], run_time = 1),
            arrow.end_vt.animate(rate_func=cubic_out).set_value(1),
            npx_dot.animate.restore()
        )

        npx_text = MathTex("n + x").move_to(axes.coords_to_point(21 + X_START, 0) + DOWN * 0.75, UP).set_color(X_COLOR)
        npx_line = DottedLine(npx_text.get_top() + UP*0.1, axes.coords_to_point(21 + X_START, 6), stroke_width=3).set_color(X_COLOR)

        self.play(
            LaggedStart(
                fade_and_shift_in(npx_text, UP),
                Create(npx_line, rate_func=cubic_out),
                lag_ratio=0.3
            ),
        )

        text_3 = Tex("\\textbf{Step 3:} ", "Step backward $n$ units.").move_to(DOWN*3 + LEFT*5, LEFT)

        self.play(fade_and_shift_in(text_3[0], LEFT * 0.5, run_time=0.5))



        arrows = [CustomArrow(axes.coords_to_point(i+X_START+1, s(i+X_START+1)), axes.coords_to_point(i+X_START, s(i+X_START)), PI*3/4, buff=0.07, tip_size=0.125, stroke_width=3) for i in range(0, 21)]
        for a in arrows:
            a.set_z_index(2)
            self.add(a)

        offset_dots = [Dot(axes.coords_to_point(i+X_START, s(i+X_START)), 0.06, color=X_COLOR) for i in range(0, 21)]
        offset_dots[0] = npx_dot.copy().move_to(offset_dots[0])
        for dot in offset_dots:
            dot.set_z_index(2)
            dot.save_state()
            dot.scale(0)

        self.play(
            Write(text_3[1], run_time = 1),
            LaggedStart(
                *[
                    LaggedStart(
                        arrows[i].end_vt.animate(rate_func=cubic_out, run_time=0.5).set_value(1),
                        offset_dots[i].animate(rate_func=cubic_out, run_time=0.5).restore(),
                        lag_ratio = 0.25
                    ) for i in reversed(range(0, 21))
                ],
                lag_ratio = 1/X_START
            )
        )


        for a in arrows + [arrow]: a.remove_arrow_updater()

        x_vt = ValueTracker(X_START)

        def updater(_):
            x = x_vt.get_value()

            arrow.become(create_arrow(n_dot.get_center(), axes.coords_to_point(21 + x, s(21 + x)), 0, 1, angle=PI*3/4, stroke_width=3))
            for i in range(0, len(arrows)):
                arrows[i].become(create_arrow(axes.coords_to_point(i+x+1, s(i+x+1)), axes.coords_to_point(i+x, s(i+x)), 0, 1, 0.07, PI*3/4, tip_size=0.125, stroke_width=3))

            npx_dot.become(Dot(axes.coords_to_point(21 + x, s(21 + x)), color=X_COLOR).scale(1.5))
            for i in range(0, len(offset_dots)):
                offset_dots[i].become(Dot(axes.coords_to_point(i+x, s(i+x)), 0.06, color=X_COLOR))
            offset_dots[0].become(npx_dot.copy().move_to(offset_dots[0]))

            x_text.become(MathTex("x").move_to(axes.coords_to_point(x, 0) + DOWN * 0.35, UP).set_color(X_COLOR))
            x_line.become(DottedLine(x_text.get_top() + UP*0.1, axes.coords_to_point(x, 6), stroke_width=3).set_color(X_COLOR))

            npx_text.become(MathTex("n + x").move_to(axes.coords_to_point(21 + x, 0) + DOWN * 0.75, UP).set_color(X_COLOR))
            npx_line.become(DottedLine(npx_text.get_top() + UP*0.1, axes.coords_to_point(21 + x, 6), stroke_width=3).set_color(X_COLOR))
        u.add_updater(updater)

        self.play(x_vt.animate.set_value(0.8), run_time = 3)
        self.play(x_vt.animate.set_value(PI), run_time = 3)

        u.remove_updater(updater)



        def updater(_):
            x = x_vt.get_value()

            arrow.become(create_arrow(n_dot.get_center(), axes.coords_to_point(21 + x, s(21 + x)), arrow.start_vt.get_value(), 1, angle=PI*3/4, stroke_width=3))
            for i in range(0, len(arrows)):
                arrows[i].become(create_arrow(axes.coords_to_point(i+x+1, s(i+x+1)), axes.coords_to_point(i+x, s(i+x)), arrows[i].start_vt.get_value(), 1, 0.07, PI*3/4, tip_size=0.125, stroke_width=3))
        u.add_updater(updater)

        self.play(
            LaggedStart(
                AnimationGroup(
                    LaggedStart(
                        *[a.start_vt.animate(rate_func=cubic_out).set_value(1) for a in reversed(arrows + [arrow])]
                    ),
                    LaggedStart(
                        *[d.animate.scale(0) for d in reversed(offset_dots + [npx_dot])]
                    )
                ),
                curve.animate.set_stroke(width=7),
                lag_ratio=0.7
            )
        )

        u.remove_updater(updater)

        curve.reverse_points()

        self.play(Uncreate(curve), rate_func=cubic_out)





        self.play(
            VGroup(x_text, x_line).animate(rate_func=bounce()).shift((axes.coords_to_point(4, 0) - x_line.get_center()) * RIGHT),
            npx_line.animate(rate_func=bounce()).shift((axes.coords_to_point(21+4, 0) - npx_line.get_center()) * RIGHT),
            npx_text.animate(rate_func=bounce()).shift((axes.coords_to_point(21+4, 0) - npx_line.get_center())/2 * RIGHT),
            dots[23].animate.scale(1.5)
        )


        STEP_X_START = text_1.get_left()


        text_2.save_state()
        text_3.save_state()

        self.play(
            # text_1.animate.shift(RIGHT * (STEP_X_START - text_1.get_left())),
            text_2.animate.scale(0.8).move_to(STEP_X_START*RIGHT + DOWN*2, LEFT).set_color(GRAY),
            text_3.animate.scale(0.8).move_to(STEP_X_START*RIGHT + DOWN*3, LEFT).set_color(GRAY),
        )

        sum_1 = MathTex("\\sum_{k=1}^n f(k)").move_to(text_1.get_center()*UP + 3*RIGHT)

        self.play(Write(sum_1))


        self.play(
            VGroup(text_1, sum_1).animate.scale(0.8).move_to(STEP_X_START*RIGHT + text_1.get_center()*UP + 0.5*UP, LEFT).set_color(GRAY),
            text_2.animate.restore().shift(UP * 0.75)
        )



        forward_arrows = [
            CustomArrow(axes.coords_to_point(21+i, s(21+i)), axes.coords_to_point(21+1+i, s(21+1+i)), PI*3/4, buff=0.07, tip_size=0.125, stroke_width=3)
            for i in range(0, 4)
        ]
        forward_arrows[0].set_text(MathTex("+\,f(n+1)").scale(0.5).move_to(UP*0.2, DOWN))
        forward_arrows[1].set_text(MathTex("+\,f(n+2)").scale(0.5).move_to(UP*0.2, DOWN))
        forward_arrows[2].set_text(MathTex("+\,\cdots").scale(0.5).move_to(UP*0.2, DOWN))
        forward_arrows[3].set_text(MathTex("+\,f(n+x)").scale(0.5).move_to(UP*0.2, DOWN))
        for a in forward_arrows: self.add(a)

        sub_text = MathTex("+", "\,f(n+1)", "+", "f(n+2)", "+", "\\cdots", "+", "f(n+x)").move_to(text_2.get_center()*UP + DOWN).scale(0.8)


        arrow_dot_animations = [a.animation for a in forward_arrows]
        arrow_dot_animations[-1] = AnimationGroup(dots[27].animate.scale(1.5), arrow_dot_animations[-1])

        self.play(
            dots[23].animate.scale(1/1.5),
            LaggedStart(
                *arrow_dot_animations,
                lag_ratio = 0.5,
            ),
            LaggedStart(
                *[fade_and_shift_in(t, LEFT) for t in sub_text[:5]],
                *[fade_and_shift_in(t, LEFT) for t in sub_text[5]],
                *[fade_and_shift_in(t, LEFT) for t in sub_text[6:]],
                lag_ratio = 0.25
            )
        )

        self.remove(*forward_arrows)

        self.remove(*sub_text, *sub_text[5])
        sub_text = MathTex("+ \,f(n+1) + f(n+2) + \\cdots + f(n+x)").move_to(text_2.get_center()*UP + DOWN).scale(0.8)
        new_sub_text = MathTex("+ \,f(n+1) + f(n+2) + \\cdots + f(n+x)", "\ =\ +\,\\sum_{k=1}^x f(n+k)").move_to(text_2.get_center()*UP + DOWN).scale(0.8)

        self.play(
            sub_text[0].animate.become(new_sub_text[0]),
            FadeIn(new_sub_text[1], shift=LEFT*2)
        )

        self.remove(*sub_text, *new_sub_text)
        sub_text = MathTex("+ \,f(n+1) + f(n+2) + \\cdots + f(n+x)\ =\ ", "+\,\\sum_{k=1}^x f(n+k)").move_to(text_2.get_center()*UP + DOWN).scale(0.8)
        self.add(sub_text)


        self.play(
            fade_and_shift_out(sub_text[0], LEFT),
            sub_text[1].animate.shift(UP * (text_2.get_center() - sub_text[1].get_center()))
        )

        self.play(
            text_2.animate.scale(0.8).move_to(STEP_X_START*RIGHT + DOWN, LEFT).set_color(GRAY),
            sub_text[1].animate.set_color(GRAY).shift(LEFT),
            text_3.animate.restore().shift(UP)
        )



        backward_arrows = [
            CustomArrow(axes.coords_to_point(4+1+i, s(4+1+i)), axes.coords_to_point(4+i, s(4+i)), PI*3/4, buff=0.07, tip_size=0.125, stroke_width=3)
            for i in range(0, 21)
        ]
        backward_arrows[20].set_text(MathTex("-\,f(x+n)").scale(0.5).move_to(DOWN * 0.1, UP))
        backward_arrows[19].set_text(MathTex("-\,f(x+n-1)").scale(0.3).move_to(DOWN * 0.1, UP))
        backward_arrows[18].set_text(MathTex("-\,f(x+n-2)").scale(0.15).move_to(DOWN * 0.1, UP))
        backward_arrows[0].set_text(MathTex("-\,f(x+1)").scale(0.5).move_to(DOWN * 0.1, UP))
        backward_arrows[1].set_text(MathTex("-\,f(x+2)").scale(0.5).move_to(DOWN * 0.1, UP))
        backward_arrows[2].set_text(MathTex("-\,f(x+3)").scale(0.3).move_to(DOWN * 0.1, UP))
        backward_arrows[3].set_text(MathTex("-\,f(x+4)").scale(0.15).move_to(DOWN * 0.1, UP))
        self.add(*backward_arrows)


        sub_text = MathTex("-\,", "f(x+n)", "-", "\\cdots", "-", "f(x+2)", "-", "f(x+1)").scale(0.8).move_to(DOWN * 3)

        def custom_lag_ratio(i, total):
            dist_from_end = min(i, total - i - 1)
            START_SLOWING_AFTER = 1
            STOP_SLOWING_AFTER = 6
            if dist_from_end <= START_SLOWING_AFTER: return 0.4
            if dist_from_end >= STOP_SLOWING_AFTER: return 0.1
            x = (dist_from_end - START_SLOWING_AFTER)/(STOP_SLOWING_AFTER-START_SLOWING_AFTER)

            return x*0.1 + (1-x)*0.4


        animations = [a.create_animation() for a in reversed(backward_arrows)]
        animations[-1] = AnimationGroup(
            animations[-1],
            dots[6].animate.scale(1.5)
        )

        self.play(
            dots[27].animate.scale(1/1.5),
            CustomLaggedStart(
                *animations,
                lag_ratio_function=custom_lag_ratio 
            ),
            LaggedStart(
                *[fade_and_shift_in(t, LEFT) for t in sub_text[:3]],
                *[fade_and_shift_in(t, LEFT) for t in sub_text[3]],
                *[fade_and_shift_in(t, LEFT) for t in sub_text[4:]],
                lag_ratio = 0.7
            )
        )




class Equation(Scene):
    def construct(self):
        text = MathTex("S(x) = \\sum_{k=1}^n f(k)", "+ \\sum_{k=1}^x f(n + k)", "- \\sum_{k=1}^n f(x + k)")
        new_text = MathTex("S(x) = \\sum_{k=1}^n f(k)", "- \\sum_{k=1}^n f(x + k)", "+ \\sum_{k=1}^x f(n + k)")
        self.add(text)
        self.play(morph_text(text, new_text, [0, 2, 1], path_arc=PI*3/4))        
        self.remove(*text, *new_text)

        text = MathTex("S(x) = \\sum_{k=1}^n", "f(k) -", "\\sum_{k=1}^n", "f(x + k)", "+ \\sum_{k=1}^x f(n + k)")
        new_text = MathTex("S(x) = \\sum_{k=1}^n", "(", "f(k) -", "f(x + k)", ")", "+ \\sum_{k=1}^x f(n + k)")
        self.add(text)
        self.play(morph_text(text, new_text, [0, 2, None, 3, 5]))
        self.remove(*text, *new_text)

        text = MathTex("S(x) =", "\\sum_{k=1}^n (f(k) - f(x + k)) + \\sum_{k=1}^x f(n + k)")
        new_text = MathTex("S(x) =", "\\lim_{n \\to \\infty} \\left(", "\\sum_{k=1}^n (f(k) - f(x + k)) + \\sum_{k=1}^x f(n + k)", "\\right)")
        self.add(text)
        self.play(morph_text(text, new_text, [0, 2]))
        self.remove(*text, *new_text)

        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left(", "\\sum_{k=1}^n (f(k) - f(x + k))", "+", "\\sum_{k=1}^x f(n + k)", "\\right)", stroke_width=0)
        text.set()
        self.add(text)

        text.save_state()

        text[1].save_state()

        self.play(
            *[obj.animate.set_stroke(width=1.5).scale(1.1) for obj in text[1]],
            VGroup(text[:1], text[2:]).animate.set_color(GRAY)
        )

        self.play(text[1][0].animate.scale(1.2).set_color(GREEN))

        self.play(
            text[1].animate.restore().set_color(GRAY),
            *[obj.animate.set_stroke(width=1.5).scale(1.1).set_color(WHITE) for obj in text[3]]
        )

        self.play(text[3][0].animate.scale(1.2).set_color(RED))
        self.play(text[3][7].animate.scale(1.2).set_color(GREEN))

        self.play(text.animate.restore())
