import streamlit as st

from app.services.scoring import calculate_score
from app.services.evaluation_service import save_evaluation

# --------------------------------------------------
# Recuperar respuestas
# --------------------------------------------------

responses = st.session_state.get("responses")

if not responses:
    st.error("No se encontraron respuestas.")
    st.stop()

# --------------------------------------------------
# Calcular puntaje
# --------------------------------------------------

score = calculate_score(responses)

# --------------------------------------------------
# Determinar nivel de riesgo
# --------------------------------------------------

if score < 8:
    risk = "Bajo"

elif score < 16:
    risk = "Moderado"

else:
    risk = "Alto"

# Guardar en session_state para futuras etapas
st.session_state["score"] = score
st.session_state["risk"] = risk

# --------------------------------------------------
# Guardar evaluación una sola vez
# --------------------------------------------------

if "evaluation_saved" not in st.session_state:
    evaluation_id = save_evaluation(
        score=score,
        risk_level=risk,
        responses=responses
    )

    st.session_state["evaluation_saved"] = True
    st.session_state["evaluation_id"] = evaluation_id

# --------------------------------------------------
# Mostrar resultado
# --------------------------------------------------

st.title("Resultado")

st.metric(
    "Puntaje obtenido",
    score
)

if risk == "Bajo":
    st.success("Riesgo Bajo")

elif risk == "Moderado":
    st.warning("Riesgo Moderado")

else:
    st.error("Riesgo Alto")

st.info(
    "Este resultado es únicamente orientativo y no constituye un diagnóstico médico."
)

# --------------------------------------------------
# Mostrar ID de evaluación
# --------------------------------------------------

if "evaluation_id" in st.session_state:

    st.caption(
        f"Evaluación registrada con ID #{st.session_state['evaluation_id']}"
    )

# --------------------------------------------------
# Mostrar respuestas
# --------------------------------------------------

with st.expander("Ver respuestas registradas"):

    for i, response in enumerate(responses, start=1):

        st.write(
            f"Pregunta {i}: {response}"
        )