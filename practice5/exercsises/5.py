import re
pattern = r'a.*b$'
text = input("Enter string: ")
print(re.findall(pattern, text))