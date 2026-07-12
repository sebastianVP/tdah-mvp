from app.services.auth_service import create_admin

admin_id = create_admin(

    full_name="Alexander Valdez",

    username="admin",

    email="alex.valdezp22@gmail.com",

    password="Admin123*"

)

print(f"Administrador creado correctamente. ID = {admin_id}")