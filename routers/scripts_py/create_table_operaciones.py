from sqlalchemy import create_engine, Column, Integer, Float, Date, String, DateTime, Time, Boolean
from sqlalchemy.orm import declarative_base
#Es necesario instalar el paquete mysqlclient

Base = declarative_base()

class Venta(Base):
    __tablename__ = 'operaciones'

    id_operacion = Column(Integer, primary_key=True)
    num_operacion = Column(String(55))
    monto_operacion = Column(Float)
    fecha_operacion = Column(Date)
    hora_operacion = Column(Time)
    id_cliente = Column(Integer)
    id_user = Column(Integer)
    fecha_sistema = Column(Date)
    hora_sistema = Column(Time)

# Ejemplo de conexión a la base de datos (cambia los parámetros según tu configuración)
engine = create_engine('mysql://root:h3c6a6hGAGCA2geBGb-fh4H5FBeC2dbf@roundhouse.proxy.rlwy.net:27692/railway')
#mysql://root:h3c6a6hGAGCA2geBGb-fh4H5FBeC2dbf@mysql.railway.internal:3306/railway
# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)