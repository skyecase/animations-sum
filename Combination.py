from manim import *
from modules.helpers import create_time_getter, create_updater_container, fade_and_shift_in, fade_and_shift_out, highlight_animation, morph_text, shrink_between
from modules.interpolation import bounce, cubic_out, pow_out, sin_smooth_in_out, cubic_in
import random


def pow_out(pow):
    return lambda x: 1 - (1 - min(1, max(0, x)))**pow


class BinomialCoefficientDerivation(Scene):
    def construct(self):
        u = create_updater_container(self)

        V_OFFSET = 1.75

        text = MathTex("\\sum_{k_1=2}^{x-1}", "\\sum_{k_2=1}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1").scale(1.2).move_to(UP * V_OFFSET)

        self.add(text)


        N = 10

        dots = VGroup(*[Dot(RIGHT * i, 0.12) for i in range(N)]).move_to(DOWN * 1.5)
        labels = [MathTex(i).move_to(dot.get_center() + 0.5 * UP, DOWN) for (i, dot) in enumerate(dots)]

        self.play(
            LaggedStart(
                *[FadeIn(VGroup(dots[i], labels[i]), scale=0.5, shift = UP, rate_func = pow_out(3)) for i in range(len(dots))]
            )
        )


        state = [2, 1, 0]

        def get_points_for_state():
            dot_1 = Dot(dots[state[0]].get_center(), 0.2, color=RED)
            label_1 = MathTex("k_1").move_to(dot_1.get_center() + 0.5 * DOWN, UP).set_color(RED)
            dot_2 = Dot(dots[state[1]].get_center(), 0.2, color=GREEN)
            label_2 = MathTex("k_2").move_to(dot_2.get_center() + 0.5 * DOWN, UP).set_color(GREEN)
            dot_3 = Dot(dots[state[2]].get_center(), 0.2, color=BLUE)
            label_3 = MathTex("k_3").move_to(dot_3.get_center() + 0.5 * DOWN, UP).set_color(BLUE)
            return VGroup(dot_1, label_1, dot_2, label_2, dot_3, label_3)


        iterations = 1
        def iterate_state():
            nonlocal iterations
            iterations += 1
            if state[2] < state[1] - 1:
                state[2] += 1
            elif state[1] < state[0] - 1:
                state[2] = 0
                state[1] += 1
            else:
                state[2] = 0
                state[1] = 1
                state[0] += 1


        points = get_points_for_state()

        text[0].save_state()

        self.play(
            highlight_animation(text[0], RED, rate_func=cubic_out),
            text[1:].animate.set_color(GRAY),
            FadeIn(points[0], scale=3, rate_func = bounce()),
            FadeIn(points[1], scale=0)
        )


        for _ in range(3, 8):
            self.play(points[0:2].animate.shift(RIGHT), rate_func=pow_out(10))

        while state[0] < 7: iterate_state()

        text[1].save_state()

        self.play(
            text[0].animate(rate_func=cubic_out).restore().set_color(RED),
            highlight_animation(text[1], GREEN, rate_func=cubic_out),
            FadeIn(points[2], scale=3, rate_func = bounce()),
            FadeIn(points[3], scale=0)
        )


        for _ in range(2, 7):
            self.play(points[2:4].animate.shift(RIGHT), rate_func=pow_out(7.5), run_time=0.75)

        while state[0] < 8: iterate_state()

        self.play(
            points[0:2].animate.shift(RIGHT),
            points[2:4].animate.shift(dots[1].get_center() - points[2].get_center()),
            rate_func=pow_out(10)
        )

        for _ in range(2, 6):
            self.play(points[2:4].animate.shift(RIGHT), rate_func=pow_out(7.5), run_time=0.75)


        while state[0] < 8: iterate_state()
        while state[1] < 5: iterate_state()


        text[2].save_state()
        self.play(
            text[1].animate(rate_func=cubic_out).restore().set_color(GREEN),
            highlight_animation(text[2], BLUE, rate_func=cubic_out),
            FadeIn(points[4], scale=3, rate_func = bounce()),
            FadeIn(points[5], scale=0)
        )


        for _ in range(4):
            self.play(points[4:6].animate.shift(RIGHT), rate_func=pow_out(5), run_time=0.5)
        
        self.play(
            points[2:4].animate.shift(RIGHT),
            points[4:6].animate.shift(dots[0].get_center() - points[4].get_center()),
            rate_func=pow_out(10)
        )

        for _ in range(2):
            self.play(points[4:6].animate.shift(RIGHT), rate_func=pow_out(5), run_time=0.5)

        while state[1] < 6: iterate_state()
        while state[2] < 2: iterate_state()
        

        text[3].save_state()
        self.play(
            text[2].animate(rate_func=cubic_out).restore().set_color(BLUE),
            highlight_animation(text[3], WHITE, rate_func=cubic_out),
        )


        # These are used to align the running total
        three_digit_invisible = MathTex("000", ".").scale(1.5)
        two_digit_invisible = MathTex("00", ".").scale(1.5)
        one_digit_invisible = MathTex("0", ".").scale(1.5)
        three_digit_invisible.move_to(RIGHT*3 + UP*V_OFFSET - three_digit_invisible[0].get_center())
        two_digit_invisible.move_to(RIGHT*3 + UP*V_OFFSET - two_digit_invisible[0].get_center())
        one_digit_invisible.move_to(RIGHT*3 + UP*V_OFFSET - one_digit_invisible[0].get_center())

        running_total = MathTex(iterations, ".").scale(1.5)
        running_total.move_to(two_digit_invisible[1].get_center() - running_total[1].get_center())
        running_total_title = Tex("Total").move_to(three_digit_invisible[0].get_bottom() + DOWN * 0.2, UP)


        self.play(
            text.animate.shift(LEFT * 1.5),
            FadeIn(running_total[0], shift = LEFT*1.5),
            FadeIn(running_total_title, shift = LEFT*1.5)
        )


        iterate_state()

        running_total.become(MathTex(iterations, ".").scale(1.5))
        running_total.move_to(two_digit_invisible[1].get_center() - running_total[1].get_center())



        get_time = create_time_getter(self)

        # Holds tuples of (start_time, offset_pos, mobj), 
        plus_one_pool = []

        # Increments the running total and handles the +1s
        def running_total_updater(_):
            nonlocal plus_one_pool
            time = get_time()
            running_total.become(MathTex(iterations, ".").scale(1.5))

            decimal_center = one_digit_invisible[1].get_center()
            if iterations >= 10 and iterations < 100: decimal_center = two_digit_invisible[1].get_center()
            if iterations >= 100: decimal_center = three_digit_invisible[1].get_center()
            running_total.move_to(decimal_center - running_total[1].get_center())

            FADE_TIME = 1

            oldest_living_plus_one_index = -1
            for i in range(len(plus_one_pool)):
                if plus_one_pool[i][0] < time - FADE_TIME:
                    oldest_living_plus_one_index = i
                    self.remove(plus_one_pool[oldest_living_plus_one_index][2])
                else:
                    break
            if oldest_living_plus_one_index != -1:
                plus_one_pool = plus_one_pool[oldest_living_plus_one_index:]
            
            for (start_time, offset_pos, mobj) in plus_one_pool:
                alpha = (time - start_time) / FADE_TIME
                mobj.become(MathTex("+1").scale(0.75).move_to(one_digit_invisible[0].get_top() + UP*0.3 + offset_pos).set_fill(opacity = 1-alpha))
                mobj.scale(0.5 + 0.75*(alpha**0.5))
                mobj.shift(RIGHT*alpha*offset_pos[0] + 1.5*UP*alpha*(1+alpha)/2)
        u.add_updater(running_total_updater)


        plus_one_pool.append((
            get_time(),
            0.5*RIGHT*(random.random()-0.5),
            MathTex("+1")
        ))
        self.add(plus_one_pool[-1][2])
        self.play(points[4:6].animate(rate_func=pow_out(5), run_time=0.5).shift(RIGHT))
        self.wait(0.5)

        plus_one_pool.append((
            get_time(),
            0.5*RIGHT*(random.random()-0.5),
            MathTex("+1")
        ))
        self.add(plus_one_pool[-1][2])
        iterate_state()
        self.play(points[4:6].animate(rate_func=pow_out(5), run_time=0.5).shift(RIGHT))

        self.wait(0.5)


        iterations_vt = ValueTracker(iterations)

        self.remove(*points)
        self.add(points)

        random.seed(1234)

        # Sets the points and adds +1s to the pool
        def pool_and_point_updater(_):
            nonlocal plus_one_pool
            time = get_time()
            while iterations <= iterations_vt.get_value() - 1:
                iterate_state()
                new_plus_one = MathTex("+1").scale(0.75)
                self.add(new_plus_one)
                plus_one_pool.append((
                    time,
                    0.5*RIGHT*(random.random()-0.5),
                    new_plus_one
                ))
            points.become(get_points_for_state())
        u.add_updater_before(pool_and_point_updater, running_total_updater)

        iterations_vt.increment_value(0.999)

        self.play(iterations_vt.animate.set_value(120), run_time = 5, rate_func=sin_smooth_in_out(0.5))

        self.wait()


        u.remove_updater_index(0)
        u.remove_updater_index(0)

        new_running_total = MathTex("1", ".").scale(1.5)
        new_running_total.shift(one_digit_invisible[1].get_center() - new_running_total[1].get_center())

        iterations_vt.set_value(0.999)
        iterations = 1
        state = [2, 1, 0]
        self.play(
            text[3].animate.restore().move_to(text[3]).set_color(WHITE),
            running_total[0][0].animate.become(new_running_total[0][0]),
            shrink_between(running_total[0][1:], new_running_total[0][0]),
            points.animate(path_arc=-1).become(get_points_for_state())
        )

        self.remove(*running_total[0])
        running_total = new_running_total
        self.add(running_total[0])

        u.add_updater(pool_and_point_updater)
        u.add_updater(running_total_updater)

        self.play(iterations_vt.animate.set_value(120), rate_func=sin_smooth_in_out(0.8), run_time = 10)

        self.wait()



        # ==================================
        # CHOICES
        # ==================================

        u.remove_updater_index(0)
        u.remove_updater_index(0)

        new_running_total = MathTex("1", ".").scale(1.5)
        new_running_total.shift(one_digit_invisible[1].get_center() - new_running_total[1].get_center())

        iterations_vt.set_value(0.999)
        iterations = 1
        state = [2, 1, 0]
        self.play(
            running_total[0][0].animate.become(new_running_total[0][0]),
            shrink_between(running_total[0][1:], new_running_total[0][0]),
            points.animate(path_arc=-1).become(get_points_for_state())
        )

        self.remove(*running_total[0])
        running_total = new_running_total
        self.add(running_total[0])

        iterations_vt.set_value(0.999)
        iterations = 1
        state = [2, 1, 0]


        choices = [7, 5, 2]
        choice_dots = VGroup(*[Circle(0.3, YELLOW).move_to(dots[choice].get_center()) for choice in choices])
        
        self.play(*[FadeIn(dot, scale=2) for dot in choice_dots])

        u.add_updater(pool_and_point_updater)
        u.add_updater(running_total_updater)


        self.play(iterations_vt.animate.set_value(36), rate_func=linear, run_time = 5)
        self.wait()

        iterations_vt.increment_value(0.999)
        self.play(iterations_vt.animate.set_value(46), rate_func=linear, run_time = 3)
        self.wait()

        iterations_vt.increment_value(0.999)
        self.play(iterations_vt.animate.set_value(48), rate_func=linear, run_time = 0.75)
        self.wait()

        iterations_vt.increment_value(0.999)
        self.play(iterations_vt.animate.set_value(120), rate_func=sin_smooth_in_out(0.8), run_time = 8)
        self.wait()


        u.remove_updater_index(0)
        u.remove_updater_index(0)


        new_text = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1", "=").scale(1.2)
        description = Tex("The number of possible ways\\\\to pick $3$ out of $x$ items").move_to((new_text[4].get_right() + 0.25)*RIGHT, LEFT)
        VGroup(new_text, description).move_to(ORIGIN)

        self.play(
            VGroup(dots, points, *labels, choice_dots).animate(remover=True).shift(DOWN*2).set_color(BLACK),
            FadeOut(VGroup(running_total, running_total_title), shift=UP),
            LaggedStart(
                Transform(text, new_text[:4]),
                Write(VGroup(new_text[4], description)),
                lag_ratio=0.7
            )
        )



class Notation(Scene):
    def construct(self):
        text = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1", "=").scale(1.2)
        description = Tex("The number of possible ways\\\\to pick $3$ out of $x$ items").move_to((text[4].get_right() + 0.25)*RIGHT, LEFT)
        VGroup(text, description).move_to(ORIGIN)
        self.add(text, description)

        binomial_coefficients_text = Tex("Binomial Coefficients").scale(1.25).shift(UP*3)

        self.play(
            VGroup(text, description).animate.move_to(UP),
            FadeIn(binomial_coefficients_text, shift=UP*0.75, scale=0.9)
        )

        SPREAD = 2.5

        notation_1 = MathTex("_xC_3").scale(1.2).move_to(DOWN*2 + LEFT*2*SPREAD)
        notation_2 = MathTex("C_{x,3}").scale(1.2).move_to(DOWN*2 + LEFT*SPREAD)
        notation_3 = MathTex("\\binom x3").scale(1.2).move_to(DOWN*2)
        notation_4 = MathTex("^xC_3").scale(1.2).move_to(DOWN*2 + RIGHT*SPREAD)
        notation_5 = MathTex("C^x_3").scale(1.2).move_to(DOWN*2 + 2*RIGHT*SPREAD)

        self.play(
            LaggedStart(
                fade_and_shift_in(notation_1, scale=0.5, shift=UP),
                fade_and_shift_in(notation_2, scale=0.5, shift=UP),
                fade_and_shift_in(notation_3, scale=0.5, shift=UP),
                fade_and_shift_in(notation_4, scale=0.5, shift=UP),
                fade_and_shift_in(notation_5, scale=0.5, shift=UP),
                lag_ratio = 0.25
            )
        )

        self.play(
            LaggedStart(
                notation_3.animate.shift(UP*0.5),
                fade_and_shift_out(notation_1, DOWN),
                fade_and_shift_out(notation_2, DOWN),
                fade_and_shift_out(notation_4, DOWN),
                fade_and_shift_out(notation_5, DOWN),
            )
        )

        choose_text = Tex("``$x$ choose $3$\"").move_to(notation_3.get_right() + RIGHT*0.75, LEFT)

        self.play(Write(choose_text))


        new_text = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1", "=", "\\binom x3").scale(1.2)

        self.play(
            Transform(text, new_text[:-1]),
            Transform(notation_3[0], new_text[-1]),
            FadeOut(VGroup(binomial_coefficients_text, description), shift=UP),
            FadeOut(choose_text, shift=DOWN)
        )

        self.remove(*text, *new_text, *notation_3)
        text = MathTex("\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3=0}^{k_2-1}", "1", "=", "\\binom x3").scale(1.2)
        self.add(text)

        m_sums =  MathTex("\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1}\\cdots\\sum_{k_m=0}^{k_{m-1}-1}", "1", "= \\binom xm").move_to(DOWN)
        m_sums_brace = Brace(VGroup(m_sums[0][4], m_sums[0][-1]))
        m_sums_brace_text = Tex("$m$ sums").scale(0.8).move_to(m_sums_brace.get_bottom() + DOWN*0.2, UP)

        self.play(
            text.animate.shift(UP * 2).scale(1/1.2),
            FadeIn(VGroup(m_sums, m_sums_brace, m_sums_brace_text), shift=UP*2)
        )

        new_text = text.copy()
        new_text.shift(UP*2.5 - new_text[-1].get_center())
        new_text[:-1].set_color(BLACK)

        self.play(
            Transform(text, new_text),
            FadeOut(VGroup(m_sums, m_sums_brace, m_sums_brace_text), shift=DOWN*2)
        )



class OtherDefinition(Scene):
    def construct(self):

        LEFT_BOUND = 5.5

        top_text = MathTex("\\binom x3").move_to(UP*2.5)
        self.add(top_text)

        dots = VGroup(*[Dot(RIGHT*i, 0.16, color=BLUE) for i in range(10)])
        dots.move_to(DOWN*2)

        brace = Brace(dots)
        brace_text = MathTex("x").move_to(brace.get_bottom() + DOWN*0.2, UP)
        self.play(
            fade_and_shift_in(VGroup(brace, brace_text, dots), UP)
        )


        total_choices = Tex("Total choices:").move_to(UP * 0.8)
        text = MathTex("x").scale(1.2)


        self.play(
            Write(total_choices, run_time=1),
            FadeIn(text, scale=0),
            LaggedStart(
                *[dot.animate(rate_func=lambda t:4*t*(1-t), run_time=0.3).shift(UP*0.2).set_color(RED) for dot in dots],
                lag_ratio=0.5
            )
        )


        choice_1 = dots[2]

        self.play(choice_1.animate.scale(1.5).set_color(RED))

        new_dots = VGroup(*[Dot(RIGHT*i, 0.16, color=BLUE) for i in range(9)])
        new_dots.move_to(DOWN*2)
        dots = VGroup(*dots[0:2], *dots[3:])

        new_brace = Brace(new_dots)
        new_brace_text = MathTex("x", "- 1").move_to(new_brace.get_bottom() + DOWN*0.2, UP)

        self.play(
            choice_1.animate(path_arc=PI/2).scale(1/1.5).move_to(LEFT*LEFT_BOUND),
            Transform(dots, new_dots),
            Transform(brace, new_brace),
            Transform(brace_text[0], new_brace_text[0]),
            FadeIn(new_brace_text[1], shift=LEFT)
        )

        self.remove(*brace_text, *new_brace_text)
        brace_text = new_brace_text
        self.add(new_brace_text)

        new_text = MathTex("x", "(x - 1)").scale(1.2)

        self.play(
            Transform(text[0], new_text[0]),
            FadeIn(new_text[1], shift=LEFT),
            LaggedStart(
                *[dot.animate(rate_func=lambda t:4*t*(1-t), run_time=0.3).shift(UP*0.2).set_color(GREEN) for dot in dots],
                lag_ratio=0.5
            )
        )


        choice_2 = dots[5]

        self.play(choice_2.animate.scale(1.5).set_color(GREEN))

        new_dots = VGroup(*[Dot(RIGHT*i, 0.16, color=BLUE) for i in range(8)])
        new_dots.move_to(DOWN*2)
        dots = VGroup(*dots[0:5], *dots[6:])

        new_brace = Brace(new_dots)
        new_brace_text = MathTex("x", "- 2").move_to(new_brace.get_bottom() + DOWN*0.2, UP)


        self.play(
            choice_2.animate(path_arc=PI/4).scale(1/1.5).move_to(LEFT*(LEFT_BOUND - 0.5)),
            Transform(dots, new_dots),
            Transform(brace, new_brace),
            Transform(brace_text, new_brace_text),
        )



        self.remove(*new_text, *text)
        text = MathTex("x(x - 1)").scale(1.2)
        self.add(text)
        new_text = MathTex("x(x - 1)", "(x - 2)").scale(1.2)

        self.play(
            Transform(text[0], new_text[0]),
            FadeIn(new_text[1], shift=LEFT),
            LaggedStart(
                *[dot.animate(rate_func=lambda t:4*t*(1-t), run_time=0.3).shift(UP*0.2).set_color(YELLOW) for dot in dots],
                lag_ratio=0.5
            )
        )


        choice_3 = dots[1]

        self.play(choice_3.animate.scale(1.5).set_color(YELLOW))

        dots = VGroup(*dots[0:1], *dots[2:])


        self.play(
            choice_3.animate(path_arc=PI/2).scale(1/1.5).move_to(LEFT*(LEFT_BOUND - 1)),
            fade_and_shift_out(VGroup(dots, brace, brace_text), DOWN)
        )


        V_SPREAD = 0.75

        choices = VGroup(choice_1, choice_2, choice_3)
        p_up_1 = VGroup(choice_1.copy(), choice_2.copy().move_to(choice_3), choice_3.copy().move_to(choice_2)).shift(UP*V_SPREAD*(1 - 0.5))
        p_up_1.save_state()
        p_up_1.become(choices).set_opacity(0.25)

        self.play(
            choices.animate.shift(DOWN*V_SPREAD*0.5),
            p_up_1.animate.restore(),
            run_time = 0.5
        )

        p_down_1 = choices
        p_up_1 = VGroup(p_up_1[0], p_up_1[2], p_up_1[1])

        p_down_2 = VGroup(p_down_1[0].copy().move_to(p_down_1[1]), p_down_1[1].copy().move_to(p_down_1[0]), p_down_1[2].copy()).shift(DOWN*V_SPREAD)
        p_down_2.save_state()
        p_down_2.become(p_down_1).set_opacity(0.25)

        p_up_2 = VGroup(p_up_1[0].copy().move_to(p_up_1[1]), p_up_1[1].copy().move_to(p_up_1[0]), p_up_1[2].copy()).shift(UP*V_SPREAD)
        p_up_2.save_state()
        p_up_2.become(p_up_1).set_opacity(0.25)


        self.play(
            p_up_2.animate.restore(),
            p_down_2.animate.restore(),
            run_time = 0.5
        )


        p_up_2 = VGroup(p_up_2[1], p_up_2[0], p_up_2[2])
        p_down_2 = VGroup(p_down_2[1], p_down_2[0], p_down_2[2])

        p_down_3 = VGroup(p_down_2[0].copy(), p_down_2[1].copy().move_to(p_down_2[2]), p_down_2[2].copy().move_to(p_down_2[1])).shift(DOWN*V_SPREAD)
        p_down_3.save_state()
        p_down_3.become(p_down_2).set_opacity(0.25)

        p_up_3 = VGroup(p_up_2[0].copy(), p_up_2[1].copy().move_to(p_up_2[2]), p_up_2[2].copy().move_to(p_up_2[1])).shift(UP*V_SPREAD)
        p_up_3.save_state()
        p_up_3.become(p_up_2).set_opacity(0.25)


        self.play(
            p_up_3.animate.restore(),
            p_down_3.animate.restore(),
            run_time = 0.5
        )


        self.remove(*text, *new_text)
        text = MathTex("x(x - 1)(x - 2)").scale(1.2)
        new_text = MathTex("{x(x - 1)(x - 2)", "\\over 3!}").shift(DOWN*0.2)

        self.play(
            Transform(text[0], new_text[0]),
            FadeIn(new_text[1], shift=UP/2)
        )


        self.remove(*text, *new_text)
        text = MathTex("{x(x - 1)(x - 2) \\over 3!}").shift(DOWN*0.2)

        new_text = MathTex("\\binom x3", "=", "{x(x - 1)(x - 2) \\over 3!}")

        self.play(
            LaggedStart(
                AnimationGroup(
                    VGroup(p_up_1, p_up_2, p_up_3, p_down_1, p_down_2, p_down_3).animate(remover=True, rate_func=cubic_in).shift(LEFT*3),
                    FadeOut(total_choices, scale=0),
                ),
                AnimationGroup(
                    Transform(top_text[0], new_text[0]),
                    Transform(text[0], new_text[2])
                ),
                FadeIn(new_text[1], scale=0),
                lag_ratio=0.35
            )
        )

        self.remove(*text, *top_text, *new_text)
        text = MathTex("\\binom x3 = {x(x - 1)(x - 2) \\over 3!}")
        self.add(text)

        bottom_text = MathTex("\\binom xm = {x(x - 1)\\cdots(x - (m - 1)) \\over m!}").move_to(DOWN*1.5)

        self.play(
            text.animate.shift(UP*1.5),
            FadeIn(bottom_text, shift=UP*3)
        )

        self.wait()


class GeneralSolution(Scene):
    def construct(self):
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\Delta^0 f(n)", "\\sum_{k_1=0}^{x-1} 1 \\\\",
            "&+ \\Delta^1 f(n)", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1} 1 \\\\",
            "&+ \\Delta^2 f(n)", "\\sum_{k_1=0}^{x-1}\\sum_{k_2=0}^{k_1-1}\\sum_{k_3=0}^{k_2-1} 1", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).scale(0.95).move_to(DOWN * 0.25)
        self.add(text)

        lim_text = MathTex("\\lim_{x \\to \\infty} \\Delta^", "3", "f(x) = 0").scale(0.8).move_to(UP * 3.25)
        self.add(lim_text)

        self.play(
            fade_and_shift_in(lim_text, UP),
            fade_and_shift_in(text, UP),
        )

        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1}\\right. (f(k) - f(x + k)) &+ \\Delta^0 f(n)", "\\binom x1 \\\\",
            "&+ \\Delta^1 f(n)", "\\binom x2 \\\\",
            "&+ \\Delta^2 f(n)", "\\binom x3", "\\left.\\vphantom{\\sum_{k_1=0}^{x-1}}\\right)"
        ).move_to(DOWN * 0.25)

        self.play(Transform(text, new_text))

        new_text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) + \\Delta^0 f(n)", "\\binom x1",
            "+ \\Delta^1 f(n)", "\\binom x2",
            "+ \\Delta^2 f(n)", "\\binom x3", "\\right)"
        ).scale(0.75)

        self.play(Transform(text, new_text, path_arc=PI/2))

        self.remove(*text)
        text = MathTex(
            "S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\Delta^0 f(n)\\binom x1 + \\Delta^1 f(n)\\binom x2 + \\Delta^2 f(n)\\binom x3", "\\right)"
        ).scale(0.75)
        self.add(text)

        brace = Brace(text[1])
        brace_text = MathTex("\\sum_{k=1}^3 \\Delta^{k-1}f(n) \\binom xk").scale(0.85).move_to(brace.get_bottom() + DOWN*0.2, UP)

        self.play(
            fade_and_shift_in(VGroup(brace, brace_text), UP)
        )

        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=1}^3 \\Delta^{k-1}f(n) \\binom xk", "\\right)")

        shift = new_text[1].get_center() - brace_text.get_center() + DOWN*text[1].height/4

        self.play(
            lim_text.animate.scale(1/0.8).move_to(UP*2),
            FadeOut(VGroup(text[1], brace), shift=shift, scale=0.5),
            Transform(brace_text[0], new_text[1]),
            Transform(VGroup(text[0], text[2]), VGroup(new_text[0], new_text[2]))
        )


        self.remove(*text, *brace_text)
        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) + \\sum_{k=1}^3", "\\Delta^{k-1}f(n)", "\\binom xk", "\\right)")
        self.add(text)

        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) + \\sum_{k=1}^3", "\\binom xk", "\\Delta^{k-1}f(n)", "\\right)")

        self.play(morph_text(text, new_text, [0, 2, 1, 3], path_arc=PI*3/4))

        self.remove(*text)
        text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=1}^3 \\binom xk \\Delta^{k-1}f(n) \\right)")
        self.add(text)

        self.play(
            highlight_animation(lim_text[1], YELLOW),
            highlight_animation(text[1][0], YELLOW),
        )

        new_text = MathTex("S(x) = \\lim_{n\\to\\infty}\\left(\\sum_{k=1}^{n-1} (f(k) - f(x + k)) +", "\\sum_{k=1}^m \\binom xk \\Delta^{k-1}f(n) \\right)")
        new_lim_text = MathTex("\\lim_{x \\to \\infty} \\Delta^", "m", "f(x) = 0").move_to(UP*2)

        self.play(
            Transform(text, new_text),
            Transform(lim_text, new_lim_text)
        )


        rect = SurroundingRectangle(text, buff=MED_SMALL_BUFF, color=WHITE)
        def rect_update_function(rect: SurroundingRectangle, alpha: float):
            rect.become(SurroundingRectangle(text, buff=MED_SMALL_BUFF + 0.25*(1-cubic_out(alpha)), color=WHITE))
            rect.set_stroke(opacity=alpha)
        self.play(UpdateFromAlphaFunc(rect, rect_update_function), rate_func=linear)
        # self.play(UpdateFromAlphaFunc(rect, rect_update_function), rate_func=lambda t: 1-t)
        # self.remove(rect)

        self.wait()