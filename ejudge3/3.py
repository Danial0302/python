def generator(x):
    for i in range(x+1):
        if i%3==0 and i%4==0:
            print(i,end=" ")
a=int(input())
generator(a)