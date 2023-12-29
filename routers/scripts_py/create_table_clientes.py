from sqlalchemy import create_engine, Column, Integer, Float, Date, String, DateTime, Time, Boolean
from sqlalchemy.orm import declarative_base
#Es necesario instalar el paquete mysqlclient

import os
import claves

## Variables de conexión a Base de Datos en Railway
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_port=os.getenv("DB_PORT")
db_name=os.getenv("DB_NAME")
db_type=os.getenv("DB_TYPE")

engine = create_engine(f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

Base = declarative_base()

class Venta(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True)
    name_cliente = Column(String(55))
    ruc_cliente = Column(String(11))
    whatsapp_cliente = Column(String(11))
    email_cliente = Column(String(100))
    ip_cliente = Column(String(25))
    pais_cliente = Column(String(55))
    user_sistema = Column(String(15))
    fecha_sistema = Column(Date)
    hora_sistema = Column(Time)

# Ejemplo de conexión a la base de datos (cambia los parámetros según tu configuración)

# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)