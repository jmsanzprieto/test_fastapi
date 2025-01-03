from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import json
import os
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from funciones import load_data_usuarios, save_data_usuarios, verify_jwt_token, delete_data_usuario
from dotenv import load_dotenv

# Cargar la ruta del archivo JSON desde el archivo .env
load_dotenv()

# Middleware de seguridad
security = HTTPBearer()

# Modelo Pydantic para validar los datos de los artículos
class usuario(BaseModel):
    id: int
    username: str
    password: str


# Iniciar el router de FastAPI
router = APIRouter()

# Dependencia para verificar el token en todas las rutas
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    return payload

# Ruta para obtener todos los artículos
@router.get("/usuarios", response_model=List[usuario])
async def get_usuarios():
    data = load_data_usuarios()
    return data

# Ruta para obtener un artículo por ID
@router.get("/usuario/{usuario_id}", response_model=usuario, dependencies=[Depends(validate_token)])
async def get_usuario(usuario_id: int):
    data = load_data_usuarios()
    usuario = next((art for art in data if art["id"] == usuario_id), None)
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return usuario

# Ruta para crear un artículo
@router.post("/usuario", response_model=usuario, dependencies=[Depends(validate_token)])
async def create_usuario(usuario: usuario):
    data = load_data_usuarios()
    # Verificar si el ID ya existe
    if any(art["id"] == usuario.id for art in data):
        raise HTTPException(status_code=400, detail="El artículo con este ID ya existe")
    data.append(usuario.dict())
    save_data_usuarios(data)
    return usuario

# Ruta para actualizar un artículo
@router.put("/usuario/{usuario_id}", response_model=usuario, dependencies=[Depends(validate_token)])
async def update_usuario(usuario_id: int, usuario: usuario):
    data = load_data_usuarios()
    for idx, art in enumerate(data):
        if art["id"] == usuario_id:
            data[idx] = usuario.dict()
            save_data_usuarios(data)
            return usuario
    raise HTTPException(status_code=404, detail="usuario no encontrado")

# Ruta para eliminar un artículo
@router.delete("/usuario/{usuario_id}", dependencies=[Depends(validate_token)])
async def delete_usuario(usuario_id: int):
    try:
        # Llamamos a la función para eliminar el artículo de la base de datos
        delete_data_usuario(usuario_id)

        # Devolvemos solo un mensaje indicando que el artículo fue eliminado
        return {"message": "usuario eliminado correctamente"}

    except HTTPException as e:
        # Si ocurre un error, lo levantamos de nuevo para que sea manejado
        raise e
    except Exception as e:
        # Capturamos cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error al eliminar el artículo: {e}")
