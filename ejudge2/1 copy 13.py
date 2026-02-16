n = int(input())
i = 1
cnt = 0
for i in range(1, n+1):
    if n % i == 0:
        cnt += 1

if cnt == 2:
    print("Yes")
else:
    print("No")


    import math

x = int(input())

if x <= 1:
    print("No")
else:
    is_prime = True
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            is_prime = False
            break
    
    if is_prime:
        print("Yes")
    else:
        print("No")
