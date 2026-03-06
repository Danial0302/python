import re
pattern = r'ab*'
text = input("Enter string: ")
print(re.findall(pattern, text))