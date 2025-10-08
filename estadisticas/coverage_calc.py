import pandas as pd
import os
import numpy as np

RUTA_BASE = os.path.dirname(os.path.dirname(__file__))
RUTA_DATOS_PROCESADOS = os.path.join(RUTA_BASE, 'manejo_de_datos', 'zonas_puntos_wifi_procesados.csv')
RUTA_SALIDA_COBERTURA = os.path.join(os.path.dirname(__file__), 'resultados', 'cobertura_prioritaria.csv')

AREAS_REALES_KM2 = {
    'ALANGASI': 40.00,
    'AMAGUAÑA': 50.00,
    'ATAHUALPA': 140.00,
    'CALACALI': 100.00,
    'CALDERON': 30.00,
    'CHECA': 55.00,
    'CHILLOGALLO': 18.00,
    'CONOCOTO': 50.00,
    'CUMBAYA': 26.51,
    'EL QUINCHE': 130.00,
    'GUALEA': 120.97,
    'GUANGOPOLO': 50.00,
    'GUAYLLABAMBA': 48.00,
    'LLANO CHICO': 15.00,
    'LLOA': 260.00,
    'NANEGAL': 350.00,
    'NANEGALITO': 45.00, # Estimado
    'NAYON': 20.00,
    'NONO': 230.00, # Estimado: Parroquia rural grande
    'PACTO': 236.00,
    'PERUCHO': 38.00, # Estimado
    'PIFO': 100.00,
    'PINTAG': 544.00, # La más grande
    'PUELLARO': 146.00,
    'PUEMBO': 40.00,
    'SAN ANTONIO': 80.00,
    'SAN JOSE DE MINAS': 150.00,
    'TABABELA': 10.00,
    'TUMBACO': 57.00,
    'YARUQUI': 80.00,
    'ZAMBIZA': 18.00,
    'CHAVEZPAMBA': 40.00, # Estimado (nueva)
    'BELISARIO QUEVEDO': 2.50,
    'CARCELEN': 7.50, # Estimado
    'CENTRO HISTORICO': 3.50,
    'CHIMBACALLE': 3.10,
    'COCHAPAMBA': 3.00, # Estimado
    'COMITE DEL PUEBLO': 4.00, # Estimado
    'COTOCOLLAO': 10.00,
    'EL CONDADO': 15.00,
    'EL INCA': 6.00,
    'GUAMANI': 12.00,
    'ITCHIMBIA': 8.00,
    'IÑAQUITO': 5.50,
    'JIPIJAPA': 4.50, # Estimado
    'KENNEDY': 3.00, # Estimado
    'LA ARGELIA': 7.00, # Estimado
    'LA CONCEPCION': 2.50,
    'LA ECUATORIANA': 8.00, # Estimado
    'LA FERROVIARIA': 3.00,
    'LA LIBERTAD': 2.00,
    'LA MAGDALENA': 3.80,
    'LA MENA': 4.00,
    'LA MERCED': 1.50, # Estimado
    'MARISCAL SUCRE': 2.80,
    'PONCEANO': 6.00,
    'PUENGASI': 15.00, # Estimado
    'QUITUMBE': 10.00,
    'RUMIPAMBA': 4.50,
    'SAN BARTOLO': 4.00,
    'SAN ISIDRO DEL INCA': 7.00,
    'SAN JUAN': 4.20,
    'SOLANDA': 4.50,
    'TURUBAMBA': 6.00,
    'CHILIBULO': 5.00,
    'POMASQUI': 8.00,
    'CHAVEZPAMBA': 40.00, 
}

def cargar_datos(ruta):
    try:
        df = pd.read_csv(ruta)
        print("Datos procesados cargados para análisis de cobertura.\n")
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta}")
        return None


# def calcular_densidad(df):
#     """
#     Calcula la densidad de puntos por área (aproximada), asigna una categoría
#     de prioridad e integra esa categoría en el DataFrame principal.
#     """
#     print("Calculando densidad y nivel de prioridad de cobertura...\n")

#     densidad = df.groupby('parroquia').agg(
#         total_puntos=('nombre', 'count'),
#         lat_min=('latitud', 'min'),
#         lat_max=('latitud', 'max'),
#         lon_min=('longitud', 'min'),
#         lon_max=('longitud', 'max')
#     ).reset_index()

#     densidad['area_aprox'] = (densidad['lat_max'] - densidad['lat_min']) * \
#         (densidad['lon_max'] - densidad['lon_min'])
#     densidad['densidad_puntos'] = densidad['total_puntos'] / \
#         densidad['area_aprox'].replace(0, np.nan)
#     densidad['densidad_puntos'].fillna(0, inplace=True) 
    
#     bins = pd.qcut(
#         densidad['densidad_puntos'], 
#         q=5,
#         labels=False, 
#         duplicates='drop',
#     )
#     bins = bins.fillna(0) 
#     densidad['nivel_prioridad'] = 5 - bins.astype(int) 
    
#     print("Categorías de prioridad (1-Baja a 5-Alta) asignadas a cada parroquia.")

#     df_enriquecido = df.merge(
#         densidad[['parroquia', 'nivel_prioridad']], 
#         on='parroquia', 
#         how='left'
#     )

#     zonas_prioritarias = densidad.nlargest(5, 'nivel_prioridad')[
#         ['parroquia', 'nivel_prioridad', 'total_puntos']]

#     print("Zonas prioritarias detectadas:\n", zonas_prioritarias)
    
#     # El resultado principal de esta función es el DataFrame enriquecido, listo para mapeo
#     return df_enriquecido, zonas_prioritarias

def calcular_densidad(df):
    """
    Calcula la densidad real usando áreas conocidas y genera la etiqueta
    de 'Nivel de Necesidad de Cobertura' (Prioridad).
    """
    print("Calculando densidad REAL y nivel de necesidad de cobertura...\n")

    densidad = df.groupby('parroquia').agg(
        total_puntos=('nombre', 'count')
    ).reset_index()

    df_areas = pd.DataFrame(AREAS_REALES_KM2.items(), columns=['parroquia', 'area_km2'])
    densidad = densidad.merge(df_areas, on='parroquia', how='left')
    densidad['densidad_puntos'] = densidad['total_puntos'] / densidad['area_km2']
    densidad['densidad_puntos'].fillna(0, inplace=True) 
    densidad.loc[densidad['area_km2'].isna(), 'densidad_puntos'] = 0
    densidad_a_categorizar = densidad.dropna(subset=['area_km2']).copy()
    
    bins = pd.qcut(
        densidad_a_categorizar['densidad_puntos'], 
        q=5,
        labels=False, 
        duplicates='drop',
    ).fillna(0)
    densidad_a_categorizar['nivel_necesidad'] = 5 - bins.astype(int) 

    columnas_fusion = ['parroquia', 'area_km2', 'densidad_puntos', 'nivel_necesidad']
    
    df_enriquecido = df.merge(
        densidad_a_categorizar[columnas_fusion], 
        on='parroquia', 
        how='left'
    )

    parroquias_desconocidas = df_enriquecido['nivel_necesidad'].isna().sum()
    if parroquias_desconocidas > 0:
        df_enriquecido['nivel_necesidad'].fillna(1, inplace=True)
        print(f"{parroquias_desconocidas} registros de parroquias sin área conocida fueron asignados a Prioridad 1 (Baja).")

    zonas_prioritarias = densidad_a_categorizar.nlargest(5, 'nivel_necesidad')[
        ['parroquia', 'nivel_necesidad', 'total_puntos', 'densidad_puntos']]

    print("Zonas prioritarias detectadas (basado en densidad real):\n", zonas_prioritarias)
    return df_enriquecido, zonas_prioritarias

def guardar_resultados(densidad, zonas_prioritarias, ruta_salida):
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    try:
        densidad.to_csv(ruta_salida, index=False)
        print(f"Resultados de cobertura guardados en: {ruta_salida}\n")
        print("Zonas prioritarias exportadas correctamente.")
    except Exception as e:
        print(f"Error al guardar el archivo de cobertura: {e}")


if __name__ == "__main__":
    df = cargar_datos(RUTA_DATOS_PROCESADOS)
    if df is not None:
        densidad, zonas_prioritarias = calcular_densidad(df)
        guardar_resultados(densidad, zonas_prioritarias, RUTA_SALIDA_COBERTURA)
