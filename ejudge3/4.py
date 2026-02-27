x, y = list(map(int, input().split()))
def squares(a, b):
    for i in range(a , b + 1):
        yield i * i
for k in squares(x, y):
    print(k)