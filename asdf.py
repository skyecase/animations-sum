from manim import *
import numpy as np
import math
from modules.helpers import morph_text


class Asdf(Scene):
    def construct(self):

        # text = MathTex("""
        #                \\sum_{k = 0}^{x - 1}f(N + 1 + k) & = \\left( \\sum_{k_1 = 0}^{x-1} \\Delta^0 f(N + 1) \\right. \\\\
        #                & + \\sum_{k_1 = 0}^{x-1} \\sum_{k_2 = 0}^{k_1 - 1} \\Delta^1 f(N + 1) \\\\
        #                & + \\sum_{k_1 = 0}^{x-1} \\sum_{k_2 = 0}^{k_1 - 1} \\sum_{k_3 = 0}^{k_2 - 1} \\Delta^2 f(N + 1) \\\\
        #                & \\vdots \\\\
        #                & + \\sum_{k_1 = 0}^{x - 1} \\sum_{k_2 = 0}^{k_1 - 1} \\cdots \\sum_{k_p = 0}^{k_{p-1} - 1} \\Delta^{p - 1} f(N + 1)
        #                """)\
        # .scale(0.8)

        # self.play(Write(text))
        # self.wait()


        text = MathTex("S(x) = \\sum_{k = 1}^N (f(k) - f(x+k)) +", "\\sum_{k=0}^{x-1}", "f(N+1 + k", ")")
        new_text = MathTex("S(x) = \\sum_{k = 1}^N (f(k) - f(x+k)) +", "\\sum_{k_1=0}^{x-1}", "f(N+1 + k", "_1", ")")

        self.add(text)

        self.play(
            morph_text(text, new_text, [0, None, 2, 4], ignore_1=[1], ignore_2=[1]),
            morph_text(text[1], new_text[1], [0, 1, 2, 3, 4, 6, 7])
        )


        self.remove(*[letter  for mobj in [text, new_text]  for word in mobj  for letter in word])

        
        text = MathTex("S(x) = \\sum_{k = 1}^N (f(k) - f(x+k)) + \\sum_{k_1=0}^{x-1}", "f(N+1 + k_1)")
        f_copy = text[1].copy()

        self.add(text)

        self.play(
            text.animate.shift(UP * 2.5),
            f_copy.animate.move_to(ORIGIN)
        )


        rule = MathTex("f(", "a", " + ", "b", ") = f(", "a", ") + \\sum_{k=0}^{", "b", "-1} \\Delta f(", "a", " + k)").move_to(DOWN * 1.5)

        self.play(
            f_copy.animate.shift(UP * 0.5),
            FadeIn(rule, shift = UP)
        )


        rule.set_color_by_tex("a", BLUE)


        self.remove(f_copy)
        f_copy = MathTex("f(", "N+1", "+", "k_1", ")").move_to(f_copy)
        self.add(f_copy)


        f_copy.set_color_by_tex("N+1", BLUE)

        self.wait()




def bold(mobject: Mobject, amount: float):
    if (len(mobject.submobjects) != 0):
        for submobject in mobject.submobjects:
            bold(submobject, amount)
    else:
        amount *= -1
        new_points = []
        for i, point in enumerate(mobject.points):
            offset = 1
            prev_point = mobject.points[i - offset]
            while (prev_point == point).all():
                offset += 1
                prev_point = mobject.points[i - offset]
            normal_low = point - prev_point
            normal_low = [-normal_low[1], normal_low[0], 0] / np.sqrt(normal_low[0]**2 + normal_low[1]**2)

            offset = 1
            next_point = mobject.points[(i + offset) % len(mobject.points)]
            while (next_point == point).all():
                offset += 1
                next_point = mobject.points[(i + offset) % len(mobject.points)]
            normal_high = next_point - point
            normal_high = [-normal_high[1], normal_high[0], 0] / np.sqrt(normal_high[0]**2 + normal_high[1]**2)

            normal = normal_low + normal_high
            normal = normal / np.sqrt(normal[0]**2 + normal[1]**2)


            dot = min(1, max(-1, normal_low[0]*normal_high[0] + normal_low[1]*normal_high[1]))
            angle = math.acos(dot)
            new_points.append(point + normal * amount / math.cos(angle/2))

            # new_points.append(point + normal * amount)
        
        for i in range(len(new_points)):
            mobject.points[i] = new_points[i]
    
    return mobject

        


class Bsdf(Scene):
    def construct(self):
        unmodified = MathTex("f(", "x", "+ n) = f(", "x", ") + \\sum_{k = 0}^{n - 1} \\Delta f(", "x", "+ k)")
        modified = bold(unmodified.copy(), 0.01)
        # modified = unmodified.copy()
        # modified[1].set_color(BLUE)
        # modified[3].set_color(BLUE)
        # modified[5].set_color(BLUE)
        # bold(modified[1], 0.01)
        # bold(modified[3], 0.01)
        # bold(modified[5], 0.01)

        unmodified.scale(1.8)
        modified.scale(1.8)

        self.add(unmodified)

        self.play(Transform(unmodified, modified), run_time=1, rate_func = there_and_back)
        self.play(Transform(unmodified, modified), run_time=1, rate_func = there_and_back)
        self.play(Transform(unmodified, modified), run_time=1, rate_func = there_and_back)
        self.play(Transform(unmodified, modified), run_time=1, rate_func = there_and_back)
        self.play(Transform(unmodified, modified), run_time=1, rate_func = there_and_back)