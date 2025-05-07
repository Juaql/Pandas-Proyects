import pandas as pd
import sqlite3
import os
import goverment_info as gi
from datetime import datetime

fecha_hoy = datetime.today().strftime('%Y-%m-%d')

hoy = pd.to_datetime(datetime.today().date())

gi.download_goverment_info()

def cargar_datos(nombre_archivo, nombre_tabla):
    print(nombre_archivo)
    ruta = os.path.join("datos_sqlite", nombre_archivo)
    conexion = sqlite3.connect(ruta)
    df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conexion)
    conexion.close()
    return df

data = cargar_datos(f"series-tiempo_{fecha_hoy}.sqlite","metadatos")
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

def comparar_y_decidir(nombre_nuevo_archivo, carpeta="datos_sqlite"):
    # Cargar el nuevo archivo
    data_nueva = cargar_datos(nombre_nuevo_archivo, "metadatos")
    df_nuevo = pd.DataFrame(data_nueva)[[
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

    # Buscar archivo anterior más reciente (que no sea el de hoy)
    archivos_sqlite = sorted([
        f for f in os.listdir(carpeta) if f.endswith(".sqlite") and f != nombre_nuevo_archivo
    ], reverse=True)

    if not archivos_sqlite:
        print("No hay versiones anteriores para comparar.")
        return

    archivo_anterior = archivos_sqlite[-1]

    # Cargar archivo anterior
    data_anterior = cargar_datos(archivo_anterior, "metadatos")
    df_anterior = pd.DataFrame(data_anterior)[df_nuevo.columns]

    # Comparar
    if df_nuevo.equals(df_anterior):
        print("Los datos no han cambiado. Eliminando archivo nuevo.")
        os.remove(os.path.join(carpeta, nombre_nuevo_archivo))
    else:
        print("Los datos han cambiado. Conservando el archivo nuevo.")

# Mostrar resultado ordenado por título
df_filtrado = df_filtrado[(df_filtrado['serie_actualizada'] == 1) & (df_filtrado['serie_discontinuada'] == 1)]

# Ver cantidad de registros por título
print(df_filtrado.value_counts('serie_titulo'))
print(df_filtrado)

comparar_y_decidir(f"series-tiempo_{fecha_hoy}.sqlite")
