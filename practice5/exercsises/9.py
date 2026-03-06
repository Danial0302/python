import re
text = input("Enter string: ")
result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
print(result)