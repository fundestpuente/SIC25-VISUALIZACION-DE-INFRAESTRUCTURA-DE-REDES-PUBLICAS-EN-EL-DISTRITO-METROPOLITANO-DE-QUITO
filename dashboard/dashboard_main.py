# Este script es para ejecutar el dashboard y presentar los datos obtenidos del módulo visualizacion anteriormente.
# Se ejecuta mediante el módulo dash.

# Módulos principales del script.
import dash, webbrowser
from dash import html, dcc, Input, Output
from threading import Timer
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Configuración de rutas para acceder a los datos generados por el equipo.
BASE_DIR = Path(__file__).parent.parent
VISUALIZACION_DIR = BASE_DIR / 'visualizacion'
RESULTADOS_DIR = VISUALIZACION_DIR / 'resultados'
ESTADISTICAS_DIR = BASE_DIR / 'estadisticas' / 'resultados'
DATOS_PROCESADOS_DIR = BASE_DIR / 'manejo_de_datos'

# Inicializar el dashboard
app = dash.Dash(__name__)

# Servir archivos estáticos
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Función para abrir el dashboard automáticamente en la dirección por defecto.
def abrir_dasboard_auto():
    webbrowser.open_new('http://127.0.0.1:8050')

# Función para cargar datos estadísticos
def cargar_estadisticas():
    """
    Carga las estadísticas ya calculadas desde los archivos CSV
    de los módulos locales del equipo.
    """
    try:
        # Cargar estadísticas básicas
        df_estadisticas = pd.read_csv(ESTADISTICAS_DIR / 'estadisticas_basicas.csv')

        # Cargar cobertura prioritaria
        df_cobertura = pd.read_csv(ESTADISTICAS_DIR / 'cobertura_prioritaria.csv')

        # Cargar datos procesados
        df_procesado = pd.read_csv(DATOS_PROCESADOS_DIR / 'zonas_puntos_wifi_procesados.csv')

        print("Datos estadísticos cargados correctamente.")
        return df_estadisticas, df_cobertura, df_procesado
    except Exception as e:
        print(f"Error cargando datos estadísticos: {e}")
        return None, None, None

# Cargar datos al iniciar
df_estadisticas, df_cobertura, df_procesado = cargar_estadisticas()

# Funciones para crear gráficos dinámicos con filtros
def crear_grafico_administracion_zonal(filtro_admin='all'):
    """
    Crea un gráfico de barras para puntos WiFi
    por administración zonal con filtro correspondiente.
    """
    if df_procesado is None or 'administracion_zonal' not in df_procesado.columns:
        return go.Figure()

    # Aplicar filtro si es necesario
    datos = df_procesado
    if filtro_admin != 'all':
        datos = datos[datos['administracion_zonal'] == filtro_admin]

    admin_counts = datos['administracion_zonal'].value_counts().reset_index()
    admin_counts.columns = ['administracion_zonal', 'total_puntos']

    fig = px.bar(admin_counts,
                 x='administracion_zonal',
                 y='total_puntos',
                 title=f'Distribución de puntos WiFi - {filtro_admin if filtro_admin != "all" else "Todas las zonas"}',
                 color='total_puntos',
                 color_continuous_scale='Darkmint')

    fig.update_layout(
        xaxis_title='Administración zonal',
        yaxis_title='Total de puntos WiFi',
        xaxis_tickangle=-45
    )
    return fig

def crear_grafico_top_parroquias(filtro_admin='all'):
    """Crea gráfico de barras para top 10 parroquias con filtro"""
    if df_estadisticas is None or 'parroquia' not in df_estadisticas.columns:
        return go.Figure()

    # Si tenemos datos procesados, podemos filtrar por administración zonal
    datos = df_estadisticas.copy()
    if filtro_admin != 'all' and df_procesado is not None:
        # Obtener parroquias de la administración zonal seleccionada
        parroquias_filtradas = df_procesado[df_procesado['administracion_zonal'] == filtro_admin]['parroquia'].unique()
        datos = datos[datos['parroquia'].isin(parroquias_filtradas)]

    top_parroquias = datos.nlargest(10, 'total_puntos')

    fig = px.bar(top_parroquias,
                 x='parroquia',
                 y='total_puntos',
                 title=f'Top 10 parroquias - {filtro_admin if filtro_admin != "all" else "Todas las zonas"}',
                 color='total_puntos',
                 color_continuous_scale='Sunset')

    fig.update_layout(
        xaxis_title='Parroquia',
        yaxis_title='Número de puntos WiFi',
        xaxis_tickangle=-45
    )
    return fig

def crear_grafico_densidad_vs_area(filtro_prioridad='all'):
    """Crea gráfico de dispersión para densidad vs área con filtro"""
    if df_cobertura is None or 'densidad_puntos' not in df_cobertura.columns:
        return go.Figure()

    # Aplicar filtro por prioridad
    datos = df_cobertura.copy()
    if filtro_prioridad != 'all':
        if filtro_prioridad == 'alta':
            datos = datos[datos['nivel_necesidad'] >= 4]
        elif filtro_prioridad == 'media':
            datos = datos[datos['nivel_necesidad'] == 3]
        elif filtro_prioridad == 'baja':
            datos = datos[datos['nivel_necesidad'] <= 2]

    fig = px.scatter(datos,
                     x='area_km2',
                     y='densidad_puntos',
                     size='area_km2',
                     color='nivel_necesidad',
                     hover_name='parroquia',
                     title=f'Densidad vs área - {filtro_prioridad if filtro_prioridad != "all" else "Todas las prioridades"}',
                     color_continuous_scale='Viridis',
                     labels={'nivel_necesidad': 'Nivel de necesidad'})

    fig.update_layout(
        xaxis_title='Área (km²)',
        yaxis_title='Densidad de puntos WiFi (Puntos/km²)'
    )
    return fig

def crear_grafico_ranking_necesidad(filtro_prioridad='all'):
    """Crea gráfico de barras horizontales para ranking de necesidad con filtro"""
    if df_cobertura is None or 'nivel_necesidad' not in df_cobertura.columns:
        return go.Figure()

    # Aplicar filtro por prioridad
    datos = df_cobertura.copy()
    if filtro_prioridad != 'all':
        if filtro_prioridad == 'alta':
            datos = datos[datos['nivel_necesidad'] >= 4]
        elif filtro_prioridad == 'media':
            datos = datos[datos['nivel_necesidad'] == 3]
        elif filtro_prioridad == 'baja':
            datos = datos[datos['nivel_necesidad'] <= 2]

    ranking = datos.groupby('parroquia')['nivel_necesidad'].mean().nlargest(10).reset_index()
    ranking = ranking.sort_values('nivel_necesidad', ascending=True)

    fig = px.bar(ranking,
                 y='parroquia',
                 x='nivel_necesidad',
                 title=f'Ranking de necesidad - {filtro_prioridad if filtro_prioridad != "all" else "Todas las prioridades"}',
                 orientation='h',
                 color='nivel_necesidad',
                 color_continuous_scale='Reds')

    fig.update_layout(
        xaxis_title='Nivel de necesidad (Score)',
        yaxis_title='Parroquia'
    )
    return fig

# Obtener métricas principales desde las estadísticas
def obtener_metricas_principales():
    """Obtiene las métricas principales desde los datos estadísticos"""
    if df_estadisticas is not None and df_cobertura is not None:
        total_puntos = df_estadisticas['total_puntos'].sum()
        parroquias_unicas = len(df_estadisticas)
        admin_zonales = df_procesado['administracion_zonal'].nunique() if df_procesado is not None else 0
        brecha_digital = len(df_cobertura[df_cobertura['nivel_necesidad'] >= 4])

        return total_puntos, parroquias_unicas, admin_zonales, brecha_digital
    return "N/A", "N/A", "N/A", "N/A"

total_puntos, parroquias_unicas, admin_zonales, brecha_digital = obtener_metricas_principales()

# Obtener opciones para filtros
def obtener_opciones_filtros():
    if df_procesado is not None:
        opciones_admin = [{'label': 'Todas las zonas', 'value': 'all'}] + [
            {'label': admin, 'value': admin}
            for admin in sorted(df_procesado['administracion_zonal'].unique())
        ]

        opciones_parroquia = [{'label': 'Todas las parroquias', 'value': 'all'}] + [
            {'label': parroquia, 'value': parroquia}
            for parroquia in sorted(df_procesado['parroquia'].unique())
        ]

        return opciones_admin, opciones_parroquia
    return [], []

opciones_admin, opciones_parroquia = obtener_opciones_filtros()

# Estilos CSS personalizados para que el dashboard se vea bonito c:
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard puntos WiFi - DMQ</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(127deg, #ff9a00 45%, #ff5e00 45%);
                min-height: 100vh;
            }

            .dashboard-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }

            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .main-title {
                color: #2c3e50;
                font-size: 2.5em;
                font-weight: 700;
                margin-bottom: 10px;
                background: linear-gradient(127deg, #1e3c72, #2a5298);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .subtitle {
                color: #7f8c8d;
                font-size: 1.2em;
                font-weight: 300;
            }

            .section {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .section:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
            }

            .section-title {
                color: #2c3e50;
                font-size: 1.8em;
                font-weight: 600;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .section-title::before {
                content: '';
                width: 4px;
                height: 25px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 2px;
            }

            .filter-container {
                background: rgba(248, 249, 250, 0.8);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 20px;
                border: 1px solid rgba(236, 240, 241, 0.5);
            }

            .filter-label {
                color: #2c3e50;
                font-weight: 600;
                margin-bottom: 10px;
                display: block;
            }

            .dropdown {
                border-radius: 10px;
                border: 2px solid #e9ecef;
                transition: all 0.3s ease;
            }

            .dropdown:hover {
                border-color: #667eea;
            }

            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }

            .metric-card {
                background: rgba(255, 255, 255, 0.9);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.3);
                transition: transform 0.3s ease;
            }

            .metric-card:hover {
                transform: translateY(-3px);
            }

            .metric-value {
                font-size: 2.5em;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 5px;
            }

            .metric-label {
                color: #7f8c8d;
                font-size: 0.9em;
                font-weight: 500;
            }

            .graph-container {
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                margin-bottom: 20px;
            }

            .map-container {
                width: 100%;
                height: 600px;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }

            .footer {
                text-align: center;
                color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                font-size: 0.9em;
                margin-top: 40px;
            }

            /* Responsive design */
            @media (max-width: 768px) {
                .dashboard-container {
                    padding: 10px;
                }

                .main-title {
                    font-size: 2em;
                }

                .section {
                    padding: 20px;
                }

                .metrics-grid {
                    grid-template-columns: 1fr;
                }

                .map-container {
                    height: 400px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Diseño del dashboard e implementación de filtros
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1("Dashboard de análisis - Puntos WiFi en Quito", className="main-title"),
            html.P(
                "VISUALIZACION DE INFRAESTRUCTURA DE REDES PUBLICAS EN EL DISTRITO METROPOLITANO DE QUITO",
                className="subtitle")
        ], className="header"),

        # Métricas principales básicas
        html.Div([
            html.Div([
                html.Div(f"{total_puntos}", className="metric-value"),
                html.Div("Total de puntos WiFi", className="metric-label")
            ], className="metric-card"),

            html.Div([
                html.Div(f"{parroquias_unicas}", className="metric-value"),
                html.Div("Parroquias cubiertas", className="metric-label")
            ], className="metric-card"),

            html.Div([
                html.Div(f"{admin_zonales}", className="metric-value"),
                html.Div("Administraciones zonales", className="metric-label")
            ], className="metric-card"),

            html.Div([
                html.Div(f"{brecha_digital}", className="metric-value"),
                html.Div("Zonas con alta brecha digital", className="metric-label")
            ], className="metric-card"),
        ], className="metrics-grid"),

        # Sección: Gráficos estadísticos
        html.Div([
            html.H2("Estadísticas de cobertura en la ciudad", className="section-title"),

            html.Div([
                html.Label("Filtrar por administración zonal", className="filter-label"),
                dcc.Dropdown(
                    id="filtro-admin-zonal",
                    options=opciones_admin,
                    value='all',
                    className="dropdown"
                ),
            ], className="filter-container"),

            # Gráficos dinámicos
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='grafico-admin-zonal'
                    )
                ], className="graph-container"),

                html.Div([
                    dcc.Graph(
                        id='grafico-top-parroquias'
                    )
                ], className="graph-container")
            ])
        ], className="section"),

        # Sección: Mapa interactivo
        html.Div([
            html.H2("Mapa interactivo de puntos WiFi", className="section-title"),

            # Mapa interactivo
            html.Div([
                html.Iframe(
                    id="mapa-interactivo",
                    srcDoc=open(VISUALIZACION_DIR / 'mapa_wifi_quito.html', 'r', encoding='utf-8').read()
                    if (VISUALIZACION_DIR / 'mapa_wifi_quito.html').exists() else
                    "<div style='padding: 20px; text-align: center;'>Mapa no disponible. Ejecute maps.py primero.</div>",
                    className="map-container"
                )
            ])
        ], className="section"),

        # Sección: Zonas prioritarias
        html.Div([
            html.H2("Análisis de posibles zonas prioritarias", className="section-title"),

            html.Div([
                html.Label("Filtrar por nivel de prioridad", className="filter-label"),
                dcc.Dropdown(
                    id="filtro-prioridad",
                    options=[
                        {'label': 'Todas las Zonas', 'value': 'all'},
                        {'label': 'Alta Prioridad - Baja cobertura', 'value': 'alta'},
                        {'label': 'Prioridad Media - Cobertura aceptable', 'value': 'media'},
                        {'label': 'Baja Prioridad - Buena cobertura', 'value': 'baja'}
                    ],
                    value='all',
                    className="dropdown"
                ),
            ], className="filter-container"),

            # Gráficos de priorización
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='grafico-densidad-area'
                    )
                ], className="graph-container"),

                html.Div([
                    dcc.Graph(
                        id='grafico-ranking-necesidad'
                    )
                ], className="graph-container")
            ])
        ], className="section"),

        # Footer
        html.Div([
            html.P(
                "Proyecto VISUALIZACION DE INFRAESTRUCTURA DE REDES PUBLICAS EN EL DISTRITO METROPOLITANO DE QUITO"),
            html.P("Datos proporcionados por el API de puntos WiFi del Distrito Metropolitano de Quito"),
            html.P("Elaborado para el Samsung Innovation Campus 2025")
        ], className="footer")

    ], className="dashboard-container")
])

# Callbacks para los filtros, para actualizarlos de forma dinámica.
@app.callback(
    [Output('grafico-admin-zonal', 'figure'),
     Output('grafico-top-parroquias', 'figure')],
    [Input('filtro-admin-zonal', 'value')]
)
def actualizar_graficos_estadisticas(filtro_admin):
    """
    Actualiza ambos gráficos de estadísticas cuando cambia el filtro de administración zonal
    """
    grafico1 = crear_grafico_administracion_zonal(filtro_admin)
    grafico2 = crear_grafico_top_parroquias(filtro_admin)
    return grafico1, grafico2

@app.callback(
    [Output('grafico-densidad-area', 'figure'),
     Output('grafico-ranking-necesidad', 'figure')],
    [Input('filtro-prioridad', 'value')]
)
def actualizar_graficos_prioridad(filtro_prioridad):
    """
    Actualiza ambos gráficos de prioridad cuando cambia el filtro de nivel de prioridad
    """
    grafico1 = crear_grafico_densidad_vs_area(filtro_prioridad)
    grafico2 = crear_grafico_ranking_necesidad(filtro_prioridad)
    return grafico1, grafico2

# Configuración final, verificación de archivos
if __name__ == '__main__':
    print("=== Inicializando el dashboard ===")
    print("Verificando componentes...")

    # Verificar que los módulos necesarios existen
    componentes = {
        'diagramas.py': VISUALIZACION_DIR / 'diagramas.py',
        'maps.py': VISUALIZACION_DIR / 'maps.py',
        'datos procesados': DATOS_PROCESADOS_DIR / 'zonas_puntos_wifi_procesados.csv',
        'estadísticas básicas': ESTADISTICAS_DIR / 'estadisticas_basicas.csv',
        'cobertura prioritaria': ESTADISTICAS_DIR / 'cobertura_prioritaria.csv'
    }

    for nombre, ruta in componentes.items():
        if ruta.exists():
            print(f"{nombre} encontrado")
        else:
            print(f"{nombre} NO encontrado")

    Timer(1, abrir_dasboard_auto).start()

    app.run(debug=False, use_reloader=False)