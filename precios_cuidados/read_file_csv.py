# read_file_csv.py

import csv

def leer_csv(path_archivo):
    """Función para leer un archivo CSV y mostrar su contenido con formato específico"""
    print(f"Leyendo archivo csv : {path_archivo}")
    input("Presiona Enter para continuar....")

    with open(path_archivo, newline='') as file_csv:
        reader = csv.reader(file_csv)
        encabezados = next(reader)
        print("Encabezados:", encabezados)
        input("Presiona Enter para continuar....")

        for num_fila, fila in enumerate(reader, start=1):
            print(f"Fila {num_fila}: ", end="")
            print(" - ".join(fila))
            print()  # Salto de línea después de cada fila

# Ejemplo de uso
leer_csv('/home/manuonda/projects/devops/precios_cuidados/data_files/precios_20240828 - Precios SEPA Minoristas 28.08.2024.sepa_miercoles/comercio.csv')
