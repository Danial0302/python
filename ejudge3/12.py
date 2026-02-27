import json

def find_diffs(obj1, obj2, path=""):
    diffs = []
    keys = set(obj1.keys()) | set(obj2.keys())
    for key in keys:
        full_path = f"{path}.{key}" if path else key
        val1 = obj1.get(key, "<missing>")
        val2 = obj2.get(key, "<missing>")

        if isinstance(val1, dict) and isinstance(val2, dict):
            diffs.extend(find_diffs(val1, val2, full_path))
        elif val1 != val2:
            # Serialize values as compact JSON literals
            v1 = json.dumps(val1, separators=(",", ":")) if val1 != "<missing>" else "<missing>"
            v2 = json.dumps(val2, separators=(",", ":")) if val2 != "<missing>" else "<missing>"
            diffs.append(f"{full_path} : {v1} -> {v2}")
    return diffs

# Read input
obj1 = json.loads(input())
obj2 = json.loads(input())

# Find differences
differences = find_diffs(obj1, obj2)

# Output
if differences:
    for line in sorted(differences):
        print(line)
else:
    print("No differences")