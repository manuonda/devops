import requests
import os
from bs4 import BeautifulSoup
import sqlite3
import datetime
from urllib.parse import urlparse
import zipfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_tablas import Comercio, Producto, Base , PreciosCuidadosHistorial
from unzip_file import descomprimir_archivo

print("Iniciando scrapping")

#Crear el motor SQLAlchemy y la session 
engine = create_engine('sqlite:///precios_cuidado.db')
Session = sessionmaker(bind=engine)
session = Session()

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(engine)

url = "https://datos.produccion.gob.ar/dataset/sepa-precios"  # URL de la página


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



    for div in divs:
        # Información del paquete
        package_info = div.find('div', class_='package-info')
        if package_info:
            nombre = package_info.find('h3').text.strip()
            descripcion = package_info.find('p').text.strip()
            nombre_concat_description = nombre + ' - ' + descripcion
            print('----------------------------------')
            print(f'nombre: {nombre}  - descripcion : {descripcion} - nombre_concat_description: {nombre_concat_description}')

            # Verificar si los datos ya existen en la base de datos
            # cursor.execute('SELECT * FROM precios_cuidado_pagina WHERE title_descarga = ? and status= ? ', (nombre_concat_description, 'PROCESADO'))
            # resultado = cursor.fetchone()
            
            resultado = session.query(PreciosCuidadosHistorial).filter(PreciosCuidadosHistorial.title_descarga == nombre_concat_description, PreciosCuidadosHistorial.status == 'PROCESADO').first()
            
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

                                nombre_concat_description = nombre_concat_description.replace('/', '-').replace('\\', '-')
                                nombre_archivo_extension = os.path.basename(urlparse(url_descarga).path)
                                nombre_archivo = os.path.join(directory, nombre_concat_description + "." + nombre_archivo_extension)

                                print(f'Guardando archivo en: {nombre_archivo}')

                                # Guardar el archivo en el directorio determinado 
                                with open(nombre_archivo, 'wb') as f:
                                    f.write(archivo_response.content)

                                print(f'Archivo {nombre_archivo} descargado con éxito.')

                                # Descomprimir el archivo zip si es necesario
                                if nombre_archivo_extension.endswith('.zip'):
                                    directorio_archivo = descomprimir_archivo(nombre_archivo, ejecutar_descompresion=True)  # Asegúrate de pasar False para ejecutar_descompresion
                                    print(f'Directorio descomprimido: {directorio_archivo}')
                                    #leer_csv(directorio_archivo)
                                    
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
                            print('No se encontró el enlace de descarga. Etiqueta "DESCARGAR"')
            else:
                print(f'El archivo de descarga {nombre_concat_description} ya existe en la base de datos.')
else:
    print(f'Error al acceder a la página: {response.status_code}')

# Cerrar la conexión a la base de datos
session.close()
