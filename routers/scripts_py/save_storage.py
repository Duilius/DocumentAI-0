from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from .create_table_billetera import Pagos
import datetime
from datetime import datetime, timedelta

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

Session = sessionmaker(bind=engine)
session = Session()

def save_storage(cabezera, json_data):

    print(" cabezera 0 ===============>>>>", cabezera[0])
    print(" cabezera 1 ===============>>>>", cabezera[1])
    print(" cabezera 2 ===============>>>>", cabezera[2])
    print(" cabezera 3 ===============>>>>", cabezera[3])
    print(" cabezera 4 ===============>>>>", cabezera[4])
    
    print("SOLES SOLES SOLES ===========================>", type(float(cabezera[1].replace("S/",""))))
    lista_esperada = ["¡Yapeaste!", "S/XXX", "Duilio Cesar Restuccia", "Eslava"]
    lista_recibida = [cabezera[0], cabezera[1], cabezera[2], cabezera[3]]
    
    # Validar el primer grupo de datos(cabecera)
    errores_1 = []

    # Comparación de listas
    for idx, (esperado, recibido) in enumerate(zip(lista_esperada, lista_recibida)):
        
        print("RECIBIDO ======> ", recibido, "========== INDICE====", idx)
        print("ESPERADO ======> ", esperado, "========== INDICE====", idx)
        if idx == 3:
            # Validación del tercer elemento
            if not recibido.startswith("S/") or not recibido[2:].isdigit() or int(recibido[2:]) <= 0:
                errores_1.append(f"El tercer elemento de la lista recibida ({recibido}) no cumple con las condiciones.")
        else:
            # Validación de otros elementos
            if esperado != recibido:
                errores_1.append(f"Elemento {idx}: Esperado '{esperado}', Recibido '{recibido}'")

    # Validar el segundo grupo de datos (JSON)
    dict_recibido = json_data

    dict_esperado = {
        "N° de celular": "*** *** 434",
        "Destino": "Yape",
        "N° de operación": "dddddddd"
    }

    errores_2 = []
    

    # Obtener el primer elemento de dict_recibido
    clave_fecha_hora, valor_fecha_hora = next(iter(dict_recibido.items()))

    # Concatenar clave y valor para formar la fecha y hora completa
    fecha_hora_completa = f"{clave_fecha_hora} {valor_fecha_hora}"

    # Dividir la cadena en fecha y hora
    fecha_hora_split = fecha_hora_completa.split(" - ")
    fecha_str = fecha_hora_split[0]  # Obtenemos la parte de la fecha
    hora_str = fecha_hora_split[1]  # Obtenemos la parte de la hora

    # Formatear el mes abreviado a número de mes
    meses = {
        "ene.": "01", "feb.": "02", "mar.": "03", "abr.": "04", "may.": "05", "jun.": "06",
        "jul.": "07", "ago.": "08", "sep.": "09", "oct.": "10", "nov.": "11", "dic.": "12"
    }
    fecha_split = fecha_str.split()
    numero_mes = meses.get(fecha_split[1])  # Obtener el número de mes

    # Dar formato a la fecha y hora
    fecha_final = f"{fecha_split[0]} {numero_mes} {fecha_split[2]}"
    fecha_final = fecha_final.replace(" ", "/")

    hora_final = hora_str.replace(" pm", "pm").replace(" ",":").replace("am", " am").replace("pm", " pm")   

    # Convertir a objetos datetime
    fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y").date()  # Convertir a formato de fecha
    hora_final = datetime.strptime(hora_final, "%I:%M %p").time()    # Convertir a formato de hora

    # Combinar fecha y hora en un solo formato
    fecha_hora_completa = f"{fecha_final} - {hora_final}"
    # Combinar fecha y hora en un solo objeto datetime
    fecha_hora_pago = datetime.combine(fecha_final, hora_final)


    # Convertir la fecha y hora a objetos de datetime para comparación
    #fecha_hora_recibida = datetime.strptime(fecha_hora_completa, "%d %m %Y - %I:%M %p")
    fecha_hora_actual = datetime.now()

    # Verificar la diferencia en segundos
    diferencia_tiempo = fecha_hora_actual - fecha_hora_pago

    # Definir el límite de tiempo permitido (10 segundos en este caso)
    limite_tiempo = timedelta(seconds=10)

    # Verificar si la diferencia de tiempo es mayor que el límite permitido
    if diferencia_tiempo > limite_tiempo:
        print("Ha pasado más de 10 segundos desde el pago.")
        errores_2.append("Fecha-hora")
    else:
        print("El pago se ha realizado dentro del límite de tiempo establecido.")
        

       
    # Validar los elementos restantes
    # Obtener el primer elemento de dict_recibido
    primer_elemento = next(iter(dict_recibido.items()))

    # Separar la clave y el valor del primer elemento
    clave_fecha_hora, valor_fecha_hora = primer_elemento

    # Remover la fecha y hora del diccionario recibido para compararlo con el esperado
    dict_recibido_sin_fecha = {k: v for k, v in dict_recibido.items() if k != clave_fecha_hora}

    # Comparar los elementos restantes
    errores_2 = []
    for key in dict_recibido_sin_fecha:
        if key in dict_esperado:
            valor_recibido = dict_recibido_sin_fecha[key]
            valor_esperado = dict_esperado[key]
            if valor_recibido != valor_esperado:
                errores_2.append(key)

    # Validar el último elemento (número de operación)
    num_operacion_recibido = valor_fecha_hora
    if not num_operacion_recibido.isdigit() or len(num_operacion_recibido) != 8:
        errores_2.append("N° Operación")

    print("la fehca final o fecha de pago es: ", fecha_final)
    # Almacenar en la base de datos
    datos_insetar=Pagos(
        operador="Yape",
        accion=cabezera[0],
        monto=float(cabezera[1].replace("S/", "")),
        mi_empresa=cabezera[2]+ " " + cabezera[3],
        otro_dato=cabezera[4],
        error_en=", ".join(errores_1 + errores_2)[:145] if errores_1 or errores_2 else None,
        validado=False if errores_1 or errores_2 else True,
        fecha_pago=fecha_final, #+ timedelta(days=1),
        hora_pago=hora_final,
        mi_celular=dict_recibido.get("N° de celular", "No existe"),
        destino=dict_recibido.get("Destino", "No existe"),
        num_operacion=dict_recibido.get("N° de operación", "No existe"),
        user_sistema="sote",
        fecha_sistema=datetime.now(), #+ timedelta(days=1),
        hora_sistema=datetime.now().time()
    )

    numOperacion = dict_recibido.get("N° de operación", "No existe")
    print(" ============= N° OPERACION ===================", numOperacion)
    # ... Código para crear y agregar el nuevo registro 'nuevo_registro'

    try:
        # Agregar el nuevo registro a la sesión y realizar la inserción en la base de datos
        session.add(datos_insetar)
        session.commit()
        return cabezera[2],numOperacion
    except SQLAlchemyError as e:
        session.rollback()  # Deshacer los cambios en caso de error
        return "Error en la inserción:", e
    finally:
        session.close()