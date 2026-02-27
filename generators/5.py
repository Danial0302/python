def countdown(n):
    while n >= 0:
        yield n
        n -= 1

# Usage
for count in countdown(5):
    print(count) # Output: 5, 4, 3, 2, 1, 0