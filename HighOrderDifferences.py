from manim import *
from modules.helpers import morph_text, align_baseline


class HighOrderDifferences(Scene):
    def construct(self):

        def align_math_tex(tex: MathTex):
            strings = tex.tex_strings
            new_text_object = MathTex("=", *strings)
            new_text_object.shift(tex.get_center() - new_text_object[0].get_center())
            tex.shift(UP*(new_text_object[1:].get_center() - tex.get_center()))
            return tex

        VERTICAL_SPACING = 1

        # Texts are indexed by the order of the Delta inside them, not the order they appear in the scene.
        text2 = align_math_tex(MathTex("\\Delta \\Delta f(x)", "=", "\\Delta f(x+1) - \\Delta f(x)"))
        self.play(Write(text2))

        new_text2 = align_math_tex(MathTex("\\Delta^2 f(x)", "=", "\\Delta f(x+1) - \\Delta f(x)"))
        self.play(Transform(text2, new_text2))
        
        
        text3 = align_math_tex(MathTex("\\Delta^3 f(x)", "=", "\\Delta^2 f(x+1) - \\Delta^2 f(x)").move_to(DOWN*VERTICAL_SPACING/2))
        self.play(
            text2.animate.shift(UP*VERTICAL_SPACING/2 + RIGHT*(text3[1].get_center() - text2[1].get_center())),
            FadeIn(text3, shift = UP * VERTICAL_SPACING)
        )


        texts = [
            align_math_tex(MathTex(f"\\Delta^{i} f(x)", "=", f"\\Delta^{i-1} f(x+1) - \\Delta^{i-1} f(x)").move_to(DOWN*VERTICAL_SPACING/2)\
                .move_to(DOWN*VERTICAL_SPACING*(0.5 + i - 3)))
            for i in range(4, 7)
        ]

        self.play(
            LaggedStart(
                *[FadeIn(text, shift=UP*VERTICAL_SPACING) for text in texts],
                lag_ratio = 0.25
            )
        )



        text1 = align_math_tex(MathTex("\\Delta", "f(x)", "=", "f(x+1) - f(x)"))
        text1.shift(UP*1.5*VERTICAL_SPACING + RIGHT*(text2[1].get_center() - text1[2].get_center()))

        self.play(FadeIn(text1, shift=DOWN))

        new_text1 = align_math_tex(MathTex("\\Delta", "^1", "f(x)", "=", "f(x+1) - f(x)"))
        new_text1.shift(UP*1.5*VERTICAL_SPACING + RIGHT*(text2[1].get_center() - new_text1[3].get_center()))
        self.remove(*text2, *new_text2)
        text2 = MathTex("\\Delta^2 f(x)", "=", "\\Delta", "f(x+1) - \\Delta", "f(x)").move_to(text2)
        new_text2 = MathTex("\\Delta^2 f(x)", "=", "\\Delta", "^1", "f(x+1) - \\Delta", "^1", "f(x)")
        new_text2.shift(text2[1].get_center() - new_text2[1].get_center())
        self.add(text2)

        self.play(
            morph_text(text1, new_text1, [0, 2, 3, 4]),
            morph_text(text2, new_text2, [0, 1, 2, 4, 6])
        )


        self.wait()
