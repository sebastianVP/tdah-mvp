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

        session.close()

        transaction.rollback()

        connection.close()