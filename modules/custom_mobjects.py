from manim import VGroup, ORIGIN, Scene, Line, UP, RIGHT, DEFAULT_STROKE_WIDTH, LaggedStart
import manim
import numpy as np
import math
from modules.helpers import cubic_out

class FullscreenAxes(VGroup):
    def __init__(
        self,
        scene: Scene,
        origin: np.ndarray = ORIGIN,
        scale: list[float] = [1, 1],
        tick_length: float = 0.25,
        tick_spacing: list[float] = [1, 1],
        stroke_width: float = DEFAULT_STROKE_WIDTH,
        **kwargs,
    ):
        VGroup.__init__(self, **kwargs)
        top = (scene.camera.frame_center + scene.camera.frame_height / 2)[1]
        bottom = top - scene.camera.frame_height
        right = (scene.camera.frame_center + scene.camera.frame_width / 2)[0]
        left = right - scene.camera.frame_width
        
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


class CreateFullscreenAxes(manim.Animation):
    def __init__(self, axes: FullscreenAxes, **kwargs):
        self.axes = axes
        super().__init__(self, **kwargs)
    
    def begin(self):
        self.interpolate(0)

    def interpolate(self, alpha):
        time = alpha

        self.axes.x_line.points


def create_axes(scene: Scene, axes: FullscreenAxes):
    for tick in [*axes.x_ticks, *axes.y_ticks]:
        tick.save_state()
        tick.scale(0)
    
    return LaggedStart(
        manim.AnimationGroup(
            manim.Create(axes.x_line, rate_func=manim.linear, run_time=0.5),
            LaggedStart(
                *[tick.animate(rate_func=cubic_out, run_time=0.5).restore() for tick in axes.x_ticks],
                lag_ratio=0.1
            ),
            lag_raio=0.4
        ),
        manim.AnimationGroup(
            manim.Create(axes.y_line, rate_func=manim.linear, run_time=0.5 * scene.camera.frame_height / scene.camera.frame_width),
            LaggedStart(
                *[tick.animate(rate_func=cubic_out, run_time=0.5).restore() for tick in axes.y_ticks],
                lag_ratio=0.1
            ),
            lag_ratio=0.4
        ),
        lag_ratio=0.2
    )