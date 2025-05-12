import os
import json
import pyodbc
import sys

CONFIG_PATH = "config.json"

def load_config(): #función para abrir el archivo "config.json", son se guardan las configuraciones
    if not os.path.exists(CONFIG_PATH):
        return {"server": "null", "database": "null", "csv_path": "null"}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config): #función para guardar los cambios hechos en los parámetros
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def test_connection(server, database): #prueba de conexión con la base de datos, devuelve verdadero o falso dependiendo de si hubo conexión con el servidor y la base de datos
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes;",
            timeout=3
        )
        conn.close()
        return True
    except:
        return False


def ask_for_server():
    while True:
        server = input("🔧 Ingresa el nombre del servidor SQL: ").strip()
        if test_connection(server, "master"):
            return server
        print("❌ Servidor inválido. Intenta nuevamente.")


def ask_for_database(server):
    while True:
        database = input("📂 Ingresa el nombre de la base de datos: ").strip()
        if test_connection(server, database):
            return database
        print("❌ Base de datos inválida. Intenta nuevamente.")


def ask_for_csv_path():
    while True:
        path = input("📁 Ingresa la ruta donde guardarás los archivos .csv: ").strip()
        # Corrige slashes si es necesario
        path = os.path.normpath(path)
        if os.path.isdir(path):
            return path
        print("❌ Ruta inválida o no existente. Intenta nuevamente.")


def config_menu(salir):
    config = load_config()
    # Verifica si hay conexión previa
    if config["server"] != "null" and config["database"] != "null":
        print(f"✅ Archivos serán subidos a la base de datos llamada: **{config['database']}** en el servidor **{config['server']}**")
    else:
        print("⚠️ No se detectó una configuración válida de base de datos.\n")
        config["server"] = ask_for_server()
        config["database"] = ask_for_database(config["server"])

    # Verifica ruta CSV
    if config["csv_path"] != "null":
        print(f"📄 Archivos .csv serán guardados en: {config['csv_path']}")
    else:
        print("⚠️ No se detectó una ruta válida para guardar archivos CSV.")
        config["csv_path"] = ask_for_csv_path()

    save_config(config)

    # Opciones del menú
    print("""=== 🛠️ MENÚ DE INICIO ===)
1. Modificar conexión de servidor y base de datos en SQL server
2. Modificar ruta de guardado de archivos .csv
3. Presiona "Enter" para continuar sin cambios.""")

    opcion = input("Selecciona una opción: ").strip()

    if opcion.lower() == salir:
        print("""Saliendo del programa...
¡Hasta luego!
              """)
        sys.exit()

    if opcion == "1":
        config["server"] = ask_for_server()
        config["database"] = ask_for_database(config["server"])
        save_config(config)
        print("✅ Configuración actualizada.")

    elif opcion == "2":
        config["csv_path"] = ask_for_csv_path()
        save_config(config)
        print("✅ Ruta actualizada.")

    return config
