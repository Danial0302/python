n = int(input())
numbers = list(map(int, input().split()))

maximum = numbers[0]
minimum = numbers[0]

for x in numbers:
    if x > maximum:
        maximum = x
    if x < minimum:
        minimum = x

for i in range(n):
    if numbers[i] == maximum:
        numbers[i] = minimum

for x in numbers:
    print(x, end=" ")