n = int(input())

def gen(n):
    for i in range(1, n + 1):
        yield i**2

for x in gen(n):
    print(x)