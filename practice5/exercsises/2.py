import re
pattern = r'ab{2,3}'
text = input("Enter string: ")
print(re.findall(pattern, text))