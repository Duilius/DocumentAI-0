from sqlalchemy import create_engine, MetaData, Table, func,select
from datetime import date
from .create_table_billetera import Pagos
import os
import claves

## Variables de conexión a Base de Datos en Railway
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_port=os.getenv("DB_PORT")
db_name=os.getenv("DB_NAME")
db_type=os.getenv("DB_TYPE")

# Convertir el puerto a un entero
#db_port = int(db_port_str) if db_port_str else None  # Puedes manejar el caso de valor None o cadena vacía aquí

def show_table_yape():

    # Crea la instancia de la base de datos (reemplaza 'mysql://user:password@host/dbname' con tu conexión)
    engine = create_engine(f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    # Establece la conexión
    #conn = engine.connect()

    # Define el nombre de la tabla y crea un objeto MetaData
    table_name = 'billetera'
    metadata = MetaData()

    # Carga la tabla existente
    billetera = Table(table_name, metadata, autoload_with=engine)

    # Crea una conexión
    with engine.connect() as connection:
        # Consulta para obtener los campos solicitados ordenados por id de manera descendente
        # Query para seleccionar columnas específicas de la tabla operaciones
        stmt = select(
            billetera.c.id,
            billetera.c.operador,
            billetera.c.monto,
            billetera.c.fecha_sistema,
            billetera.c.hora_sistema,
            billetera.c.num_operacion
        )
        stmt = stmt.order_by(billetera.c.id.desc())  # Ordenar por ID de forma descendente

        # Ejecutar la consulta y obtener los resultados
        results_query = connection.execute(stmt).fetchall()
        
        # Imprime los resultados
        for row in results_query:
            print(row)

        today = date.today()
        stmt2 = select(func.count().label('total-yapes')).where(billetera.c.fecha_sistema == today)
        count_result = connection.execute(stmt2).scalar()

        print("Número de operaciones del día:", count_result)

        return results_query, count_result
