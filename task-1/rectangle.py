from functools import reduce
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return reduce(lambda x, y: x * y, [length, width])


length = int(input("Enter a length :"))
width = int(input("Enter a Width :"))
rectangle_instance = Rectangle(length, width)
result = rectangle_instance.calculate_area()
print(f"Area of Rectangle: {result}")