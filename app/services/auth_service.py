import bcrypt

from app.database.db import SessionLocal
from app.database.models import Administrator


# ============================================================
# Generar hash de contraseña
# ============================================================

def hash_password(password: str) -> str:

    hashed = bcrypt.hashpw(

        password.encode("utf-8"),

        bcrypt.gensalt()

    )

    return hashed.decode("utf-8")


# ============================================================
# Verificar contraseña
# ============================================================

def verify_password(

    password: str,

    password_hash: str

) -> bool:

    return bcrypt.checkpw(

        password.encode("utf-8"),

        password_hash.encode("utf-8")

    )


# ============================================================
# Buscar administrador por usuario
# ============================================================

def get_admin_by_username(

    username: str

):

    db = SessionLocal()

    try:

        admin = (

            db.query(Administrator)

            .filter(

                Administrator.username == username

            )

            .first()

        )

        return admin

    finally:

        db.close()


# ============================================================
# Buscar administrador por correo
# ============================================================

def get_admin_by_email(

    email: str

):

    db = SessionLocal()

    try:

        admin = (

            db.query(Administrator)

            .filter(

                Administrator.email == email

            )

            .first()

        )

        return admin

    finally:

        db.close()


# ============================================================
# Crear administrador
# ============================================================

def create_admin(

    full_name,

    username,

    email,

    password

):

    db = SessionLocal()

    try:

        # Verificar usuario

        existing = (

            db.query(Administrator)

            .filter(

                Administrator.username == username

            )

            .first()

        )

        if existing:

            raise ValueError(

                "El usuario ya existe."

            )

        # Verificar correo

        existing = (

            db.query(Administrator)

            .filter(

                Administrator.email == email

            )

            .first()

        )

        if existing:

            raise ValueError(

                "El correo ya existe."

            )

        admin = Administrator(

            full_name=full_name,

            username=username,

            email=email,

            password_hash=hash_password(password),

            is_active=True

        )

        db.add(admin)

        db.commit()

        db.refresh(admin)

        return admin.id

    finally:

        db.close()


# ============================================================
# Autenticación
# ============================================================

def authenticate(

    username,

    password

):

    db = SessionLocal()

    try:

        admin = (

            db.query(Administrator)

            .filter(

                Administrator.username == username

            )

            .first()

        )

        if admin is None:

            return None

        if not admin.is_active:

            return None

        if verify_password(

            password,

            admin.password_hash

        ):

            return admin

        return None

    finally:

        db.close()