import math
import typing


class Navigation:
    def __init__(self,
                 locations: typing.List[typing.Tuple[float, float]],
                 paths: typing.List[typing.List[int]]):
        self.locations: typing.List[typing.Tuple[float, float]] = locations
        self.paths: typing.List[typing.List[int]] = paths

    def closest_location(self,
                         location: typing.Tuple[float, float]) -> int:
        min_dist2 = math.inf
        closest = None
        for i, l in enumerate(self.locations):
            dist2 = (l[0] - location[0]) ** 2 + (l[1] - location[1]) ** 2
            if dist2 < min_dist2:
                closest = i
                min_dist2 = dist2
        return closest

    def get_path(self,
                 src: typing.Tuple[float, float],
                 dst: typing.Tuple[float, float]) -> typing.List[typing.Tuple[float, float]]:
        src_index = self.closest_location(location=src)
        dst_index = self.closest_location(location=dst)
        current = src_index
        path_indexes = [current]
        while current is not None and current != dst_index:
            current = self.paths[current][dst_index]
            path_indexes.append(current)
        return [self.locations[step_index] for step_index in path_indexes]
