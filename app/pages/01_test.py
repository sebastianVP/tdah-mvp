import sys
import streamlit as st
from pathlib import Path

#ROOT = Path(__file__).resolve().parents[2]
#sys.path.append(str(ROOT))
from app.services.questions import QUESTIONS

st.title("Evaluación Preliminar TDAH")

responses = []

options = [
    "Nunca",
    "Rara vez",
    "Algunas veces",
    "Frecuentemente",
    "Muy frecuentemente"
]

for i, question in enumerate(QUESTIONS):
    answer = st.radio(
        question,
        options,
        key=f"q{i}"
    )
    responses.append(answer)

if st.button("Finalizar Evaluación"):
    st.session_state["responses"] = responses
    st.switch_page("pages/02_resultado.py")