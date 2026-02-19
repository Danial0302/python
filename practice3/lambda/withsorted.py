# lambda_with_sorted.py

students = [
    {"name": "Tom", "grade": 85},
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 78}
]

# Sort by grade
sorted_students = sorted(students, key=lambda student: student["grade"])

print(sorted_students)
