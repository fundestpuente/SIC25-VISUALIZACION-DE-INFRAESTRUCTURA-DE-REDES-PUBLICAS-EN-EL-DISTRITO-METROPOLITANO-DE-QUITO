import pandas as pd
import os

RUTA_ENTRADA = os.path.join(os.path.dirname(__file__), 'zonas_puntos_wifi.csv')
RUTA_SALIDA_DATOS_PROCESADOS = os.path.join(os.path.dirname(__file__), 'zonas_puntos_wifi_procesados.csv')

def cargar_datos_no_procesdos(ruta):
    """
    Esta función carga el CSV sin procesar
    en un DataFrame de Pandas.
    """
    try:
        df = pd.read_csv(ruta)
        print("Se a cargado el registro para es procesamiento de los datos.\n")
        return df
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {ruta}. Asegúrese de ejecutar extraccion_datos.py primero.")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None

def limpiar_estructurar_datos(df):
    """
    Realiza la limpieza esencial y la estandarización de columnas.
    """
    df.columns = ['nombre', 'latitud', 'longitud', 'administracion_zonal', 'parroquia']
    print("Se ha renombrado las columnas.")
    
    df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
    df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
    print("Tipos de datos geográficos longitud y latitud normalizados.")
    
    df['administracion_zonal'] = df['administracion_zonal'].astype(str).str.strip().str.upper()
    df['parroquia'] = df['parroquia'].astype(str).str.strip().str.upper()
    print("Estandarización exitosa de campos de texto.")
    
    registros_iniciales = len(df)
    df.dropna(subset=['latitud', 'longitud'], inplace=True)
    registros_eliminados = registros_iniciales - len(df)
    return df

def guardar_datos_procesados(df, ruta_salida):
    """
    Esta función guarda el DataFrame limpio, procesado
    para que el uso posterior en los otros módulos.
    """
    if df is not None:
        if os.path.exists(ruta_salida):
            print(f"Advertencia: El archivo ya existe en {ruta_salida}.")
            print("El archivo no se sobreescribirá.\n") 
            return False
        try:
            df.to_csv(ruta_salida, index=False)
            print(f"Datos procesados guardados exitosamente en: {ruta_salida}")
        except Exception as e:
            print(f"Error al guardar los datos procesados: {e}")

if __name__ == "__main__":
    datos_extraidos = cargar_datos_no_procesdos(RUTA_ENTRADA)
    
    if datos_extraidos is not None:
        datos_procesados = limpiar_estructurar_datos(datos_extraidos)
        guardar_datos_procesados(datos_procesados, RUTA_SALIDA_DATOS_PROCESADOS)