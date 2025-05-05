import pandas as pd
import sqlite3
import os
import goverment_info as gi

gi.download_goverment_info()

def cargar_datos(nombre_archivo, nombre_tabla):
    ruta = os.path.join("datos_sqlite", nombre_archivo)
    conexion = sqlite3.connect(ruta)
    df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conexion)
    conexion.close()
    return df

data = cargar_datos("series-tiempo.sqlite","metadatos")
data = pd.DataFrame(data)
print(data.columns)