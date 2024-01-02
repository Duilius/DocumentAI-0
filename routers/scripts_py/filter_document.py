import os, json

def filter_document(document):

    extracted_data = {}
    cabezera = []

    # Procesar 'document.text' para extraer información
    lines = document.text.split('\n')
    x=0
    for line in lines:
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            extracted_data[key] = value
        else:
            if not line=='yape':
                cabezera.append(line)
                print("XXXXX :", x+1)
                print("LA CABEZERA ES :", cabezera)
    # Convertir el diccionario a formato JSON
    #json_data = json.dumps(extracted_data, indent=2)
    
    return cabezera,extracted_data