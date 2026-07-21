from sqlalchemy import text

from app.database.db import engine


def create_settings_table():

    sql = """

    DROP TABLE IF EXISTS settings;

    CREATE TABLE settings(

        id SERIAL PRIMARY KEY,

        key VARCHAR(120) UNIQUE NOT NULL,

        value TEXT NOT NULL,

        description TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );

    """

    with engine.begin() as connection:

        connection.execute(text(sql))

    print("✅ Tabla settings creada correctamente.")


if __name__ == "__main__":

    create_settings_table()