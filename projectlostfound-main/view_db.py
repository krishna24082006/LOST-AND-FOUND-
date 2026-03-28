import sqlite3

conn = sqlite3.connect("lostfound.db")
c = conn.cursor()

c.execute("SELECT * FROM items")
rows = c.fetchall()

print("Total rows:", len(rows))

for row in rows:
    print(row)

conn.close()