import time
from extract import obtener_datos     
from transform import limpieza   
from load import guardar_datos     

def correr_pipeline(liga_codigo='PL'):
    """
    Orquesta el flujo ETL completo: API -> JSON -> Pandas -> SQLite.
    """
    print(f"🚀 Iniciando Pipeline para la liga: {liga_codigo}")
    start_time = time.time() # Cronómetro: Los ingenieros miden cuánto tarda todo
    
    try:
        # PASO 1: EXTRACT
        print("1️⃣ [EXTRACT] Buscando datos en la API...")
        json_crudo = obtener_datos(liga_codigo)
        
        if not json_crudo:
            print("⚠️ El proceso se detuvo: No vinieron datos.")
            return

        # PASO 2: TRANSFORM
        print("2️⃣ [TRANSFORM] Limpiando y estructurando datos...")
        df_limpio = limpieza(json_crudo)
        
        print(f"   -> Se encontraron {len(df_limpio)} equipos.")

        # PASO 3: LOAD
        print("3️⃣ [LOAD] Guardando en Base de Datos...")
        nombre_tabla = f"posiciones_{liga_codigo}" # Ej: posiciones_PL
        guardar_datos(df_limpio, nombre_tabla)
        
        # FIN
        elapsed_time = time.time() - start_time
        print(f"✅ ¡Pipeline finalizado con éxito! Tiempo total: {elapsed_time:.2f} segundos.")

    except Exception as e:
        print(f"💥 Error crítico en el pipeline: {e}")

if __name__ == "__main__":
    # Acá podés cambiar 'PL' (Premier) por 'PD' (España) o 'CL' (Champions)
    correr_pipeline('PL')