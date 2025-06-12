import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Audios",
    page_icon="🎵",
    layout="wide"
)

# Configuración de la API
API_BASE_URL = "http://127.0.0.1:8000"

def get_audio_stats(periodo='total', limit=10):
    """Obtiene estadísticas de audios desde la API"""
    # apunto a la URL correcta de Mi Api Rest
    url = f"{API_BASE_URL}/api/audios/stats/mas_reproducidos/"  
    try:
        response = requests.get(url, params={'periodo': periodo, 'limit': limit})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Error {response.status_code}: No se pudo obtener los datos de la API.")
            st.error(f"URL intentada: {url}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("🔌 No se pudo conectar con la API. ¿Está corriendo el servidor Django?")
        st.error(f"URL intentada: {url}")
        return []
    except Exception as e:
        st.error(f"⚠️ Error inesperado al conectar con la API: {e}")
        return []
def get_all_audios():
    """Obtiene todos los audios desde la API"""
    url = f"{API_BASE_URL}/api/audios/"  # debo asegurarme de que este endpoint exista
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Error {response.status_code}: No se pudo obtener la lista de audios.")
            return []
    except Exception as e:
        st.error(f"⚠️ Error al obtener audios: {e}")
        return []

# Título principal
st.title("🎵 Dashboard de Análisis de Audios")
st.markdown("---")

# Sidebar para filtros
st.sidebar.header("Filtros")
periodo = st.sidebar.selectbox(
    "Período de análisis:",
    ["total", "mes", "semana"],
    format_func=lambda x: {"total": "Todo el tiempo", "mes": "Último mes", "semana": "Última semana"}[x]
)
limite_audios = st.sidebar.slider("Número de audios a mostrar:", 1, 50, 10)

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

# Obtengo los  datos
audios_data = get_audio_stats(periodo, limite_audios)

if audios_data:
    df = pd.DataFrame(audios_data)

    # Verifico  que los campos existan antes de usarlos
    campo_reproducciones = 'total_reproducciones' if periodo == 'total' else f'reproducciones_{periodo}'
    if campo_reproducciones not in df.columns:
        st.error(f"🚫 El campo '{campo_reproducciones}' no existe en los datos recibidos.")
        st.write("Campos disponibles:", list(df.columns))
        st.stop()

    # Calcular métricas
    total_reproducciones = df[campo_reproducciones].sum()
    audio_mas_popular = df.iloc[0]['titulo'] if len(df) > 0 else "N/A"
    
    #  Aquí puedo  cambiaar  a 'artista' si el  modelo lo usa
    interprete_mas_popular = df['interprete'].mode()[0] if 'interprete' in df.columns and len(df) > 0 else "N/A"
    promedio_reproducciones = df[campo_reproducciones].mean()

    with col1:
        st.metric("Total Reproducciones", f"{total_reproducciones:,}")

    with col2:
        st.metric("Audio Más Popular", audio_mas_popular)

    with col3:
        st.metric("Intérprete Más Popular", interprete_mas_popular)

    with col4:
        st.metric("Promedio por Audio", f"{promedio_reproducciones:.1f}")

    st.markdown("---")

    # Gráficos principales
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔥 Top Audios Más Reproducidos")

        df_top = df.head(10).copy()
        df_top['titulo_corto'] = df_top['titulo'].apply(lambda x: x[:30] + '...' if len(x) > 30 else x)

        fig_bar = px.bar(
            df_top,
            x=campo_reproducciones,
            y='titulo_corto',
            orientation='h',
            title=f"Reproducciones ({periodo})",
            color=campo_reproducciones,
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("🎭 Distribución por Intérprete")

        if 'interprete' in df.columns:
            interprete_stats = df.groupby('interprete')[campo_reproducciones].sum().sort_values(ascending=False).head(8)
            fig_pie = px.pie(
                values=interprete_stats.values,
                names=interprete_stats.index,
                title="Reproducciones por Intérprete"
            )
            fig_pie.update_layout(height=500)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("⚠️ No hay información disponible sobre los intérpretes.")

    # Tabla detallada
    st.subheader("📊 Tabla Detallada")

    df_display = df.copy()
    df_display = df_display.rename(columns={
        'titulo': 'Título',
        'interprete': 'Intérprete',
        'compositor': 'Compositor',
        'total_reproducciones': 'Total',
        'reproducciones_mes': 'Último Mes',
        'reproducciones_semana': 'Última Semana'
    })

    # Mostrar columnas relevantes según el período
    if periodo == 'total':
        columns_to_show = ['Título', 'Intérprete', 'Compositor', 'Total']
    elif periodo == 'mes':
        columns_to_show = ['Título', 'Intérprete', 'Compositor', 'Último Mes', 'Total']
    else:
        columns_to_show = ['Título', 'Intérprete', 'Compositor', 'Última Semana', 'Total']

    existing_columns = [col for col in columns_to_show if col in df_display.columns]

    st.dataframe(
        df_display[existing_columns],
        use_container_width=True,
        hide_index=True
    )

    # Análisis adicionales
    st.markdown("---")
    st.subheader("📈 Análisis Adicional")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Top 5 Compositores:**")
        if 'compositor' in df.columns:
            compositor_stats = df.groupby('compositor')[campo_reproducciones].sum().sort_values(ascending=False).head(5)
            for compositor, reproducciones in compositor_stats.items():
                st.write(f"• {compositor}: {reproducciones:,} reproducciones")
        else:
            st.write("No hay información sobre compositores.")

    with col2:
        st.write("**Estadísticas Generales:**")
        st.write(f"• Total de audios analizados: {len(df)}")
        st.write(f"• Reproducción máxima: {df[campo_reproducciones].max():,}")
        st.write(f"• Reproducción mínima: {df[campo_reproducciones].min():,}")
        st.write(f"• Desviación estándar: {df[campo_reproducciones].std():.1f}")

else:
    st.warning("⚠️ No se pudieron cargar los datos. Verifica la conexión con la API.")
    st.info("Asegúrate de que tu servidor Django esté ejecutándose y los endpoints estén configurados correctamente.")

    if st.button("🧪 Probar conexión con API"):
        st.write("Probando conexión...")
        audios_basicos = get_all_audios()
        if audios_basicos:
            st.success(f"✅ Conexión exitosa! Se encontraron {len(audios_basicos)} audios.")
            st.write("Ejemplo de datos:", audios_basicos[0] if audios_basicos else "No hay datos")
        else:
            st.error("❌ No se pudo conectar con la API básica.")

# Botón de actualización
if st.button("🔄 Actualizar Datos"):
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*Dashboard actualizado automáticamente desde tu API de Django*")