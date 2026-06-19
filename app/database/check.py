import psycopg

print(psycopg.__version__)

conn = psycopg.connect(
    "postgresql://admin:admin123@localhost:5435/tdah"
)

print("OK")

conn.close()