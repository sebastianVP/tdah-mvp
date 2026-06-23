import streamlit as st

st.set_page_config(
    page_title="Registro - MindAlert",
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

    /* ── Card ─────────────────────────────────────────────── */
    .register-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 28px;
        padding: 2.5rem 2.25rem 2rem;
        margin-top: 1rem;
    }

    /* ── Typography ───────────────────────────────────────── */
    .register-title {
        font-size: 1.9rem;
        font-weight: 700;
        text-align: center;
        line-height: 1.25;
        margin-bottom: 0.4rem;
        color: #FFFFFF;
    }
    .register-subtitle {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.45);
        text-align: center;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    .badge {
        display: inline-block;
        background: rgba(108,92,231,0.15);
        color: #9F92EC;
        border: 1px solid rgba(108,92,231,0.3);
        padding: 5px 16px;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-bottom: 1.5rem;
    }

    /* ── Input labels ─────────────────────────────────────── */
    label p, .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #CBD5E0 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }

    /* ── Text inputs ──────────────────────────────────────── */
    input[type="text"], input[type="email"], input[type="number"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1.5px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        font-size: 0.97rem !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.65rem 0.9rem !important;
        transition: border-color 0.2s ease !important;
    }
    input[type="text"]:focus, input[type="email"]:focus, input[type="number"]:focus {
        border-color: rgba(108,92,231,0.6) !important;
        box-shadow: 0 0 0 3px rgba(108,92,231,0.1) !important;
        outline: none !important;
    }
    input::placeholder { color: rgba(255,255,255,0.25) !important; }

    /* ── Selectbox ────────────────────────────────────────── */
    [data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1.5px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSelectbox"] svg { fill: rgba(255,255,255,0.4) !important; }

    /* ── Number input controls ────────────────────────────── */
    [data-testid="stNumberInput"] button {
        background: rgba(255,255,255,0.06) !important;
        border-color: rgba(255,255,255,0.1) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    [data-testid="stNumberInput"] button:hover {
        background: rgba(108,92,231,0.15) !important;
        border-color: rgba(108,92,231,0.4) !important;
    }

    /* ── Checkbox ─────────────────────────────────────────── */
    [data-testid="stCheckbox"] label p {
        color: rgba(255,255,255,0.65) !important;
        font-size: 0.87rem !important;
        font-weight: 400 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        line-height: 1.5 !important;
    }
    [data-testid="stCheckbox"] input[type="checkbox"] + div {
        border-color: rgba(108,92,231,0.5) !important;
        border-radius: 6px !important;
    }
    [data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
        background: #6C5CE7 !important;
        border-color: #6C5CE7 !important;
    }

    /* ── Submit button ────────────────────────────────────── */
    div.stButton > button {
        background: linear-gradient(135deg, #5A4FCF 0%, #8B7FE8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.97rem !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 2rem !important;
        border-radius: 14px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 1.25rem !important;
        box-shadow: 0 4px 20px rgba(108,92,231,0.35) !important;
        transition: box-shadow 0.2s ease !important;
        letter-spacing: 0.2px !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 6px 28px rgba(108,92,231,0.55) !important;
    }

    /* ── Error messages ───────────────────────────────────── */
    [data-testid="stAlert"] {
        background: rgba(226,75,74,0.1) !important;
        border: 1px solid rgba(226,75,74,0.25) !important;
        border-radius: 12px !important;
        color: #F09595 !important;
    }

    /* ── Column gap ───────────────────────────────────────── */
    [data-testid="stHorizontalBlock"] { gap: 1rem !important; }

    /* ── Section divider label ────────────────────────────── */
    .field-group-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: rgba(255,255,255,0.25);
        margin: 1.5rem 0 0.75rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        padding-top: 1.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center; padding: 0.5rem 0 0.25rem;'>"
    "<span style='font-size:1.05rem; font-weight:700; letter-spacing:0.5px; color:#A29BFE;'>🧠 MindAlert</span>"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center;'>"
    "<span class='badge'>Paso 1 de 2 &nbsp;·&nbsp; Datos de perfil</span>"
    "</div>",
    unsafe_allow_html=True,
)

# ── Card ───────────────────────────────────────────────────────────────────────
# st.markdown('<div class="register-card">', unsafe_allow_html=True)

st.markdown('<h2 class="register-title">Antes de comenzar</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="register-subtitle">Ingresa tus datos para calibrar los parámetros de la evaluación.<br>'
    'Solo tomarás unos segundos.</p>',
    unsafe_allow_html=True,
)

# ── Form fields ────────────────────────────────────────────────────────────────
name  = st.text_input("Nombre completo", placeholder="Ej. Alexander Valdez")
email = st.text_input("Correo electrónico", placeholder="Ej. nombre@correo.com")

st.markdown('<p class="field-group-label">Información demográfica</p>', unsafe_allow_html=True)

col_age, col_gender = st.columns(2)
with col_age:
    age = st.number_input("Edad", min_value=5, max_value=100, value=25)
with col_gender:
    gender = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])

# ── Privacy notice ─────────────────────────────────────────────────────────────
st.markdown(
    """<div style="background:rgba(108,92,231,0.07); border:1px solid rgba(108,92,231,0.2);
                  border-radius:14px; padding:1rem 1.1rem; margin-top:1.5rem;
                  font-size:0.84rem; color:#A29BFE; line-height:1.6;">
        🔒 <strong style="color:#B8B0F0;">Privacidad asegurada:</strong>
        Tu información está protegida mediante anonimización y encriptación de extremo a extremo.
        No compartimos tus datos con terceros.
    </div>""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

consent = st.checkbox(
    "Acepto las políticas de privacidad y el procesamiento de mis respuestas con fines de tamizaje."
)

# ── Submit ─────────────────────────────────────────────────────────────────────
if st.button("Continuar con la evaluación →"):
    if not name.strip():
        st.error("Ingresa tu nombre completo.")
    elif not email.strip() or "@" not in email:
        st.error("Ingresa un correo electrónico válido.")
    elif not consent:
        st.error("Debes aceptar la política de privacidad para continuar.")
    else:
        st.session_state["name"]   = name
        st.session_state["email"]  = email
        st.session_state["age"]    = age
        st.session_state["gender"] = gender
        st.switch_page("pages/01_test.py")

st.markdown('</div>', unsafe_allow_html=True)