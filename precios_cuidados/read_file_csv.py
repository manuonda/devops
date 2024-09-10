# read_file_csv.py

import csv
from models import Comercio
from datetime import datetime
from db import get_session


"""
Function to read the comercio.csv file
"""
def read_file_comercio_csv(path_archivo):
    session = get_session()
    with open(path_archivo, newline='') as file_csv:
        reader = csv.reader(file_csv, delimiter='|')  # Specify the delimiter as '|'
        encabezados = next(reader)
        print("Encabezados:", encabezados)
        input("Press Enter to continue...")

        for num_fila, fila in enumerate(reader, start=1):
            now = datetime.now()
            formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

            print(f"Fila {num_fila}: ", end="")
            if fila:
                id_comercio = fila[0]
                id_bandera = fila[1]
                comercio_cuit = fila[2]
                comercio_razon_social = fila[3]
                comercio_bandera_nombre = fila[4]
                comercio_bandera_url = fila[5]
                comercio_ultima_actualizacion = fila[6]
                comercio_version_sepa = fila[7]
                fecha_alta = formatted_date
                comercio = Comercio()
                comercio.id_comercio =id_comercio 
                comercio.id_bandera = id_bandera 
                comercio.comercio_cuit = comercio_cuit
                comercio.comercio_razon_social = comercio_razon_social
                comercio.comercio_bandera_nombre = comercio_bandera_nombre
                comercio.comercio_bandera_url = comercio_bandera_url
                comercio.comercio_ultima_actualizacion = comercio_ultima_actualizacion
                comercio.comercio_version_sepa = comercio_version_sepa
                comercio.fecha_alta = fecha_alta
                print(comercio)

                # Insertar en la base de datos 
                comercio.insert_comercio(session)

            print()  # Salto de línea después de cada fila



def leer_directorio(path_directorio):
    """Función para leer archivos CSV en un directorio y procesarlos según su tipo"""
    print(f"Leyendo archivos en el directorio: {path_directorio}")
    
    for filename in os.listdir(path_directorio):
        if filename.endswith('.csv'):
            file_path = os.path.join(path_directorio, filename)
            print(f"Procesando archivo: {filename}")
            
            if filename.endswith('comercio.csv'):
                print("Es un archivo de comercio")
                read_file_comercio_csv(file_path)
            elif filename.endswith('productos.csv'):
                print("Es un archivo de productos")
                # Aquí puedes llamar a una función para procesar archivos de productos
            elif filename.endswith('precios.csv'):
                print("Es un archivo de precios")
                # Aquí puedes llamar a una función para procesar archivos de precios
            else:
                print("No se reconoce el tipo de archivo CSV")
            
            print("--------------------")

# Uso de la función
#leer_directorio('/ruta/al/directorio')
# Ejemplo de uso
#leer_csv('/home/manuonda/projects/devops/precios_cuidados/data_files/Jueves - Precios SEPA Minoristas jueves, 05-09-2024.sepa_jueves/sepa_1_comercio-sepa-3_2024-09-05_09-05-12/comercio.csv')

