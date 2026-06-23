import streamlit as st
import pandas as pd

from app.services.statistics_service import (
    get_total_participants,
    get_total_evaluations,
    get_risk_distribution,
    get_gender_distribution,
    get_age_distribution,
)

st.set_page_config(
    page_title="Dashboard - MindAlert",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Base ─────────────────────────────────────────────── */
    .stApp {
        background-color: #0B0F19 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stAppViewBlockContainer"] {
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding-top: 0 !important;
    }

    /* ── Hide Streamlit chrome ────────────────────────────── */
    header, [data-testid="stHeader"] { background: transparent !important; height: 2.5rem !important; }
    #MainMenu, [data-testid="stStatusWidget"], header [data-testid="stActionButton"] { visibility: hidden; }
    footer { visibility: hidden; }

    /* ── Sidebar toggle ───────────────────────────────────── */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important; transform: scale(0.75) !important;
        opacity: 0.2 !important; background: transparent !important;
        color: #A0AEC0 !important; border: none !important; transition: opacity 0.3s !important;
    }
    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover { opacity: 0.9 !important; color: #A29BFE !important; }

    /* ── Metric cards ─────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.025) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 20px !important;
        padding: 1.4rem 1.6rem !important;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        color: rgba(255,255,255,0.4) !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
    }

    /* ── Section cards ────────────────────────────────────── */
    .section-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 24px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        color: rgba(255,255,255,0.35);
        margin-bottom: 1.25rem;
    }

    /* ── Dataframe ────────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border-radius: 14px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
    }
    iframe[title="st_aggrid"] { border-radius: 14px !important; }

    /* ── Bar chart coloring ───────────────────────────────── */
    [data-testid="stVegaLiteChart"] canvas { border-radius: 12px; }

    /* ── Info / empty state ───────────────────────────────── */
    [data-testid="stAlert"] {
        background: rgba(108,92,231,0.07) !important;
        border: 1px solid rgba(108,92,231,0.2) !important;
        border-radius: 14px !important;
        color: #A29BFE !important;
    }

    /* ── Column gap ───────────────────────────────────────── */
    [data-testid="stHorizontalBlock"] { gap: 1.25rem !important; }

    /* ── Back button ──────────────────────────────────────── */
    div.stButton > button {
        background: transparent !important;
        color: rgba(255,255,255,0.35) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
        width: auto !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        color: #FFFFFF !important;
        border-color: rgba(255,255,255,0.3) !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='display:flex; align-items:center; justify-content:space-between; "
    "padding: 0.5rem 0 1.75rem;'>"
    "<span style='font-size:1.05rem; font-weight:700; color:#A29BFE;'>🧠 MindAlert</span>"
    "<span style='font-size:0.75rem; font-weight:700; text-transform:uppercase; "
    "letter-spacing:1.2px; color:rgba(255,255,255,0.25);'>Panel administrativo</span>"
    "</div>",
    unsafe_allow_html=True,
)

# ── KPI metrics ────────────────────────────────────────────────────────────────
total_participants = get_total_participants()
total_evaluations  = get_total_evaluations()
risk_data          = get_risk_distribution()

# Calcular % de riesgo alto si hay datos
pct_alto = 0
if risk_data:
    df_risk_raw = pd.DataFrame(risk_data, columns=["Riesgo", "Cantidad"])
    total_eval_count = df_risk_raw["Cantidad"].sum()
    alto_row = df_risk_raw[df_risk_raw["Riesgo"] == "Alto"]["Cantidad"]
    pct_alto = int(round(alto_row.values[0] / total_eval_count * 100)) if not alto_row.empty and total_eval_count > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Participantes", total_participants)
with col2:
    st.metric("Evaluaciones realizadas", total_evaluations)
with col3:
    st.metric("Riesgo alto", f"{pct_alto}%")

st.markdown("<br>", unsafe_allow_html=True)

# ── Risk distribution ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Distribución de riesgo</p>', unsafe_allow_html=True)

if risk_data:
    df_risk = pd.DataFrame(risk_data, columns=["Riesgo", "Cantidad"])

    # Tabla y gráfico lado a lado
    col_t, col_c = st.columns([1, 2])
    with col_t:
        st.dataframe(
            df_risk,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Riesgo":   st.column_config.TextColumn("Nivel"),
                "Cantidad": st.column_config.NumberColumn("Casos", format="%d"),
            }
        )
    with col_c:
        # Color map manual para los 3 niveles
        color_map = {"Bajo": "#5DCAA5", "Moderado": "#FAC775", "Alto": "#F09595"}
        df_risk["Color"] = df_risk["Riesgo"].map(color_map).fillna("#A29BFE")
        st.bar_chart(
            df_risk.set_index("Riesgo")[["Cantidad"]],
            color="#6C5CE7",
            use_container_width=True,
        )
else:
    st.info("Aún no hay evaluaciones registradas.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Gender distribution ────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Distribución por sexo</p>', unsafe_allow_html=True)

gender_data = get_gender_distribution()
if gender_data:
    df_gender = pd.DataFrame(gender_data, columns=["Sexo", "Cantidad"])
    col_t, col_c = st.columns([1, 2])
    with col_t:
        st.dataframe(
            df_gender,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sexo":     st.column_config.TextColumn("Sexo"),
                "Cantidad": st.column_config.NumberColumn("Participantes", format="%d"),
            }
        )
    with col_c:
        st.bar_chart(
            df_gender.set_index("Sexo")[["Cantidad"]],
            color="#A29BFE",
            use_container_width=True,
        )
else:
    st.info("Aún no hay participantes registrados.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Age distribution ───────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Distribución por edad</p>', unsafe_allow_html=True)

age_data = get_age_distribution()
if age_data:
    df_age = pd.DataFrame(age_data.items(), columns=["Rango", "Cantidad"])
    col_t, col_c = st.columns([1, 2])
    with col_t:
        st.dataframe(
            df_age,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rango":    st.column_config.TextColumn("Rango de edad"),
                "Cantidad": st.column_config.NumberColumn("Participantes", format="%d"),
            }
        )
    with col_c:
        st.bar_chart(
            df_age.set_index("Rango")[["Cantidad"]],
            color="#5DCAA5",
            use_container_width=True,
        )
else:
    st.info("Aún no hay datos de edad registrados.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Back button ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("← Volver al inicio"):
    # Limpiar todo el estado para permitir una nueva evaluación limpia
    for key in ["evaluation_saved", "evaluation_id", "score", "risk",
                "responses", "name", "email", "age", "gender",
                "current_index", "answers_map"]:
        st.session_state.pop(key, None)
    st.switch_page("main.py")