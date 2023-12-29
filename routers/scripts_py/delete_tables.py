from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine

engine = create_engine('mysql://root:h3c6a6hGAGCA2geBGb-fh4H5FBeC2dbf@roundhouse.proxy.rlwy.net:27692/railway')
# Crear una instancia de MetaData
metadata = MetaData()

# Enlazar el motor con la MetaData
metadata.reflect(bind=engine)

# Eliminar la tabla 'tipo_user' de la base de datos
metadata.drop_all(engine, [metadata.tables['billetera']], checkfirst=True)