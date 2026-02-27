# inheritance_basics.py

class Animal:
    def speak(self):
        print("I make a sound")

class Dog(Animal):  # Dog inherits from Animal
    def bark(self):
        print("Woof!")

d = Dog()
d.speak()  # inherit
