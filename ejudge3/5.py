y = int(input())
def generator(n):
    for i in range(n , -1 , -1):
        yield i
for x in generator(y):
    print(x)
   
#def generator(n):
    #while n >= 0:
       # yield n
       # n -= 1

#n = int(input())
#for x in generator(n):
   # print(x)