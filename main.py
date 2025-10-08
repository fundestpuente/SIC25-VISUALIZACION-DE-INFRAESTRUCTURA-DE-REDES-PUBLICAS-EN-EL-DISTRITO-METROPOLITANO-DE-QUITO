"""
Este script va a ejecutar todos los módulos creados por el equipo, en el siguiente orden:
extraccion_datos.py
datos_procesados.py
basic_stats.py
coverage_calc.py
diagramas.py
maps.py
dashboard_main.py
"""

# Módulos principales
import sys
import subprocess
import time
from pathlib import Path

def verificar_python():
    """
    Verifica que Python esté instalado y sea compatible con el proyecto
    """
    try:
        version = sys.version_info
        print(f"Python {version.major}.{version.minor}.{version.micro} detectado")
        if version.major < 3 or (version.major == 3 and version.minor < 13):
            print("Se requiere Python 3.13 o superior")
            return False
        return True
    except Exception as e:
        print(f"Error verificando Python: {e}")
        return False


def instalar_dependencias():
    """
    Instala las dependencias directamente del archivo requirements.txt
    """
    print("\nINSTALANDO DEPENDENCIAS...")
    print("-" * 50)

    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        print("Archivo requirements.txt no encontrado")
        return False

    try:
        # Instalar dependencias usando pip
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("Dependencias instaladas correctamente")
            return True
        else:
            print(f"Error instalando dependencias: {result.stderr}")
            return False

    except Exception as e:
        print(f"Error durante la instalación: {e}")
        return False


def ejecutar_script(ruta_script, descripcion):
    """
    Ejecuta un script específico con manejo de errores
    """
    print(f"\nEJECUTANDO: {descripcion}")
    print(f"Script: {ruta_script}")
    print("-" * 50)

    if not Path(ruta_script).exists():
        print(f"Script no encontrado: {ruta_script}")
        return False

    try:
        # Ejecutar el script
        inicio = time.time()
        result = subprocess.run([sys.executable, ruta_script],
                                capture_output=True, text=True)

        duracion = time.time() - inicio

        if result.returncode == 0:
            print(f"{descripcion} completado en {duracion:.2f} segundos")
            # Mostrar salida del script si existe
            if result.stdout.strip():
                print("Salida del script:")
                print(result.stdout)
            return True
        else:
            print(f"Error en {descripcion}:")
            print(f"Código de error: {result.returncode}")
            if result.stderr:
                print(f"Mensaje de error: {result.stderr}")
            return False

    except Exception as e:
        print(f"Error ejecutando {ruta_script}: {e}")
        return False


def verificar_estructura_proyecto():
    """
    Verifica que la estructura de carpetas del proyecto sea correcta
    """
    print("\nVERIFICANDO ESTRUCTURA DEL PROYECTO...")

    estructura_esperada = [
        "manejo_de_datos/extraccion_datos.py",
        "manejo_de_datos/datos_procesados.py",
        "estadisticas/basic_stats.py",
        "estadisticas/coverage_calc.py",
        "visualizacion/diagramas.py",
        "visualizacion/maps.py",
        "dashboard/dashboard_main.py",
        "requirements.txt"
    ]

    todos_existen = True
    for ruta in estructura_esperada:
        if Path(ruta).exists():
            print(f"Correcto {ruta}")
        else:
            print(f"Incorrecto {ruta} - NO ENCONTRADO")
            todos_existen = False

    return todos_existen


def main():
    """
    Función principal del proyecto
    """

    # Paso 1: Verificar Python
    if not verificar_python():
        sys.exit(1)

    # Paso 2: Verificar estructura del proyecto
    if not verificar_estructura_proyecto():
        print("\nAdvertencia: Algunos archivos no se encontraron.")
        print("El proceso continuará, pero pueden ocurrir errores.\n")
        time.sleep(2)

    # Paso 3: Instalar dependencias
    if not instalar_dependencias():
        print("\nNo se pudieron instalar las dependencias.")
        sys.exit(1)

    # Paso 4: Definir secuencia de ejecución
    secuencia_scripts = [
        {
            "ruta": "manejo_de_datos/extraccion_datos.py",
            "descripcion": "Extracción de datos de puntos WiFi"
        },
        {
            "ruta": "manejo_de_datos/datos_procesados.py",
            "descripcion": "Procesamiento y limpieza de datos"
        },
        {
            "ruta": "estadisticas/basic_stats.py",
            "descripcion": "Cálculo de estadísticas básicas"
        },
        {
            "ruta": "estadisticas/coverage_calc.py",
            "descripcion": "Cálculo de cobertura y priorización"
        },
        {
            "ruta": "visualizacion/diagramas.py",
            "descripcion": "Generación de gráficos y diagramas"
        },
        {
            "ruta": "visualizacion/maps.py",
            "descripcion": "Generación de mapa interactivo"
        }
    ]

    # Paso 5: Ejecutar scripts en secuencia
    print("\n" + "=" * 70)
    print("INICIANDO EJECUCIÓN SECUENCIAL DE SCRIPTS")
    print("=" * 70)

    todos_exitosos = True
    for script in secuencia_scripts:
        if not ejecutar_script(script["ruta"], script["descripcion"]):
            print(f"\nError en {script['descripcion']}. Continuando con el siguiente...")
            todos_exitosos = False
        time.sleep(0.5)

    # Paso 6: Ejecutar dashboard
    if todos_exitosos:
        print("\n" + "=" * 70)
        print("INICIANDO DASHBOARD INTERACTIVO")
        print("=" * 70)
        print("Presiona Ctrl+C en esta ventana para detener el dashboard")
        print("-" * 70)

        try:
            # Ejecutar dashboard (se mantiene en ejecución)
            subprocess.run([sys.executable, "dashboard/dashboard_main.py"])
        except KeyboardInterrupt:
            print("\n\nDashboard detenido por el usuario")
        except Exception as e:
            print(f"\nError ejecutando el dashboard: {e}")
    else:
        print("\nAlgunos scripts fallaron. El dashboard no se iniciará automáticamente.")
        print("Puedes intentar ejecutar manualmente: python dashboard/dashboard_main.py")

    # Mensaje final
    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO")
    print("=" * 70)
    if todos_exitosos:
        print("Todos los componentes se ejecutaron correctamente")
    else:
        print("Algunos componentes tuvieron problemas. Revisa los mensajes arriba.")
    print("\nEstructura de archivos generados:")
    print("   - manejo_de_datos/zonas_puntos_wifi_procesados.csv")
    print("   - estadisticas/resultados/estadisticas_basicas.csv")
    print("   - estadisticas/resultados/cobertura_prioritaria.csv")
    print("   - visualizacion/resultados/(gráficos PNG)")
    print("   - visualizacion/mapa_wifi_quito.html")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()