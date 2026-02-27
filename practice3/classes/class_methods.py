# class_methods.py

class Robot:
    robot_count = 0

    def __init__(self, name):
        self.name = name
        Robot.robot_count += 1

    @classmethod
    def show_robot_count(cls):
        print(f"Total robots created: {cls.robot_count}")


r1 = Robot("Tom")
r2 = Robot("Alice")
Robot.show_robot_count()
