arr = input().split()
n = int(input())
def cycle_list(list, times):
    for i in range(times):
        for item in list:
            yield item


for x in cycle_list(arr, n):
    print(x, end = " ")