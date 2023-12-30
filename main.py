## Importing the Modules Needed to Communicate Backend and Frontend.
import uvicorn
from fastapi.responses import JSONResponse, HTMLResponse
import asyncio
from fastapi import APIRouter
import os
from os import getcwd
from fastapi import FastAPI, UploadFile, Request, Response,Form,File,Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

#import mysql.connector

## Importing the functions needed to filter and validate the text extracted from the documents.
from routers.scripts_py.filter_document import filter_document
from routers.scripts_py.save_storage import save_storage
from routers.scripts_py.show_table_yape import show_table_yape

##Importing the Modules Needed to Extract Text with Google Artificial Intelligence

from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import os, json
import claves # Archivo con las claves de acceso a la API de DocumentAI


## Variables de conexión a Base de Datos en Railway
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_port=os.getenv("DB_PORT")
db_name=os.getenv("DB_NAME")
db_type=os.getenv("DB_TYPE")

app = FastAPI()

templates = Jinja2Templates(directory="templates/html")
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/yape", response_class=HTMLResponse)
async def yape(request: Request):
    return templates.TemplateResponse("yape.html", {"request": request})

@app.post("/upload_documents")
async def upload_documents(request: Request, archivos: List[UploadFile]):

    ## Variables de entorno - Servicio de Google Cloud
    endpoint = os.getenv('ENDPOINT')
    project_id = os.getenv('PROJECT_ID')
    processor_id = os.getenv('PROCESSOR_ID') # Create processor in Cloud Console
    location = os.getenv('REGION') # Format is 'us' or 'eu'

    #Create an instantiate to "DocumentProcessorServiceClient" class
    client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(api_endpoint=f"{location}-{endpoint}"))

    #Get processor path
    name = client.processor_path(project_id, location, processor_id)

    carpeta_pdf = getcwd() + "/templates/image"

    for file_uri in archivos:
        print("file_uri===================>",file_uri)
        print("Nombre del Archivo ===================>",file_uri.filename)
        #Get mime_type
        if file_uri.filename.endswith('.pdf'):
            mime_type = "application/pdf"
        else:        
            mime_type = "image/jpeg"
	
        #Get file contents (PDF or Images)
        with open(file_uri.filename, 'rb') as file_bites:
            file_content_bites = file_bites.read()    

        #Create a "RawDocument" object (encapsulate the file content + mime_type)
        raw_file_documentai = documentai.RawDocument(
            content=file_content_bites,
            mime_type=mime_type)

        #Request to process the document (raw_file_documentai)
        request_doc = documentai.ProcessRequest(
            name=name,
            raw_document=raw_file_documentai)   
        
        #Request the document to be processed and receive the response
        response = client.process_document(request=request_doc)
        document = response.document #Get the document object, already processed, from the response
        
        #Validate and Filter each document 👀
        cabecera,json_data = filter_document(document)

        #Insert the document into the database
        mto_pagado, num_operacion = save_storage(cabecera,json_data)

        #Return the result of query
        results, count_result = show_table_yape()

        #Return the result of the insertion
        #print("Monto pagado: S/. ", mto_pagado)
        #print("Número de operación: ", num_operacion)	


        return templates.TemplateResponse("partial_yape.html", {"request": request,"yapes": results, "toal_yapes_hoy": count_result})