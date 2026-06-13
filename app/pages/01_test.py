import streamlit as st

st.title("Parte 1")

respuesta = st.radio(
    "¿Con qué frecuencia tiene dificultad para terminar tareas?",
    [
        "Nunca",
        "Rara vez",
        "Algunas veces",
        "Frecuentemente",
        "Muy frecuentemente"
    ]
)

st.write("Respuesta:", respuesta)