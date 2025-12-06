# ⚽ Premier League ETL Pipeline

## 📋 Descripción
Pipeline de Ingeniería de Datos automatizado para la extracción, transformación y carga (ETL) de estadísticas de fútbol en tiempo real.
Este proyecto consume datos de la API de **Football-Data.org**, procesa métricas clave de rendimiento de los equipos y persiste la información histórica en una base de datos **SQL** relacional.

## 🚀 Arquitectura del Proyecto
El flujo de datos sigue una arquitectura modular:

1.  **Extract:** Conexión a API REST con manejo de autenticación (Headers) y tolerancia a fallos de red.
2.  **Transform:** Limpieza de JSON anidado, normalización de datos y cálculo de métricas (Puntos, Dif. de Gol) utilizando **Pandas**.
3.  **Load:** Persistencia de datos en **SQLite** utilizando **SQLAlchemy** con control de transacciones.
4.  **Orchestration:** Script maestro (`main.py`) que coordina el flujo y mide tiempos de ejecución.

## 🛠️ Tecnologías Utilizadas
* **Python 3.10+**
* **Pandas** (Transformación de datos)
* **Requests** (Consumo de API)
* **SQLAlchemy** (ORM y Conexión a Base de Datos)
* **Python-Dotenv** (Gestión de variables de entorno y seguridad)

## ⚙️ Cómo ejecutar este proyecto

1. **Clonar el repositorio**
   ```bash
   git clone [https://github.com/TU_USUARIO/futbol-etl.git](https://github.com/TU_USUARIO/futbol-etl.git)
   cd futbol-etl

2. **Instalar dependencias**
    pip install -r requirements.txt

3. **Configurar variables de entorno**
    Crear un archivo .env en la raíz y agregar tu API Key (conseguila gratis en football-data.org):
    API_TOKEN=tu_api_key_aqui
    DB_NAME=premier_league.db

4. **Correr el pipeline**
    python src/main.py

## 📊 Resultados
Al finalizar la ejecución, se generará una base de datos en data/processed/premier_league.db con la tabla posiciones_PL actualizada al día de la fecha.