# test_pg.py

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="tdah",
    user="admin",
    password="admin123"
)

print("✅ Conectado")

conn.close()