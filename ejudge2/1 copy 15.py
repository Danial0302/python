n = int(input())
surnames = []
for i in range(n):
    s = input().strip()
    surnames.append(s)
unique_surnames = set(surnames)
count = len(unique_surnames)
print(count)
