n = int(input())
numbers = list(map(int, input().split()))

numbers.sort(reverse=True)

for x in numbers:
    print(x, end=" ")