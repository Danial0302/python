import re
text = input("Enter string: ")
result = re.sub(r'[ ,.]', ':', text)
print(result)