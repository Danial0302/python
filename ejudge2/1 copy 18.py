n = int(input())  # number of phone numbers
numbers = []

# Step 1: Read all numbers
for i in range(n):
    numbers.append(input().strip())

count_three_times = 0  # final answer

# Step 2: Go through each number
for num in numbers:
    if numbers.count(num) == 3:
        count_three_times += 1
        # Step 3: Replace all occurrences so we don't count it again
        for i in range(n):
            if numbers[i] == num:
                numbers[i] = ""  # mark as counted

# Step 4: Print the result
print(count_three_times)
