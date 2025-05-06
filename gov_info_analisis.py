import pandas as pd
import sqlite3
import os
import goverment_info as gi
from datetime import datetime

#gi.download_goverment_info()

def cargar_datos(nombre_archivo, nombre_tabla):
    ruta = os.path.join("datos_sqlite", nombre_archivo)
    conexion = sqlite3.connect(ruta)
    df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conexion)
    conexion.close()
    return df

data = cargar_datos("series-tiempo.sqlite","metadatos")
data = pd.DataFrame(data)

df_filtrado = data[[
    'serie_titulo',
    'serie_unidades',
    'serie_indice_inicio',
    'serie_indice_final',
    'serie_valor_ultimo',
    'serie_valor_anterior',
    'serie_var_pct_anterior',
    'serie_actualizada',
    'serie_discontinuada'
]]

# Mostrar resultado ordenado por título
df_filtrado = df_filtrado[(df_filtrado['serie_actualizada'] == 1) & (df_filtrado['serie_discontinuada'] == 1)]

# Ver cantidad de registros por título
print(df_filtrado.value_counts('serie_titulo'))

print(df_filtrado)
