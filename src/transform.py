import pandas as pd
from extract import obtener_datos

def limpieza(json_data):
    """
    Limpia y transforma los datos JSON de la API de fútbol en un DataFrame de pandas.
    
    Args:
        json_data (dict): Datos JSON obtenidos de la API.
        
    Returns:
        pd.DataFrame: DataFrame limpio con la información relevante.
    """

    lista_equipos = [standing['table'] for standing in json_data['standings'] if standing['type'] == 'TOTAL'][0]

    datos_para_tabla = []

    for equipo in lista_equipos:
        equipo_info = {
            'Posición': equipo['position'],
            'Equipo': equipo['team']['name'],
            'Puntos': equipo['points'],
            'Partidos Jugados': equipo['playedGames'],
            'Goles a Favor': equipo['goalsFor'],
            'Goles en Contra': equipo['goalsAgainst'],
            'Diferencia de Goles': equipo['goalDifference'],
            'Victorias': equipo['won'],
            'Empates': equipo['draw'],
            'Derrotas': equipo['lost']
        }
        datos_para_tabla.append(equipo_info)

    df = pd.DataFrame(datos_para_tabla)
    return df

if __name__ == "__main__":
    try:
        print("⏳ Transformando datos...")
        datos = obtener_datos('PL')
        df_limpio = limpieza(datos)
        
        print("✅ ¡Transformación exitosa! Aquí están los primeros 5 registros:")
        print(df_limpio.head())
        
    except Exception as e:
        print(f"❌ Error durante la transformación: {e}")


