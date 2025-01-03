# Proyecto FastAPI

Este documento proporciona instrucciones para descargar, instalar y lanzar el proyecto FastAPI.

## Requisitos previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio del proyecto:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea y activa un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura un fichero .env con parametros de conexion
      ```
        DB_SERVER = "localhost"
        DATABASE = ""
        USER = ""
        PASSWORD = "" 
    ```
   

## Ejecución

1. Inicia la aplicación FastAPI:
    ```bash
     python -m uvicorn main:app --reload
    ```

2. Abre tu navegador web y navega a `http://127.0.0.1:8000` para ver la aplicación en funcionamiento.

## Documentación de la API

FastAPI genera automáticamente documentación interactiva para la API. Puedes acceder a ella en las siguientes URLs una vez que la aplicación esté en ejecución:

- Documentación Swagger: `http://127.0.0.1:8000/docs`
- Documentación ReDoc: `http://127.0.0.1:8000/redoc`

## Notas adicionales

- Asegúrate de revisar y ajustar las configuraciones en el archivo `main.py` según sea necesario para tu entorno de desarrollo.
- Para más información sobre FastAPI, visita la [documentación oficial](https://fastapi.tiangolo.com/).
