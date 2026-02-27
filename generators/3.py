def divisible_by_12(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# Example usage for n=50
for num in divisible_by_12(50):
    print(num, end=" ") # Output: 0 12 24 36 48