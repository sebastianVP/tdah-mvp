import streamlit as st
import pandas as pd

from io import BytesIO

from app.services.dashboard_service import (
    get_total_participants,
    get_total_evaluations,
    get_average_age,
    get_high_risk_percentage,
    get_risk_distribution,
    get_gender_distribution,
    get_age_distribution,
    get_daily_evaluations,
    get_dashboard_table,
)

from app.utils.charts import (
    plot_risk_distribution,
    plot_gender_distribution,
    plot_age_distribution,
    plot_daily_evaluations,
)

from app.services.security_service import require_admin

#from app.services.statistics_service import (
#    get_total_participants,
#    get_total_evaluations,
#    get_risk_distribution,
#    get_gender_distribution,
#    get_age_distribution,
#)

st.set_page_config(
    page_title="Dashboard - MindAlert",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_admin()

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
header_left, header_center,  header_right = st.columns([5,1, 1])
with header_left:
    st.markdown(
    """
    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:25px;
    ">

    <div>

    <h1 style="margin-bottom:0;">
    🧠 MindAlert
    </h1>

    <p style="
    color:#A0AEC0;
    margin-top:5px;
    font-size:16px;
    ">

    Dashboard Inteligente de Analítica

    </p>

    </div>

    <div style="text-align:right;">

    <h4 style="margin-bottom:0;">
    Panel Administrativo
    </h4>

    <p style="
    color:#6C5CE7;
    font-size:14px;
    ">

    Versión MVP

    </p>

    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

with header_center:

    if st.button("🔄 Actualizar", use_container_width=True):

        st.rerun()

with header_right:

    if st.button("🏠 Inicio", use_container_width=True):

        # Limpiar el estado de la sesión

        for key in [

            "evaluation_saved",
            "evaluation_id",
            "score",
            "risk",
            "responses",
            "name",
            "email",
            "age",
            "gender",
            "current_index",
            "answers_map"

        ]:

            st.session_state.pop(key, None)

        st.switch_page("main.py")

#st.markdown(
#    "<div style='display:flex; align-items:center; justify-content:space-between; "
#    "padding: 0.5rem 0 1.75rem;'>"
#    "<span style='font-size:1.05rem; font-weight:700; color:#A29BFE;'>🧠 MindAlert</span>"
#    "<span style='font-size:0.75rem; font-weight:700; text-transform:uppercase; "
#    "letter-spacing:1.2px; color:rgba(255,255,255,0.25);'>Panel administrativo</span>"
#    "</div>",
#    unsafe_allow_html=True,
#) 

# ── KPI metrics ────────────────────────────────────────────────────────────────
total_participants = get_total_participants()

total_evaluations = get_total_evaluations()

average_age = get_average_age()

high_risk = get_high_risk_percentage()
c1,c2,c3,c4 = st.columns(4)
with c1:

    st.metric(

        "👥 Participantes",

        total_participants

    )
with c2:

    st.metric(

        "📋 Evaluaciones",

        total_evaluations

    )
with c3:

    st.metric(

        "🎂 Edad promedio",

        average_age

    )
with c4:

    st.metric(

        "⚠ Riesgo Alto",

        f"{high_risk}%"

    )
st.markdown("<br>", unsafe_allow_html=True)

# ── Risk distribution ──────────────────────────────────────────────────────────
risk_data = get_risk_distribution()

gender_data = get_gender_distribution()

age_data = get_age_distribution()

daily_data = get_daily_evaluations()

df_risk = pd.DataFrame(

    risk_data,

    columns=[

        "Riesgo",

        "Cantidad"

    ]

)

df_gender = pd.DataFrame(

    gender_data,

    columns=[

        "Sexo",

        "Cantidad"

    ]

)

df_age = pd.DataFrame(

    age_data.items(),

    columns=[

        "Rango",

        "Cantidad"

    ]

)

df_daily = pd.DataFrame(

    daily_data,

    columns=[

        "Fecha",

        "Cantidad"

    ]

)

dashboard_df = get_dashboard_table()

left,right = st.columns(2)

with left:

    fig = plot_risk_distribution(df_risk)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    fig = plot_age_distribution(df_age)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    fig = plot_gender_distribution(df_gender)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    fig = plot_daily_evaluations(df_daily)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.markdown("---")

st.subheader("🔍 Buscar participante")

texto = st.text_input(

    "Nombre o correo",

    placeholder="Escriba un nombre..."

)

if texto:

    dashboard_df = dashboard_df[

        dashboard_df["Nombre"]

        .str.contains(

            texto,

            case=False,

            na=False

        )

        |

        dashboard_df["Correo"]

        .str.contains(

            texto,

            case=False,

            na=False

        )

    ]

st.subheader("📋 Historial de Evaluaciones")

st.dataframe(

    dashboard_df,

    use_container_width=True,

    hide_index=True

)

csv = dashboard_df.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    "📄 Descargar CSV",

    csv,

    "evaluaciones.csv",

    "text/csv"

)

buffer = BytesIO()

with pd.ExcelWriter(

    buffer,

    engine="openpyxl"

) as writer:

    dashboard_df.to_excel(

        writer,

        index=False,

        sheet_name="Evaluaciones"

    )

st.download_button(

    "📊 Descargar Excel",

    data=buffer.getvalue(),

    file_name="evaluaciones.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)

st.markdown("---")

st.subheader("📈 Métricas de Uso")

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(

        "Evaluaciones registradas",

        len(dashboard_df)

    )

with m2:

    if not dashboard_df.empty:

        st.metric(

            "Última evaluación",

            dashboard_df.iloc[0]["Fecha"].strftime("%d/%m/%Y")

        )

with m3:

    if not dashboard_df.empty:

        st.metric(

            "Edad media",

            round(

                dashboard_df["Edad"].mean(),

                1

            )

        )