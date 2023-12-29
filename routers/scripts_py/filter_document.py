import os, json

def filter_document(document):

    extracted_data = {}
    cabecera = []

    # Procesar 'document.text' para extraer información
    lines = document.text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            extracted_data[key] = value
        else:
            cabecera.append(line)

    # Convertir el diccionario a formato JSON
    #json_data = json.dumps(extracted_data, indent=2)
    
    return cabecera,extracted_data