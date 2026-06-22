import streamlit as st

st.title("Registro")

name = st.text_input(
    "Nombre completo"
)

email = st.text_input(
    "Correo electrónico"
)

age = st.number_input(
    "Edad",
    min_value=5,
    max_value=100
)

gender = st.selectbox(
    "Sexo",
    [
        "Masculino",
        "Femenino",
        "Otro"
    ]
)

consent = st.checkbox(
    "Acepto la política de privacidad"
)

if st.button("Continuar"):

    if not consent:

        st.error(
            "Debe aceptar la política."
        )

    elif not name:

        st.error(
            "Ingrese nombre."
        )

    elif not email:

        st.error(
            "Ingrese correo."
        )

    else:

        st.session_state["name"] = name
        st.session_state["email"] = email
        st.session_state["age"] = age
        st.session_state["gender"] = gender

        st.switch_page(
            "pages/01_test.py"
        )