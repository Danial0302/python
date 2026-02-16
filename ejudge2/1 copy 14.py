n = int(input())
numbers = list(map(int, input().split()))

max_count = 0
result = numbers[0]

for i in range(n):
    count = 0
    for j in range(n):
        if numbers[i] == numbers[j]:
            count += 1

    if count > max_count or (count == max_count and numbers[i] < result):
        max_count = count
        result = numbers[i]

print(result)
