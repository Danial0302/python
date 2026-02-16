n = int(input())
numbers = list(map(int, input().split()))
seen = set()
for x in numbers:
    if x in seen:
        print("No", end = " ")
    else:
        print("Yes", end = " ")
        seen.add(x)