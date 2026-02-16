n = int(input())
numbers = list(map(int, input().split()) )
maximum = numbers[0]
pos = 1
for i in range(1, n):
    if numbers[i] > maximum:
        maximum = numbers[i]
        pos = i + 1
print(pos)