import pandas as pd
import sqlite3
import os
import goverment_info as gi
from datetime import datetime

fecha_hoy = datetime.today().strftime('%Y-%m-%d')

hoy = pd.to_datetime(datetime.today().date())

gi.download_goverment_info()

def cargar_datos(nombre_archivo, nombre_tabla):
    ruta = os.path.join("datos_sqlite", nombre_archivo)
    conexion = sqlite3.connect(ruta)
    df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conexion)
    conexion.close()
    return df

def conservar_nuevo_y_eliminar_viejo(nombre_nuevo_archivo, carpeta="datos_sqlite"):
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
    
    # Buscar archivo anterior más reciente (que no sea el nuevo)
    archivos_sqlite = sorted([
        f for f in os.listdir(carpeta) if f.endswith(".sqlite") and f != nombre_nuevo_archivo
    ], reverse=True)

    if archivos_sqlite:
        archivo_anterior = archivos_sqlite[0]
        os.remove(os.path.join(carpeta, archivo_anterior))
        print(f"Archivo anterior eliminado: {archivo_anterior}")
    else:
        print("No hay archivos anteriores para eliminar.")

    print(f"Archivo nuevo conservado: {nombre_nuevo_archivo}")
    return df_nuevo

ultima_infromacion = conservar_nuevo_y_eliminar_viejo(f"series-tiempo_{fecha_hoy}.sqlite")    

# Mostrar resultado ordenado por título
ultima_infromacion = ultima_infromacion[(ultima_infromacion['serie_actualizada'] == 1) & (ultima_infromacion['serie_discontinuada'] == 1)]

# Ver cantidad de registros por título
print(ultima_infromacion.value_counts('serie_titulo'))

def filtrar_por_titulo(df, titulo_serie):
    df_filtrado = df[df['serie_titulo'] == titulo_serie].copy()
    return df_filtrado

# Ejemplo de uso
titulo_deseado = "gtos_primarios_despues_figurativos_2017"
df_serie = filtrar_por_titulo(ultima_infromacion, titulo_deseado)

# Visualización previa
print(df_serie.head())
