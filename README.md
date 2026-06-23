# 🧠 MindAlert

## Plataforma Inteligente de Evaluación Preliminar de TDAH

MindAlert es una aplicación web desarrollada con Python, Streamlit y PostgreSQL que permite realizar una evaluación preliminar de TDAH (Trastorno por Déficit de Atención e Hiperactividad), registrar participantes, almacenar resultados y generar estadísticas para análisis posteriores.

> ⚠️ Importante: Esta herramienta no reemplaza una evaluación médica o psicológica profesional. Su propósito es servir como mecanismo de tamizaje y orientación inicial.

---

# 📖 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Objetivos del Proyecto](#-objetivos-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Flujo de Usuario](#-flujo-de-usuario)
- [Modelo de Datos](#-modelo-de-datos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Instalación Local](#-instalación-local)
- [Configuración Docker](#-configuración-docker)
- [Base de Datos](#-base-de-datos)
- [Estado Actual del Proyecto](#-estado-actual-del-proyecto)
- [Roadmap](#-roadmap)
- [Próximas Mejoras](#-próximas-mejoras)
- [Autor](#-autor)

---

# 🎯 Descripción General

MindAlert nace como una plataforma digital para facilitar la detección temprana de posibles síntomas asociados al TDAH mediante cuestionarios estructurados y almacenamiento de resultados para análisis posteriores.

La plataforma busca ofrecer:

- Acceso rápido a una evaluación preliminar.
- Experiencia amigable para usuarios.
- Persistencia segura de información.
- Estadísticas agregadas para investigación.
- Escalabilidad hacia un modelo SaaS.

---

# 🚀 Objetivos del Proyecto

## Objetivo General

Desarrollar una plataforma web que permita realizar evaluaciones preliminares de TDAH de forma digital, almacenando resultados y facilitando su análisis posterior.

## Objetivos Específicos

- Registrar participantes.
- Aplicar cuestionarios de evaluación.
- Calcular puntajes automáticamente.
- Clasificar niveles de riesgo.
- Almacenar información en PostgreSQL.
- Visualizar estadísticas en un dashboard.
- Generar reportes automáticos.
- Incorporar pagos electrónicos.
- Escalar hacia un producto SaaS.

---

# 🏗️ Arquitectura del Sistema

## Arquitectura de Alto Nivel

```text
┌───────────────────┐
│     Usuario       │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   Landing Page    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Registro Usuario  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Test de TDAH      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Resultado         │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ PostgreSQL        │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Dashboard Admin   │
└───────────────────┘
```

---

# 👤 Flujo de Usuario

```text
Usuario
   │
   ▼
Landing Page
   │
   ▼
Registro
   │
   ▼
Aceptación de Consentimiento
   │
   ▼
Test de Evaluación
   │
   ▼
Procesamiento de Puntaje
   │
   ▼
Resultado
   │
   ▼
Almacenamiento en PostgreSQL
```

---

# 🗄️ Modelo de Datos

## Tabla participants

```text
participants
│
├── id
├── created_at
├── full_name
├── email
├── age
├── gender
└── consent
```

### Descripción

| Campo | Tipo |
|---------|---------|
| id | Integer |
| created_at | DateTime |
| full_name | String |
| email | String |
| age | Integer |
| gender | String |
| consent | Boolean |

---

## Tabla evaluations

```text
evaluations
│
├── id
├── participant_id
├── score
├── max_score
├── probability_level
├── responses
└── created_at
```

### Descripción

| Campo | Tipo |
|---------|---------|
| id | Integer |
| participant_id | Integer |
| score | Integer |
| max_score | Integer |
| probability_level | String |
| responses | JSON |
| created_at | DateTime |

---

## Relación entre tablas

```text
participants
    │
    │ 1
    ▼
evaluations
    *
```

Un participante puede tener múltiples evaluaciones.

---

# 📂 Estructura del Proyecto

```text
tdah-mvp/
│
├── app/
│   │
│   ├── assets/
│   │
│   ├── components/
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── init_db.py
│   │
│   ├── pages/
│   │   ├── 00_registro.py
│   │   ├── 01_test.py
│   │   ├── 02_resultado.py
│   │   └── 03_dashboard.py
│   │
│   ├── services/
│   │   ├── questions.py
│   │   ├── scoring.py
│   │   ├── participant_service.py
│   │   └── evaluation_service.py
│   │
│   └── main.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

---

# 🛠️ Tecnologías Utilizadas

## Frontend

- Streamlit
- HTML
- CSS

## Backend

- Python 3.13

## ORM

- SQLAlchemy 2.x

## Base de Datos

- PostgreSQL 17

## Infraestructura

- Docker
- Docker Compose

## Gestión de Dependencias

- UV

---

# ⚙️ Instalación Local

## 1. Clonar repositorio

```bash
git clone https://github.com/tu_usuario/tdah-mvp.git

cd tdah-mvp
```

---

## 2. Crear entorno

```bash
uv sync
```

---

## 3. Configurar variables de entorno

Crear archivo:

```env
DATABASE_URL=postgresql+psycopg://admin:admin123@localhost:5435/tdah
```

---

## 4. Levantar PostgreSQL

```bash
docker compose up -d
```

Verificar:

```bash
docker ps
```

---

## 5. Crear tablas

```bash
uv run python app/database/init_db.py
```

---

## 6. Ejecutar aplicación

```bash
uv run streamlit run app/main.py
```

---

# 🐳 Configuración Docker

## Construir imagen

```bash
docker compose build
```

## Levantar servicios

```bash
docker compose up -d
```

## Ver logs

```bash
docker compose logs -f
```

## Detener servicios

```bash
docker compose down
```

---

# 🗃️ Base de Datos

## Acceso PostgreSQL

```bash
docker exec -it tdah-db psql -U admin -d tdah
```

## Consultar participantes

```sql
SELECT * FROM participants;
```

## Consultar evaluaciones

```sql
SELECT * FROM evaluations;
```

## Conteo de registros

```sql
SELECT COUNT(*) FROM participants;

SELECT COUNT(*) FROM evaluations;
```

---

# 📊 Estado Actual del Proyecto

## Día 1 — Arquitectura Base

- Estructura inicial del proyecto
- Navegación Streamlit

## Día 2 — Motor de Evaluación

- Preguntas
- Puntajes
- Niveles de riesgo

## Día 3 — Persistencia

- PostgreSQL
- SQLAlchemy
- Docker

## Día 4 — Registro

- Participantes
- Consentimiento
- Relación participante-evaluación

## Día 5 — Dashboard

- KPIs
- Estadísticas
- Visualización

## Sprint UX/UI

- Landing moderna
- Diseño responsive
- Hero section
- Branding MindAlert
- Experiencia visual mejorada

---

# 🛣️ Roadmap

## ✅ Completado

- [x] Día 1
- [x] Día 2
- [x] Día 3
- [x] Día 4
- [x] Día 5
- [x] Sprint UX/UI

---

## 🚧 Día 6

Correo automático de resultados.

```text
Resultado
    │
    ▼
Email
```

---

## 🚧 Día 7

Generación de PDF.

```text
Resultado
    │
    ▼
PDF Profesional
```

---

## 🚧 Día 8

Pasarela de Pago.

```text
Evaluación
      │
      ▼
Pago
      │
      ▼
Reporte Premium
```

---

## 🚧 Día 9

Historial de Evaluaciones.

```text
Usuario
     │
     ▼
Historial
```

---

## 🚧 Día 10

Dashboard SaaS.

```text
Usuarios
Evaluaciones
Conversiones
Ingresos
```

---

# 🔮 Próximas Mejoras

- Exportación PDF.
- Envío automático por correo.
- Login de usuarios.
- Panel administrativo avanzado.
- Integración con Mercado Pago.
- Integración con Stripe.
- Reportes estadísticos avanzados.
- Machine Learning para análisis predictivo.
- Aplicación móvil.

---

# 📈 Estado del MVP

```text
██████████████████░░░░░░░░░░

Arquitectura      ✅
Evaluación        ✅
Persistencia      ✅
Registro          ✅
Dashboard         ✅
UX/UI             ✅

Progreso estimado:
60% MVP Comercial
```

---

# 👨‍💻 Autor

**Alexander Olmedo Valdez Portocarrero**

- Instituto Geofísico del Perú (IGP)
- Maestría en Ciencias de la Computación
- Especialista en Machine Learning
- Especialista en Sistemas Radar

## Proyecto

**MindAlert — Plataforma Inteligente de Evaluación Preliminar de TDAH**

2026