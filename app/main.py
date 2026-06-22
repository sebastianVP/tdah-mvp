import streamlit as st

st.set_page_config(
    page_title="Evaluación Preliminar TDAH",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Evaluación Preliminar de TDAH")

st.markdown("""
Bienvenido.

Esta herramienta realiza un tamizaje preliminar basado en cuestionarios
utilizados internacionalmente.

**No constituye un diagnóstico médico.**
""")

if st.button("Comenzar Evaluación"):
    st.switch_page("pages/00_registro.py")

if st.button("Dashboard Administrativo"):
    st.switch_page(
        "pages/03_dashboard.py"
    )