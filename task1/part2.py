from typing import Union


"""
A ----- B
|       |
D ----- C
"""


class Rectangle:
    def __init__(
        self,
        x1: Union[int, float],
        y1: Union[int, float],
        x2: Union[int, float],
        y2: Union[int, float],
    ) -> None:
        """Условимся именовать точки как в школьной геометрии - A, B, C, D.\n
        A - верхняя левая точка. Дальше - по часовой стрелке.
        """
        self.A = (min(x1, x2), max(y1, y2))
        self.B = (max(x1, x2), max(y1, y2))
        self.C = (max(x1, x2), min(y1, y2))
        self.D = (min(x1, x2), min(y1, y2))
        self._xmax = max(x1, x2)
        self._xmin = min(x1, x2)
        self._ymax = max(y1, y2)
        self._ymin = min(y1, y2)

    def is_overlap(self, other) -> bool:
        if (
            (self.D[0] >= other.B[0])
            or (self.B[0] <= other.D[0])
            or (self.B[1] <= other.D[1])
            or (self.D[1] >= other.B[1])
        ):
            return False
        else:
            return True

    @staticmethod
    def calculate_overlap_area(R1, R2) -> Union[float, int]:
        dx = min(R1._xmax, R2._xmax) - max(R1._xmin, R2._xmin)
        dy = min(R1._ymax, R2._ymax) - max(R1._ymin, R2._ymin)
        return dx * dy


def task(x1, y1, x2, y2, x3, y3, x4, y4) -> Union[bool, tuple[bool, float]]:
    R1 = Rectangle(x1, y1, x2, y2)
    R2 = Rectangle(x3, y3, x4, y4)
    overlap = R1.is_overlap(R2)
    if not overlap:
        return overlap
    else:
        return overlap, Rectangle.calculate_overlap_area(R1, R2)


if __name__ == "__main__":
    print(task(1, 1, 2, 2, 3, 3, 4, 4))
    print(task(0, 0, 2, 2, 1, 1, 3, 3))
