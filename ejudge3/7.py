class Reverse:
    def __init__(self, data):
        self.data = data
        self.i = len(data) - 1
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i < 0:
            raise StopIteration
        ch = self.data[self.i]
        self.i -= 1
        return ch
s = input()
print("".join(Reverse(s)))