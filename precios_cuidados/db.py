from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

#Crear el motor SQLAlchemy y la session 
engine = create_engine('sqlite:///precios_cuidado.db')
Session = sessionmaker(bind=engine)
session = Session()

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(engine)

# Crear una fábrica de sesiones
Session = sessionmaker(bind=engine)

# Función para obtener una nueva sesión
def get_session():
    return Session()
