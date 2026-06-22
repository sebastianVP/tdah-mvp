import streamlit as st

from app.services.scoring import calculate_score
from app.services.evaluation_service import save_evaluation
from app.services.participant_service import save_participant

# --------------------------------------------------
# Recuperar respuestas
# --------------------------------------------------

responses = st.session_state.get("responses")

if not responses:
    st.error("No se encontraron respuestas.")
    st.stop()


if not "name" in st.session_state:
    st.error("Faltan datos del participante. Por favor, vuelva a realizar el test.")
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
    # 1. Guardar al participante primero para obtener su ID
    participant_id = save_participant(
        full_name = st.session_state["name"],
        email     = st.session_state["email"],
        age       = st.session_state["age"],
        gender    = st.session_state["gender"]
        )
    # 2. Ahora si, guardar la evaluacion enlazada al participante
    evaluation_id = save_evaluation(
        participant_id=participant_id,
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