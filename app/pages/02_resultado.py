import streamlit as st
import sys
from pathlib import Path

#ROOT = Path(__file__).resolve().parents[2]
#sys.path.append(str(ROOT))

from app.services.scoring import calculate_score

responses = st.session_state.get("responses")

if not responses:
    st.error("No se encontraron respuestas.")
    st.stop()

score = calculate_score(responses)

st.title("Resultado")

st.metric(
    "Puntaje obtenido",
    score
)

if score < 8:
    st.success("Riesgo Bajo")
elif score < 16:
    st.warning("Riesgo Moderado")
else:
    st.error("Riesgo Alto")

st.info(
    "Este resultado es únicamente orientativo y no constituye un diagnóstico médico."
)