import streamlit as st
import pandas as pd

from app.services.statistics_service import (
    get_total_participants,
    get_total_evaluations,
    get_risk_distribution,
    get_gender_distribution,
    get_age_distribution,
)

st.title("📊 Dashboard Administrativo")

# =====================================
# Métricas principales
# =====================================

total_participants = get_total_participants()
total_evaluations = get_total_evaluations()

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Participantes",
        total_participants
    )

with col2:

    st.metric(
        "Evaluaciones",
        total_evaluations
    )

st.divider()

# =====================================
# Riesgo
# =====================================

st.subheader(
    "Distribución de Riesgo"
)

risk_data = get_risk_distribution()

if risk_data:

    df_risk = pd.DataFrame(
        risk_data,
        columns=[
            "Riesgo",
            "Cantidad"
        ]
    )

    st.dataframe(
        df_risk,
        use_container_width=True
    )

    st.bar_chart(
        df_risk.set_index(
            "Riesgo"
        )
    )

else:

    st.info(
        "No existen evaluaciones."
    )

st.divider()

# =====================================
# Sexo
# =====================================

st.subheader(
    "Distribución por Sexo"
)

gender_data = get_gender_distribution()

if gender_data:

    df_gender = pd.DataFrame(
        gender_data,
        columns=[
            "Sexo",
            "Cantidad"
        ]
    )

    st.dataframe(
        df_gender,
        use_container_width=True
    )

    st.bar_chart(
        df_gender.set_index(
            "Sexo"
        )
    )

else:

    st.info(
        "No existen participantes."
    )
# =====================================
# Edad
# =====================================

st.divider()

st.subheader(
    "Distribución por Edad"
)

age_data = get_age_distribution()

df_age = pd.DataFrame(
    age_data.items(),
    columns=[
        "Rango",
        "Cantidad"
    ]
)

st.dataframe(
    df_age,
    use_container_width=True
)

st.bar_chart(
    df_age.set_index(
        "Rango"
    )
)