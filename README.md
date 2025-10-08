# 📌 <VISUALIZACION_DE_INFRAESTRUCUTURA_DE_REDES_PUBLICAS_EN_EL_DISTRITO_METROPOLITANO_DE_QUITO>

**Curso:** Samsung Innovation Campus – Módulo de Python (Ecuador 2025)  
**Seccion:** EC04  
**Carpeta:** `/EC04/VISUALIZACION DE INFRAESTRUCTURA DE REDES PUBLICAS EN EL DISTRITO METROPOLITANO DE QUITO`

---

## 👥 Integrantes del Grupo
- Mario Anrrango
- Adriana Padilla
- Diego Montesdeoca
- Gabriel Andrade
- Camilo Vasquez 

---

## 📝 Descripción del Proyecto
Este proyecto es un programa de visualización y análisis de los puntos WiFi municipales del Distrito Metropolitano de Quito el cual facilita el acceso a información de conectividad pública con el propósito de identificar brechas de cobertura y optimizar recursos beneficiando a ciudadanos sin acceso a datos móviles y conexión a internet.

## ⚙️ Instrucciones de Instalación y Ejecución

### Requisitos
- Python 3.13.7 (recomendado)
- Git

### Pasos
1. Clonar el repositorio (o asegurarse de estar en la carpeta del proyecto):
   ```bash
   git clone <(https://github.com/fundestpuente/sic-ecuador-2025-proyectos.git)>
   cd <EC04/VISUALIZACION DE INSFRAESTRUCTURA DE REDES PUBLICAS EN EL DISTRITO METROPOLITANO DE QUITO>   # ej: cd ecuador03/proyecto-01-nombre
   ```

2. Actualizar pip y ejecutar la aplicación:
   ```bash
   pip install --upgrade pip
   python3 main.py
   ```

---

## 📂 Estructura del proyecto:
```
VISUALIZACION DE INFRAESTRUCTURA DE REDES PUBLICAS EN EL DISTRITO METROPOLITANO DE QUITO/
├── 📂 dashboard/
│   └── dashboard_main.py                               # Script del dashboard en Dash.
├── 📂 estadisticas/
│   ├── 📂 resultados                                   # Carpeta que contiene los resultados estadísticos.
│   │   ├── cobertura_prioritaria.csv            
│   │   └── estadisticas_basicas.csv             
│   ├── basic_stats.py                                  # Script para calcular las estadísticas básicas.
│   └── coverage_calc.py                                # Script para calcular la cobertura prioritaria.
├── 📂 manejo_de_datos/
│   ├── datos_procesados.py                             # Script de procesamiento de los datos.
│   ├── extraccion_datos.py                             # Script de extracción de los datos desde la API.
│   ├── zonas_puntos_wifi.csv                    
│   └── zonas_puntos_wifi_procesados.csv         
├── 📂 visualizacion/
│   ├── 📂 resultados/                                  # Contiene las imágenes PNG generadas por 'diagramas.py'.
│   │   ├── diagrama_barras_puntos_por_admin_zonal.png
│   │   ├── diagrama_barras_ranking_necesidad.png
│   │   ├── diagrama_barras_top_10_parroquias.png
│   │   └── diagrama_dispersion_densidad_vs_area.png
│   ├── diagramas.py                                    # Script para generar los gráficos estáticos.
│   ├── mapa_wifi_quito.html                            # El mapa generado por maps.py
│   └── maps.py                                         # Script para generar el mapa de puntos WiFi
├── main.py                                             # Aplicación principal.
├── requirements.txt                                    # Dependencias del proyecto.
└── README.md                                           # Este archivo.
```

---

## ✅ Herramientas Implementadas
- **Lenguaje:** Python 3.13.x
- **Librerías principales:** `<pandas, geopandas, numpy, requests, matplotlib, seaborn, folium, plotly, dash, scipy>`

---

## 💡 Buenas prácticas y reglas internas
- Trabajar únicamente dentro de la carpeta asignada al grupo.
- Realizar commits claros, por ejemplo: `feat: agrega función X`, `fix: corrige bug en Y`, `docs: actualiza README`.
- Mantener el README del proyecto actualizado con cambios importantes.
