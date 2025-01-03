from pydantic import BaseModel
import json
import os
import jwt
import datetime
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()
# Ubicación del archivo de usuarios
file_path = os.getenv("USERS_FILE")
# Clave secreta para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
# Lista de tokens revocados
REVOKED_TOKENS_FILE = os.getenv("REVOKED_TOKENS_FILE")
# Lista de artículos
DATOS_ARTICULOS_PATH = os.getenv("DATOS_ARTICULOS")

# Función para cargar los datos del archivo JSON
def load_data_articulos():
    try:
        with open(DATOS_ARTICULOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar los datos: {e}")

# Función para guardar los datos en el archivo JSON
def save_data_articulos(data):
    try:
        with open(DATOS_ARTICULOS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")



# Ruta para cargar datos de usuarios desde un archivo JSON, en este caso o desde una base de datos
def load_user_data():
    # Obtiene la ruta del archivo desde el .env
    file_path = os.getenv("USERS_FILE")
    print(f"Ruta del archivo: {file_path}")
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f)

# Función para cargar los tokens revocados desde el archivo
def load_revoked_tokens():
    if os.path.exists(REVOKED_TOKENS_FILE):
        with open(REVOKED_TOKENS_FILE, "r") as f:
            return set(json.load(f))
    return set()


# Función para crear un JWT
def create_jwt_token(username: str) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token válido por 1 hora
    payload = {
        "sub": username,
        "exp": expiration,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Inicializar la lista de tokens revocados
revoked_tokens = load_revoked_tokens()

# Función para verificar un JWT
def verify_jwt_token(token: str):
    if token in revoked_tokens:  # Verifica si el token está en la lista de revocados
        raise HTTPException(status_code=401, detail="Token has been revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    



# Función para guardar los tokens revocados en el archivo
def save_revoked_tokens(tokens):
    with open(REVOKED_TOKENS_FILE, "w") as f:
        json.dump(list(tokens), f)