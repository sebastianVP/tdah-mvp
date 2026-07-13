import streamlit as st
import pandas as pd
from app.services.participant_dashboard_service import (
    get_all_participants,
    search_participants,
    get_total_participants,
    get_total_males,
    get_total_females,
    get_average_age
)

from app.services.security_service import require_admin

st.set_page_config(

    page_title="Participantes",

    page_icon="👥",

    layout="wide"

)

# ==========================================================
# SEGURIDAD
# ==========================================================

require_admin()

# ==========================================================
# HEADER
# ==========================================================

st.title("👥 Participantes registrados")

st.caption(
    "Administración de los participantes registrados en MindAlert."
)

st.divider()

total = get_total_participants()

males = get_total_males()

females = get_total_females()

average = get_average_age()

# ==========================================================
# BARRA SUPERIOR
# ==========================================================

col1, col2, col3 = st.columns([3, 1, 1])

with col1:

    search = st.text_input(

        "Buscar participante",

        placeholder="Nombre o correo"

    )
    if search:

        df = search_participants(search)

    else:

        df = get_all_participants()

with col2:

    export_excel = st.button(

        "📗 Excel",

        use_container_width=True

    )

with col3:

    export_csv = st.button(

        "📄 CSV",

        use_container_width=True

    )

# ==========================================================
# KPIs
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Participantes",

        total

    )

with col2:

    st.metric(

        "Hombres",

        males

    )

with col3:

    st.metric(

        "Mujeres",

        females

    )

with col4:

    st.metric(

        "Edad promedio",

        average

    )

st.divider()

# ==========================================================
# TABLA O ENSAJE CUANDO NO HAY DATOS
# ==========================================================

if df.empty:

    st.info(

        "No existen participantes registrados."

    )

else:

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

# ==========================================================
# BOTONES INFERIORES
# ==========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(

        "⬅ Volver",

        use_container_width=True

    ):

        st.switch_page(

            "pages/05_admin_panel.py"

        )

with col2:

    if st.button(

        "📊 Dashboard",

        use_container_width=True

    ):

        st.switch_page(

            "pages/03_dashboard.py"

        )