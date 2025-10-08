import pandas as pd
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN DE RUTAS ---

# Obtener la ruta base del proyecto
RUTA_BASE = os.path.dirname(os.path.dirname(__file__))

# Rutas de Archivos de Entrada (CSV)
RUTA_DATOS_ZONAS_PUNTOS_PROCESADOS = os.path.join(RUTA_BASE, 'manejo_de_datos', 'zonas_puntos_wifi_procesados.csv')
RUTA_ESTADISTICAS_BASICAS = os.path.join(RUTA_BASE, "estadisticas", "resultados", "estadisticas_basicas.csv")
RUTA_COBERTURA_PRIORITARIA = os.path.join(RUTA_BASE, "estadisticas", "resultados", "cobertura_prioritaria.csv")

# Directorio de Salida para los Diagramas
DIRECTORIO_SALIDA = os.path.join(RUTA_BASE, 'visualizacion', 'resultados')


# --- FUNCIÓN DE CARGA DE DATOS ---

def cargar_datos(file_path):
    """Carga un DataFrame específico y maneja errores."""
    try:
        df = pd.read_csv(file_path)
        print(f"Datos cargados: {file_path}")
        return df
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado en {file_path}. Ejecuta la Persona 1/2 primero.")
        return None
    except Exception as e:
        print(f"ERROR al cargar {file_path}: {e}")
        return None


# --- FUNCIÓN DE UTILIDAD PARA GUARDAR ---

def guardar_diagrama(plt_object, filename):
    """Crea el directorio de salida si no existe y guarda el gráfico."""

    # 1. Crear el directorio si no existe
    if not os.path.exists(DIRECTORIO_SALIDA):
        os.makedirs(DIRECTORIO_SALIDA)
        print(f"Directorio creado: {DIRECTORIO_SALIDA}")

    # 2. Construir la ruta completa de salida
    output_path = os.path.join(DIRECTORIO_SALIDA, filename)

    # 3. Guardar la figura
    plt_object.savefig(output_path)
    plt_object.close()
    print(f"Diagrama guardado: {output_path}")


# --- FUNCIONES DE GENERACIÓN DE GRÁFICOS ---

def diagrama_puntos_por_administracion_zonal():
    """Diagrama de Barras: Distribución de infraestructura por Administración Zonal."""
    df = cargar_datos(RUTA_DATOS_ZONAS_PUNTOS_PROCESADOS)
    if df is None or 'administracion_zonal' not in df.columns:
        print("Saltando Diagrama de Barras por administracion zonal.")
        return

    admin_counts = df['administracion_zonal'].value_counts()

    plt.figure(figsize=(12, 6))
    plt.bar(admin_counts.index, admin_counts.values, color='#3498DB')

    plt.title('Distribución de Puntos WiFi por Administración Zonal', fontsize=14, fontweight='bold')
    plt.xlabel('Administración Zonal', fontsize=12)
    plt.ylabel('Total de Puntos WiFi', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Usar la nueva función para guardar
    guardar_diagrama(plt, 'diagrama_barras_puntos_por_admin_zonal.png')


def diagrama_top_10_puntos_por_parroquia():
    """Diagrama de Barras: Top 10 de Parroquias por número de puntos."""
    df = cargar_datos(RUTA_ESTADISTICAS_BASICAS)
    if df is None or 'parroquia' not in df.columns or 'total_puntos' not in df.columns:
        print("Saltando Diagrama de Barras parroquias por numero de puntos.")
        return

    top_parroquias = df.sort_values(by='total_puntos', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(top_parroquias['parroquia'], top_parroquias['total_puntos'], color='#2ECC71')

    plt.title('Top 10 Parroquias con Mayor Concentración de Puntos WiFi', fontsize=14, fontweight='bold')
    plt.xlabel('Parroquia', fontsize=12)
    plt.ylabel('Número de Puntos WiFi', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    guardar_diagrama(plt, 'diagrama_barras_top_10_parroquias.png')


def diagrama_parroquia_por_densidad_vs_area():
    """Diagrama de Dispersión: Densidad de Puntos vs Área (km²)."""
    df = cargar_datos(RUTA_COBERTURA_PRIORITARIA)
    required_cols = ['parroquia', 'densidad_puntos', 'area_km2']
    if df is None or not all(col in df.columns for col in required_cols):
        print("Saltando Diagrama de Dispersion densidad de puntos vs Area.")
        return

    plt.figure(figsize=(10, 6))

    scatter = plt.scatter(df['area_km2'], df['densidad_puntos'],
                          s=df['area_km2'] * 20,
                          c=df['densidad_puntos'], cmap='viridis', alpha=0.7, edgecolors='w')

    plt.title('Densidad de Puntos WiFi vs. Área de la Parroquia', fontsize=14, fontweight='bold')
    plt.xlabel('Área (km²)', fontsize=12)
    plt.ylabel('Densidad de Puntos (Puntos/km²)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)

    cbar = plt.colorbar(scatter)
    cbar.set_label('Densidad de Puntos', rotation=270, labelpad=15)

    plt.tight_layout()

    guardar_diagrama(plt, 'diagrama_dispersion_densidad_vs_area.png')


def diagrama_ranking_por_nivel_necesidad():
    """Diagrama de Barras Horizontales: Ranking de Parroquias por Nivel de Necesidad."""
    df = cargar_datos(RUTA_COBERTURA_PRIORITARIA)
    required_cols = ['parroquia', 'nivel_necesidad']
    if df is None or not all(col in df.columns for col in required_cols):
        print("Saltando Diagrama de Barras parroquias por necesidad.")
        return

    ranking = df.groupby('parroquia')['nivel_necesidad'].mean().nlargest(10).sort_values(ascending=True)

    plt.figure(figsize=(10, 6))

    colors = plt.cm.Reds(ranking.values / ranking.values.max())

    plt.barh(ranking.index, ranking.values, color=colors)

    plt.title('Top 10 Parroquias por Nivel de Necesidad Social/Brecha Digital', fontsize=14, fontweight='bold')
    plt.xlabel('Nivel de Necesidad (Score)', fontsize=12)
    plt.ylabel('Parroquia', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()

    guardar_diagrama(plt, 'diagrama_barras_ranking_necesidad.png')


# --- BLOQUE DE EJECUCIÓN PRINCIPAL ---

if __name__ == "__main__":
    print("\n--- INICIANDO GENERACIÓN DE GRÁFICOS ESTÁTICOS ---")

    # 1. Gráficos para la sección de Estadísticas
    diagrama_puntos_por_administracion_zonal()
    diagrama_top_10_puntos_por_parroquia()

    # 2. Gráficos para la sección de Priorización
    diagrama_parroquia_por_densidad_vs_area()
    diagrama_ranking_por_nivel_necesidad()

    print("\nArchivos PNG listos en el directorio de resultados.")