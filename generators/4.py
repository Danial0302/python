def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# Testing with a for loop
print("Testing range 3 to 6:")
for val in squares(3, 6):
    print(val) # Output: 9, 16, 25, 36