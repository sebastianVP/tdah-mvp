from app.database.db import engine

with engine.connect() as conn:
    print("CONEXION OK")