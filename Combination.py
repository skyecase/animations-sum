from manim import *
from modules.interpolation import bounce


def pow_out(pow):
    return lambda x: 1 - (1 - x)**pow


class BinomialCoefficientDerivation(Scene):
    def construct(self):

        text = MathTex("\\sum_{k_1 = 2}^{n - 1}", "\\sum_{k_2 = 1}^{k_1 - 1}", "\\sum_{k_3 = 0}^{k_2 - 1}", "1").move_to(UP * 2)

        text[0].set_color(RED)
        text[1].set_color(GREEN)
        text[2].set_color(BLUE)

        self.add(text)


        N = 10

        dots = VGroup(*[Dot(RIGHT * i) for i in range(N)]).move_to(DOWN)
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

        self.play(
            FadeIn(points[0], scale=3, rate_func = bounce()),
            FadeIn(points[1], scale=0)
        )

        for i in range(3, 8):
            while state[0] < i: iterate_state()
            self.wait(0.75)
            new_points = get_points_for_state()
            points[0].become(new_points[0])
            points[1].become(new_points[1])

        self.wait(0.75)
        self.play(
            FadeIn(points[2], scale=3, rate_func = bounce()),
            FadeIn(points[3], scale=0)
        )

        for i in range(2, 7):
            while state[1] < i: iterate_state()
            self.wait(0.75)
            new_points = get_points_for_state()
            points[2].become(new_points[2])
            points[3].become(new_points[3])


        self.wait(0.75)
        while state[0] < 8: iterate_state()

        new_points = get_points_for_state()
        points[0].become(new_points[0])
        points[1].become(new_points[1])
        points[2].become(new_points[2])
        points[3].become(new_points[3])

        for i in range(2, 6):
            while state[1] < i: iterate_state()
            self.wait(0.75)
            new_points = get_points_for_state()
            points[2].become(new_points[2])
            points[3].become(new_points[3])
        
        self.wait(0.75)
        new_points = get_points_for_state()
        self.play(
            FadeIn(points[4], scale=3, rate_func = bounce()),
            FadeIn(points[5], scale=0)
        )

        self.remove(*points)
        self.add(points)


        for i in range(7):
            iterate_state()
            self.wait(0.75)
            points.become(get_points_for_state())
        


        running_total = MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5)
        running_total_title = Tex("Total").move_to(running_total.get_top() + UP * 0.2, DOWN)
        self.play(
            FadeIn(running_total, scale = 1.5),
            FadeIn(running_total_title, scale = 1.5)
        )



        while state[0] < 10:
            iterate_state()
            if state[0] == 10: break
            points.become(get_points_for_state())
            running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))

            self.wait(0.15)
            # self.play(
            #     Transform(points, get_points_for_state(), run_time = 0.1, rate_func = pow_out(5))
            # )



        iterations = 1
        state = [2, 1, 0]
        points.become(get_points_for_state())
        running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))

        while state[0] < 10:
            iterate_state()
            if state[0] == 10: break
            points.become(get_points_for_state())
            running_total.become(MathTex(iterations).move_to(RIGHT * 5 + UP * 2).scale(1.5))

            self.wait(0.1)
            # self.play(
            #     Transform(points, get_points_for_state(), run_time = 0.1, rate_func = pow_out(5))
            # )



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