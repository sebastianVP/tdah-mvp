import streamlit as st

import pandas as pd

from app.services.security_service import require_admin

from app.services.evaluation_dashboard_service import (

    get_total_evaluations,

    get_total_high_risk,

    get_total_medium_risk,

    get_total_low_risk,

    get_all_evaluations,

    search_evaluations,

)

from app.services.evaluation_dashboard_service import (

    regenerate_pdf,

    resend_email,

    delete_evaluation,

    get_evaluation_detail

)

st.set_page_config(

    page_title="Evaluaciones",

    page_icon="📝",

    layout="wide"

)

require_admin()

st.title("📝 Evaluaciones")

st.caption(

    "Administración de todas las evaluaciones realizadas."

)

st.divider()

col1,col2,col3=st.columns([4,1,1])

with col1:

    search_text=st.text_input(

        "Buscar",

        placeholder="Nombre o correo"

    )

with col2:

    export_excel=st.button(

        "📗 Excel",

        use_container_width=True

    )

with col3:

    export_csv=st.button(

        "📄 CSV",

        use_container_width=True

    )

total=get_total_evaluations()

alto=get_total_high_risk()

medio=get_total_medium_risk()

bajo=get_total_low_risk()


c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(

        "Evaluaciones",

        total

    )

with c2:

    st.metric(

        "Alto",

        alto

    )

with c3:

    st.metric(

        "Moderado",

        medio

    )

with c4:

    st.metric(

        "Bajo",

        bajo

    )

if search_text:

    df=search_evaluations(

        search_text

    )

else:

    df=get_all_evaluations()

st.divider()

st.subheader("📋 Evaluaciones registradas")

if df.empty:

    st.info("No existen evaluaciones registradas.")

else:

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True,

        column_config={

            "ID": st.column_config.NumberColumn(

                "ID",

                width="small"

            ),

            "Fecha": st.column_config.DatetimeColumn(

                "Fecha",

                format="DD/MM/YYYY HH:mm"

            ),

            "Nombre": st.column_config.TextColumn(

                "Participante"

            ),

            "Correo": st.column_config.TextColumn(

                "Correo"

            ),

            "Puntaje": st.column_config.NumberColumn(

                "Puntaje"

            ),

            "Máximo": st.column_config.NumberColumn(

                "Máximo"

            ),

            "Riesgo": st.column_config.TextColumn(

                "Nivel"

            )

        }

    )

if not df.empty:

    st.divider()

    selected = st.selectbox(

        "Seleccione una evaluación",

        options=df["ID"],

        format_func=lambda x: (

            df[df["ID"] == x]

            .iloc[0]["Nombre"]

            + f" (ID {x})"

        )

    )

selected_row = df[

    df["ID"] == selected

].iloc[0]

selected_row["Nombre"]

selected_row["Correo"]

selected_row["Riesgo"]

selected_row["Fecha"]

st.markdown("### Información")

c1, c2 = st.columns(2)

with c1:

    st.write("**Participante**")

    st.write(selected_row["Nombre"])

    st.write("**Correo**")

    st.write(selected_row["Correo"])

with c2:

    st.write("**Riesgo**")

    st.write(selected_row["Riesgo"])

    st.write("**Puntaje**")

    st.write(

        f"{selected_row['Puntaje']} / {selected_row['Máximo']}"

    )

st.divider()

st.subheader("⚙ Acciones")

b1, b2, b3, b4 = st.columns(4)

with b1:

    view_pdf = st.button(

        "📄 Ver PDF",

        use_container_width=True

    )

with b2:

    resend = st.button(

        "📧 Reenviar correo",

        use_container_width=True

    )

with b3:

    detail = st.button(

        "👁 Ver detalle",

        use_container_width=True

    )

with b4:

    delete = st.button(

        "🗑 Eliminar",

        use_container_width=True,

        type="primary"

    )

if view_pdf:

    pdf_path = regenerate_pdf(selected)

    st.success("PDF generado correctamente.")

    with open(pdf_path, "rb") as pdf:

        st.download_button(

            "⬇ Descargar PDF",

            pdf,

            file_name="resultado.pdf",

            mime="application/pdf"

        )

if resend:

    resend_email(selected)

    st.success(

        "Correo reenviado correctamente."

    )

if delete:

    delete_evaluation(selected)

    st.success(

        "Evaluación eliminada."

    )

    st.rerun()

if detail:

    row = get_evaluation_detail(selected)

    st.json({

        "Participante": row.Participant.full_name,

        "Correo": row.Participant.email,

        "Edad": row.Participant.age,

        "Sexo": row.Participant.gender,

        "Puntaje": row.Evaluation.score,

        "Máximo": row.Evaluation.max_score,

        "Riesgo": row.Evaluation.probability_level,

        "Respuestas": row.Evaluation.responses

    })