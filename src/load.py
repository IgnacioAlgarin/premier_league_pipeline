import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

def guardar_datos(df, tabla_nombre):
    """
    Guarda un DataFrame de pandas en una base de datos SQLite.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar.
        tabla_nombre (str): Nombre de la tabla en la base de datos.
    """
    db_name = os.getenv('DB_NAME', 'futbol_data.db')
    ruta_carpeta = 'data/processed'
    os.makedirs(ruta_carpeta, exist_ok=True)  # Crear carpeta si no existe

    engine = create_engine(f'sqlite:///{ruta_carpeta}/{db_name}')
    
    try:
        df.to_sql(tabla_nombre, con=engine, if_exists='replace', index=False)
        print(f"✅ Datos guardados exitosamente en la tabla '{tabla_nombre}' de la base de datos '{db_name}'.")
    
    except Exception as e:
        print(f"❌ Error al guardar los datos: {e}")


if __name__ == "__main__":
    try:
        print("⏳ Guardando datos en la base de datos...")
        
        # Ejemplo de DataFrame para guardar
        datos_ejemplo = {
            'Posición': [1, 2, 3],
            'Equipo': ['Equipo A', 'Equipo B', 'Equipo C'],
            'Puntos': [75, 70, 65]
        }
        df_ejemplo = pd.DataFrame(datos_ejemplo)
        
        guardar_datos(df_ejemplo, 'tabla_equipos')
        
    except Exception as e:
        print(f"❌ Error al guardar los datos: {e}")