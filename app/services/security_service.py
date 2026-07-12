import streamlit as st


def require_admin():

    """
    Verifica que exista una sesión de administrador.

    Si no existe, redirige automáticamente
    al Login.
    """

    if not st.session_state.get(

        "admin_logged",

        False

    ):

        st.warning(

            "Debe iniciar sesión para acceder."

        )

        st.switch_page(

            "pages/04_admin_login.py"

        )