# class_variables.py

class Robot:
    species = "Android"  # class variable

    def __init__(self, name):
        self.name = name  # instance variable

r1 = Robot("Tom")
r2 = Robot("Alice")

print(r1.name, "-", r1.species)
print(r2.name, "-", r2.species)

# Changing class variable
Robot.species = "Cyborg"
print(r1.name, "-", r1.species)
print(r2.name, "-", r2.species)
