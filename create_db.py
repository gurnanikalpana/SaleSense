import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    price REAL
)
""")

# Sample categories
categories = ["Electronics", "Clothing", "Books", "Home", "Sports"]

# Insert random sample data
for _ in range(100):
    date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    category = random.choice(categories)
    price = round(random.uniform(10.0, 500.0), 2)
    cursor.execute("INSERT INTO sales (date, category, price) VALUES (?, ?, ?)", (date, category, price))

conn.commit()
conn.close()

print("Database created with sample data!")
