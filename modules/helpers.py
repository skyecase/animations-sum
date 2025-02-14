from typing import Union
from manim import ValueTracker, Scene, Mobject
import manim
import numpy as np
from modules.interpolation import cubic_in, cubic_out

def create_time_getter(scene: Scene, debug = False):
    vt = ValueTracker()
    scene.add(vt)
    def updater(vt, dt):
        vt.increment_value(dt)
        if(debug): print(vt.get_value())
    vt.add_updater(updater)
    return lambda: vt.get_value()

class UpdaterContainer(Mobject):
    def __init__(self, scene):
        self.scene = scene
        super().__init__()

    def add_updater_before(self, updater, other_updater):
        self.add_updater(updater, self.get_updaters().index(other_updater))
    
    def add_updater_after(self, updater, other_updater):
        self.add_updater(updater, self.get_updaters().index(other_updater) + 1)
    
    def remove_updater_index(self, index):
        self.remove_updater(self.get_updaters()[index])
    
    def pop_updater(self):
        self.remove_updater_index(len(self.get_updaters()) - 1)

def create_updater_container(scene):
    u = UpdaterContainer(scene)
    scene.add(u)
    return u

def sigmoid(x):
    return np.tanh(x / 0.15)



def fade_and_shift_in(mobject: manim.VMobject, shift: np.array = manim.ORIGIN, fade_rate_func = manim.linear, shift_rate_func = cubic_out, scale = 1, **kwargs):
    start_obj = mobject.copy()
    target_pos = mobject.get_center()
    target_opacity = 1
    def update_func(mobject: manim.VMobject, alpha: float):
        mobject.become(start_obj)
        mobject.scale((1 - shift_rate_func(alpha)) * scale + shift_rate_func(alpha))
        mobject.move_to(target_pos - shift * (1 - shift_rate_func(alpha)))
        mobject.set_opacity(target_opacity * fade_rate_func(alpha))
        manim.ImageMobject
    return manim.UpdateFromAlphaFunc(mobject, update_func, rate_func = manim.linear, **kwargs)

def fade_and_shift_out(mobject: manim.VMobject, shift: np.array = manim.ORIGIN, fade_rate_func = manim.linear, shift_rate_func = cubic_in, **kwargs):
    target_pos = mobject.get_center()

    leaf_mobjects = get_all_mobjects(mobject)

    target_fill_opacities = [mobj.get_fill_opacity() for mobj in leaf_mobjects]
    target_stroke_opacities = [mobj.get_stroke_opacity() for mobj in leaf_mobjects]

    def update_func(mobject: manim.VMobject, alpha: float):
        mobject.move_to(target_pos + shift * shift_rate_func(alpha))
        for i in range(len(leaf_mobjects)):
            leaf_mobjects[i].set_stroke(opacity = target_stroke_opacities[i] * (1 - fade_rate_func(alpha)))
            leaf_mobjects[i].set_fill(opacity = target_fill_opacities[i] * (1 - fade_rate_func(alpha)))
    return manim.UpdateFromAlphaFunc(mobject, update_func, rate_func = manim.linear, remover=True, **kwargs)





class PCreate(manim.Create):
    def __init__(self, mobject: manim.VMobject, lag_ratio: float = 1, introducer: bool = True, **kwargs) -> None:
        self.target_stroke_opacity = mobject.stroke_opacity
        super().__init__(mobject, lag_ratio, introducer, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        if (alpha == 0):
            self.mobject.set_stroke(opacity = 0)
        else:
            self.mobject.set_stroke(opacity = self.target_stroke_opacity)
        return super().interpolate_mobject(alpha)


def align_baseline(*tex_objects: manim.Tex):
    text_type = type(tex_objects[0])
    strings = [''.join(tex_object.tex_strings) for tex_object in tex_objects]
    center = manim.VGroup(*tex_objects).get_center()
    new_text_object = text_type(*strings).move_to(center)
    for i in range(len(tex_objects)):
        tex_objects[i].shift((new_text_object[i].get_center() - tex_objects[i].get_center())[1] * manim.UP)


def grow_between(mobject: manim.Mobject, left: manim.Mobject | np.ndarray = None, right: manim.Mobject | np.ndarray = None, **kwargs):
    if isinstance(left, manim.Mobject):
        left = left.get_right()
    if isinstance(right, manim.Mobject):
        right = right.get_left()
    
    if right is None:
        shift = mobject.get_center() - left
    elif left is None:
        shift = mobject.get_center() - right
    else:
        shift = mobject.get_center() - (right + left) / 2
    return manim.FadeIn(mobject, scale = 0, shift = shift, **kwargs)


def shrink_between(mobject: manim.Mobject, left: manim.Mobject | np.ndarray = None, right: manim.Mobject | np.ndarray = None, **kwargs):
    if isinstance(left, manim.Mobject):
        left = left.get_right()
    if isinstance(right, manim.Mobject):
        right = right.get_left()
    
    if right is None:
        shift = mobject.get_center() - left
    elif left is None:
        shift = mobject.get_center() - right
    else:
        shift = mobject.get_center() - (right + left) / 2
    return manim.FadeOut(mobject, scale = 0, shift = -shift, **kwargs)


def morph_text(
    text_1: manim.Mobject,
    text_2: manim.Mobject,
    map: Union[dict, list],
    ignore_1: list[int] = [],
    ignore_2: list[int] = [],
    **global_kwargs
):
    if type(map) == list: # If map is a list, convert it to a dict
        new_map = {}
        for i in range(len(map)):
            if map[i] != None:
                new_map[i] = map[i]
        map = new_map
        del new_map

    len_1 = len(text_1)
    len_2 = len(text_2)

    # Parallel array representation of the map
    processed_1 = list(map.keys())
    processed_1.sort() # Just in case
    processed_2 = []

    animations = []
    for key in map:
        kwargs = {}
        swap_index = map[key]
        if type(map[key]) == list:
            # If it maps to a list, then the first index is the int, and the second is some kwargs
            swap_index = map[key][0]
            kwargs = map[key][1]
        processed_2.append(swap_index)
        animations.append(manim.Transform(text_1[key], text_2[swap_index], **{**global_kwargs, **kwargs}))

    last_processed = -1
    for text_1_index in range(len_1):
        if text_1_index in processed_1:
            last_processed = processed_1.index(text_1_index)
        elif text_1_index not in ignore_1:
            last_text_2 = text_2[processed_2[last_processed]] if last_processed != -1 else None
            next_text_2 = text_2[processed_2[last_processed + 1]] if last_processed + 1 < len(processed_1) else None
            animations.append(shrink_between(text_1[text_1_index], last_text_2, next_text_2, **global_kwargs))
    
    last_processed = -1
    for text_2_index in range(len_2):
        if text_2_index in processed_2:
            last_processed = processed_2.index(text_2_index)
        elif text_2_index not in ignore_2:
            last_text_1 = text_1[processed_1[last_processed]] if last_processed != -1 else None
            next_text_1 = text_1[processed_1[last_processed + 1]] if last_processed + 1 < len(processed_2) else None
            animations.append(grow_between(text_2[text_2_index], last_text_1, next_text_1, **global_kwargs))

    return manim.AnimationGroup(*animations)




def get_wait_function(scene: manim.Scene, map: list = None, show_numbers: bool = False, default_wait_time = 1):
    """
    This function takes in list of wait times and returns a function. When you call the returned function
    for the nth time, your scene will wait for the amount specified in the nth index of the list.

    This is useful for when you have some updater in the background, so you can't just freeze a frame in post.
    Rather than searching for your scene for all the wait times, you can adjust them in the list.

    If `show_numbers` is true, the index of each call to the returned function will appear in the corner
    of the frame when it is called, so you can know which index to modify.
    """
    if map == None: map = []
    current_index = 0

    def wait_function():
        nonlocal current_index

        try: wait_time = map[current_index]
        except: wait_time = default_wait_time

        if wait_time == 0:
            current_index += 1
            return

        if show_numbers:
            tex = manim.MathTex(str(current_index))
            rect = manim.SurroundingRectangle(tex, manim.WHITE, fill_color = manim.BLACK, fill_opacity = 1)
            obj = manim.VGroup(rect, tex).move_to(scene.camera.frame_center + manim.LEFT * scene.camera.frame_width/2 + manim.UP * scene.camera.frame_height/2, manim.UP + manim.LEFT)
            scene.add(obj)

        scene.wait(wait_time)

        if show_numbers:
            scene.remove(obj)
        
        current_index += 1
    
    return wait_function






def normalize_point_speed(points: list[np.array], segment_length = 0.1):
    """
    This function takes in points from a VMobject and returns a new points array
    such that each line segment is (approximately) the same length.
    This function assumes that everything is a line segment -- there are no curves.

    Parameters:
        points: list[np.array] - The points of the VMobject
        segment_length[float] - The desired length of each segment
    """
    new_points = []
    new_remaining_length = segment_length
    new_start = points[0]
    for i in range(int(len(points) / 4)):
        start_point = points[4 * i]
        end_point = points[4 * i + 3]
        length = np.linalg.norm(end_point - start_point)
        unit_vector = (end_point - start_point) / length
        remaining_length = length

        first_time = True
        while remaining_length > new_remaining_length:
            new_end = start_point + unit_vector * new_remaining_length if first_time else (new_start + unit_vector * segment_length)
            first_time = False

            new_points.append(new_start)
            new_points.append(new_start * 2/3 + new_end * 1/3)
            new_points.append(new_start * 1/3 + new_end * 2/3)
            new_points.append(new_end)

            remaining_length -= new_remaining_length
            new_remaining_length = segment_length
            new_start = new_end

        new_remaining_length = new_remaining_length - remaining_length
    
    new_points.append(new_end)
    new_points.append(new_end * 2/3 + points[-1] * 1/3)
    new_points.append(new_end * 1/3 + points[-1] * 2/3)
    new_points.append(points[-1])


    return new_points




class CustomLaggedStart(manim.LaggedStart):
    """
    Rather than a single lag ratio, you pass in a function which
    takes in the index of the animation and the total number of animations
    and returns the desired delay for that particular animation.
    """
    def __init__(
        self,
        *animations: manim.Animation,
        lag_ratio_function: callable = lambda i, total: 0.02,
        **kwargs,
    ):
        self.lag_ratio_function = lag_ratio_function
        super().__init__(*animations, **kwargs)
    
    def build_animations_with_timings(self) -> None:
        """Creates a list of triplets of the form (anim, start_time, end_time)."""
        run_times = np.array([anim.run_time for anim in self.animations])
        num_animations = run_times.shape[0]
        dtype = [("anim", "O"), ("start", "f8"), ("end", "f8")]
        self.anims_with_timings = np.zeros(num_animations, dtype=dtype)
        self.anims_begun = np.zeros(num_animations, dtype=bool)
        self.anims_finished = np.zeros(num_animations, dtype=bool)
        if num_animations == 0:
            return

        # lags = run_times[:-1] * np.array(self.lag_ratio_map)
        lags = np.array([run_times[i] * self.lag_ratio_function(i, len(run_times)) for i in range(len(run_times)-1)])
        self.anims_with_timings["anim"] = self.animations
        self.anims_with_timings["start"][1:] = np.add.accumulate(lags)
        self.anims_with_timings["end"] = self.anims_with_timings["start"] + run_times



def get_all_mobjects(mobject: manim.VMobject) -> list[manim.VMobject]:
    """
    Returns a flattened list of all leaf mobjects.
    """
    mobjects = []
    if mobject.points is not None:
        mobjects.append(mobject)
    if mobject.submobjects != None and len(mobject.submobjects) != 0:
        for submobject in mobject.submobjects:
            mobjects += get_all_mobjects(submobject)
    return mobjects


def highlight(mobject: manim.VMobject, color=None):
    mobjects = get_all_mobjects(mobject)

    for mobj in mobjects:
        mobj.scale(1.1).set_stroke(width=1.5)
        if color: mobj.set_color(color)
    
    return mobject


def highlight_animation(mobject: manim.VMobject, color=None, **kwargs):
    mobjects = get_all_mobjects(mobject)

    for mobj in mobjects:
        if mobj.stroke_width == None:
            mobj.set_stroke(width=0)

    return mobject.animate(**kwargs).become(highlight(mobject.copy(), color))



def rotate_points(mobj: manim.Mobject, num: int):
    points_list = list(mobj.points)
    mobj.points = np.array(points_list[num:] + points_list[:num])
    return mobj