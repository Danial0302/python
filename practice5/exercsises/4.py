import re
pattern = r'[A-Z][a-z]+'
text = input("Enter string: ")
print(re.findall(pattern, text))