import requests
import pandas as pd
import os


URL_API = "https://tecnologia.quito.gob.ec/wifi_apirest.php"
ARCHIVO_SALIDA = os.path.join(os.path.dirname(__file__), 'zonas_puntos_wifi.csv')


def extraer_datos(url):
    
    """
    Algoritmo de la función para extraer los datos de la API elegida
    sin ordenar, para comprobar la correcta extracción de los mismos.
    """
    print("="*30)
    print("CONECTANDO A LA API...")
    print("="*30)
    try:
        response = requests.get(url)
        data = response.json()
        
        zonas_wifi = data.get("resultados", [])
        
        if not zonas_wifi:
            print("La API no devolvió datos.")
            return None
        
        df = pd.DataFrame(zonas_wifi)
        print("Extracción exitosa de datos. Zonas Wifi obtenidas\n")
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None
    
def guardar_datos(df, ruta_salida):
    
    """
    Algoritmo de la funcion que guarda los datos sin
    procesar para uso posterior (archivo CSV).
    """
    if df is not None:
        if os.path.exists(ruta_salida):
            print(f"Advertencia: El archivo ya existe en {ruta_salida}.")
            print("El archivo no se sobreescribirá.\n") 
            return False
        try:
            df.to_csv(ruta_salida, index=False)
            print(f"Datos sin procesar guardados en: {ruta_salida}\n")
            return True
        except Exception as e:
            print(f"Error al guardar los datos en archivo CSV: {e}")
            return False
    return False
    
if __name__ == "__main__":
    datos_extraidos = extraer_datos(URL_API)
    
    if datos_extraidos is not None:
        guardar_datos(datos_extraidos, ARCHIVO_SALIDA)
