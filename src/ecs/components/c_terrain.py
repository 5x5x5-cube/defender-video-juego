class CTerrain:
    def __init__(self, points: list[tuple[int, int]]) -> None:
        self.points = points

    def surface_height_at(self, x: float) -> float:
        if not self.points:
            return 0
        if x <= self._first_point_x():
            return self._first_point_y()
        if x >= self._last_point_x():
            return self._last_point_y()
        return self._interpolate_height(x)

    def _first_point_x(self) -> int:
        return self.points[0][0]

    def _first_point_y(self) -> int:
        return self.points[0][1]

    def _last_point_x(self) -> int:
        return self.points[-1][0]

    def _last_point_y(self) -> int:
        return self.points[-1][1]

    def _interpolate_height(self, x: float) -> float:
        for i in range(len(self.points) - 1):
            x0, y0 = self.points[i]
            x1, y1 = self.points[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0) if x1 != x0 else 0
                return y0 + (y1 - y0) * t
        return self._last_point_y()
