import streamlit as st

from collections import defaultdict

from app.services.security_service import require_admin

from app.services.settings_service import (
    get_all_settings,
    search_settings,
    update_setting,
    create_setting,
    delete_setting
)

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(

    page_title="Configuración",

    page_icon="⚙️",

    layout="wide"

)

require_admin()

# ==========================================================
# HEADER
# ==========================================================

st.title("⚙️ Configuración del Sistema")

st.caption(

    "Administra todos los parámetros generales de MindAlert."

)

st.divider()

# ==========================================================
# NUEVA CONFIGURACIÓN
# ==========================================================

st.subheader("➕ Nueva configuración")

with st.expander("Crear nueva configuración"):

    with st.form("new_setting"):

        new_key = st.text_input(

            "Clave"

        )

        new_value = st.text_input(

            "Valor"

        )

        new_description = st.text_input(

            "Descripción"

        )

        create = st.form_submit_button(

            "Crear configuración",

            use_container_width=True

        )

        if create:

            if new_key.strip() == "":

                st.warning("Debe ingresar una clave.")

            else:

                create_setting(

                    new_key,

                    new_value,

                    new_description

                )

                st.success(

                    "Configuración creada correctamente."

                )

                st.rerun()

# ==========================================================
# BUSCADOR
# ==========================================================

search = st.text_input(

    "Buscar configuración",

    placeholder="Ejemplo: smtp"

)




# ==========================================================
# CARGAR CONFIGURACIONES
# ==========================================================

if search:

    settings = search_settings(search)

else:

    settings = get_all_settings()

# ==========================================================
# VALIDACIÓN
# ==========================================================

if len(settings) == 0:

    st.info(

        "No existen configuraciones registradas."

    )

    st.stop()

# ==========================================================
# AGRUPAR CONFIGURACIONES
# ==========================================================

grouped = defaultdict(list)

for setting in settings:

    key = setting.key.lower()

    if key.startswith("smtp"):

        grouped["📧 Correo SMTP"].append(setting)

    elif key.startswith("pdf"):

        grouped["📄 Reportes PDF"].append(setting)

    elif key.startswith("security"):

        grouped["🔒 Seguridad"].append(setting)

    elif key.startswith("app"):

        grouped["🧠 Aplicación"].append(setting)

    else:

        grouped["⚙ General"].append(setting)

# ==========================================================
# FORMULARIO
# ==========================================================

with st.form("settings_form"):

    values = {}

    for section in grouped:

        st.subheader(section)

        st.divider()

        for setting in grouped[section]:

            label = setting.description or setting.key

            key = setting.key.lower()

            # ----------------------------
            # Password
            # ----------------------------

            if "password" in key:

                values[setting.key] = st.text_input(

                    label,

                    value=setting.value,

                    type="password"

                )

            # ----------------------------
            # Puerto
            # ----------------------------

            elif "port" in key:

                values[setting.key] = st.number_input(

                    label,

                    value=int(setting.value),

                    step=1

                )

            # ----------------------------
            # Timeout
            # ----------------------------

            elif "timeout" in key:

                values[setting.key] = st.number_input(

                    label,

                    value=int(setting.value),

                    step=1

                )

            # ----------------------------
            # Intentos
            # ----------------------------

            elif "attempt" in key:

                values[setting.key] = st.number_input(

                    label,

                    value=int(setting.value),

                    step=1

                )

            # ----------------------------
            # Texto
            # ----------------------------

            else:

                values[setting.key] = st.text_input(

                    label,

                    value=setting.value,

                    help=setting.key

                )

    save = st.form_submit_button(

        "💾 Guardar configuración",

        use_container_width=True,

    )

# ==========================================================
# GUARDAR
# ==========================================================

if save:

    changes = 0

    for setting in settings:

        old = str(setting.value)

        new = str(values[setting.key])

        if old != new:

            update_setting(

                setting.key,

                new

            )

            changes += 1

    if changes == 0:

        st.info(

            "No hubo cambios para guardar."

        )

    else:

        st.success(

            f"Se actualizaron {changes} configuraciones correctamente."

        )

        st.rerun()

# ==========================================================
# TABLA RESUMEN
# ==========================================================

st.divider()

st.subheader("📋 Configuraciones registradas")

rows = []

for setting in settings:

    rows.append({

        "Clave": setting.key,

        "Valor": setting.value,

        "Descripción": setting.description

    })

st.dataframe(

    rows,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# BOTONES
# ==========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(

        "⬅ Volver al Panel",

        use_container_width=True

    ):

        st.switch_page(

            "pages/05_admin_panel.py"

        )

with col2:

    if st.button(

        "📊 Dashboard",

        use_container_width=True

    ):

        st.switch_page(

            "pages/03_dashboard.py"

        )