from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Iterable


@dataclass
class Point:
    x: float
    y: float
    repr = "+"
    context: Shape


def get_vector_destination_coordinates(starting_point: Point, angle: float, length: float):
    angle_rad = math.radians(angle)
    x_offset = length * math.cos(angle_rad)
    y_offset = length * math.sin(angle_rad)
    return Point(starting_point.x + x_offset, starting_point.y + y_offset, starting_point.context)


class Drawable(ABC):
    @abstractmethod
    def get_points(self) -> List[Point]:
        pass


class Shape(ABC):
    name: str
    _accuracy = 0.1

    @abstractmethod
    def get_perimeter(self):
        pass

    @abstractmethod
    def get_area(self):
        pass

    def __repr__(self):
        return self.name


class Rectangle(Shape, Drawable):
    name = "Rectangle"

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h

    def get_perimeter(self):
        return (self.w + self.h) * 2

    def get_area(self):
        return self.w * self.h

    def __repr__(self):
        rpr = super(Rectangle, self).__repr__()
        return f"{rpr} (w={self.w}, h={self.h})"

    def get_points(self) -> List[Point]:
        return [Point(0, 0, self), Point(self.w, 0, self), Point(0, self.h, self), Point(self.w, self.h, self)]


class Circle(Shape, Drawable):
    name = "Circle"

    def __init__(self, r: int):
        self.r = r

    def get_perimeter(self):
        return math.pi * 2 * self.r

    def get_area(self):
        return math.pi * self.r ** 2

    def __repr__(self):
        rpr = super(Circle, self).__repr__()
        return f"{rpr} (r={self.r})"

    def get_points(self) -> List[Point]:
        return [Point(self.r, self.r, self),
                Point(self.r, 0, self),
                Point(0, self.r, self),
                Point(self.r, self.r * 2, self),
                Point(self.r * 2, self.r, self)]


class Triangle(Shape, Drawable):
    name = "Triangle"

    def __init__(self, A: float, b: int, c: int):  # noqa
        self.A = A
        self._A_radians = math.radians(A)
        self.b = b
        self.c = c

    def get_perimeter(self):
        return math.sqrt(self.b ** 2 + self.c ** 2 - 2 * self.b * self.c * math.cos(self._A_radians)) + self.b + self.c

    def get_area(self):
        return self.b * self.c * math.sin(self._A_radians) / 2

    def __repr__(self):
        rpr = super(Triangle, self).__repr__()
        return f"{rpr} (A={self.A} b={self.b} c={self.c})"

    def get_points(self) -> List[Point]:
        starting_point = Point(0, 0, self)
        pts = []
        pts.append(starting_point)
        pts.append(get_vector_destination_coordinates(starting_point, self.A, self.b))
        pts.append(
            get_vector_destination_coordinates(starting_point, 0, self.c))  # assumes that "c" is always on X axis
        return pts


def shapes_perimeter(shapes: Iterable[Shape]) -> float:
    return sum([s.get_perimeter() for s in shapes])


def shapes_area(shapes: Iterable[Shape]) -> float:
    return sum([s.get_area() for s in shapes])


class TerminalCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._canvas = self._empty_canvas(self.width, self.height)

    @staticmethod
    def _empty_canvas(w: int, h: int):
        return [list(" " * (w + 1)) for _ in range(0, h + 1)]

    def add_point(self, point: Point):
        try:

            line = self._canvas[len(self._canvas) - int(point.y) - 1]
            line[int(point.x)] = point.repr
        except IndexError:
            raise RuntimeError(f"{self.__class__} out of bounds for {point.context}")

    def add_points(self, points: List[Point]):
        for p in points:
            self.add_point(p)

    def draw(self):
        for _ord in self._canvas:
            for each in _ord:
                print(each, end="  ")
            print()

    def clear(self):
        self._canvas = self._empty_canvas(self.width, self.height)

    @classmethod
    def lazy_draw(cls, points: List[Point]):
        max_h = max(p.y for p in points)
        max_w = max(p.x for p in points)
        _canvas = cls(math.ceil(max_w), math.ceil(max_h))
        _canvas.add_points(points)
        _canvas.draw()


if __name__ == '__main__':
    triangle = Triangle(21, 44, 40)
    circle = Circle(5)
    rect = Rectangle(6, 9)
    shapes_list = triangle, circle, rect
    print("Shapes: ", shapes_list)
    print("Shapes perimeter = ", shapes_perimeter(shapes_list))
    print("Shapes area = ", shapes_area(shapes_list))
    print(triangle)
    TerminalCanvas.lazy_draw(triangle.get_points())
    print(circle)
    TerminalCanvas.lazy_draw(circle.get_points())
    print(rect)
    TerminalCanvas.lazy_draw(rect.get_points())
