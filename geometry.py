class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Rectangle:

    toto = 3

    def __init__(self, width=0, length=0, origin:Point = Point()):
        self._width = width
        self._length = length
        self.origin = origin

    def perimeter(self):
        return 2 * (self._width + self._length)

    def area(self):
        return self._width * self._length

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value < 0:
            raise ValueError
        else:
            self._width = value

    def move(self, x, y):
        self.origin.x = x
        self.origin.y = y

    def __eq__(self, other):
        return self.width == other.width and self._length == other._length and self.origin == other.origin

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Rectangle {self._width} {self._length} {self.origin}"

class Square(Rectangle):

    def __init__(self, side):
        super(Rectangle).__init__(side, side)

