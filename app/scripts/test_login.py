from app.services.auth_service import authenticate

admin = authenticate(

    "admin",

    "Admin123*"

)

if admin:

    print("Login correcto")

    print(admin.full_name)

else:

    print("Usuario o contraseña incorrectos")