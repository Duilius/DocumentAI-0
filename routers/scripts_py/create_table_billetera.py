from sqlalchemy import create_engine, Column, Integer, Float, Date, String, DateTime, Time, Boolean
from sqlalchemy.orm import declarative_base
#Es necesario instalar el paquete mysqlclient

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

# Ejemplo de conexión a la base de datos (cambia los parámetros según tu configuración)
engine = create_engine('mysql://root:h3c6a6hGAGCA2geBGb-fh4H5FBeC2dbf@roundhouse.proxy.rlwy.net:27692/railway')
#mysql://root:h3c6a6hGAGCA2geBGb-fh4H5FBeC2dbf@mysql.railway.internal:3306/railway
# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)