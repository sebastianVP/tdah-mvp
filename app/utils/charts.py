import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

PRIMARY = "#6C5CE7"

SECONDARY = "#A29BFE"

SUCCESS = "#5DCAA5"

WARNING = "#FAC775"

DANGER = "#F09595"

BACKGROUND = "#0B0F19"

CARD = "#161B2E"

TEXT = "#FFFFFF"

TEXT_LIGHT = "#A0AEC0"

def apply_theme(fig):

    fig.update_layout(

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font=dict(

            color=TEXT,

            family="Inter"

        ),

        title_font_size=18,

        title_font_color=TEXT,

        legend=dict(

            font=dict(

                color=TEXT

            )

        ),

        margin=dict(

            l=20,

            r=20,

            t=45,

            b=20

        )

    )

    return fig


def plot_risk_distribution(df):

    fig = px.bar(

        df,

        x="Riesgo",

        y="Cantidad",

        color="Riesgo",

        color_discrete_map={

            "Bajo":SUCCESS,

            "Moderado":WARNING,

            "Alto":DANGER

        },

        text="Cantidad"

    )

    fig.update_traces(

        textposition="outside"

    )

    fig.update_layout(

        title="Distribución de Riesgo",

        showlegend=False

    )

    return apply_theme(fig)

def plot_gender_distribution(df):

    fig = px.pie(

        df,

        names="Sexo",

        values="Cantidad",

        hole=0.60,

        color="Sexo",

        color_discrete_sequence=[

            PRIMARY,

            SECONDARY,

            SUCCESS,

            WARNING

        ]

    )

    fig.update_layout(

        title="Distribución por Sexo"

    )

    return apply_theme(fig)

def plot_age_distribution(df):

    fig = px.bar(

        df,

        x="Cantidad",

        y="Rango",

        orientation="h",

        color="Cantidad",

        color_continuous_scale="Purples"

    )

    fig.update_layout(

        title="Distribución por Edad",

        coloraxis_showscale=False

    )

    return apply_theme(fig)

def plot_daily_evaluations(df):

    fig = px.line(

        df,

        x="Fecha",

        y="Cantidad",

        markers=True

    )

    fig.update_traces(

        line=dict(

            color=PRIMARY,

            width=4

        ),

        marker=dict(

            size=8

        )

    )

    fig.update_layout(

        title="Evaluaciones por Día"

    )

    return apply_theme(fig)