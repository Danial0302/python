import re
text = input("Enter string: ")
result = re.findall(r'[A-Z][^A-Z]*', text)
print(result)