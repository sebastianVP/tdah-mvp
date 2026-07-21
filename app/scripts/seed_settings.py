from app.database.db import SessionLocal
from app.database.models import Setting


def seed_settings():

    db = SessionLocal()

    settings = [

        Setting(

            key="app_name",

            value="MindAlert",

            description="Nombre del sistema"

        ),

        Setting(

            key="institution",

            value="MindAlert",

            description="Institución"

        ),

        Setting(

            key="contact_email",

            value="admin@mindalert.pe",

            description="Correo institucional"

        ),

        Setting(

            key="smtp_server",

            value="smtp.gmail.com",

            description="Servidor SMTP"

        ),

        Setting(

            key="smtp_port",

            value="465",

            description="Puerto SMTP"

        ),

        Setting(

            key="smtp_ssl",

            value="True",

            description="SSL"

        ),

        Setting(

            key="smtp_email",

            value="",

            description="Correo remitente"

        ),

        Setting(

            key="smtp_password",

            value="",

            description="Contraseña SMTP"

        ),

        Setting(

            key="pdf_title",

            value="Resultado de Evaluación",

            description="Título del PDF"

        ),

        Setting(

            key="pdf_footer",

            value="Documento generado automáticamente",

            description="Pie del PDF"

        ),

        Setting(

            key="system_version",

            value="1.0",

            description="Versión"

        ),

    ]

    db.add_all(settings)

    db.commit()

    db.close()

    print("✅ Configuración inicial insertada.")


if __name__ == "__main__":

    seed_settings()