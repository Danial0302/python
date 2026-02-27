# method_overriding.py

class Animal:
    def speak(self):
        print("I make a sound")

class Cat(Animal):
    def speak(self):
        print("Meow!")  # override parent method

a = Animal()
a.speak()  # parent method
c = Cat()
c.speak()  # overridden method
