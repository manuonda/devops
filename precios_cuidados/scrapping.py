import requests
import os
from bs4 import BeautifulSoup
import sqlite3
import datetime
from urllib.parse import urlparse
import zipfile

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

    # Recorrer el directorio de los archivos y leer los csv
    for root, dirs, files in os.walk(directorio_archivo):
        for file in files:
            print(f'leyendo archivo: {file}')
            if file.endswith('.zip'):
                # Descomprimir los archivos zip
                path_archivo = os.path.join(root, file)
                with zipfile.ZipFile(path_archivo, 'r') as zip_ref:
                    zip_ref.extractall(root)
            elif file.endswith('.csv'):
                # Leer los archivos csv
                path_archivo = os.path.join(root, file)
                print(f'leyendo archivo: {path_archivo}')

url = "https://datos.produccion.gob.ar/dataset/sepa-precios"  # URL de la página

# Configuración de la conexión a la base de datos
conn = sqlite3.connect('base_de_datos.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS precios_cuidado_pagina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_descarga TEXT,
        descripcion TEXT,
        nombre_archivo TEXT,
        status TEXT,
        fecha_alta TEXT
    )
''')
conn.commit()

# Truncar la tabla
cursor.execute('DELETE FROM precios_cuidado_pagina')

# Hacer una petición GET a la URL
response = requests.get(url)

# Verificar si el directorio existe, si no, crearlo
directory = "data_files"
if not os.path.exists(directory):
    os.makedirs(directory)

# Si la respuesta es exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='pkg-container')

    # Mostrar los registros de la tabla
    cursor.execute('SELECT * FROM precios_cuidado_pagina')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    for div in divs:
        # Información del paquete
        package_info = div.find('div', class_='package-info')
        if package_info:
            nombre = package_info.find('h3').text.strip()
            descripcion = package_info.find('p').text.strip()
            nombre_concat_description = nombre + ' - ' + descripcion

            # Verificar si los datos ya existen en la base de datos
            cursor.execute('SELECT * FROM precios_cuidado_pagina WHERE title_descarga = ? and status= ? ', (nombre_concat_description, 'PROCESADO'))
            resultado = cursor.fetchone()

            if not resultado:  # Si no se encontró el resultado
                div_actions = div.find('div', class_='pkg-actions')
                if div_actions:
                    div_action_a_list = div_actions.find_all('a', href=True)

                    for a_action in div_action_a_list:
                        if a_action and a_action.find('button', string='DESCARGAR'):
                            url_descarga = a_action['href']
                            print(f'Descargando archivo desde: {url_descarga}')

                            try:
                                # Descargar el archivo
                                archivo_response = requests.get(url_descarga)
                                archivo_response.raise_for_status()  # Esto lanzará una excepción si hay un error

                                nombre_archivo_extension = os.path.basename(urlparse(url_descarga).path)
                                nombre_archivo = os.path.join(directory, nombre_concat_description + "." + nombre_archivo_extension)

                                # Guardar el archivo en el directorio determinado 
                                with open(nombre_archivo, 'wb') as f:
                                    f.write(archivo_response.content)

                                print(f'Archivo {nombre_archivo} descargado con éxito.')

                                # Descomprimir el archivo zip si es necesario
                                if nombre_archivo_extension.endswith('.zip'):
                                    descomprimir_archivo(nombre_archivo)

                                # Obtener la fecha y hora actual
                                fecha_alta = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                status = "PROCESADO"  # Definir el estado

                                # Insertar los datos en la base de datos
                                cursor.execute('INSERT INTO precios_cuidado_pagina (title_descarga, descripcion, nombre_archivo, status, fecha_alta) VALUES (?, ?, ?, ?, ?)',
                                               (nombre_concat_description, descripcion.replace('\n', ' '), nombre_archivo, status, fecha_alta))
                                conn.commit()

                            except requests.RequestException as e:
                                print(f'Error al descargar el archivo desde {url_descarga}: {e}')
                        else:
                            print('No se encontró el enlace de descarga.')
            else:
                print(f'El archivo de descarga {nombre} ya existe en la base de datos.')
else:
    print(f'Error al acceder a la página: {response.status_code}')

# Cerrar la conexión a la base de datos
conn.close()
