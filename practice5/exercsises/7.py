text = input("Enter snake_case string: ")
components = text.split('_')
camel = components[0] + ''.join(x.title() for x in components[1:])
print(camel)