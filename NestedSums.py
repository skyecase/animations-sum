from manim import *
import numpy as np
import math
from modules.helpers import morph_text


class Asdf(Scene):
    def construct(self):

        # text = MathTex("""
        #                \\sum_{k = 0}^{x - 1}f(n + 1 + k) & = \\left( \\sum_{k_1 = 0}^{x-1} \\Delta^0 f(n + 1) \\right. \\\\
        #                & + \\sum_{k_1 = 0}^{x-1} \\sum_{k_2 = 0}^{k_1 - 1} \\Delta^1 f(n + 1) \\\\
        #                & + \\sum_{k_1 = 0}^{x-1} \\sum_{k_2 = 0}^{k_1 - 1} \\sum_{k_3 = 0}^{k_2 - 1} \\Delta^2 f(n + 1) \\\\
        #                & \\vdots \\\\
        #                & + \\sum_{k_1 = 0}^{x - 1} \\sum_{k_2 = 0}^{k_1 - 1} \\cdots \\sum_{k_p = 0}^{k_{p-1} - 1} \\Delta^{p - 1} f(n + 1)
        #                """)\
        # .scale(0.8)

        # self.play(Write(text))
        # self.wait()


        text = MathTex("S(x) = \\sum_{k = 1}^n (f(k) - f(x+k)) +", "\\sum_{k=0}^{x-1}", "f(n+1 + k", ")")
        new_text = MathTex("S(x) = \\sum_{k = 1}^n (f(k) - f(x+k)) +", "\\sum_{k_1=0}^{x-1}", "f(n+1 + k", "_1", ")")

        self.add(text)

        self.play(
            morph_text(text, new_text, [0, None, 2, 4], ignore_1=[1], ignore_2=[1]),
            morph_text(text[1], new_text[1], [0, 1, 2, 3, 4, 6, 7])
        )


        self.remove(*[letter  for mobj in [text, new_text]  for word in mobj  for letter in word])

        
        text = MathTex("S(x) = \\sum_{k = 1}^n (f(k) - f(x+k)) + \\sum_{k_1=0}^{x-1}", "f(n+1 + k_1)")
        f_copy = text[1].copy()

        self.add(text)

        self.play(
            text.animate.shift(UP * 2.5),
            f_copy.animate.move_to(ORIGIN)
        )


        rule = MathTex("f(", "a", " + ", "b", ") = f(", "a", ") + \\sum_{k=0}^{b-1} \\Delta f(", "a", " + k)").move_to(DOWN * 1.5)

        self.play(
            f_copy.animate.shift(UP * 0.5),
            FadeIn(rule, shift = UP)
        )

        self.remove(f_copy)
        f_copy = MathTex("f(", "n+1", "+", "k_1", ")").move_to(f_copy)
        self.add(f_copy)

        f_copy.save_state()

        self.play(
            *[rule.animate.set_color(RED).set_stroke(width=2).scale(1.1) for rule in [rule[1], rule[5], rule[7], *f_copy[1]]]
        )

        new_rule = MathTex("f(", "n+1", " + ", "b", ") = f(", "n+1", ") + \\sum_{k=0}^{b-1} \\Delta f(", "n+1", " + k)").move_to(DOWN * 1.5)

        self.play(
            Transform(rule, new_rule),
            Restore(f_copy)
        )

        self.remove(*rule)
        rule = MathTex("f(n+1 + ", "b", ") = f(n+1) +", "\\sum_{k=0}^{b-1}", "\\Delta f(n+1 + k)").move_to(DOWN * 1.5)
        self.add(rule)

        self.play(
            *[rule.animate.set_color(RED).set_stroke(width=2).scale(1.1) for rule in [rule[1], rule[3][0], f_copy[3]]]
        )

        new_rule = MathTex("f(n+1 + ", "k_1", ") = f(n+1) +", "\\sum_{k=0}^{k_1-1}", "\\Delta f(n+1 + k)").move_to(DOWN * 1.5)

        self.play(
            Transform(rule[:3], new_rule[:3]),
            Transform(rule[3][0], new_rule[3][0:2]),
            Transform(rule[3][1:], new_rule[3][2:]),
            Transform(rule[4], new_rule[4]),
            Restore(f_copy)
        )


        self.wait()




class Bsdf(Scene):
    def construct(self):
        text = MathTex("S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+", "\\left. \\sum_{k_1=0}^{x-1} f(n + 1 + k_1)", "\\right)")
        text.scale(0.8)

        self.add(text)


        focus_text = text[1].copy()
        self.add(focus_text)
        text[1].set_color(DARK_GRAY)
        self.play(
            focus_text.animate.move_to(DOWN),
            text[0].animate.shift(UP * 2),
            text[1].animate.shift(UP * 2),
            text[2].animate.shift(UP * 2),
        )


        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1)", "= \\sum_{k_1=0}^{x-1} \\left(f(n + 1) + \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)\\right)")
        new_focus_text.move_to(DOWN).scale(0.8)

        self.play(morph_text(VGroup(focus_text), new_focus_text, [0]))

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1) = \\sum_{k_1=0}^{x-1}", "\\left(", "f(n + 1) +", "\\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "\\right)")
        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1) = \\sum_{k_1=0}^{x-1}", "f(n + 1) +", "\\sum_{k_1=0}^{x-1}", "\\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)")
        focus_text.move_to(DOWN).scale(0.8)
        new_focus_text.move_to(DOWN).scale(0.8)
        self.play(morph_text(focus_text, new_focus_text, [0, None, 1, 3]))

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} f(n + 1 + k_1) =", "\\sum_{k_1=0}^{x-1} f(n + 1)", "+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)")
        focus_text.move_to(DOWN).scale(0.8)
        new_text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+", "\\sum_{k_1=0}^{x-1} f(n + 1) \\\\",
            "&+ \\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "\\right)"
        ).move_to(UP).scale(0.8)
        self.add(focus_text)

        self.play(
            Transform(text[0], new_text[0]),
            Transform(focus_text[1], new_text[1]),
            Transform(focus_text[2], new_text[2]),
            Transform(text[2], new_text[3]),
            FadeOut(text[1], shift = UP),
            FadeOut(focus_text[0], shift = LEFT),
        )


        self.remove(*text, *new_text, *focus_text)

        text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+ \\sum_{k_1=0}^{x-1} f(n + 1) \\\\"
            "&+", "\\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "\\right)"
        ).move_to(UP).scale(0.8)
        focus_text = text[1].copy()
        text[1].set_color(DARK_GRAY)

        self.play(
            text.animate.move_to(UP * 1.5),
            focus_text.animate.move_to(DOWN * 1.5)
        )

        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2)", "= \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\left(\\Delta f(n + 1) + \\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)\\right)")
        new_focus_text.move_to(DOWN * 1.5).scale(0.8)
        self.play(
            focus_text.animate.move_to(new_focus_text[0]),
            FadeIn(new_focus_text[1], shift = LEFT * 5)
        )

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2) = \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}", "\\left(", "\\Delta f(n + 1) +", "\\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)", "\\right)")
        focus_text.move_to(DOWN * 1.5).scale(0.8)
        new_focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2) = \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}", "\\Delta f(n + 1) +", "\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}", "\\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)")
        new_focus_text.move_to(DOWN * 1.5).scale(0.75)
        self.play(morph_text(focus_text, new_focus_text, [0, None, 1, 3]))

        self.remove(*focus_text, *new_focus_text)
        focus_text = MathTex("\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1}\\Delta f(n + 1 + k_2) =", "\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\Delta f(n + 1)", "+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3 = 0}^{k_2 - 1}\\Delta^2f(n + 1 + k_3)")
        focus_text.move_to(DOWN * 1.5).scale(0.75)
        new_text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+ \\sum_{k_1=0}^{x-1} f(n + 1) \\\\"
            "&+", "\\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\Delta f(n + 1) \\\\",
            "&+ \\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + 1 + k_3)", "\\right)"
        ).scale(0.8)
        self.add(focus_text)

        self.play(
            Transform(text[0], new_text[0]),
            Transform(focus_text[1], new_text[1]),
            Transform(focus_text[2], new_text[2]),
            Transform(text[2], new_text[3]),
            FadeOut(text[1], shift = new_text[1].get_top() - text[1].get_center(), scale = 0),
            FadeOut(focus_text[0], shift = LEFT),
        )




        self.remove(*text, *new_text, *focus_text)

        text = MathTex(
            "S(x) = \\lim_{n \\to \\infty} \\left( \\sum_{k=0}^n\\right. (f(k) - f(x+k)) &+ \\sum_{k_1=0}^{x-1} f(n + 1) \\\\"
            "&+ \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\Delta f(n + 1) \\\\"
            "&+", "\\left. \\sum_{k_1=0}^{x-1} \\sum_{k_2=0}^{k_1-1} \\sum_{k_3=0}^{k_2-1} \\Delta^2 f(n + 1 + k_3)", "\\right)"
        ).scale(0.8)
        self.add(text)



        self.wait()
