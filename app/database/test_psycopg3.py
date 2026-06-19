# test_psycopg3.py

import psycopg

conn = psycopg.connect(
    "host=127.0.0.1 port=5432 dbname=tdah user=admin password=admin123"
)

print("✅ Conectado con psycopg3")

conn.close()