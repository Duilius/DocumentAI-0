import claves, os
import os

def probar_acceso_credenciales():
    try:
        project_id = os.environ.get('PROJECT_ID')
        processor_id = os.environ.get('PROCESSOR_ID')
        endpoint = os.environ.get('ENDPOINT')
        region = os.environ.get('REGION')

        print("Credenciales accesibles:")
        print(f"PROJECT_ID: {project_id}")
        print(f"PROCESSOR_ID: {processor_id}")
        print(f"ENDPOINT: {endpoint}")
        print(f"REGION: {region}")
    except Exception as e:
        print(f"Error al acceder a las credenciales: {e}")

if __name__ == "__main__":
    probar_acceso_credenciales()
