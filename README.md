# ⚽ Premier League End-to-End Data Engineering Project

## 📋 Descripción
Proyecto integral de Ingeniería de Datos que automatiza el ciclo de vida completo de la información deportiva: desde la ingesta de datos crudos hasta la visualización analítica para el usuario final.

El sistema consume la API de **Football-Data.org**, procesa estadísticas avanzadas con **Pandas**, persiste la historia en **SQLite** y despliega un dashboard interactivo en la nube. Todo el flujo es orquestado automáticamente mediante **CI/CD** con notificaciones en tiempo real.

### 🔴 [Ver Dashboard en Vivo](https://premierleagueanalytics.streamlit.app/)

---

## 🚀 Arquitectura del Sistema
El proyecto sigue una arquitectura moderna y modular:

1.  **Ingestion Layer (Extract):** Conexión robusta a API REST con manejo de `Rate Limiting` y seguridad de credenciales.
2.  **Processing Layer (Transform):** Limpieza de JSONs anidados, normalización de tipos de datos y cálculo de métricas avanzadas (*Win Rate, Goles/PJ, Cuadrantes de Rendimiento*).
3.  **Storage Layer (Load):** Persistencia incremental en base de datos relacional **SQLite**.
4.  **Automation & CI/CD:** Pipeline configurado en **GitHub Actions** que ejecuta el proceso ETL diariamente (Cron Job) en un entorno Linux aislado.
5.  **Alerting System:** Integración con **Discord Webhooks** para monitoreo proactivo del estado del pipeline (éxito/fallo) y tiempos de ejecución.
6.  **Visualization Layer:** Web App interactiva construida con **Streamlit** y **Plotly** para análisis de datos exploratorio (EDA).

---

## 🛠️ Tech Stack
* **Lenguaje:** Python 3.10+
* **ETL:** Pandas, Requests, SQLAlchemy, Python-Dotenv.
* **Visualización:** Streamlit, Plotly Express, Plotly Graph Objects.
* **Infraestructura:** GitHub Actions (Runner Ubuntu).
* **Monitoreo:** Discord API (Webhooks).

---

## ⚙️ Instalación y Ejecución Local

Si deseas correr este proyecto en tu propia máquina:

1. **Clonar el repositorio**
   ```bash
   git clone [https://github.com/IgnacioAlgarin/premier_league_pipeline.git](https://github.com/IgnacioAlgarin/premier_league_pipeline.git)
   cd premier_league_pipeline

2. **Instalar dependencias**
    pip install -r requirements.txt

3. **Configurar variables de entorno**
    Crear un archivo .env en la raíz y agregar tu API Key (conseguila gratis en football-data.org):
    API_TOKEN=tu_api_key_aqui
    DB_NAME=premier_league.db
    DISCORD_WEBHOOK_URL=tu_url_de_discord

4. **Correr el pipeline**
    python src/main.py

5. **Lanzar el Dashboard**
    streamlit run src/dashboard.py

## 📊 Resultados
KPIs en Tiempo Real: Líder, promedios de gol y defensas destacadas.

Matriz de Rendimiento: Scatter Plot interactivo de Ataque vs. Defensa con tooltips detallados.

Radar Charts: Comparativa táctica de cada equipo contra el promedio de la liga.

Data Grid: Tabla de posiciones con Heatmaps condicionales y exportación a CSV.

Desarrollado por Ignacio Algarin como parte de portfolio de Ingeniería de Datos.