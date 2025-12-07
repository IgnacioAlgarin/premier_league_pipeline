import time
import requests
import os
from extract import obtener_datos     
from transform import limpieza   
from load import guardar_datos     

def enviar_alerta_discord(mensaje):
    """Envía un mensaje al canal de Discord configurado."""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("⚠️ No se configuró el Webhook de Discord. Saltando notificación.")
        return

    try:
        data = {"content": mensaje}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("📨 Notificación enviada a Discord exitosamente.")
    except Exception as e:
        print(f"❌ Error al enviar a Discord: {e}")

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
        mensaje_final = f"✅ **Reporte Premier League**: Pipeline finalizado con éxito.\n⏱️ Tiempo: {elapsed_time:.2f}s.\n🏆 Datos actualizados en la base de datos."
        
        print(mensaje_final)
        enviar_alerta_discord(mensaje_final) # <--- LLAMAMOS AL BOT

    except Exception as e:
        error_msg = f"💥 **Error crítico** en el pipeline: {e}"
        print(error_msg)
        enviar_alerta_discord(error_msg) # <--- TAMBIÉN AVISAMOS SI FALLA

if __name__ == "__main__":
    # Acá podés cambiar 'PL' (Premier) por 'PD' (España) o 'CL' (Champions)
    correr_pipeline('PL')