import requests 
import os
from bs4 import BeautifulSoup
import sqlite3  # S

url = "https://datos.produccion.gob.ar/dataset/sepa-precios"  # Reemplaza esta URL con la dirección de la página que deseas leer

# Configuración de la conexión a la base de datos
# Cambia esto según el tipo de base de datos que estés usando
conn = sqlite3.connect('base_de_datos.db')
cursor = conn.cursor()

# Crea una tabla para almacenar los datos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS precios_claro_tbl (
        nombre TEXT PRIMARY KEY,
        etiqueta TEXT,
        descripcion TEXT,
        fecha_carga TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
        fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
    )
''')
conn.commit()

# URL de la página que deseas analizar
response = requests.get(url)

# Check if the directory exists, if not, create it
directory = "data_files"
if not os.path.exists(directory):
    os.makedirs(directory)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='pkg-container')

    for div in divs:
        #package that contains the name and description of the file dataset
        package_info = div.find('div', class_='package-info')
        if package_info:
            nombre = package_info.find('h3').text.strip()
            descripcion = package_info.find('p').text.strip()
            print(f'Paquete encontrado: {nombre} - {descripcion}')

            # Verifica si los datos ya existen en la base de datos
            cursor.execute('SELECT * FROM precios WHERE nombre = ?', (nombre,))
            resultado = cursor.fetchone()

            resultado = None
            if not resultado:
                div_actions = div.find('div', class_='pkg-actions')
                if div_actions:
                    div_action_a_list = div_actions.find_all('a', href=True)
                    
                    for a_action in div_action_a_list:
                       print(f'Enlace de descarga a_action: {a_action}')     
                       
                       if a_action and a_action.find('button', string='DESCARGAR'):
                           url_descarga = a_action['href']
                           print(f'Descargando archivo desde: {url_descarga}')
           
                           # Descargar el archivo
                           archivo_response = requests.get(url_descarga)
                           nombre_archivo = url_descarga.split('/')[-1]
           
                           with open(nombre_archivo, 'wb') as f:
                               f.write(archivo_response.content)
                           print(f'Archivo {nombre_archivo} descargado con éxito.')
           
                           # Insertar los datos en la base de datos
                           #cursor.execute('INSERT INTO precios (nombre, descripcion) VALUES (?, ?)', (nombre, descripcion))
                           #conn.commit()
                       else:
                           print('No se encontró el enlace de descarga.')
        else:
            print(f'El paquete {nombre} ya existe en la base de datos.') 
else:
    print(f'Error al acceder a la página: {response.status_code}')

# Cierra la conexión a la base de datos
#conn.close()
