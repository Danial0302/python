# args_kwargs.py

# *args example (multiple positional arguments)
def add_numbers(*args):
    total = 0
    for num in args:
        total += num
    return total

print(add_numbers(1, 2, 3, 4))


# **kwargs example (multiple keyword arguments)
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(key + ":", value)

print_info(name="Tom", age=25, city="London")
