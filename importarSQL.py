#importar a SQL
from sqlalchemy import create_engine #librería encargada de crear el engine
import os

def subirSQL(df,nombre,tipo):
    server = "LAPTOP-Arturo" #especificar el nombre del servidor con el que te vas a conectar
    database = "Trading" #el nombre de la base de datos con la que vas a trabajar
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
                print(f"📤 Subiendo la tabla a SQL...")
                df.to_sql(nombre, engine, schema = tipo, if_exists='replace', index=True)
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