def square_generator(N):
    for i in range(N):
        yield i ** 2

# Usage
for num in square_generator(5):
    print(num)  # Output: 0, 1, 4, 9, 16