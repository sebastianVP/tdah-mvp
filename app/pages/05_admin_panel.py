import streamlit as st

from app.services.security_service import require_admin

require_admin()

st.set_page_config(

    page_title="Panel Administrativo",

    page_icon="🛡️",

    layout="wide"

)

st.markdown("""

<style>

.stApp{

    background:#0F172A;

}

.card{

    background:#1E293B;

    border-radius:20px;

    padding:30px;

    border:1px solid #334155;

    text-align:center;

}

.big{

    font-size:60px;

}

.title{

    color:white;

    font-size:22px;

    font-weight:700;

}

.subtitle{

    color:#94A3B8;

    font-size:15px;

}

</style>

""",

unsafe_allow_html=True)

st.title("🛡️ Panel Administrativo")

st.write("Bienvenido")

st.success(

    st.session_state["admin_name"]

)

col1,col2=st.columns(2)

col3,col4=st.columns(2)

with col1:

    st.markdown("""

<div class="card">

<div class="big">📊</div>

<div class="title">

Dashboard

</div>

<div class="subtitle">

Indicadores

</div>

</div>

""",unsafe_allow_html=True)

    if st.button(

        "Abrir Dashboard",

        use_container_width=True,

        key="dashboard"

    ):

        st.switch_page(

            "pages/03_dashboard.py"

        )

with col2:

    st.markdown("""

<div class="card">

<div class="big">👥</div>

<div class="title">

Participantes

</div>

<div class="subtitle">

Base de datos

</div>

</div>

""",unsafe_allow_html=True)

    if st.button(

        "Ver Participantes",

        use_container_width=True,

        key="participants"

    ):

        st.switch_page(

            "pages/06_participants.py"

        )

with col3:

    st.markdown("""

<div class="card">

<div class="big">📝</div>

<div class="title">

Evaluaciones

</div>

<div class="subtitle">

Resultados

</div>

</div>

""",unsafe_allow_html=True)

    if st.button(

        "Ver Evaluaciones",

        use_container_width=True,

        key="evaluations"

    ):

        st.info("Disponible en Sprint 9")

with col4:

    st.markdown("""

<div class="card">

<div class="big">⚙️</div>

<div class="title">

Configuración

</div>

<div class="subtitle">

Sistema

</div>

</div>

""",unsafe_allow_html=True)

    if st.button(

        "Configuración",

        use_container_width=True,

        key="config"

    ):

        st.info("Disponible en Sprint 9")

st.divider()

st.subheader("Administrador")

st.write(

    f"**Nombre:** {st.session_state['admin_name']}"

)

st.write(

    f"**ID:** {st.session_state['admin_id']}"

)

if st.button(

    "🚪 Cerrar sesión",

    use_container_width=True

):

    st.session_state.clear()

    st.switch_page(

        "pages/04_admin_login.py"

    )