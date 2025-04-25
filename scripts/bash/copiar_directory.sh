#!/bin/bash

# Validar argumentos 
if [ "$#" -ne 2 ]; then 
  echo "Uso: $0 <directorio_origen> <directorio_destino>"
  exit 1
fi

ORIGEN="$1"
DESTINO="$2"

# Verificar si el directorio de origen existe
if [ ! -d "$ORIGEN" ]; then
  echo "El directorio de origen no existe: $ORIGEN"
  exit 1
fi

#Verificar si el directorio destino existe 
if [ ! -d "$DESTINO" ]; then 
  echo "El directorio destino no existe: $DESTINO"
  exit 1
fi


#Copiar solo src y public 
rsync -av --progress "$ORIGEN/src/" "$DESTINO/src/"
rsync -av --progress "$ORIGEN/public/" "$DESTINO/public/"

echo "Copia completada de $ORIGEN a $DESTINO"
# Fin del script
