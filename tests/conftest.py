import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.db import DATABASE_URL

# -----------------------------------------
# Crear Engine
# -----------------------------------------

engine = create_engine(
    DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------------
# Fixture principal
# -----------------------------------------

@pytest.fixture
def db_session():

    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    try:

        yield session

    finally:

        # 1. Primero revertimos los cambios en la base de datos de forma segura
        transaction.rollback()
        
        # 2. Ahora sí, cerramos los canales de comunicación limpiamente
        session.close()
        connection.close()