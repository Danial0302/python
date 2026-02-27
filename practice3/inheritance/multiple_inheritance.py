# multiple_inheritance.py

class Flyer:
    def fly(self):
        print("I can fly!")

class Swimmer:
    def swim(self):
        print("I can swim!")

class Duck(Flyer, Swimmer):
    pass

d = Duck()
d.fly()
d.swim()
