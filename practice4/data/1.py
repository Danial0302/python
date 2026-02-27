from datetime import date, timedelta

current_date = date.today()
five_days_ago = current_date - timedelta(days=5)

print(f"Today: {current_date}")
print(f"Five days ago: {five_days_ago}")