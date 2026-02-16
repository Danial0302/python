n = int(input())
numbers = list(map(int, input().split()))

for i in range(n):
    numbers[i] = numbers[i] * numbers[i]

print(*numbers)




n = int(input())
numbers = list(map(int, input().split()))

print(*[x*x for x in numbers])
