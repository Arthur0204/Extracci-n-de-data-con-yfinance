import sys
import pandas as pd #librería para gestionar dataframes
from sqlalchemy import create_engine #librería encargada de crear el engine
from datetime import datetime
import time

salir ='q' #esta es la tecla asignada a el botón para salir


print(f"""Bienvenido
iniciando modulo ETL para activos del mercado de valores...
    
    """)
time.sleep(2)

#INICIAR EL MODULO DE CONFIGURACIÓN
from config import config_menu #modulo de configuración
config_menu(salir)

#PRESENTACIÓN
def mostrar_menu():
    time.sleep(2)
    print(f"""

Versión 1.1.0
Creado por: Cesar Arturo Ulloa Torres
EL proyecto se encuentra aún en desarrollo

""")

#MENU DE EXTRACCIÓN
while True:
    mostrar_menu
    opcion = input("Presione Enter para continuar: ").strip()

    if opcion.lower() == salir:
        print("""Saliendo del programa...
¡Hasta luego!
              """)
        sys.exit()

    if opcion == "":
        try:
            from Ticker import ejecutar_etl #llama al modulo "ETL"
            ejecutar_etl(salir)          #extráe el objeto "salir"
            time.sleep(2)
            
        except ModuleNotFoundError:
            print(f"❌ No se encontró el módulo.")
        except AttributeError:
            print(f"❌ La función no existe en el módulo.")
    else:
        print("❌ Opción inválida. Intenta nuevamente.")
