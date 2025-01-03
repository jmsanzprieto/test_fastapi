from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import json
import os
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from funciones import load_data_articulos,  save_data_articulos,  verify_jwt_token
from dotenv import load_dotenv

# Cargar la ruta del archivo JSON desde el archivo .env
load_dotenv()

# Ruta del archivo JSON
DATOS_ARTICULOS_PATH = os.getenv("DATOS_ARTICULOS")

# Middleware de seguridad
security = HTTPBearer()

# Modelo Pydantic para validar los datos de los artículos
class Articulo(BaseModel):
    id: int
    titulo: str
    fecha: str
    autor: str
    contenido: str

# Iniciar el router de FastAPI
router = APIRouter()

# Dependencia para verificar el token en todas las rutas
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    return payload

# Ruta para obtener todos los artículos
@router.get("/articulos", response_model=List[Articulo])
async def get_articulos():
    data = load_data_articulos()
    return data

# Ruta para obtener un artículo por ID
@router.get("/articulo/{articulo_id}", response_model=Articulo, dependencies=[Depends(validate_token)])
async def get_articulo(articulo_id: int):
    data = load_data_articulos()
    articulo = next((art for art in data if art["id"] == articulo_id), None)
    if articulo is None:
        raise HTTPException(status_code=404, detail="Articulo no encontrado")
    return articulo

# Ruta para crear un artículo
@router.post("/articulo", response_model=Articulo, dependencies=[Depends(validate_token)])
async def create_articulo(articulo: Articulo):
    data = load_data_articulos()
    # Verificar si el ID ya existe
    if any(art["id"] == articulo.id for art in data):
        raise HTTPException(status_code=400, detail="El artículo con este ID ya existe")
    data.append(articulo.dict())
    save_data_articulos(data)
    return articulo

# Ruta para actualizar un artículo
@router.put("/articulo/{articulo_id}", response_model=Articulo, dependencies=[Depends(validate_token)])
async def update_articulo(articulo_id: int, articulo: Articulo):
    data = load_data_articulos()
    for idx, art in enumerate(data):
        if art["id"] == articulo_id:
            data[idx] = articulo.dict()
            save_data_articulos(data)
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

# Ruta para eliminar un artículo
@router.delete("/articulo/{articulo_id}", response_model=Articulo, dependencies=[Depends(validate_token)])
async def delete_articulo(articulo_id: int):
    data = load_data_articulos()
    for idx, art in enumerate(data):
        if art["id"] == articulo_id:
            deleted_articulo = data.pop(idx)
            save_data_articulos(data)
            return deleted_articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")
