from pydantic import BaseModel
import json
import os
import jwt
import datetime
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from auth import router as auth_router  # Importar las rutas desde auth.py
from articulos import router as articulos_router  # Importar las rutas desde articulos.py

# Cargar las variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir las rutas del archivo auth.py
app.include_router(auth_router)
app.include_router(articulos_router)

@app.get("/")
async def read_root():
    return {"message": "Hola Mundo!"}
