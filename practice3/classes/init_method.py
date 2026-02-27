# init_method.py

class Robot:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def show_info(self):
        print(f"{self.name} weighs {self.weight} kg")


r1 = Robot("Tom", 30)
r1.show_info()
