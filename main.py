import importlib
import sys
import os
import pandas as pd #librería para gestionar dataframes
import pyodbc #librería que sirve para conectarse a diferentes tipos de bases de datos
from sqlalchemy import create_engine #librería encargada de crear el engine
from datetime import datetime
import time

salir ='q' #esta es la tecla asignada a el botón para salir

print(f"""Bienvenido
iniciando modulo ETL para activos del mercado de valores
    
    """)
time.sleep(2)


def mostrar_menu(): #esta es la lista de activos disponibles
    print(f"""Versión 1.0

Actualmente estos son los activos disponibles para importar desde yfinance
1) Acciones         4) Commodities
2) Indice bursatil  5) Divisas
3) ETF              6) Criptomonedas

Para Salir escriba {salir}

    """)


def ejecutar_etl(): #esta es la función que me permite importar las variables
    while True:
        try:
            print(f"\n(Escribe {salir} para regresar al menú principal)") #para escribir el ticker del activo
            Ticker = input("Ticker o símbolo: ").upper()
            if Ticker.lower() == salir:
                return
            
            from verificacion import info_ticker
            respuesta, resultado, nombre, bolsa, tipo = info_ticker(Ticker)
            print(respuesta)
            if resultado == "no válido":
                return
            
            time.sleep(2) #pequeña pausa
            
            start = input("Fecha de inicio (YYYY-MM-DD): ") #escribir fecha de inicio de los datos
            if start.lower() == salir:
                return

            end = input("Fecha de fin (YYYY-MM-DD): ") #escribir fecha final de los datos
            if end.lower() == salir:
                return
            
            from ETL_general import ETL #llamar al ETL que usa yfinance
            df = ETL(Ticker, start, end)
            print(f"\n✅ {Ticker} → Datos obtenidos para: {Ticker}")
            print(df.head())
            
            from importarSQL import subirSQL
            subirSQL(df,nombre,tipo)
            
            break  # salir tras ejecución exitosa
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Intenta nuevamente...\n")
 

while True:
    mostrar_menu()
    opcion = input("Presione Enter para continuar: ").strip()

    if opcion.lower() == salir:
        print("""Saliendo del programa...
¡Hasta luego!
              """)
        sys.exit()

    if opcion == "":
        try:
            ejecutar_etl()            
            time.sleep(2)

#falta quitar esta parte que tiene lineas de código que ya no sirven:        
        except ModuleNotFoundError:
            print(f"❌ No se encontró el módulo.")
        except AttributeError:
            print(f"❌ La función no existe en el módulo.")
    else:
        print("❌ Opción inválida. Intenta nuevamente.")
