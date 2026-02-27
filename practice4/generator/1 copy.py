def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n_input = int(input("Enter a number: "))
# We join the yielded strings with a comma
print(",".join(even_numbers(n_input)))