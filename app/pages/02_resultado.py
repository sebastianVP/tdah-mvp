import streamlit as st
import os
from app.services.scoring import calculate_score
from app.services.evaluation_service import save_evaluation
from app.services.participant_service import save_participant

from app.services.email_service import send_result_email
from app.services.pdf_service import generate_pdf

st.set_page_config(
    page_title="Resultado - MindAlert",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Base ─────────────────────────────────────────────── */
    .stApp {
        background-color: #0B0F19 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
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

    /* ── Score hero ───────────────────────────────────────── */
    .score-hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1.5rem 0 2rem;
        gap: 0.4rem;
    }
    .score-number {
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -2px;
    }
    .score-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: rgba(255,255,255,0.4);
        margin-top: 0.2rem;
    }
    .risk-badge {
        display: inline-block;
        padding: 0.45rem 1.5rem;
        border-radius: 99px;
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 0.75rem;
        letter-spacing: 0.3px;
    }

    /* ── Risk colors ──────────────────────────────────────── */
    .risk-bajo     { background: rgba(29,158,117,0.18); color: #5DCAA5; border: 1px solid rgba(29,158,117,0.35); }
    .risk-moderado { background: rgba(186,117,23,0.18); color: #FAC775; border: 1px solid rgba(186,117,23,0.35); }
    .risk-alto     { background: rgba(226,75,74,0.18);  color: #F09595; border: 1px solid rgba(226,75,74,0.35); }

    /* ── Divider ──────────────────────────────────────────── */
    .soft-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.07);
        margin: 1.25rem 0;
    }

    /* ── Info notice ──────────────────────────────────────── */
    .notice-box {
        background: rgba(108,92,231,0.08);
        border: 1px solid rgba(108,92,231,0.2);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        font-size: 0.87rem;
        color: #B8B0F0;
        line-height: 1.6;
    }

    /* ── Eval ID ──────────────────────────────────────────── */
    .eval-id {
        text-align: center;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.25);
        margin-top: 1.25rem;
        letter-spacing: 0.5px;
    }

    /* ── Expander ─────────────────────────────────────────── */
    details {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 16px !important;
        padding: 0.25rem 0.5rem !important;
        margin-top: 1rem !important;
    }
    details summary {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        padding: 0.6rem 0.5rem !important;
    }
    details summary:hover { color: rgba(255,255,255,0.8) !important; }

    /* ── Response rows ────────────────────────────────────── */
    .response-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.875rem;
    }
    .response-row:last-child { border-bottom: none; }
    .response-num { color: rgba(255,255,255,0.3); font-size: 0.75rem; min-width: 2.5rem; }
    .response-val {
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.2rem 0.65rem;
        border-radius: 99px;
        background: rgba(108,92,231,0.12);
        color: #A29BFE;
    }

    /* ── Todos los botones base ───────────────────────────── */
    div[data-testid="stButton"] > button {
        border-radius: 14px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.2px !important;
    }

    /* ── NUEVA SECCIÓN: Estilo Estético para el Botón de Descarga PDF ── */
    div[data-testid="stDownloadButton"] > button {
        border-radius: 14px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.2px !important;
        
        /* Diseño Cyberpunk/Oscuro unificado con el ecosistema */
        background: rgba(108, 92, 231, 0.15) !important;
        color: #A29BFE !important;
        border: 1.5px solid rgba(108, 92, 231, 0.4) !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.1) !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: rgba(108, 92, 231, 0.25) !important;
        color: #FFFFFF !important;
        border-color: rgba(108, 92, 231, 0.7) !important;
        box-shadow: 0 6px 22px rgba(108, 92, 231, 0.25) !important;
    }
    div[data-testid="stDownloadButton"] > button:active {
        background: rgba(108, 92, 231, 0.35) !important;
    }
            
    /* ── Botón primario (Nueva evaluación — primer botón) ── */
    div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #5A4FCF 0%, #8B7FE8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(108,92,231,0.35) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stButton"] > button:hover {
        box-shadow: 0 6px 28px rgba(108,92,231,0.55) !important;
    }

    /* ── Botón secundario (Volver al inicio — segundo botón) */
    div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] > button {
        background: transparent !important;
        color: rgba(255,255,255,0.6) !important;
        border: 1.5px solid rgba(255,255,255,0.15) !important;
        box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] > button:hover {
        color: #FFFFFF !important;
        border-color: rgba(255,255,255,0.35) !important;
        background: rgba(255,255,255,0.04) !important;
    }

    /* ── Column gap ───────────────────────────────────────── */
    [data-testid="stHorizontalBlock"] { gap: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Guards ─────────────────────────────────────────────────────────────────────
responses = st.session_state.get("responses")
if not responses:
    st.error("No se encontraron respuestas.")
    st.stop()

if "name" not in st.session_state:
    st.error("Faltan datos del participante. Por favor, vuelve a realizar el test.")
    st.stop()

# ── Score & risk ───────────────────────────────────────────────────────────────
score = calculate_score(responses)

if score < 8:
    risk = "Bajo"
    risk_class = "risk-bajo"
    risk_emoji = "✓"
    risk_desc = "Tus respuestas no muestran señales de alerta significativas."
elif score < 16:
    risk = "Moderado"
    risk_class = "risk-moderado"
    risk_emoji = "⚡"
    risk_desc = "Hay algunas áreas que vale la pena atender con un profesional."
else:
    risk = "Alto"
    risk_class = "risk-alto"
    risk_emoji = "!"
    risk_desc = "Te recomendamos hablar con un especialista pronto."

st.session_state["score"] = score
st.session_state["risk"]  = risk

# ── Save evaluation once ───────────────────────────────────────────────────────
if "evaluation_saved" not in st.session_state:
    participant_id = save_participant(
        full_name=st.session_state["name"],
        email=st.session_state["email"],
        age=st.session_state["age"],
        gender=st.session_state["gender"],
    )
    evaluation_id = save_evaluation(
        participant_id=participant_id,
        score=score,
        risk_level=risk,
        responses=responses,
    )

    # -------------------------------------------------------
    # Generar Reporte PDF
    # -------------------------------------------------------

    pdf_path = generate_pdf(

        filename=f"report_{evaluation_id}.pdf",

        participant=st.session_state["name"],

        email=st.session_state["email"],

        age=st.session_state["age"],

        gender=st.session_state["gender"],

        score=score,

        risk=risk,

        evaluation_id=evaluation_id

    )

    st.session_state["pdf_path"] = pdf_path
    #print("pdf_path:", pdf_path)
    # -------------------------------------------------------
    # Enviar correo
    # -------------------------------------------------------


    send_result_email(
    recipient=st.session_state["email"],
    score=score,
    risk=risk,
    pdf_path=pdf_path,
    evaluation_id=evaluation_id
    )
    st.session_state["evaluation_saved"] = True
    st.session_state["email_sent"] = True
    st.session_state["evaluation_id"]    = evaluation_id


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center; padding: 0.5rem 0 0.25rem;'>"
    "<span style='font-size:1.05rem; font-weight:700; letter-spacing:0.5px; color:#A29BFE;'>🧠 MindAlert</span>"
    "</div>",
    unsafe_allow_html=True,
)

# ── Greeting ───────────────────────────────────────────────────────────────────
st.markdown(
    f"<p style='text-align:center; font-size:0.85rem; font-weight:600; "
    f"text-transform:uppercase; letter-spacing:1.5px; color:rgba(255,255,255,0.35); margin-bottom:0; margin-top:1rem;'>"
    f"Resultados de</p>"
    f"<p style='text-align:center; font-size:1.3rem; font-weight:700; color:#FFFFFF; margin:0.15rem 0 0;'>"
    f"{st.session_state.get('name', 'Participante')}</p>",
    unsafe_allow_html=True,
)

# ── Score hero ─────────────────────────────────────────────────────────────────
score_color = '#5DCAA5' if risk == 'Bajo' else '#FAC775' if risk == 'Moderado' else '#F09595'
st.markdown(
    f"""<div class="score-hero">
        <span class="score-number" style="color:{score_color};">{score}</span>
        <span class="score-label">puntos obtenidos</span>
        <span class="risk-badge {risk_class}">{risk_emoji} &nbsp; Riesgo {risk}</span>
    </div>""",
    unsafe_allow_html=True,
)

st.markdown(
    f"<p style='text-align:center; font-size:0.92rem; color:rgba(255,255,255,0.55); margin: 0 0 1.5rem;'>"
    f"{risk_desc}</p>",
    unsafe_allow_html=True,
)

st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

# ── Score scale ────────────────────────────────────────────────────────────────
max_score = 24
pct = min(score / max_score * 100, 100)

st.markdown(
    f"""<div style="margin: 0.5rem 0 1.5rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
            <span style="font-size:0.75rem; color:rgba(255,255,255,0.35); font-weight:600;
                         text-transform:uppercase; letter-spacing:1px;">Escala de riesgo</span>
            <span style="font-size:0.75rem; color:rgba(255,255,255,0.35);">{score} / {max_score}</span>
        </div>
        <div style="height:8px; background:rgba(255,255,255,0.07); border-radius:99px; overflow:hidden;">
            <div style="height:100%; width:{pct:.1f}%; background:{score_color};
                        border-radius:99px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:0.35rem;">
            <span style="font-size:0.7rem; color:rgba(255,255,255,0.25);">Bajo</span>
            <span style="font-size:0.7rem; color:rgba(255,255,255,0.25);">Moderado</span>
            <span style="font-size:0.7rem; color:rgba(255,255,255,0.25);">Alto</span>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

# ── Disclaimer ─────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="notice-box">⚠️&nbsp; Este resultado es <strong>únicamente orientativo</strong> '
    'y no constituye un diagnóstico médico. Si tienes dudas, consulta con un profesional de la salud mental.</div>',
    unsafe_allow_html=True,
)

# ── Confirmación de envío de correo ────────────────────────────────────────────

if st.session_state.get("email_sent", False):

    st.success(
        "📧 Tu reporte ha sido enviado correctamente al correo registrado. "
        "Si no lo encuentras en tu bandeja de entrada, revisa también la carpeta de spam o correo no deseado."
    )

if "evaluation_id" in st.session_state:
    st.markdown(
        f'<p class="eval-id">Evaluación #{st.session_state["evaluation_id"]} registrada correctamente</p>',
        unsafe_allow_html=True,
    )

# ── Descargar Reporte PDF (CORREGIDA INDENTACIÓN EXTRASECCIÓN) ─────────────────
# Sacamos este bloque de la condicional anidada para asegurar que Streamlit lo dibuje siempre 
# que la ruta del PDF exista físicamente en el servidor.
if "pdf_path" in st.session_state and os.path.exists(st.session_state["pdf_path"]):
    with open(st.session_state["pdf_path"], "rb") as pdf_file:
        st.download_button(
            label="📄 Descargar Reporte PDF",
            data=pdf_file,
            file_name=f"MindAlert_Report_{st.session_state.get('evaluation_id', 0)}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.warning("⚠️ El archivo PDF no se encuentra o aún no ha sido generado en el servidor.")
# ── Mensaje motivacional ───────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center; margin-top:1.5rem; margin-bottom:0.5rem; "
    "color:rgba(255,255,255,0.3); font-size:0.85rem; line-height:1.7;'>"
    "Comprender tu atención es el primer paso para mejorar tu bienestar.<br>"
    "Gracias por utilizar <strong style='color:rgba(255,255,255,0.5);'>MindAlert</strong>."
    "</div>",
    unsafe_allow_html=True,
)

# ── Botones de acción ──────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("Nueva evaluacion", key="btn_nueva", use_container_width=True):
        for key in ["responses", "score", "risk", "evaluation_saved", "evaluation_id",
                    "name", "email", "age", "gender", "current_index", "answers_map"]:
            st.session_state.pop(key, None)
        st.switch_page("pages/00_registro.py")

with col2:
    if st.button("Volver al inicio", key="btn_inicio", use_container_width=True):
        st.session_state.clear()
        st.switch_page("main.py")

# ── Expander de respuestas ─────────────────────────────────────────────────────
with st.expander("Ver respuestas registradas"):
    from app.services.questions import QUESTIONS
    for i, (question, response) in enumerate(zip(QUESTIONS, responses), start=1):
        short_q = question if len(question) <= 60 else question[:57] + "…"
        st.markdown(
            f'<div class="response-row">'
            f'<span class="response-num">#{i}</span>'
            f'<span style="color:rgba(255,255,255,0.65); flex:1; padding: 0 1rem;">{short_q}</span>'
            f'<span class="response-val">{response}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )