import requests
from bs4 import BeautifulSoup
import sqlite3  # S

url = "https://datos.produccion.gob.ar/dataset/sepa-precios"  # Reemplaza esta URL con la dirección de la página que deseas leer

# Configuración de la conexión a la base de datos
# Cambia esto según el tipo de base de datos que estés usando
conn = sqlite3.connect('base_de_datos.db')
cursor = conn.cursor()

# Crea una tabla para almacenar los datos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS precios (
        nombre TEXT PRIMARY KEY,
        descripcion TEXT
    )
''')
conn.commit()

# URL de la página que deseas analizar
response = requests.get(url)

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
            #cursor.execute('SELECT * FROM precios WHERE nombre = ?', (nombre,))
            #resultado = cursor.fetchone()

            resultado = None
            if not resultado:
                #print(f'Nuevo paquete encontrado: {nombre} - {descripcion}')
                # Buscar el enlace de descarga que contiene un botón con el texto DESCARGAR
                enlace_descargar = div.find('a', href=True)
                print(f'Enlace de descarga: {enlace_descargar}')
                if enlace_descargar and enlace_descargar.find('button', string='DESCARGAR'):
                    url_descarga = enlace_descargar['href']
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
