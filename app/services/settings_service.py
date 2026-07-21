from sqlalchemy import func

from app.database.db import SessionLocal

from app.database.models import Setting

def get_setting(key):

    db = SessionLocal()

    try:

        setting = (

            db.query(

                Setting

            )

            .filter(

                Setting.key == key

            )

            .first()

        )

        if setting is None:

            return None

        return setting.value

    finally:

        db.close()

def get_all_settings():

    db = SessionLocal()

    try:

        settings = (

            db.query(

                Setting

            )

            .order_by(

                Setting.key

            )

            .all()

        )

        return settings

    finally:

        db.close()

def update_setting(

    key,

    value

):

    db = SessionLocal()

    try:

        setting = (

            db.query(

                Setting

            )

            .filter(

                Setting.key == key

            )

            .first()

        )

        if setting is None:

            return False

        setting.value = value

        db.commit()

        return True

    finally:

        db.close()

def create_setting(

    key,

    value,

    description=""

):

    db = SessionLocal()

    try:

        exists = (

            db.query(

                Setting

            )

            .filter(

                Setting.key == key

            )

            .first()

        )

        if exists:

            return False

        setting = Setting(

            key=key,

            value=value,

            description=description

        )

        db.add(setting)

        db.commit()

        return True

    finally:

        db.close()

def delete_setting(

    key

):

    db = SessionLocal()

    try:

        setting = (

            db.query(

                Setting

            )

            .filter(

                Setting.key == key

            )

            .first()

        )

        if setting is None:

            return False

        db.delete(setting)

        db.commit()

        return True

    finally:

        db.close()

def get_settings_dict():

    db = SessionLocal()

    try:

        rows = db.query(

            Setting

        ).all()

        config = {}

        for row in rows:

            config[row.key] = row.value

        return config

    finally:

        db.close()

def search_settings(

    text

):

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Setting

            )

            .filter(

                Setting.key.ilike(

                    f"%{text}%"

                )

            )

            .all()

        )

        return rows

    finally:

        db.close()