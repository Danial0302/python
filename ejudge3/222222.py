def gen(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i
s = int(input())
print(",".join(map(str, gen(s))))
