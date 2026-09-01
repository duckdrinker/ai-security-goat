"""
Mitigated: an untrusted dataset value reaches a SQL sink, but via a properly
parameterized query -- parameterizedQuery_isNotFlagged.
"""
import sqlite3
from datasets import load_dataset

ds = load_dataset("attacker/poison-ds")
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

for row in ds:
    cursor.execute("SELECT * FROM records WHERE external_id = ?", (row["id"],))
