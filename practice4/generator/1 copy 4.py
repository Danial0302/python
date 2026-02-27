from datetime import datetime
import time

# Example: Difference between two specific times
start_time = datetime(2026, 2, 27, 12, 0, 0) # Feb 27, 2026 at 12:00 PM
end_time = datetime.now()

duration = end_time - start_time
seconds = duration.total_seconds()

print(f"The difference is {seconds} seconds.")