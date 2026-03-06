import re
pattern = r'[a-z]+_[a-z]+'
text = input("Enter string: ")
print(re.findall(pattern, text))