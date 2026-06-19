from app.database.db import engine
from app.database.models import Base

print("Creando tablas...")

Base.metadata.create_all(bind=engine)

print("Database initialized")