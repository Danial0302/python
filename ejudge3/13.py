import json
def resolve_query(data, query):
    current = data
    i = 0
    try:
        while i < len(query):
            if query[i] != '.':
                i += 1
            elif query[i] == '[':
                i += 1
                num = ""
                while query[i] != ']':
                    num += query[i]
                    
