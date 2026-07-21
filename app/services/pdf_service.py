from datetime import datetime
import os

from app.services.settings_service import get_setting

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


# =====================================================
# CONFIGURACIÓN DE ESTILOS
# =====================================================
# =====================================================
# DIRECTORIO DONDE SE GUARDARÁN LOS REPORTES
# =====================================================

REPORTS_DIR = "reports"


APP_NAME = get_setting("app_name") or "MindAlert"

APP_VERSION = get_setting("app_version") or "1.0"

APP_INSTITUTION = get_setting("app_institution") or ""

PDF_TITLE = get_setting("pdf_title") or "Evaluación Preliminar de TDAH"

PDF_FOOTER = get_setting("pdf_footer") or "©2026 MindAlert"

PDF_WEBSITE = get_setting("app_website") or "https://mindalert.app"

PDF_LEGAL = get_setting(

    "pdf_legal"

) or """Este reporte fue generado automáticamente por MindAlert.

La presente evaluación constituye únicamente una herramienta de tamizaje y no reemplaza una valoración clínica realizada por un profesional de la salud.

Ante cualquier duda consulte con un especialista."""


os.makedirs(
    REPORTS_DIR,
    exist_ok=True
)

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "MindAlertTitle",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontSize=24,
    textColor=colors.HexColor("#1E3A8A"),
    spaceAfter=20
)

SUBTITLE_STYLE = ParagraphStyle(
    "Subtitle",
    parent=styles["Heading2"],
    fontSize=15,
    textColor=colors.HexColor("#374151"),
    spaceBefore=12,
    spaceAfter=8
)

NORMAL_STYLE = ParagraphStyle(
    "Normal",
    parent=styles["BodyText"],
    fontSize=11,
    leading=18
)

FOOTER_STYLE = ParagraphStyle(
    "Footer",
    parent=styles["BodyText"],
    alignment=TA_CENTER,
    fontSize=8,
    textColor=colors.grey
)


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def generate_pdf(
    filename: str,
    participant: str,
    email: str,
    age: int,
    gender: str,
    score: int,
    risk: str,
    evaluation_id: int
):
    """
    Genera el reporte PDF de MindAlert.

    Parameters
    ----------

    filename:
        Ruta donde se guardará el PDF.

    participant:
        Nombre del participante.

    email:
        Correo electrónico.

    age:
        Edad.

    gender:
        Sexo.

    score:
        Puntaje obtenido.

    risk:
        Nivel de riesgo.

    evaluation_id:
        ID de la evaluación.
    """

    # ==============================================
    # Crear documento PDF
    # ==============================================
# ==============================================
# Ruta completa del PDF
# ==============================================

    filename = os.path.join(
        REPORTS_DIR,
        filename
    )


    doc = SimpleDocTemplate(
        filename,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    story = []

    # ==============================================
    # Logo (si existe)
    # ==============================================

    logo_path = "app/assets/logo.png"

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=3.2 * cm,
            height=3.2 * cm
        )

        logo.hAlign = "CENTER"

        story.append(logo)

        story.append(
            Spacer(1, 0.4 * cm)
        )

    # ==============================================
    # Título
    # ==============================================

    story.append(

        Paragraph(
            APP_NAME,
            TITLE_STYLE
        )

    )

    story.append(

        Paragraph(
            PDF_TITLE,
            SUBTITLE_STYLE
        )

    )


    if APP_INSTITUTION:

        story.append(

            Paragraph(

                APP_INSTITUTION,
                NORMAL_STYLE
            )

        )

    story.append(

        Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            NORMAL_STYLE
        )

    )

    story.append(

        Paragraph(
            f"Número de Reporte: MA-{evaluation_id:06d}",
            NORMAL_STYLE
        )

    )

    story.append(

        Spacer(
            1,
            0.8 * cm
        )

    )

    # ==============================================
    # Información del participante
    # ==============================================

    story.append(

        Paragraph(
            "Información del Participante",
            SUBTITLE_STYLE
        )

    )

    participant_data = [

        ["Nombre", participant],

        ["Correo", email],

        ["Edad", str(age)],

        ["Sexo", gender]

    ]

    participant_table = Table(

        participant_data,

        colWidths=[4 * cm, 10 * cm]

    )

    participant_table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E5E7EB")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.black
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ]

        )

    )

    story.append(
        participant_table
    )

    story.append(
        Spacer(1, 0.8 * cm)
    )

    # ==============================================
    # Resultado (continuará en Parte 2)
    # ==============================================

    story.append(

        Paragraph(
            "Resultado de la Evaluación",
            SUBTITLE_STYLE
        )

    )

    story.append(

        Paragraph(
            f"<b>Puntaje obtenido:</b> {score} / 24",
            NORMAL_STYLE
        )

    )

    story.append(

        Paragraph(
            f"<b>Nivel de Riesgo:</b> {risk}",
            NORMAL_STYLE
        )

    )

    if risk == "Bajo":

        risk_color = colors.HexColor("#22C55E")
        risk_text = "RIESGO BAJO"

    elif risk == "Moderado":

        risk_color = colors.HexColor("#FACC15")
        risk_text = "RIESGO MODERADO"

    else:

        risk_color = colors.HexColor("#EF4444")
        risk_text = "RIESGO ALTO"

    risk_table = Table(

        [[risk_text]],

        colWidths=[15 * cm]

    )

    risk_table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,-1),
                    risk_color
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,-1),
                    colors.white
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                ),

                (
                    "FONTNAME",
                    (0,0),
                    (-1,-1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    16
                ),

                (
                    "BOTTOMPADDING",
                    (0,0),
                    (-1,-1),
                    12
                ),

                (
                    "TOPPADDING",
                    (0,0),
                    (-1,-1),
                    12
                )

            ]

        )

    )

    story.append(risk_table)

    story.append(
        Spacer(1, 0.8 * cm)
    )

    # ==============================================
    # CONTINÚA EN LA PARTE 2
    # ==============================================

    # ==============================================
    # Interpretación
    # ==============================================

    story.append(

        Paragraph(

            "Interpretación",

            SUBTITLE_STYLE

        )

    )

    if risk == "Bajo":

        interpretation = """
    Los resultados obtenidos indican una baja probabilidad de presentar síntomas compatibles con el Trastorno por Déficit de Atención e Hiperactividad (TDAH).

    Actualmente no se observan indicadores suficientes para sugerir una evaluación clínica.
    """

    elif risk == "Moderado":

        interpretation = """
    Los resultados muestran algunos indicadores compatibles con TDAH.

    Aunque no representan un diagnóstico, sería recomendable realizar una evaluación clínica más profunda si los síntomas afectan las actividades diarias.
    """

    else:

        interpretation = """
    Los resultados muestran una alta presencia de síntomas compatibles con TDAH.

    Se recomienda acudir a un profesional de la salud mental para realizar una evaluación clínica completa y obtener un diagnóstico adecuado.
    """

    story.append(

        Paragraph(

            interpretation,

            NORMAL_STYLE

        )

    )

    story.append(
        Spacer(1,0.8*cm)
    )

    # ==============================================
    # Recomendaciones
    # ==============================================

    story.append(

        Paragraph(

            "Recomendaciones",

            SUBTITLE_STYLE

        )

    )

    recommendations = [

    "• Dormir entre 7 y 8 horas diariamente.",

    "• Mantener horarios organizados.",

    "• Reducir distractores durante el trabajo o estudio.",

    "• Practicar actividad física regularmente.",

    "• Consultar con un especialista si los síntomas persisten."

    ]

    for item in recommendations:

        story.append(

            Paragraph(

                item,

                NORMAL_STYLE

            )

        )

    story.append(
        Spacer(1,0.8*cm)
    )

    # ==============================================
    # Aviso Legal
    # ==============================================

    story.append(

        Paragraph(

            "Aviso Importante",

            SUBTITLE_STYLE

        )

    )

    legal = """
    Este reporte fue generado automáticamente por la plataforma MindAlert.

    La presente evaluación constituye únicamente una herramienta de tamizaje y no reemplaza una valoración clínica realizada por un profesional de la salud.

    Ante cualquier duda o preocupación, consulte con un especialista en salud mental.
    """

    story.append(

        Paragraph(

            PDF_LEGAL,

            NORMAL_STYLE

        )

    )

    story.append(
        Spacer(1,0.7*cm)
    )

    story.append(

        Paragraph(

            PDF_FOOTER,

            FOOTER_STYLE

        )

    )

    story.append(

        Paragraph(

            "https://mindalert.app",

            FOOTER_STYLE

        )

    )

    doc.build(story)

    return filename