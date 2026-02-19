# super_function.py

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # call parent constructor
        self.breed = breed

    def speak(self):
        super().speak()  # call parent method
