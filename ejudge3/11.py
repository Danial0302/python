import json

def patch_dict(source, patch):
    for key in patch:

        if patch[key] is None:
            if key in source:
                del source[key]

        elif key in source and type(source[key]) == dict and type(patch[key]) == dict:
            patch_dict(source[key], patch[key])

        else:
            source[key] = patch[key]

    return source


source = json.loads(input())
patch = json.loads(input())

result = patch_dict(source, patch)

print(json.dumps(result, sort_keys=True, separators=(",", ":")))