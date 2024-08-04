from manim import *


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
        
        points = get_points_for_state()

        self.play(
            Create(points)
        )


        def iterate_state():
            if state[2] < state[1] - 1:
                state[2] += 1
            elif state[1] < state[0] - 1:
                state[2] = 0
                state[1] += 1
            else:
                state[2] = 0
                state[1] = 1
                state[0] += 1
        
        for i in range(119):
            iterate_state()
            points.become(get_points_for_state())
            self.wait(0.1)
            # self.play(
            #     Transform(points, get_points_for_state(), run_time = 0.1, rate_func = pow_out(5))
            # )
            