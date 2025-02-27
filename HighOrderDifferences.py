from manim import *
from modules.custom_mobjects import CheckMark
from modules.helpers import fade_and_shift_in, grow_between, morph_text, align_baseline




class HighOrderDifferences(Scene):
    def construct(self):

        LEFT_EDGE = 1.75

        text_0 = MathTex("\\lim_{x\\to\\infty} f(x) = 0").move_to(UP*2 + LEFT*LEFT_EDGE, LEFT)
        check_0 = CheckMark(text_0.get_left())

        self.play(
            LaggedStart(
                fade_and_shift_in(text_0, UP),
                check_0.create_animation(),
                lag_ratio=0.3333
            )
        )

        text_1 = MathTex("\\lim_{x\\to\\infty}", "\\Delta f(x)", "=", "0").move_to(UP*0 + LEFT*LEFT_EDGE, LEFT)
        check_1 = CheckMark(text_1.get_left())

        self.play(
            LaggedStart(
                fade_and_shift_in(text_1, UP),
                check_1.create_animation(),
                lag_ratio=0.3333
            )
        )

        text_2 = MathTex("\\lim_{x\\to\\infty}", "\\Delta\\Delta f(x)", "=", "0").move_to(UP*-2 + LEFT*LEFT_EDGE, LEFT)

        self.play(
            fade_and_shift_in(text_2, UP)
        )


        V_SPACING = 1

        invisible_text = MathTex("\\Delta^1 f(x)", "=", "\\Delta^0 f(x+1) - \\Delta^0 f(x)")
        center = invisible_text[1].get_center() + UP*0.5


        new_text_1 = MathTex("\\Delta f(x)", "=", "f(x+1) - f(x)")
        new_text_1.shift(center - new_text_1[1].get_center())
        new_text_2 = MathTex("\\Delta\\Delta f(x)", "=", "\\Delta f(x+1) - \\Delta f(x)")
        new_text_2.shift(center - new_text_2[1].get_center() + DOWN*V_SPACING)



        shift_1 = new_text_1[1].get_center() - text_1[2].get_center()
        shift_2 = new_text_2[1].get_center() - text_2[2].get_center()

        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(VGroup(text_1[0], check_1), shift=shift_1),
                    FadeOut(text_1[3], shift=RIGHT),
                    text_1[1:3].animate.shift(shift_1),
                    FadeOut(text_2[0], shift=shift_2),
                    FadeOut(text_2[3], shift=RIGHT),
                    text_2[1:3].animate.shift(shift_2),
                    FadeOut(VGroup(text_0, check_0), shift=UP),
                ),
                LaggedStart(
                    *[fade_and_shift_in(t, LEFT * 1.5, run_time=0.5, shift_rate_func = lambda x: 2*smooth((x+1)/2)-1) for t in new_text_1[2]],
                    lag_ratio=0.1
                ),
                lag_ratio=0.5
            )
        )

        self.play(
            LaggedStart(
                *[fade_and_shift_in(t, LEFT * 1.5, run_time=0.5, shift_rate_func = lambda x: 2*smooth((x+1)/2)-1) for t in new_text_2[2]],
                lag_ratio=0.1
            )
        )


        self.remove(*text_1, *text_2, *new_text_1, *new_text_2, *new_text_1[2], *new_text_2[2])
        text_1 = new_text_1
        text_2 = MathTex("\\Delta", "\\Delta", "f(x)", "=", "\\Delta", "f(x+1) - \\Delta", "f(x)")
        text_2.shift(new_text_2[1].get_center() - text_2[3].get_center())
        self.add(text_1, text_2)

        new_text_2 = MathTex("\\Delta^", "2", "f(x)", "=", "\\Delta", "f(x+1) - \\Delta", "f(x)")
        new_text_2.move_to(text_2[3].get_center() - new_text_2[3].get_center())

        self.play(Transform(text_2, new_text_2))


        text_3 = MathTex("\\Delta^3 f(x)", "=", "\\Delta^2 f(x+1) - \\Delta^2 f(x)")
        text_3.shift(center - text_3[1].get_center() + DOWN*V_SPACING*2)

        self.play(fade_and_shift_in(text_3, UP))


        text_4 = MathTex("\\Delta^4 f(x)", "=", "\\Delta^3 f(x+1) - \\Delta^3 f(x)")
        text_4.shift(center - text_4[1].get_center() + DOWN*V_SPACING*3)

        text_5 = MathTex("\\Delta^5 f(x)", "=", "\\Delta^4 f(x+1) - \\Delta^4 f(x)")
        text_5.shift(center - text_5[1].get_center() + DOWN*V_SPACING*4)

        self.play(
            LaggedStart(
                fade_and_shift_in(text_4, UP),
                fade_and_shift_in(text_5, UP),
                lag_ratio=0.5
            )
        )



        self.remove(text_1)
        text_1 = MathTex("\\Delta", "f(x)", "=", "f(x+1) - f(x)")
        text_1.shift(center - text_1[2].get_center())
        self.add(text_1)

        new_text_1 = MathTex("\\Delta^", "1", "f(x)", "=", "f(x+1) - f(x)")
        new_text_1.shift(center - new_text_1[3].get_center())

        new_text_2 = MathTex("\\Delta^", "2", "f(x)", "=", "\\Delta^", "1", "f(x+1) - \\Delta^", "1", "f(x)")
        new_text_2.shift(text_2[3].get_center() - new_text_2[3].get_center())

        self.play(
            morph_text(text_1, new_text_1, [0, 2, 3, 4]),
            morph_text(text_2, new_text_2, [0, 1, 2, 3, 4, 6, 8]),
        )


        self.remove(*text_1, *new_text_1, *text_2, *new_text_2)

        text_1 = MathTex("\\Delta^1 f(x)", "=", "f(x+1) -", "f(x)")
        text_1.shift(center - text_1[1].get_center())
        self.add(text_1)

        text_2 = MathTex("\\Delta^2 f(x)", "=", "\\Delta^1 f(x+1) - \\Delta^1 f(x)").move_to(new_text_2)
        self.add(text_2)

        new_text_1 = MathTex("\\Delta^1 f(x)", "=", "\\Delta^0", "f(x+1) -", "\\Delta^0", "f(x)")
        new_text_1.shift(center - new_text_1[1].get_center())

        text_0 = MathTex("\\Delta^0 f(x)", "=", "f(x)").move_to(UP * 2.25)

        self.play(fade_and_shift_in(text_0, UP))

        self.play(morph_text(text_1, new_text_1, [0, 1, 3, 5]))

        self.remove(*text_1, *new_text_1)

        text_1 = MathTex("\\Delta^1 f(x)", "=", "\\Delta^0 f(x+1) - \\Delta^0 f(x)").move_to(new_text_1)
        self.add(text_1)





        V_SPACING = 1.2

        new_text_0 = MathTex("\\lim_{x \\to \\infty}", "\\Delta^0 f(x)", "=", "0").move_to(UP*2.25)
        center = new_text_0[2].get_center()

        new_text_1 = MathTex("\\lim_{x \\to \\infty}", "\\Delta^1 f(x)", "=", "0")
        new_text_1.shift(center - new_text_1[2].get_center() + DOWN*V_SPACING*1)

        new_text_2 = MathTex("\\lim_{x \\to \\infty}", "\\Delta^2 f(x)", "=", "0")
        new_text_2.shift(center - new_text_2[2].get_center() + DOWN*V_SPACING*2)

        new_text_3 = MathTex("\\lim_{x \\to \\infty}", "\\Delta^3 f(x)", "=", "0")
        new_text_3.shift(center - new_text_3[2].get_center() + DOWN*V_SPACING*3)

        new_text_4 = MathTex("\\lim_{x \\to \\infty}", "\\Delta^4 f(x)", "=", "0")
        new_text_4.shift(center - new_text_4[2].get_center() + DOWN*V_SPACING*4)

        new_text_5 = MathTex("\\lim_{x \\to \\infty}", "\\Delta^5 f(x)", "=", "0")
        new_text_5.shift(center - new_text_5[2].get_center() + DOWN*V_SPACING*5)



        self.play(
            text_0[0:2].animate.move_to(new_text_0[1:3]),
            FadeIn(new_text_0[0], shift=new_text_0[2].get_center()-text_0[1].get_center()),
            FadeOut(text_0[2], shift=new_text_0[2].get_center()-text_0[1].get_center() + RIGHT*0.75),
            grow_between(new_text_0[3], text_0[1], text_0[2]),

            text_1[0:2].animate.move_to(new_text_1[1:3]),
            FadeIn(new_text_1[0], shift=new_text_1[2].get_center()-text_1[1].get_center()),
            FadeOut(text_1[2], shift=new_text_1[2].get_center()-text_1[1].get_center() + RIGHT*0.75),
            grow_between(new_text_1[3], text_1[1], text_1[2]),

            text_2[0:2].animate.move_to(new_text_2[1:3]),
            FadeIn(new_text_2[0], shift=new_text_2[2].get_center()-text_2[1].get_center()),
            FadeOut(text_2[2], shift=new_text_2[2].get_center()-text_2[1].get_center() + RIGHT*0.75),
            grow_between(new_text_2[3], text_2[1], text_2[2]),

            text_3[0:2].animate.move_to(new_text_3[1:3]),
            FadeIn(new_text_3[0], shift=new_text_3[2].get_center()-text_3[1].get_center()),
            FadeOut(text_3[2], shift=new_text_3[2].get_center()-text_3[1].get_center() + RIGHT*0.75),
            grow_between(new_text_3[3], text_3[1], text_3[2]),

            text_4[0:2].animate.move_to(new_text_4[1:3]),
            FadeIn(new_text_4[0], shift=new_text_4[2].get_center()-text_4[1].get_center()),
            FadeOut(text_4[2], shift=new_text_4[2].get_center()-text_4[1].get_center() + RIGHT*0.75),
            grow_between(new_text_4[3], text_4[1], text_4[2]),

            text_5[0:2].animate.move_to(new_text_5[1:3]),
            FadeIn(new_text_5[0], shift=new_text_5[2].get_center()-text_5[1].get_center()),
            FadeOut(text_5[2], shift=new_text_5[2].get_center()-text_5[1].get_center() + RIGHT*0.75),
            grow_between(new_text_5[3], text_5[1], text_5[2]),
        )