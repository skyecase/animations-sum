from manim import *
from modules.custom_mobjects import FullscreenAxes, create_axes
from modules.interpolation import bounce, cubic_out, quadratic_out
from modules.helpers import fade_and_shift_in, fade_and_shift_out
import math

class Recursive(Scene):
    def construct(self):
        text = MathTex("S(x+1)").scale(1.25)

        self.play(Write(text))


        new_text = MathTex("S(x+1)", "=", "f(1)", "+", "f(2)", "+", "f(3)", "+", "\\cdots", "+", "f(x)", "+", "f(x+1)")

        self.play(
            Transform(text[0], new_text[0]),
            FadeIn(new_text[1], scale=1.25, shift = new_text[0].get_right() - text[0].get_right() + LEFT*(new_text[1].width * (1.25 - 1)/2)),
        )

        self.play(
            LaggedStart(
                # Transform(text[0], new_text[0]),
                *[fade_and_shift_in(sub, shift = LEFT * 2) for sub in new_text[2:8]],
                *[fade_and_shift_in(sub, shift = LEFT * 2) for sub in new_text[8]],
                *[fade_and_shift_in(sub, shift = LEFT * 2) for sub in new_text[9:]],
                lag_ratio = 0.3
            )
        )


        self.remove(*text, *new_text, *new_text[8])
        text = MathTex("S(x+1) =", "f(1) + f(2) + f(3) + \\cdots + f(x)", "+ f(x+1)")
        self.add(text)


        brace = Brace(text[1], DOWN)
        self.play(fade_and_shift_in(brace, UP))

        s_x_text = MathTex("S(x)").move_to(brace.get_bottom() + DOWN * 0.2, UP)
        self.play(Write(s_x_text))


        new_text = MathTex("S(x+1) =", "S(x)", "+ f(x+1)")
        shift = new_text[1].get_center() - s_x_text.get_center()

        self.play(
            LaggedStart(
                AnimationGroup(
                    VGroup(s_x_text).animate.shift(shift),
                    FadeOut(VGroup(brace, text[1]), shift=shift),
                ),
                AnimationGroup(
                    Transform(text[0], new_text[0], rate_func = bounce()),
                    Transform(text[2], new_text[2], rate_func = bounce()),
                    run_time = 1.5
                ),
                lag_ratio=0.5
            )
        )

        self.remove(*text, *new_text, s_x_text)
        text = MathTex("S(x+1) = S(x) + f(x+1)")
        self.add(text)

        self.play(text.animate.scale(1.25))




        def f(x):
            # There is no significance to these variable names.
            a = 0.96; b = 0.4; c = -0.48; d = 4.9; p = 1.9
            return a + p*(b*x)/math.sqrt(1 + (b*x)**2) + c*x/math.sqrt(1 + (c*(x - d))**2) - 0.2


        axes = FullscreenAxes(self, LEFT * 2.5 + DOWN * 1.5, [0.8, 0.8])
        f_curve = ParametricFunction(lambda t: axes.coords_to_point(t, f(t)), [-6, 12], color=RED)
        f_text = MathTex("f(x)").set_color(RED).move_to(axes.coords_to_point(11.5, f(11.5)) + (LEFT+UP)*0.2, RIGHT+DOWN).scale(0.9)

        self.play(
            LaggedStart(
                text.animate.scale(0.9 * 1/1.25).move_to(RIGHT * 6.5 + DOWN * 2, RIGHT + UP),
                create_axes(self, axes),
                Create(f_curve, rate_func = quadratic_out),
                fade_and_shift_in(f_text, RIGHT),
                lag_ratio = 0.5
            )
        )



        point_1 = Dot(axes.coords_to_point(1, f(1)), 0.1, color=BLUE)
        s1_text = MathTex("S(1) = f(1)").scale(0.8).move_to(axes.coords_to_point(0, f(1)) + UP + RIGHT*0.4, DOWN + LEFT)
        s1_arrow = Arrow(s1_text.get_bottom()*UP + DOWN*0.15 + point_1.get_center()*RIGHT, point_1.get_center() + UP*0.2, buff=0)

        self.play(
            FadeIn(point_1, scale=3, rate_func = bounce()),
            fade_and_shift_in(VGroup(s1_text, s1_arrow), DOWN * 0.5)
        )

        self.play(FadeOut(VGroup(s1_text, s1_arrow), scale=0, shift = point_1.get_center() - VGroup(s1_text, s1_arrow).get_center() + UP*0.15))


        point_2 = Dot(axes.coords_to_point(2, f(1) + f(2)), 0.1, color=BLUE)



        start_vt = ValueTracker(0)
        end_vt = ValueTracker(0)
        arrow = VMobject()
        self.add(start_vt, end_vt, arrow)

        def arrow_updater(arrow: Arc):
            arrow.become(create_arrow(point_1.get_center(), point_2.get_center(), start_vt.get_value(), end_vt.get_value(), angle=PI/2))
        arrow.add_updater(arrow_updater)

        addition_text = MathTex("+ f(2)").scale(0.8).move_to(axes.coords_to_point(1, f(1) + f(2)) + UP * 0.2, DOWN)


        self.play(
            end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(point_2, scale=3, rate_func = bounce()),
            fade_and_shift_in(addition_text, shift = UP, scale = 0)
        )
        self.play(
            start_vt.animate.set_value(1),
            fade_and_shift_out(addition_text, shift = UP * 0.7),
            rate_func = cubic_out,
        )
        self.remove(arrow, addition_text)


        point_3 = Dot(axes.coords_to_point(3, f(1) + f(2) + f(3)), 0.1, color=BLUE)

        start_vt.set_value(0); end_vt.set_value(0)
        arrow = VMobject()
        self.add(start_vt, end_vt, arrow)

        def arrow_updater(arrow: Arc):
            arrow.become(create_arrow(point_2.get_center(), point_3.get_center(), start_vt.get_value(), end_vt.get_value(), angle=PI/2))
        arrow.add_updater(arrow_updater)

        addition_text = MathTex("+ f(3)").scale(0.8).move_to(axes.coords_to_point(2, f(1) + f(2) + f(3)) + UP * 0.2, DOWN)


        self.play(
            end_vt.animate(rate_func=cubic_out).set_value(1),
            FadeIn(point_3, scale=3, rate_func = bounce()),
            fade_and_shift_in(addition_text, shift = UP, scale = 0)
        )
        self.play(
            start_vt.animate.set_value(1),
            fade_and_shift_out(addition_text, shift = UP * 0.7),
            rate_func = cubic_out,
        )
        self.remove(arrow, addition_text)



        point_4 = Dot(axes.coords_to_point(4, f(1) + f(2) + f(3) + f(4)), 0.1, color=BLUE)
        point_5 = Dot(axes.coords_to_point(5, f(1) + f(2) + f(3) + f(4) + f(5)), 0.1, color=BLUE)

        asdf = ArrowThing(point_3.get_center(), point_4.get_center(), text="+f(4)")
        self.add(asdf)
        asdf2 = ArrowThing(point_4.get_center(), point_5.get_center(), text="+f(5)")
        self.add(asdf2)
        self.play(
            LaggedStart(
                    AnimationGroup(
                        asdf.animation,
                        FadeIn(point_4, scale=3, rate_func = bounce())
                    ),
                    AnimationGroup(
                        asdf2.animation,
                        FadeIn(point_5, scale=3, rate_func = bounce())
                    ),
                    lag_ratio = 0.4
            )
        )




def create_arrow(target_start, target_end, start=0, end=1, buff = 0.15, angle=PI*3/4):
    diff = target_end - target_start
    distance = math.sqrt(np.dot(diff, diff))
    radius = distance / (2*math.sin(angle/2))
    center = (target_start + target_end)/2 + normalize(np.array((diff[1], -diff[0], 0))) * radius*math.cos(angle/2)

    angle_to_target_start = angle_of_vector(target_start - center)

    modified_buff = buff / radius
    start_angle = (angle_to_target_start - modified_buff) * (1 - start) + (angle_to_target_start - angle + modified_buff) * start
    angle_to_move = (end - start) * (2*modified_buff - angle)


    LENGTH_THRESHOLD = 0.6
    length = abs(angle_to_move * radius)
    size_modifier = 1 if length >= LENGTH_THRESHOLD else length / LENGTH_THRESHOLD
    size_modifier = cubic_out(size_modifier)

    stroke_width = DEFAULT_STROKE_WIDTH * size_modifier

    tip_size = 0.2 * size_modifier

    untipped_arc = Arc(radius, start_angle, angle_to_move, arc_center=center)
    untipped_arc.add_tip(tip_length = tip_size, tip_width = tip_size)
    tip = untipped_arc.tip

    take_back_length = 1/3 * stroke_width/100 + 2/3 * tip_size

    arc = Arc(radius, start_angle, angle_to_move + take_back_length/radius, arc_center=center, stroke_width=stroke_width)
    arc.tip = tip
    arc.set_cap_style(CapStyleType.BUTT)
    arc.add(tip)

    return arc



class ArrowThing(VMobject):
    def __init__(self, start_pos, end_pos, angle=PI/2, text=None):
        super().__init__()
        self.start_vt = ValueTracker(0)
        self.end_vt = ValueTracker(0)
        self.arrow = VMobject()
        self.has_text = text != None
        if self.has_text:
            self.text = VMobject()
            self.text_pos_vt = ValueTracker(0)
            self.text_opacity_vt = ValueTracker(1)
            self.text_scale_vt = ValueTracker(0)

        self.add(self.arrow)
        if self.has_text: self.add(self.text)
        
        def arrow_updater(mobject: ArrowThing):
            mobject.arrow.become(create_arrow(start_pos, end_pos, self.start_vt.get_value(), self.end_vt.get_value(), angle=angle))
            if mobject.has_text:
                mobject.text.become(MathTex(text).scale(0.7).move_to((start_pos + end_pos) / 2 + UP *(0.2 + mobject.text_pos_vt.get_value()), DOWN))
                mobject.text.scale(mobject.text_scale_vt.get_value())
                mobject.text.set_opacity(mobject.text_opacity_vt.get_value())
        self.add_updater(arrow_updater)

        self.animation = AnimationGroup(
            LaggedStart(
                self.end_vt.animate(rate_func = cubic_out).set_value(1),
                self.start_vt.animate(rate_func = cubic_out).set_value(1),
                lag_ratio = 0.5),
            self.text_pos_vt.animate(rate_func=linear, run_time=1.5).set_value(0.5),
            LaggedStart(
                self.text_scale_vt.animate(rate_func=cubic_out, run_time=1.5).set_value(1),
                self.text_opacity_vt.animate(rate_func=linear, run_time=1).set_value(0),
                lag_ratio = 0.3333)
        )