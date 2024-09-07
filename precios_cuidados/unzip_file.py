import zipfile
import os
#from read_file_csv import leer_csv 


def descomprimir_archivo(pathArchivo, ejecutar_descompresion=False):
    print(f'Descomprimiendo archivo: {pathArchivo}')
    """
    Descomprime el archivo zip y extrae los archivos en un directorio con el nombre del archivo zip
    """
    # Crear un directorio para el archivo
    directorio = os.path.dirname(pathArchivo)
    nombre_archivo = os.path.basename(pathArchivo)
    nombre_directorio = os.path.splitext(nombre_archivo)[0]
    directorio_archivo = os.path.join(directorio, nombre_directorio)

    print(f'Directorio descomprimido: {directorio_archivo}')
    if not os.path.exists(directorio_archivo):
        os.makedirs(directorio_archivo)

    # Abrir el archivo zip
    with zipfile.ZipFile(pathArchivo, 'r') as zip_ref:
        # Extraer los archivos del zip en el directorio creado
        zip_ref.extractall(directorio_archivo)

    print(f'Archivo descomprimido en: {directorio_archivo}')

    if ejecutar_descompresion:
        # Recorrer el directorio de los archivos descomprimidos
        for root, dirs, files in os.walk(directorio_archivo):
            for file in files:
                if file.endswith('.zip'):
                    print(f'Archivo zip encontrado: {file}')
                    # Descomprimir los archivos zip contenidos en el mismo directorio
                    path_archivo = os.path.join(root, file)
                    descomprimir_archivo(path_archivo, ejecutar_descompresion=True)  # Llamada recursiva para descomprimir archivos zip contenidos en el mismo directorio

    return directorio_archivo
