import sqlite3
import os

db_path = 'faraiz.db'
if not os.path.exists(db_path):
    print(f"{db_path} does not exist")
else:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(f"Tables: {cur.fetchall()}")
    conn.close()
