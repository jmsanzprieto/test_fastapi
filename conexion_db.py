# db_connection.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_db_connection():
    try:
        # Leer los valores de conexión desde las variables de entorno
        host = os.getenv('DB_SERVER')
        database = os.getenv('DATABASE')
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')

        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None