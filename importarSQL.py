#importar a SQL
from sqlalchemy import create_engine #librería encargada de crear el engine
from sqlalchemy import text  # ejecutar comandos SQL directamente
from sqlalchemy.types import DateTime, Float, BigInteger
import json #lectura de archivos .json
import os


def asegurar_schema(engine, tipo):
    # Usamos begin() para asegurarnos que los cambios se confirmen (commit) automáticamente
    with engine.begin() as connection:
        result = connection.execute(
            text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"),
            {'schema': tipo}
        )
        if result.fetchone() is None:
            print(f"ℹ️ El esquema '{tipo}' no existe en la base de datos, creando...")
            connection.execute(text(f"CREATE SCHEMA {tipo}"))
            print(f"✅ Esquema '{tipo}' creado exitosamente.")
        else:
            print("")  # Esquema ya existe, no se hace nada


def cargar_config(): #extrar los parámetros desde el archivo json "config"
    with open("config.json", "r") as f:
        return json.load(f)



def subirSQL(df,nombre,tipo): #función principal (para extraer los parámetros)
    config = cargar_config() #esto carga la configuración de conexión del servidor
    server = config.get("server", "null")
    database = config.get("database", "null")
    conn_str = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server" 
    engine = create_engine(conn_str)

    while True:        
        print(f"""¿Qué deseas hacer con los datos de {nombre}?
1. Subir a SQL Server → Base de datos: {database}
2. Exportar como archivo CSV
3. Cancelar y regresar al menú anterior""")

        respuesta = input("Elige una opción (1, 2 o 3): ").strip()

        if respuesta == '1':
            try:
                asegurar_schema(engine, tipo)  # nuevo paso antes de subir
                print(f"📤 Subiendo la tabla a SQL...")
                
                df.to_sql(nombre,engine,schema=tipo,if_exists='replace',index=True,
                    dtype={
                        "Date": DateTime(),
                        "Open": Float(),
                        "High": Float(),
                        "Low": Float(),
                        "Close": Float(),
                        "Adj Close": Float(),
                        "Volume": BigInteger(),
                        "Dividends": Float(),
                        "Stock Splits": Float()
                    }
                )
                
                print(f"✅ Los datos de {nombre} fueron subidos exitosamente a la base de datos '{database}'.")
                break
            except Exception as e:
                print(f"❌ Error al subir a SQL: {e}")
        elif respuesta == '2':
            try:
                nombre_archivo = f"{nombre}.csv"
                df.to_csv(nombre_archivo, index=False)
                print(f"✅ Archivo CSV exportado como '{nombre_archivo}' en: {os.getcwd()}")
                break
            except Exception as e:
                print(f"❌ Error al exportar a CSV: {e}")
        elif respuesta == '3':
            print("🔙 Operación cancelada. Regresando al menú principal.")
            break
        else:
            print("⚠️ Entrada inválida. Por favor elige 1, 2 o 3.")