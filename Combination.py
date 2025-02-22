from manim import *
from modules.helpers import create_time_getter, create_updater_container, highlight_animation, shrink_between
from modules.interpolation import bounce, cubic_out, pow_out, sin_smooth_in_out
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



class BinomialCoefficientSpecificChoice(Scene):
    def construct(self):
        text = MathTex("\\sum_{k_1 = 2}^{n - 1}", "\\sum_{k_2 = 1}^{k_1 - 1}", "\\sum_{k_3 = 0}^{k_2 - 1}", "1").move_to(UP * 2)

        text[0].set_color(RED)
        text[1].set_color(GREEN)
        text[2].set_color(BLUE)

        self.add(text)


        N = 10

        dots = VGroup(*[Dot(RIGHT * i) for i in range(N)]).move_to(DOWN)
        labels = [MathTex(i).move_to(dot.get_center() + 0.5 * UP, DOWN) for (i, dot) in enumerate(dots)]

        self.add(dots, *labels)


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

        running_total = MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5)
        running_total_title = Tex("Total").move_to(running_total.get_top() + UP * 0.2, DOWN)
        self.add(points, running_total, running_total_title)
        

        choices = [7, 5, 2]

        choice_dots = VGroup(*[Circle(0.3, WHITE).move_to(dots[choice].get_center()) for choice in choices])

        self.play(
            *[FadeIn(dot, scale=2) for dot in choice_dots]
        )

        self.wait()

        while state[0] < choices[0]:
            iterate_state()
            points.become(get_points_for_state())
            running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))
            self.wait(0.1)

        self.wait()

        while state[1] < choices[1]:
            iterate_state()
            points.become(get_points_for_state())
            running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))
            self.wait(0.2)

        self.wait()

        while state[2] < choices[2]:
            iterate_state()
            points.become(get_points_for_state())
            running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))
            self.wait(0.4)
        
        self.wait()


        while state[0] < 10:
            iterate_state()
            if state[0] == 10: break
            points.become(get_points_for_state())
            running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))
            self.wait(0.1)