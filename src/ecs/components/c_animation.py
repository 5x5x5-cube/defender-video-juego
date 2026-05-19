class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate


class CAnimation:
    def __init__(self, number_frames: int, animations_list: list[dict]) -> None:
        self.number_frames = number_frames
        self.animations: list[AnimationData] = []
        for anim in animations_list:
            self.animations.append(
                AnimationData(anim["name"], anim["start"],
                              anim["end"], anim["framerate"])
            )
        self.current_animation = 0
        self.current_animation_time = 0.0
        self.current_frame = self.animations[0].start


def set_animation(c_animation: CAnimation, animation_index: int):
    if c_animation.current_animation == animation_index:
        return
    c_animation.current_animation = animation_index
    c_animation.current_animation_time = 0.0
    c_animation.current_frame = c_animation.animations[animation_index].start
