def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Take input from user
k = int(input())

# Print Fibonacci numbers, comma-separated
print(",".join(map(str, fib(k))))

      