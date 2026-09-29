#task 2
from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Абстрактний клас "Фігура"."""

    @abstractmethod
    def area(self):
        """Повертає площу фігури."""

    @abstractmethod
    def perimeter(self):
        """Повертає периметр фігури."""


class Circle(Shape):
    def __init__(self, radius):
        self.__radius = radius

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def area(self):
        return self.__width * self.__height

    def perimeter(self):
        return 2 * (self.__width + self.__height)


class Square(Shape):
    def __init__(self, side):
        self.__side = side

    def area(self):
        return self.__side ** 2

    def perimeter(self):
        return 4 * self.__side


class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c):
        # Перевірка нерівності трикутника
        if (side_a + side_b <= side_c or
                side_a + side_c <= side_b or
                side_b + side_c <= side_a):
            raise ValueError("Такий трикутник не існує: порушена нерівність трикутника")
        self.__side_a = side_a
        self.__side_b = side_b
        self.__side_c = side_c

    def area(self):
        # Формула Герона
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.__side_a) * (p - self.__side_b) * (p - self.__side_c))

    def perimeter(self):
        return self.__side_a + self.__side_b + self.__side_c


if __name__ == "__main__":
    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Square(3),
        Triangle(3, 4, 5),
    ]

    for shape in shapes:
        print(f"{type(shape).__name__}: "
              f"площа = {shape.area():.2f}, "
              f"периметр = {shape.perimeter():.2f}")