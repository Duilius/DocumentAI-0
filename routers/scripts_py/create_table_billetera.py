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

class Pagos(Base):
    __tablename__ = 'billetera'

    id = Column(Integer, primary_key=True)
    operador = Column(String(55))
    accion = Column(String(55))
    monto = Column(Float)
    mi_empresa = Column(String(50))
    fecha_pago = Column(Date)
    hora_pago = Column(Time)
    mi_celular = Column(String(15))
    destino = Column(String(55))
    num_operacion = Column(String(55))
    otro_dato = Column(String(50))
    error_en = Column(String(150))
    validado = Column(Boolean)
    user_sistema = Column(String(15))
    fecha_sistema = Column(Date)
    hora_sistema = Column(Time)


# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)