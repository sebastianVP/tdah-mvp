import streamlit as st

from app.services.auth_service import authenticate

st.set_page_config(

    page_title="Administrador",

    page_icon="🔐",

    layout="centered"

)

st.markdown("""

<style>

.stApp{

    background:#0F172A;

}

.main-box{

    width:420px;

    margin:auto;

    margin-top:70px;

    padding:35px;

    border-radius:18px;

    background:#111827;

    border:1px solid #334155;

}

.title{

    text-align:center;

    font-size:34px;

    font-weight:700;

    color:white;

}

.subtitle{

    text-align:center;

    color:#94A3B8;

    margin-bottom:30px;

}

</style>

""",

unsafe_allow_html=True)

st.markdown(

'<div class="main-box">',

unsafe_allow_html=True

)

st.markdown(

'<div class="title">🔐 MindAlert</div>',

unsafe_allow_html=True

)

st.markdown(

'<div class="subtitle">Panel Administrativo</div>',

unsafe_allow_html=True

)

username = st.text_input(

    "Usuario"

)

password = st.text_input(

    "Contraseña",

    type="password"

)

login = st.button(

    "Ingresar",

    use_container_width=True

)

if login:

    admin = authenticate(

        username,

        password

    )

    if admin:

        st.session_state["admin_logged"] = True

        st.session_state["admin_id"] = admin.id

        st.session_state["admin_name"] = admin.full_name

        st.success(

            "Bienvenido."

        )

        st.switch_page(

            "pages/05_admin_panel.py"

        )

    else:

        st.error(

            "Usuario o contraseña incorrectos."

        )

        st.markdown(

"</div>",

unsafe_allow_html=True

)