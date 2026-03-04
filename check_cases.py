import sqlite3
import os

db_path = 'faraiz.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT * FROM cases LIMIT 5;")
print(f"Cases (first 5): {cur.fetchall()}")
conn.close()
