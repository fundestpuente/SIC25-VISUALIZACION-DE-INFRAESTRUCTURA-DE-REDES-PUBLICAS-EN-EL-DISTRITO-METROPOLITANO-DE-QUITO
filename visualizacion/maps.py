import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

CARPETA_PROYECTO = os.path.dirname(os.path.dirname(__file__))
RUTA_CSV = os.path.join(CARPETA_PROYECTO, 'estadisticas', 'resultados', 'cobertura_prioritaria.csv')
RUTA_MAPA = os.path.join(os.path.dirname(__file__), 'mapa_wifi_quito.html')

COLORES = {'CRITICA': 'red', 'ALTA': 'orange', 'MEDIA': 'yellow', 'BAJA': 'lightgreen', 'OPTIMA': 'green'}
NIVELES = {5: 'CRITICA', 4: 'ALTA', 3: 'MEDIA', 2: 'BAJA', 1: 'OPTIMA'}

def generar_mapa():
    df = pd.read_csv(RUTA_CSV)
    mapa = folium.Map(location=[-0.1807, -78.4678], zoom_start=11)
    cluster = MarkerCluster().add_to(mapa)
    
    for _, fila in df.iterrows():
        nivel = int(fila['nivel_necesidad'])
        color = COLORES[NIVELES[nivel]]
        folium.CircleMarker(
            location=[fila['latitud'], fila['longitud']],
            radius=8,
            color='black',
            fillColor=color,
            fillOpacity=0.7,
            weight=2
        ).add_to(cluster)
    leyenda_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 10px">
        <h4 style="margin-top:0; margin-bottom:10px;">Nivel de Necesidad</h4>
        <p style="margin: 5px 0;"><i style="background:red; width:20px; height:20px; 
           float:left; margin-right:8px; border-radius:50%; border: 2px solid black;"></i> CRÍTICA</p>
        <p style="margin: 5px 0;"><i style="background:orange; width:20px; height:20px; 
           float:left; margin-right:8px; border-radius:50%; border: 2px solid black;"></i> ALTA</p>
        <p style="margin: 5px 0;"><i style="background:yellow; width:20px; height:20px; 
           float:left; margin-right:8px; border-radius:50%; border: 2px solid black;"></i> MEDIA</p>
        <p style="margin: 5px 0;"><i style="background:lightgreen; width:20px; height:20px; 
           float:left; margin-right:8px; border-radius:50%; border: 2px solid black;"></i> BAJA</p>
        <p style="margin: 5px 0;"><i style="background:green; width:20px; height:20px; 
           float:left; margin-right:8px; border-radius:50%; border: 2px solid black;"></i> ÓPTIMA</p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    mapa.save(RUTA_MAPA)
    print("Mapa generado exitosamente y guardado")

if __name__ == "__main__":
    generar_mapa()
