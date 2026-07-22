import base64
from pathlib import Path
import streamlit as st

def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

img_path = Path(__file__).parent / "assets" / "hero_image.png"
# ── Limpiar estado de evaluaciones anteriores al llegar al inicio ──────────────
# Esto garantiza que una nueva evaluación siempre se guarde en BD
for key in ["evaluation_saved", "evaluation_id", "score", "risk",
            "responses", "name", "email", "age", "gender",
            "current_index", "answers_map"]:
    st.session_state.pop(key, None)

st.set_page_config(
    page_title="MindAlert - Evaluación TDAH",
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

    /* ── Limitar ancho máximo del contenido ───────────────── */
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

    /* ── Badge ────────────────────────────────────────────── */
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
        margin-bottom: 1.75rem;
    }

    /* ── Hero text ────────────────────────────────────────── */
    .hero-title {
        font-size: clamp(2.2rem, 4vw, 3.2rem);
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 1.25rem;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Gradiente en texto — fallback a color sólido si falla */
    .hero-highlight {
        color: #A29BFE;
        background: linear-gradient(135deg, #A29BFE 0%, #6C5CE7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    @supports not (-webkit-background-clip: text) {
        .hero-highlight { color: #A29BFE; -webkit-text-fill-color: unset; background: none; }
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(255,255,255,0.5);
        line-height: 1.7;
        margin-bottom: 2.25rem;
        max-width: 480px;
    }

    /* ── Feature boxes ────────────────────────────────────── */
    .feature-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1rem 1.1rem;
    }
    .feature-icon {
        font-size: 1.3rem;
        margin-bottom: 0.4rem;
    }
    .feature-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #FFFFFF;
        margin-bottom: 0.25rem;
    }
    .feature-desc {
        font-size: 0.82rem;
        color: rgba(255,255,255,0.4);
        line-height: 1.5;
    }

    /* ── CTA button ───────────────────────────────────────── */
    div.stButton > button {
        background: linear-gradient(135deg, #5A4FCF 0%, #8B7FE8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.8rem 2rem !important;
        border-radius: 14px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(108,92,231,0.35) !important;
        transition: box-shadow 0.2s ease !important;
        letter-spacing: 0.2px !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 6px 28px rgba(108,92,231,0.55) !important;
    }

    /* ── Admin link (texto puro, sin botón) ───────────────── */
    .admin-link {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.18);
        text-align: right;
        margin-top: 2.5rem;
        cursor: pointer;
        transition: color 0.2s;
    }
    .admin-link:hover { color: rgba(255,255,255,0.45); }

    /* ── Social proof ─────────────────────────────────────── */
    .social-proof {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.3);
        margin-top: 0.9rem;
    }

    /* ── Hero image ───────────────────────────────────────── */
    .hero-img {
        width: 100%;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* ── Column gap ───────────────────────────────────────── */
    [data-testid="stHorizontalBlock"] { gap: 2rem !important; align-items: center !important; }
</style>
""", unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
col_info, col_img = st.columns([1.1, 0.9], gap="large")

with col_info:
    st.markdown(
        "<p style='font-size:1.05rem; font-weight:700; color:#A29BFE; margin-bottom:2.5rem;'>🧠 MindAlert</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<span class="badge">🔬 Evaluación científica &nbsp;·&nbsp; 100% online &nbsp;·&nbsp; 3 minutos</span>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h1 class="hero-title">Descubre cómo funciona<br><span class="hero-highlight">tu atención</span></h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="hero-subtitle">Evaluación preliminar basada en instrumentos internacionales '
        'para detectar señales de TDAH de manera rápida y segura.</p>',
        unsafe_allow_html=True,
    )

    # Feature cards
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">⚡</div>'
            '<div class="feature-title">Rápido</div>'
            '<div class="feature-desc">Solo 3 minutos de tu tiempo.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">🛡️</div>'
            '<div class="feature-title">Privado</div>'
            '<div class="feature-desc">Tus datos están protegidos.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">📊</div>'
            '<div class="feature-title">Confiable</div>'
            '<div class="feature-desc">Basado en escalas validadas.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Comenzar evaluación →", key="btn_start"):
        st.switch_page("pages/00_registro.py")

    st.markdown(
        '<p class="social-proof">✨ Miles de personas ya han dado el primer paso.</p>',
        unsafe_allow_html=True,
    )

with col_img:
    if img_path.exists():
        encoded_img = get_image_base64(img_path)
        st.markdown(
            f'<img src="data:image/png;base64,{encoded_img}" class="hero-img">',
            unsafe_allow_html=True,
        )
    else:
        # Placeholder decorativo si no hay imagen
        st.markdown(
            '<div style="width:100%; aspect-ratio:4/3; border-radius:24px; '
            'border:1px solid rgba(255,255,255,0.07); background:rgba(255,255,255,0.02); '
            'display:flex; align-items:center; justify-content:center; '
            'color:rgba(255,255,255,0.15); font-size:0.85rem;">'
            'hero_image.png</div>',
            unsafe_allow_html=True,
        )

# ── Admin access — discreto al fondo ──────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
_, col_admin = st.columns([5, 1])
with col_admin:
    if st.button("⚙ Admin", key="btn_admin"):
        st.switch_page("pages/03_dashboard.py")

# Override: botón admin con estilo mínimo usando su posición en el DOM
st.markdown("""
<style>
    /* Último botón de la página = admin, sin afectar los demás */
    [data-testid="stAppViewBlockContainer"] > div:last-child button {
        background: transparent !important;
        color: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        box-shadow: none !important;
        font-size: 0.75rem !important;
        padding: 0.3rem 0.75rem !important;
        border-radius: 8px !important;
        font-weight: 400 !important;
        width: auto !important;
    }
    [data-testid="stAppViewBlockContainer"] > div:last-child button:hover {
        color: rgba(255,255,255,0.5) !important;
        border-color: rgba(255,255,255,0.2) !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)


