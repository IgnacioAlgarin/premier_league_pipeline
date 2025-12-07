import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Premier League Analytics Pro",
    layout="wide",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS ---
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #0e1117;
        border-radius: 4px 4px 0px 0px;
        border: 1px solid #333;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #00ff00;
    }
    
    /* --- NUEVO: LOGO BLANCO EN SIDEBAR --- */
    /* Apuntamos a cualquier imagen (img) que esté adentro del sidebar */
    [data-testid="stSidebar"] img {
        /* brightness(0) lo pone negro, invert(1) lo pasa a blanco */
        filter: brightness(0) invert(1); 
        opacity: 0.9; /* Un toque de transparencia para que se fusione mejor */
    }
    
</style>
""", unsafe_allow_html=True)

# --- 3. CARGA DE DATOS ---
@st.cache_data
def load_data():
    db_path = 'data/processed/premier_league.db'
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    # Cargamos todo
    df = pd.read_sql("SELECT * FROM posiciones_PL", conn)
    conn.close()
    
    # CALCULAMOS MÉTRICAS AVANZADAS
    if df is not None:
        # Win Rate: (Victorias / Partidos Jugados) * 100
        df['Win Rate %'] = ((df['Victorias'] / df['Partidos Jugados']) * 100).round(1)
        # Goles por Partido
        df['Goles/PJ'] = (df['Goles a Favor'] / df['Partidos Jugados']).round(2)
    
    return df

df = load_data()

# --- 4. SIDEBAR (FILTROS GLOBALES) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg", width=150)
    st.header("⚙️ Panel de Control")
    
    if df is not None:
        # Filtro de Equipo Principal (Focus)
        equipos = df['Equipo'].unique().tolist()
        equipo_seleccionado = st.selectbox("Seleccionar Equipo a Analizar:", equipos, index=0)
        
        st.divider()
        
        # Mini perfil del equipo seleccionado
        datos_equipo = df[df['Equipo'] == equipo_seleccionado].iloc[0]
        st.write(f"**{equipo_seleccionado}**")
        st.write(f"📍 Posición: {datos_equipo['Posición']}")
        st.write(f"📈 Puntos: {datos_equipo['Puntos']}")
        st.progress(int(datos_equipo['Win Rate %']))
        st.caption(f"Win Rate: {datos_equipo['Win Rate %']}%")

    st.markdown("---")
    st.info("Dashboard desarrollado con **Python + Streamlit + Plotly**.")

# --- 5. CONTENIDO PRINCIPAL ---
if df is not None:
    # Título Principal
    col_logo, col_titulo = st.columns([1, 6])
    with col_titulo:
        st.title("⚽ Premier League: Intelligence Hub")
        st.markdown(f"Análisis detallado de la temporada. Última actualización: **En tiempo real**.")

    # --- KPIs GLOBALES (Tarjetas) ---
    st.markdown("### 📊 Métricas de Liga")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    puntero = df.iloc[0]
    promedio_gol = df['Goles a Favor'].mean()
    
    kpi1.metric("🏆 Líder Actual", puntero['Equipo'], f"{puntero['Puntos']} Pts")
    kpi2.metric("⚽ Promedio Goles/Equipo", f"{promedio_gol:.1f}")
    kpi3.metric("🔥 Equipo + Goleador", df.loc[df['Goles a Favor'].idxmax()]['Equipo'], f"{df['Goles a Favor'].max()} GF")
    kpi4.metric("🧱 Muro Defensivo", df.loc[df['Goles en Contra'].idxmin()]['Equipo'], f"{df['Goles en Contra'].min()} GC")

    st.markdown("---")

    # --- PESTAÑAS (TABS) ---
    tab1, tab2, tab3 = st.tabs(["🌍 Panorama General", "🔍 Análisis de Equipo (Radar)", "📋 Base de Datos"])

    # === TAB 1: PANORAMA (SCATTER & BARS) ===
    with tab1:
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Cuadrantes: Ataque vs Defensa")
            st.markdown("💡 *Pasá el mouse sobre los puntos para ver el equipo.*")
            
            # Scatter Plot Interactivo (CORREGIDO)
            fig_scatter = px.scatter(
                df, 
                x="Goles a Favor", 
                y="Goles en Contra", 
                color="Puntos",
                size="Puntos",
                hover_name="Equipo", 
                hover_data={
                    "Puntos": True,
                    "Goles a Favor": True,
                    "Goles en Contra": True,
                    "Win Rate %": True
                    # BORRAMOS LA LÍNEA QUE DECÍA "size": False
                },
                color_continuous_scale="RdYlGn",
                title="Rendimiento Ofensivo vs Defensivo",
                template="plotly_dark",
                height=500,
                size_max=30
            )
            
            # Ajustes visuales y Líneas de Promedio
            fig_scatter.update_yaxes(autorange="reversed", title="Goles en Contra (Menos es mejor)")
            fig_scatter.update_xaxes(title="Goles a Favor (Más es mejor)")
            
            fig_scatter.add_hline(y=df['Goles en Contra'].mean(), line_dash="dot", line_color="gray", annotation_text="Promedio Defensa")
            fig_scatter.add_vline(x=df['Goles a Favor'].mean(), line_dash="dot", line_color="gray", annotation_text="Promedio Ataque")
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_right:
            st.subheader("Top 10: Eficiencia")
            # Bar Chart ordenado por Win Rate
            top_10_win = df.nlargest(10, 'Win Rate %')
            fig_bar = px.bar(
                top_10_win,
                x='Win Rate %',
                y='Equipo',
                orientation='h',
                color='Win Rate %',
                color_continuous_scale='Greens',
                template="plotly_dark",
                text_auto='.1f'
            )
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)

    # === TAB 2: RADAR CHART (COMPARATIVA) ===
    with tab2:
        st.subheader(f"Radiografía: {equipo_seleccionado} vs Promedio de la Liga")
        
        col_radar, col_stats = st.columns([2, 1])
        
        with col_radar:
            # Preparamos datos del Radar
            stats_team = df[df['Equipo'] == equipo_seleccionado].iloc[0]
            stats_avg = df.mean(numeric_only=True)
            
            categories = ['Win Rate %', 'Goles a Favor', 'Puntos', 'Partidos Jugados', 'Goles/PJ']
            
            values_team = [stats_team['Win Rate %'], stats_team['Goles a Favor'], stats_team['Puntos'], stats_team['Partidos Jugados'], stats_team['Goles/PJ']*10]
            values_avg = [stats_avg['Win Rate %'], stats_avg['Goles a Favor'], stats_avg['Puntos'], stats_avg['Partidos Jugados'], stats_avg['Goles/PJ']*10]
            
            fig_radar = go.Figure()

            # Capa Equipo
            fig_radar.add_trace(go.Scatterpolar(
                r=values_team,
                theta=categories,
                fill='toself',
                name=equipo_seleccionado,
                line_color='#00ff00'
            ))
            
            # Capa Promedio
            fig_radar.add_trace(go.Scatterpolar(
                r=values_avg,
                theta=categories,
                fill='toself',
                name='Promedio Liga',
                line_color='#ff0000',
                opacity=0.5,
                line=dict(dash='dash')
            ))

            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(values_team)*1.2])),
                showlegend=True,
                template="plotly_dark",
                height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with col_stats:
            st.info("💡 Cómo leer esto:")
            st.markdown("""
            - **Verde > Rojo:** El equipo supera el promedio.
            - **Rojo > Verde:** El equipo está por debajo.
            - **Forma Amplia:** Equipo balanceado.
            """)
            
            st.metric("Racha (Win Rate)", f"{stats_team['Win Rate %']}%", delta=f"{stats_team['Win Rate %'] - stats_avg['Win Rate %']:.1f}% vs Avg")
            st.metric("Potencia de Gol", f"{stats_team['Goles a Favor']}", delta=f"{int(stats_team['Goles a Favor'] - stats_avg['Goles a Favor'])} vs Avg")

    # === TAB 3: DATA GRID ===
    with tab3:
        st.subheader("Base de Datos Completa")
        
        # Botón de Descarga
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name='premier_league_data.csv',
            mime='text/csv',
        )
        
        # Tabla con Heatmap
        cols_show = ['Posición', 'Equipo', 'Puntos', 'Partidos Jugados', 'Victorias', 'Empates', 'Derrotas', 'Goles a Favor', 'Goles en Contra', 'Diferencia de Goles', 'Win Rate %']
        
        st.dataframe(
            df[cols_show].style
            .background_gradient(subset=['Puntos', 'Win Rate %'], cmap='Greens')
            .background_gradient(subset=['Goles a Favor'], cmap='Blues')
            .background_gradient(subset=['Goles en Contra'], cmap='Reds')
            .format({'Win Rate %': "{:.1f}%"}),
            use_container_width=True,
            height=600
        )

else:
    st.error("⚠️ No se encontró la base de datos. Asegurate de correr 'src/main.py' primero.")