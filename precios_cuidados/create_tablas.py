from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import CHAR, DateTime

Base = declarative_base()

class Comercio(Base):
    __tablename__ = 'comercios'

    id_comercio = Column(String(255), primary_key=True)
    id_bandera = Column(Integer, primary_key=True)
    comercio_cuit = Column(String(20), nullable=False)
    comercio_razon_social = Column(String(255), nullable=False)
    comercio_bandera_nombre = Column(String(255), nullable=False)
    comercio_bandera_url = Column(String(255), nullable=False)
    comercio_ultima_actualizacion = Column(TIMESTAMP(timezone=True), nullable=False)
    comercio_version_sepa = Column(String(10), nullable=False)
    fecha_alta = Column(DateTime)
    usuario_alta = Column(Text)
    fecha_modificacion = Column(DateTime)
    usuario_modificacion = Column(Text)

class Producto(Base):
    __tablename__ = 'productos'

    id_comercio = Column(Integer, nullable=False)
    id_bandera = Column(Integer, nullable=False)
    id_sucursal = Column(Integer, nullable=False)
    id_producto = Column(CHAR(13), primary_key=True)
    productos_ean = Column(CHAR(1), nullable=False)
    productos_descripcion = Column(Text, nullable=False)
    productos_cantidad_presentacion = Column(Integer, nullable=False)
    productos_unidad_medida_presentacion = Column(String(10), nullable=False)
    productos_marca = Column(String(255), nullable=False)
    productos_precio_lista = Column(DECIMAL(10, 2), nullable=False)
    productos_precio_referencia = Column(DECIMAL(10, 2), nullable=False)
    productos_cantidad_referencia = Column(DECIMAL(10, 2), nullable=False)
    productos_unidad_medida_referencia = Column(String(10), nullable=False)
    productos_precio_unitario_promo1 = Column(DECIMAL(10, 2), nullable=True)
    fecha_alta = Column(DateTime)
    usuario_alta = Column(Text)
    fecha_modificacion = Column(DateTime)
    usuario_modificacion = Column(Text)

class Sucursal(Base):
    __tablename__ = 'sucursales'

    id_sucursal = Column(Integer, primary_key=True)
    sucursales_latitud = Column(DECIMAL(9, 6), nullable=True)
    sucursales_longitud = Column(DECIMAL(9, 6), nullable=True)
    sucursales_observaciones = Column(Text, nullable=True)
    sucursales_barrio = Column(String(255), nullable=True)
    sucursales_codigo_postal = Column(String(10), nullable=True)
    sucursales_localidad = Column(String(255), nullable=True)
    sucursales_provincia = Column(CHAR(5), nullable=True)
    sucursales_lunes_horario_atencion = Column(String(20), nullable=True)
    sucursales_martes_horario_atencion = Column(String(20), nullable=True)
    sucursales_miercoles_horario_atencion = Column(String(20), nullable=True)
    sucursales_jueves_horario_atencion = Column(String(20), nullable=True)
    sucursales_viernes_horario_atencion = Column(String(20), nullable=True)
    sucursales_sabado_horario_atencion = Column(String(20), nullable=True)
    sucursales_domingo_horario_atencion = Column(String(20), nullable=True)
    fecha_alta = Column(DateTime)
    usuario_alta = Column(Text)
    fecha_modificacion = Column(DateTime)
    usuario_modificacion = Column(Text)


class PreciosCuidadosHistorial(Base):
    __tablename__ = 'precios_cuidados_historial'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title_descarga = Column(Text)
    descripcion = Column(Text)
    nombre_archivo = Column(Text)
    status = Column(Text)
    fecha_alta = Column(DateTime)
    usuario_alta = Column(Text)
    fecha_modificacion = Column(DateTime)
    usuario_modificacion = Column(Text)


