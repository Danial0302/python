def gen(n):
    for i in range(n + 1):
        yield (2 ** i)
s = int(input())
for x in gen(s):
    print(x, end = " ")