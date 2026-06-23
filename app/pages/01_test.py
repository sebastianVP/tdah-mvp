import streamlit as st
from app.services.questions import QUESTIONS

st.set_page_config(
    page_title="Evaluación - MindAlert",
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
        visibility: visible !important;
        transform: scale(0.75) !important;
        opacity: 0.2 !important;
        background: transparent !important;
        color: #A0AEC0 !important;
        border: none !important;
        transition: opacity 0.3s !important;
    }
    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover {
        opacity: 0.9 !important;
        color: #A29BFE !important;
    }

    /* ── Progress bar ─────────────────────────────────────── */
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #6C5CE7, #A29BFE) !important;
    }
    [data-testid="stProgressBar"] > div {
        background: rgba(255,255,255,0.07) !important;
        border-radius: 99px !important;
        height: 6px !important;
    }

    /* ── Card wrapper ─────────────────────────────────────── */
    .test-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 28px;
        padding: 2.5rem 2.25rem 2rem;
        margin-top: 1rem;
    }

    /* ── Labels ───────────────────────────────────────────── */
    .progress-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #9F92EC;
        margin-bottom: 0.6rem;
    }
    .question-text {
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1.4;
        color: #FFFFFF;
        margin: 1.4rem 0 1.8rem;
    }
    .options-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(255,255,255,0.35);
        margin-bottom: 0.75rem;
    }

    /* ── Option buttons (custom via st.button) ────────────── */
    /* Un-selected */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        text-align: left !important;
        background: rgba(255,255,255,0.04) !important;
        border: 1.5px solid rgba(255,255,255,0.09) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.1rem !important;
        color: #CBD5E0 !important;
        font-size: 0.97rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.18s ease !important;
        margin-bottom: 0 !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: rgba(108,92,231,0.12) !important;
        border-color: rgba(108,92,231,0.45) !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: scale(0.99) !important;
    }

    /* ── Selected option (special class injected via key) ─── */
    div[data-testid="stButton"].selected-option > button {
        background: rgba(108,92,231,0.18) !important;
        border-color: #7C6FE8 !important;
        color: #E9E5FF !important;
    }

    /* ── Nav buttons ──────────────────────────────────────── */
    .nav-back > div[data-testid="stButton"] > button {
        background: transparent !important;
        border: 1.5px solid rgba(255,255,255,0.12) !important;
        color: #94A3B8 !important;
        border-radius: 14px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 0.7rem 1rem !important;
    }
    .nav-back > div[data-testid="stButton"] > button:hover {
        border-color: rgba(255,255,255,0.3) !important;
        color: #FFFFFF !important;
    }

    .nav-next > div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #5A4FCF 0%, #8B7FE8 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 4px 20px rgba(108,92,231,0.35) !important;
    }
    .nav-next > div[data-testid="stButton"] > button:hover {
        box-shadow: 0 6px 24px rgba(108,92,231,0.5) !important;
    }

    /* ── Collapse all gap / padding on columns ────────────── */
    [data-testid="stVerticalBlock"] > div { gap: 0 !important; }
    [data-testid="stHorizontalBlock"] { gap: 1rem !important; }

    /* ── Hide all native radio components (unused) ─────────── */
    div[data-testid="stRadio"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
OPTIONS = [
    ("0", "Nunca"),
    ("1", "Rara vez"),
    ("2", "Algunas veces"),
    ("3", "Frecuentemente"),
    ("4", "Muy frecuentemente"),
]
OPTION_ICONS = ["○", "◐", "◑", "●", "⬤"]  # subtle visual scale
total_questions = len(QUESTIONS)

# ── Session state ─────────────────────────────────────────────────────────────
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "answers_map" not in st.session_state:
    st.session_state["answers_map"] = {}

current_idx = st.session_state["current_index"]
saved_answer = st.session_state["answers_map"].get(current_idx, None)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center; padding: 0.5rem 0 0.25rem;'>"
    "<span style='font-size:1.05rem; font-weight:700; letter-spacing:0.5px; color:#A29BFE;'>🧠 MindAlert</span>"
    "</div>",
    unsafe_allow_html=True
)

# ── Card open ─────────────────────────────────────────────────────────────────
st.markdown('<div class="test-card">', unsafe_allow_html=True)

# Progress
progress_pct = (current_idx + 1) / total_questions
st.markdown(f'<p class="progress-label">Pregunta {current_idx + 1} de {total_questions}</p>', unsafe_allow_html=True)
st.progress(progress_pct)

# Question
st.markdown(f'<p class="question-text">{QUESTIONS[current_idx]}</p>', unsafe_allow_html=True)

# ── Option buttons ─────────────────────────────────────────────────────────────
st.markdown('<p class="options-label">¿Con qué frecuencia?</p>', unsafe_allow_html=True)

for i, (val, label) in enumerate(OPTIONS):
    is_selected = saved_answer == label
    # Inject a visual checkmark when selected
    display_label = f"✓  {label}" if is_selected else f"   {label}"
    col_btn, = st.columns([1])
    # Style the button container differently when selected
    if is_selected:
        st.markdown(
            f"""<style>
            div[data-testid="stButton"]:has(button[kind="secondary"][data-key="opt_{current_idx}_{i}"]) > button {{
                background: rgba(108,92,231,0.18) !important;
                border-color: #7C6FE8 !important;
                color: #E9E5FF !important;
            }}
            </style>""",
            unsafe_allow_html=True
        )
    clicked = st.button(
        display_label,
        key=f"opt_{current_idx}_{i}",
        use_container_width=True
    )
    if clicked:
        st.session_state["answers_map"][current_idx] = label
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── Navigation ─────────────────────────────────────────────────────────────────
col_back, col_next = st.columns([1, 2])

with col_back:
    if current_idx > 0:
        st.markdown('<div class="nav-back">', unsafe_allow_html=True)
        if st.button("← Atrás", key="btn_back", use_container_width=True):
            st.session_state["current_index"] -= 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with col_next:
    has_answer = saved_answer is not None
    st.markdown('<div class="nav-next">', unsafe_allow_html=True)
    if current_idx < total_questions - 1:
        if st.button(
            "Siguiente →" if has_answer else "Selecciona una opción",
            key="btn_next",
            use_container_width=True,
            disabled=not has_answer
        ):
            st.session_state["current_index"] += 1
            st.rerun()
    else:
        if st.button(
            "Finalizar evaluación ✓" if has_answer else "Selecciona una opción",
            key="btn_finish",
            use_container_width=True,
            disabled=not has_answer
        ):
            ordered_responses = [
                st.session_state["answers_map"].get(i, "Nunca")
                for i in range(total_questions)
            ]
            st.session_state["responses"] = ordered_responses
            del st.session_state["current_index"]
            del st.session_state["answers_map"]
            st.switch_page("pages/02_resultado.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .test-card