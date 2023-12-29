import datetime



# Lista de vouchers (reemplaza esta lista con la tuya)
lista_vouchers = [
    # Grupo 1
    ["yape", "¡Yapeaste!", "S/307", "Duilio Cesar Restuccia", "Eslava", "", "20 dic. 2023 - 10:01 pm", "*** *** 434", "Yape", "09897477"],
    #['Interbank', 'Yape', 'plin', 'S/ 500.00', 'GRATIS', '¡Pago exitoso!', 'DUILIO CESAR RESTUCCIA ESLAVA', '974 089 434', '55095555', '']
    # Agrega más vouchers aquí
]

# Procesar y almacenar los vouchers en la base de datos
for voucher_data in lista_vouchers:
    # Validaciones para el grupo 1
    errores_grupo_1 = []
    monto_valido = voucher_data[2].startswith("S/") and len(voucher_data[2].split("/")[1]) > 0
    if not monto_valido:
        errores_grupo_1.append("monto")

    mi_empresa = voucher_data[3]
    if voucher_data[4]:
        mi_empresa += " " + voucher_data[4]

    # Comparación con términos fijos
    terminos_fijos = ["yape", "¡Yapeaste!", "Duilio Cesar Restuccia Eslava", ""]
    campos_no_coincidentes = [campo for campo, valor in zip(terminos_fijos, voucher_data[:5]) if valor != campo]
    errores_grupo_1.extend(campos_no_coincidentes)

    # Validación de campos del grupo 2
    fecha_hora = voucher_data[6].split(" - ")
    fecha_str = fecha_hora[0]
    hora_str = fecha_hora[1].replace("pm", "").strip() if "pm" in fecha_hora[1] else fecha_hora[1].replace("am", "").strip()
    mes_abr = fecha_str.split()[1]

    try:
        fecha_pago = datetime.datetime.strptime(f"{fecha_str.split()[0]} {mes_abr} {fecha_str.split()[2]}", "%d %b %Y").date()
        hora_pago = datetime.datetime.strptime(hora_str, "%I:%M").time()

        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.datetime.now()

        # Combinar la fecha y hora del voucher en un solo objeto datetime
        fecha_hora_pago = datetime.datetime.combine(fecha_pago, hora_pago)

        # Calcular la diferencia de tiempo entre la fecha y hora actual y la fecha y hora del pago
        diferencia_tiempo = fecha_hora_actual - fecha_hora_pago

        # Si la diferencia es mayor a 10 segundos, entonces el pago se realizó hace más de 10 segundos
        if diferencia_tiempo.total_seconds() > 10:
            errores_grupo_2 = ["fecha_hora"]
    except ValueError:
        errores_grupo_2 = ["fecha_hora"]

    mi_celular = voucher_data[7].replace("*", "").replace(" ", "")[-3:]
    celular_valido = voucher_data[7].count("*") == 3 and voucher_data[7][-4] == " " and voucher_data[7][-8:-4].count("*") == 3
    if not celular_valido:
        errores_grupo_2.append("celular")

    destino_valido = voucher_data[8] == "Yape"
    if not destino_valido:
        errores_grupo_2.append("destino")

    num_operacion_valido = len(voucher_data[9]) == 8 and voucher_data[9].isdigit()
    if not num_operacion_valido:
        errores_grupo_2.append("num_operacion")

    # Almacenar en la base de datos
    voucher_db = VoucherTabla(
        operador=voucher_data[0],
        accion=voucher_data[1],
        monto=float(voucher_data[2].replace("S/", "")),
        mi_empresa=mi_empresa,
        otro_dato=voucher_data[5],
        error_en=", ".join(errores_grupo_1 + errores_grupo_2) if errores_grupo_1 or errores_grupo_2 else None,
        validado=False if errores_grupo_1 or errores_grupo_2 else True,
        fecha_pago=fecha_pago if not errores_grupo_2 else None,
        hora_pago=hora_pago if not errores_grupo_2 else None,
        mi_celular=mi_celular if not errores_grupo_2 else None,
        destino=voucher_data[8] if not errores_grupo_2 else None,
        num_operacion=voucher_data[9] if not errores_grupo_2 else None
    )
    session.add(voucher_db)

# Confirmar los cambios en la base de datos
session.commit()
