import zipfile
import os
from read_file_csv import leer_csv 

def descomprimir_archivo(pathArchivo):
    """
    Descomprime el archivo zip y extrae los archivos csv
    """
    # Crear un directorio para el archivo
    directorio = os.path.dirname(pathArchivo)
    nombre_archivo = os.path.basename(pathArchivo)
    nombre_directorio = os.path.splitext(nombre_archivo)[0]
    directorio_archivo = os.path.join(directorio, nombre_directorio)

    if not os.path.exists(directorio_archivo):
        os.makedirs(directorio_archivo)

    # Abrir el archivo zip
    with zipfile.ZipFile(pathArchivo, 'r') as zip_ref:
        # Extraer los archivos del zip
        zip_ref.extractall(directorio_archivo)

    print(f'Archivo descomprimido en: {directorio_archivo}')
    # Recorrer el directorio de los archivos y leer los csv
    for root, dirs, files in os.walk(directorio_archivo):
        for file in files:
            if file.endswith('.zip'):
                print(f'Archivo zip: {file}')
                # Descomprimir los archivos zip
                path_archivo = os.path.join(root, file)
                with zipfile.ZipFile(path_archivo, 'r') as zip_ref:
                    zip_ref.extractall(root)
            elif file.endswith('.csv'):
                # Leer los archivos csv
                print(f'Archivo csv: {file}')
                path_archivo = os.path.join(root, file)
                print(f'Leyendo archivo csv: {path_archivo}')
                #como puedo leer el archivo con columnas y filas en python
                with open(path_archivo, 'r') as file_csv:
                  # Primera lectura del archivo completo
                  contenido = file_csv.read()
                  print(contenido)

                  # Mover el puntero del archivo al inicio para leer de nuevo
                  file_csv.seek(0)

                  # Segunda lectura del archivo completo
                  contenido = file_csv.read()
                  print(contenido)

# Ruta del archivo ZIP que quieres descomprimir
ruta_del_archivo = '/home/manuonda/projects/devops/precios_cuidados/data_files/precios_20240828 - Precios SEPA Minoristas 28.08.2024.sepa_miercoles.zip'

# Llamar a la función con la ruta especificada
descomprimir_archivo(ruta_del_archivo)
