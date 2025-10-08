import pandas as pd
import geopandas as gpd
import os

RUTA_BASE = os.path.dirname(os.path.dirname(__file__))
RUTA_DATOS_PROCESADOS = os.path.join(RUTA_BASE,'manejo_de_datos', 'zonas_puntos_wifi_procesados.csv')
RUTA_SALIDA_ANALISIS = os.path.join(RUTA_BASE, "estadisticas", "resultados","estadisticas_basicas.csv")

def load_wifi_data(ruta: str) -> gpd.GeoDataFrame:
    """
    Carga un archivo CSV con puntos WiFi y lo convierte en GeoDataFrame.
    Ajusta los nombres de columnas según el CSV original.
    """
    
    try:
        print(" Cargando datos WiFi...")
        df = pd.read_csv(ruta)
        print(f" Datos cargados correctamente. Total de registros: {len(ruta)}\n")
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df["longitud"], df["latitud"]),
            crs="EPSG:4326"
        )
        return gdf

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta}")
        return None

def count_points_by_sector(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Cuenta el número total de puntos WiFi por sector/zona.
    """
    return gdf.groupby("administracion_zonal").size().reset_index(name="total_puntos")


def count_points_by_parroquia(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Cuenta el número total de puntos WiFi por parroquia.
    """
    return gdf.groupby("parroquia").size().reset_index(name="total_puntos")


def compute_basic_metrics(gdf: gpd.GeoDataFrame) -> dict:
    """
    Calcula métricas descriptivas básicas.
    """
    metrics = {
        "total_puntos": len(gdf),
        "sectores_unicos": gdf["administracion_zonal"].nunique(),
        "parroquias_unicas": gdf["parroquia"].nunique(),
        "promedio_por_sector": gdf.groupby("administracion_zonal").size().mean(),
        "promedio_por_parroquia": gdf.groupby("parroquia").size().mean()
    }
    return metrics


def calcular_centroide_por_parroquia(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Calcula el centroide (latitud y longitud central) de cada parroquia.
    """
    gdf_proyectado = gdf.to_crs("EPSG:32717")
    centroides_proyectados = gdf_proyectado.dissolve(by="parroquia").centroid
    centroides_geograficos = centroides_proyectados.to_crs("EPSG:4326")
    df_centroides = pd.DataFrame({
        "parroquia": centroides_geograficos.index,
        "latitud_centroide": centroides_geograficos.y,
        "longitud_centroide": centroides_geograficos.x
    })
    return df_centroides


if __name__ == "__main__":
    cargar_data = load_wifi_data(RUTA_DATOS_PROCESADOS)
    if cargar_data is not None:
        print(" MÉTRICAS BÁSICAS")
        metrics = compute_basic_metrics(cargar_data)
        for key, value in metrics.items():
            print(f"- {key}: {value}")

        print("\n CONTEO POR SECTOR")
        df_sector = count_points_by_sector(cargar_data)
        print(df_sector)

        print("\n CONTEO POR PARROQUIA")
        df_parroquia = count_points_by_parroquia(cargar_data)
        print(df_parroquia)

        print("\n CENTROIDES POR PARROQUIA")
        df_centroides = calcular_centroide_por_parroquia(cargar_data)
        print(df_centroides)

        os.makedirs(os.path.dirname(RUTA_SALIDA_ANALISIS), exist_ok=True)
        df_parroquia.to_csv(RUTA_SALIDA_ANALISIS, index=False)
        print(f"\n Archivo guardado con métricas en: {RUTA_SALIDA_ANALISIS}")