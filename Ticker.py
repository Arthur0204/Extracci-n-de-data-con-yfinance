import pandas as pd #librería para gestionar dataframes
from sqlalchemy import create_engine #librería encargada de crear el engine
from datetime import datetime
import time


def ejecutar_etl(salir): #esta es la función que me permite importar las variables
    while True:
        try:
            print(f"\n(Escribe {salir} para regresar al menú principal)") #para escribir el ticker del activo
            Ticker = input("Ticker o símbolo: ").upper()
            if Ticker.lower() == salir:
                return
            
            from verificacion import info_ticker #llama al módulo de verificacion
            respuesta, resultado, nombre, bolsa, tipo = info_ticker(Ticker) #tomando el ticker de referencia, devuelve los metadatos del ticker
            print(respuesta)
            if resultado == "no válido":
                return
            
            time.sleep(2)
            
            start = input("Fecha de inicio (YYYY-MM-DD): ") #escribir fecha de inicio de los datos
            if start.lower() == salir:
                return

            end = input("Fecha de fin (YYYY-MM-DD): ") #escribir fecha final de los datos
            if end.lower() == salir:
                return
            
            from ETL_general import ETL #llamar al modulo ETL_general
            df = ETL(Ticker, start, end) #toma los parámetros ingresados y los manda a la función ETL, devuelve un DF
            print(f"\n✅ {Ticker} → Datos obtenidos para: {Ticker}")
            print(df.head())
            
            from importarSQL import subirSQL
            subirSQL(df,nombre,tipo)
            
            break  # salir tras ejecución exitosa
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Intenta nuevamente...\n")