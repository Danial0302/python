# class_definition.py

class Robot:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def introduce_self(self):
        print(f"My name is {self.name} and my color is {self.color}")


r1 = Robot("Tom", "red")
r1.introduce_self()
