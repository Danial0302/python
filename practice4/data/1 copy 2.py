import datetime

# Get current time with microseconds
now = datetime.datetime.now()

# Create a new object with microsecond set to 0
now_without_ms = now.replace(microsecond=0)

print(f"With microseconds:    {now}")
print(f"Without microseconds: {now_without_ms}")