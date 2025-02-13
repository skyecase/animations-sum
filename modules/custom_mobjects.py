from manim import VGroup, ORIGIN, Scene, Line, UP, RIGHT, DEFAULT_STROKE_WIDTH, LaggedStart
import manim
import numpy as np
import math
from modules.helpers import cubic_out
from modules.interpolation import quadratic_in, cubic_out

class FullscreenAxes(VGroup):
    def __init__(
        self,
        scene: Scene,
        origin: np.ndarray = ORIGIN,
        scale: list[float] = [1, 1],
        tick_length: float = 0.25,
        tick_spacing: list[float] = [1, 1],
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        rect: manim.Rectangle = None,
        **kwargs,
    ):
        VGroup.__init__(self, **kwargs)
        top = rect.get_top()[1] if rect != None else (scene.camera.frame_center + scene.camera.frame_height / 2)[1]
        bottom = rect.get_bottom()[1] if rect != None else top - scene.camera.frame_height
        right = rect.get_right()[0] if rect != None else (scene.camera.frame_center + scene.camera.frame_width / 2)[0]
        left = rect.get_left()[0] if rect != None else right - scene.camera.frame_width
        
        x_line = Line(origin[1] * UP + left * RIGHT, origin[1] * UP + right * RIGHT, stroke_width=stroke_width, **kwargs)
        y_line = Line(origin[0] * RIGHT + bottom * UP, origin[0] * RIGHT + top * UP, stroke_width=stroke_width, **kwargs)

        # X axis tick marks
        x_ticks = []
        x = origin[0] + math.ceil((left - stroke_width / 100 / 2 - origin[0]) / tick_spacing[0] / scale[0]) * tick_spacing[0] * scale[0]
        tick_bottom = min(top - tick_length, max(bottom, (origin[1] - tick_length / 2)))
        tick_top  = min(top, max(bottom + tick_length, (origin[1] + tick_length / 2)))
        while x <= right + stroke_width / 100 / 2:
            if abs(x - origin[0]) > scale[0] * tick_spacing[0] / 2:
                x_ticks += Line(x * RIGHT + tick_bottom * UP, x * RIGHT + tick_top * UP, stroke_width = stroke_width, **kwargs)
            x += tick_spacing[0] * scale[0]

        # Y axis tick marks
        y_ticks = []
        y = origin[1] + math.ceil((bottom - stroke_width / 100 / 2 - origin[1]) / tick_spacing[1] / scale[1]) * tick_spacing[1] * scale[1]
        tick_bottom = min(right - tick_length, max(left, (origin[0] - tick_length / 2)))
        tick_top  = min(right, max(left + tick_length, (origin[0] + tick_length / 2)))
        while y <= top + stroke_width / 100 / 2:
            if abs(y - origin[1]) > scale[1] * tick_spacing[1] / 2:
                y_ticks += Line(y * UP + tick_bottom * RIGHT, y * UP + tick_top * RIGHT, stroke_width = stroke_width, **kwargs)
            y += tick_spacing[1] * scale[1]
        

        self.x_ticks = x_ticks
        self.x_line = x_line
        self.y_ticks = y_ticks
        self.y_line = y_line

        self.add(VGroup(x_line, *x_ticks))
        self.add(VGroup(y_line, *y_ticks))

        self.a_origin = origin
        self.a_scale = scale


    def coords_to_point(self, x: float, y: float):
        return self.a_origin + RIGHT * self.a_scale[0] * x + UP * self.a_scale[1] * y
    
    def point_to_coords(self, point: np.ndarray):
        return ((point[0] - self.a_origin[0]) / self.a_scale[0], (point[1] - self.a_origin[1]) / self.a_scale[1])
    

    def become(self, mobj):
        self.a_origin = mobj.a_origin
        self.a_scale = mobj.a_scale
        super().become(mobj)


def create_axes(scene: Scene, axes: FullscreenAxes, x_axis_time = 0.5, **kwargs):
    for tick in [*axes.x_ticks, *axes.y_ticks]:
        tick.save_state()
        tick.scale(0)

    y_axis_time = x_axis_time * scene.camera.frame_height / scene.camera.frame_width
    
    return LaggedStart(
        manim.AnimationGroup(
            manim.Create(axes.x_line, rate_func=manim.linear, run_time=x_axis_time),
            LaggedStart(
                *[tick.animate(rate_func=cubic_out, run_time=0.5).restore() for tick in axes.x_ticks],
                lag_ratio = x_axis_time / (0.5 * len(axes.x_ticks))
            ),
            lag_ratio = x_axis_time / (0.5 * len(axes.x_ticks))
        ),
        manim.AnimationGroup(
            manim.Create(axes.y_line, rate_func=manim.linear, run_time=y_axis_time),
            LaggedStart(
                *[tick.animate(rate_func=cubic_out, run_time=0.5).restore() for tick in axes.y_ticks],
                lag_ratio = y_axis_time / (0.5 * len(axes.y_ticks))
            ),
            lag_ratio = y_axis_time / (0.5 * len(axes.y_ticks))
        ),
        lag_ratio=0.2,
        **kwargs
    )


LENGTH_THRESHOLD = 0.6

def create_arrow(
    target_start, # Point which arrow comes from
    target_end, # Point which arrow points to
    start = 0, # Start point along arc (lerp from 0 to 1)
    end = 1, # Start point along arc (lerp from 0 to 1)
    buff = 0.15, # Distance to separate arrow from target_start and target_end
    angle = manim.PI*3/4, # How much does it curve? Positive = clockwise,
    stroke_width = DEFAULT_STROKE_WIDTH,
    tip_size = 0.2,
    **kwargs
):

    if angle == 0: return create_straight_arrow(target_start, target_end, start, end, buff, stroke_width, tip_size, **kwargs)

    diff = target_end - target_start
    distance = math.sqrt(np.dot(diff, diff))
    signed_radius = distance / (2*math.sin(angle/2)) # Negative if counterclockwise
    center = (target_start + target_end)/2 + manim.normalize(np.array((diff[1], -diff[0], 0))) * signed_radius*math.cos(angle/2)
    angle_to_target_start = manim.angle_of_vector(target_start - center)

    modified_buff = buff / signed_radius
    start_angle = (angle_to_target_start - modified_buff) * (1 - start) + (angle_to_target_start - angle + modified_buff) * start
    angle_to_move = (end - start) * (2*modified_buff - angle)


    length = abs(angle_to_move * signed_radius)
    size_modifier = 1 if length >= LENGTH_THRESHOLD else length / LENGTH_THRESHOLD
    size_modifier = cubic_out(size_modifier)

    real_stroke_width = stroke_width * size_modifier

    real_tip_size = tip_size * size_modifier

    untipped_arc = manim.Arc(abs(signed_radius), start_angle, angle_to_move, arc_center=center)
    untipped_arc.add_tip(tip_length = real_tip_size, tip_width = real_tip_size)
    tip = untipped_arc.tip

    take_back_length = 1/3 * real_stroke_width/100 + 2/3 * real_tip_size

    arc = manim.Arc(abs(signed_radius), start_angle, angle_to_move + take_back_length/signed_radius, arc_center=center, stroke_width=real_stroke_width, **kwargs)
    arc.tip = tip
    arc.set_cap_style(manim.CapStyleType.BUTT)
    arc.add(tip)

    return arc


def create_straight_arrow(
    target_start, # Point which arrow comes from
    target_end, # Point which arrow points to
    start=0, # Start point along line (lerp from 0 to 1)
    end=1, # Start point along line (lerp from 0 to 1)
    buff = 0.15, # Distance to separate arrow from target_start and target_end,
    stroke_width = DEFAULT_STROKE_WIDTH,
    tip_size = 0.2,
    **kwargs
):
    diff = target_end - target_start
    dir = manim.normalize(diff)
    length = np.linalg.norm(target_end - target_start) - 2*buff

    real_start = target_start + (buff + start*length) * dir
    real_end = target_start + (buff + end*length) * dir

    real_length = length * (end - start)

    size_modifier = 1 if real_length >= LENGTH_THRESHOLD else real_length / LENGTH_THRESHOLD
    real_tip_size = tip_size * size_modifier
    real_stroke_width = stroke_width * size_modifier

    untipped_line = Line(real_start, real_end)
    untipped_line.add_tip(tip_length = real_tip_size, tip_width = real_tip_size)
    tip = untipped_line.tip
    take_back_length = 1/3 * real_stroke_width/100 + 2/3 * real_tip_size

    arrow = Line(real_start, real_end - dir*take_back_length, stroke_width=real_stroke_width, **kwargs)
    arrow.tip = tip
    arrow.set_cap_style(manim.CapStyleType.BUTT)
    arrow.add(tip)

    return arrow


class CustomArrow(manim.VMobject):
    def __init__(self, start_pos, end_pos, angle=manim.PI/2, text: manim.VMobject = None, **kwargs):
        super().__init__()
        self.start_vt = manim.ValueTracker(0)
        self.end_vt = manim.ValueTracker(0)
        self.arrow = manim.VMobject()
        self.set_text(text)
        self.text_pos_vt = manim.ValueTracker(0)
        self.text_opacity_vt = manim.ValueTracker(1)
        self.text_scale_vt = manim.ValueTracker(0)

        self.add(self.arrow)
        
        def arrow_updater(mobject: CustomArrow):
            mobject.arrow.become(create_arrow(start_pos, end_pos, self.start_vt.get_value(), self.end_vt.get_value(), angle=angle, **kwargs))
            if mobject.has_text:
                direction = UP if (end_pos[0] - start_pos[0])*angle >= 0 else manim.DOWN
                mobject.text.become(mobject.original_text)
                mobject.text.shift((start_pos + end_pos) / 2 + direction * mobject.text_pos_vt.get_value())
                mobject.text.scale(mobject.text_scale_vt.get_value())
                mobject.text.set_opacity(mobject.text_opacity_vt.get_value())
        self.arrow_updater=arrow_updater
        self.add_arrow_updater()

        self.animation = self.create_animation()
    
    def create_animation(self, **kwargs):
        return manim.AnimationGroup(
            LaggedStart(
                self.end_vt.animate(rate_func = cubic_out).set_value(1),
                self.start_vt.animate(rate_func = cubic_out).set_value(1),
                lag_ratio = 0.5),
            self.text_pos_vt.animate(rate_func=manim.linear, run_time=1.5).set_value(0.5),
            LaggedStart(
                self.text_scale_vt.animate(rate_func=cubic_out, run_time=1.5).set_value(1),
                self.text_opacity_vt.animate(rate_func=manim.linear, run_time=1).set_value(0),
                lag_ratio = 0.3333),
            **kwargs
        )
    
    def set_text(self, text: manim.VMobject = None):
        self.has_text = text != None
        if self.has_text:
            self.original_text = text.copy()
            self.text = manim.VMobject()
            self.add(self.text)
    
    def add_arrow_updater(self):
        self.add_updater(self.arrow_updater)
    
    def remove_arrow_updater(self):
        self.remove_updater(self.arrow_updater)



class DottedLine(manim.VMobject):
    def __init__(self, start=manim.LEFT, end=RIGHT, line_length = 0.1, space_length = 0.1, buff = 0, **kwargs):
        self.dim = 3
        self.buff = buff

        points = []
        length = np.linalg.norm(start - end)
        if length > line_length:
            direction = (end - start) / length

            for dist in np.arange(0, length - line_length, line_length + space_length):
                points.extend([
                    start + direction * dist,
                    start + direction * (dist + line_length / 3),
                    start + direction * (dist + 2 * line_length / 3),
                    start + direction * (dist + line_length)
                ])
                last_dist = dist + line_length
            if length - last_dist > space_length:
                dist = last_dist + space_length
                points.extend([
                    start + direction * dist,
                    start + direction * (dist * 2/3 + length * 1/3),
                    start + direction * (dist * 1/3 + length * 2/3),
                    start + direction * length
                ])
        else:
            points = Line(start, end).points
        
        super().__init__(**kwargs)
        self.set_points(points)


class CheckMark(manim.VMobject):
    manim.Square
    def __init__(
            self,
            position = ORIGIN,
            aligned_edge = RIGHT,
            buff = 0.2,
            color = manim.ManimColor("#6beb31"),
            joint_type: manim.LineJointType | None = manim.LineJointType.ROUND,
            cap_style: manim.CapStyleType | None = manim.CapStyleType.ROUND,
            stroke_width = 6,
            **kwargs
    ):
        super().__init__(joint_type=joint_type, cap_style=cap_style, color=color, stroke_width=stroke_width, **kwargs)
        self.set_points([
            [0, 0, 0],
            [0.681639, -0.21439, 0],
            [1.270686, -0.70656, 0],
            [1.794158, -1.39545, 0],

            [1.794158, -1.39545, 0],
            [1.794158+0.706821, -1.39545+1.51986, 0],
            [1.794158+1.342334, -1.39545+3.05161, 0],
            [1.794158+2.968567, -1.39545+4.41824, 0],
        ])

        self.scale_to_fit_height(0.5)
        self.move_to(position, aligned_edge).shift(-aligned_edge * buff)

    
    def create_animation(self, **kwargs):
        def thing(t):
            CUT_OFF = 0.2
            if t < CUT_OFF: return (t/CUT_OFF) * CUT_OFF
            return CUT_OFF + cubic_out((t-CUT_OFF))*(1-CUT_OFF)
        return manim.Create(self, rate_func=thing, **kwargs)