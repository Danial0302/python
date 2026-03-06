import re
import json

text = open("raw.txt").read()
prices = re.findall(r'\d+\.\d{2}', text)
products = [p.strip() for p in re.findall(r'([A-Za-z ]+)\s+\d+\.\d{2}', text)]
total = re.search(r'Total[: ]+\$?(\d+\.\d{2})', text, re.IGNORECASE)
total = total.group(1) if total else str(sum(map(float, prices)))
date = re.findall(r'\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}', text)
time = re.findall(r'\d{2}:\d{2}', text)
date = date[0] if date else None
time = time[0] if time else None
payment = re.search(r'Cash|Card|Visa|MasterCard|Credit|Debit', text, re.IGNORECASE)
payment = payment.group(0) if payment else None

print(json.dumps({
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment
}, indent=4))