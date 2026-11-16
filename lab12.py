# ISM2411 - Lab 12: Reading and Writing CSV Files
# Run from the repo folder:  python3 lab12.py

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"


# ----- Exercise 1: Setup -----
# Make sure the data file exists and opens before doing anything else.
print("=== Exercise 1: Setup ===")
try:
    with open(SALES_FILE, "r") as f:
        f.readline()
    print(SALES_FILE, "opened successfully.")
except FileNotFoundError:
    print("ERROR: could not find", SALES_FILE)
    print("Download sales.csv from the assignment page and put it in the data/ folder,")
    print("then run this script again from the ism2411-lab12 folder.")
    raise SystemExit(1)
print()


# ----- Exercise 2: Read with csv.reader -----
# Every row comes back as a list of strings (even the numbers).
print("=== Exercise 2: Read every row ===")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
print()


# ----- Exercise 3: Skip the header -----
print("=== Exercise 3: Header separate from data ===")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    header = next(reader)  # first row is the header
    data_rows = []
    for row in reader:
        data_rows.append(row)

print("Header:", header)
for row in data_rows:
    print(row)
print()


# ----- Exercise 4: Calculate revenue -----
print("=== Exercise 4: Revenue per row ===")
total_revenue = 0
for row in data_rows:
    product = row[0]
    price = float(row[1])
    quantity = int(row[2])
    line_total = price * quantity
    total_revenue += line_total
    print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")
print()


# ----- Exercise 5: Write a cleaned CSV -----
# Only keep rows where the total is over $100.
# newline="" stops Windows from adding blank lines between rows.
print("=== Exercise 5: Write cleaned.csv ===")
rows_written = 0
with open(CLEANED_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in data_rows:
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        if line_total > 100:
            writer.writerow([row[0], f"{price:.2f}", quantity, f"{line_total:.2f}"])
            rows_written += 1
print(f"Wrote {rows_written} of {len(data_rows)} rows to {CLEANED_FILE}")
print()


# ----- Exercise 6: Use csv.DictReader -----
# csv.reader is fine for small files when you know the column order.
# csv.DictReader is clearer and safer when columns might move, since you use the column names.
print("=== Exercise 6: DictReader ===")
dict_total = 0
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue (DictReader): ${dict_total:.2f}")
if round(dict_total, 2) == round(total_revenue, 2):
    print("Matches the Exercise 4 total.")
else:
    print("Does NOT match the Exercise 4 total!")
print()


# ----- Exercise 7: Revenue by product -----
# Products can show up more than once, so add to what is already there.
print("=== Exercise 7: Revenue by product ===")
revenue_by_product = {}
for row in data_rows:
    product = row[0]
    line_total = float(row[1]) * int(row[2])
    if product in revenue_by_product:
        revenue_by_product[product] += line_total
    else:
        revenue_by_product[product] = line_total

for product in sorted(revenue_by_product):
    print(f"{product}: ${revenue_by_product[product]:.2f}")
print()


# ----- Exercise 8: Append to a run log -----
# Mode "a" adds to the end of the file instead of overwriting it.
print("=== Exercise 8: Run log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as f:
    f.write(f"{timestamp} - Total revenue: ${total_revenue:.2f}\n")
print("Added an entry to", LOG_FILE)

with open(LOG_FILE, "r") as f:
    entries = f.readlines()
print(f"{LOG_FILE} now has {len(entries)} entries:")
for line in entries:
    print("  " + line.strip())
