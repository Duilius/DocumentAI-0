from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import os, json
import claves # Archivo con las claves de acceso a la API de DocumentAI

os.environ['Google_Application_Credentials'] = 'rtf_ocr_claves.json'

## Variables de entorno
endpoint = os.getenv('ENDPOINT')
project_id = os.getenv('PROJECT_ID')
processor_id = os.getenv('PROCESSOR_ID') # Create processor in Cloud Console
location = os.getenv('REGION') # Format is 'us' or 'eu'

## Variables de conexión a Base de Datos en Railway


#Get file contents (PDF or Images)
def get_file_contents(file_uri):
    print("file_uri===================>",file_uri)
    try:
        if file_uri.endswith('.pdf'):
            mime_type = "application/pdf"
        else:        
            mime_type = "image/jpeg"

        client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(api_endpoint=f"{location}-{endpoint}"))
        name = client.processor_path(project_id, location, processor_id)
        
        #Capturar contenido del PDF
        with open(file_uri, 'rb') as file_bites:
            file_content_bites = file_bites.read()

        raw_file_documentai = documentai.RawDocument(
            content=file_content_bites,
            mime_type=mime_type)
        
        request = documentai.ProcessRequest(
            name=name,
            raw_document=raw_file_documentai)
        
        response = client.process_document(request=request)
        document = response.document
    
        #return document.text

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
        json_data = json.dumps(extracted_data, indent=2)
        
        return cabecera,json_data

    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    pdf_prueba = 'yape-1.jpg'

    json_data = get_file_contents(pdf_prueba)[1]
    cabecera = get_file_contents(pdf_prueba)[0]
                               
    decoded_data = json.loads(json_data)
    print(cabecera)
    print(json.dumps(decoded_data, indent=2, ensure_ascii=False))
    #print(pdf_text) 