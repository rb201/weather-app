import os
import sqlite3

CWD = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(CWD, "weather.db")
SCHEMA_FILE = os.path.join(CWD, "schema.sql")

with open(SCHEMA_FILE, 'r') as sf:
    SQL_QUERY = sf.read()

conn = sqlite3.connect(DATABASE)

cur = conn.cursor()

cur.executescript(SQL_QUERY)

conn.close()