import streamlit as st

import pandas as pd

from app.services.security_service import require_admin

from app.services.evaluation_dashboard_service import (

    get_total_evaluations,

    get_total_high_risk,

    get_total_medium_risk,

    get_total_low_risk,

    get_all_evaluations,

    search_evaluations,

)

st.set_page_config(

    page_title="Evaluaciones",

    page_icon="📝",

    layout="wide"

)

require_admin()

st.title("📝 Evaluaciones")

st.caption(

    "Administración de todas las evaluaciones realizadas."

)

st.divider()

col1,col2,col3=st.columns([4,1,1])

with col1:

    search_text=st.text_input(

        "Buscar",

        placeholder="Nombre o correo"

    )

with col2:

    export_excel=st.button(

        "📗 Excel",

        use_container_width=True

    )

with col3:

    export_csv=st.button(

        "📄 CSV",

        use_container_width=True

    )

total=get_total_evaluations()

alto=get_total_high_risk()

medio=get_total_medium_risk()

bajo=get_total_low_risk()


c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(

        "Evaluaciones",

        total

    )

with c2:

    st.metric(

        "Alto",

        alto

    )

with c3:

    st.metric(

        "Moderado",

        medio

    )

with c4:

    st.metric(

        "Bajo",

        bajo

    )

if search_text:

    df=search_evaluations(

        search_text

    )

else:

    df=get_all_evaluations()