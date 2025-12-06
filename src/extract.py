import os
import requests
import json
from dotenv import load_dotenv

load_dotenv() # Una vez cargadas las variables de entorno del .env file podemos usarlas

def obtener_datos(league_name):
    api_token = os.getenv('API_TOKEN')

    if api_token is None:
        raise ValueError("API_TOKEN not found in environment variables")
    
    url = f'https://api.football-data.org/v4/competitions/{league_name}/standings'

    headers = {
        'X-Auth-Token': api_token # Es una restricción de clave valor de la API
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
    
# Bloque de ejecución: Solo corre si ejecutás este archivo directamente

if __name__ == "__main__":
    try:
        print("⏳ Buscando datos de la Premier League...")
        datos = obtener_datos('PL')
        
        print("✅ ¡Éxito! Datos recibidos.")
        
        temporada = datos['filters']['season']
        print(f"📅 Temporada: {temporada}")
        
        primer_equipo = datos['standings'][0]['table'][0]['team']['name']
        print(f"🥇 Puntero actual: {primer_equipo}")

    except Exception as e:
        print(f"❌ Error: {e}")