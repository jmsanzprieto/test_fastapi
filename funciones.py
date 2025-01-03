from pydantic import BaseModel
import json
import os
import jwt
from datetime import datetime,timedelta
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from conexion_db import get_db_connection


# Cargar las variables de entorno
load_dotenv()

# Clave secreta para JWT
SECRET_KEY = os.getenv("SECRET_KEY")


# Función para cargar los datos de los artículos desde la base de datos
def load_data_articulos():
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = connection.cursor(dictionary=True)  # Usar dictionary=True para obtener un diccionario por fila
        query = "SELECT * FROM posts"
        cursor.execute(query)
        data = cursor.fetchall()  # Obtener todos los registros
        
        # Convertir fechas de tipo datetime a formato string "YYYY-MM-DD"
        for row in data:
            if isinstance(row['fecha'], datetime):  # Asegúrate de usar datetime del módulo datetime
                row['fecha'] = row['fecha'].strftime('%Y-%m-%d')  # Formato de fecha como string

        cursor.close()
        connection.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar los datos de la base de datos: {e}")
    
# Funcion para cargar los datos de los usuarios desde la base de datos
def load_data_usuarios():
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = connection.cursor(dictionary=True)  # Usar dictionary=True para obtener un diccionario por fila
        query = "SELECT * FROM users"
        cursor.execute(query)
        data = cursor.fetchall()  # Obtener todos los registros

        cursor.close()
        connection.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar los datos de la base de datos: {e}")


# Función para guardar los datos de los artículos en la base de datos
def save_data_articulos(data):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = connection.cursor()

        for articulo in data:
            # Insertar o actualizar los datos
            query = """
                INSERT INTO posts (id, titulo, fecha, autor, contenido)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    titulo  = VALUES(titulo),
                    fecha = VALUES(fecha),
                    autor = VALUES(autor),
                    contenido = VALUES(contenido)
            """
            cursor.execute(query, (
                articulo.get("id"),
                articulo.get("titulo"),
                articulo.get("fecha"),
                articulo.get("autor"),
                articulo.get("contenido")
            ))

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos en la base de datos: {e}")
    
# Función para guardar los datos de los usuarios en la base de datos
def save_data_usuarios(data):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = connection.cursor()

        for articulo in data:
            # Insertar o actualizar los datos
            query = """
                INSERT INTO users (id, username, password)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    username  = VALUES(username),
                    password = VALUES(password)
                    
            """
            cursor.execute(query, (
                articulo.get("id"),
                articulo.get("username"),
                articulo.get("password"),
           
            ))

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos en la base de datos: {e}")
    
# Función para eliminar un artículo de la base de datos
def delete_data_articulo(articulo_id: int):
    try:
        # Establecer la conexión con la base de datos
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = connection.cursor()

        # Query para eliminar el artículo con el id especificado
        query = """
            DELETE FROM posts WHERE id = %s
        """
        cursor.execute(query, (articulo_id,))

        # Si no se eliminó ningún registro, es probable que el artículo no exista
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Articulo no encontrado")

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el artículo de la base de datos: {e}")
    

# Función para eliminar un usuario de la base de datos
def delete_data_usuario(articulo_id: int):
    try:
        # Establecer la conexión con la base de datos
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

        cursor = connection.cursor()

        # Query para eliminar el artículo con el id especificado
        query = """
            DELETE FROM users WHERE id = %s
        """
        cursor.execute(query, (articulo_id,))

        # Si no se eliminó ningún registro, es probable que el artículo no exista
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario de la base de datos: {e}")

# Función para cargar datos de usuarios desde la base de datos
def load_user_data():
    try:
        # Obtener la conexión a la base de datos
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = connection.cursor(dictionary=True)
        # Consulta para obtener los datos de los usuarios
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()
        
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar datos de usuarios: {e}")


# Función para cargar los tokens revocados desde la base de datos
def load_revoked_tokens():
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = connection.cursor()
        # Consulta para obtener los tokens revocados
        query = "SELECT token FROM tokens_revocados"
        cursor.execute(query)
        tokens = cursor.fetchall()
        
        # Convertir los resultados en un conjunto de tokens
        revoked_tokens = {token[0] for token in tokens}  # Cambiado a token[0]
        
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()
        
        return revoked_tokens
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar tokens revocados: {e}")


# Función para crear un JWT
def create_jwt_token(username: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)
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
    

# Función para guardar los tokens revocados en la BD
def save_revoked_tokens(token):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = connection.cursor()
        # Insertar el token revocado en la base de datos
        query = "INSERT INTO tokens_revocados (token) VALUES (%s)"
        cursor.execute(query, (token,))  # Pasar el token individual
        connection.commit()
        
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el token revocado: {e}")