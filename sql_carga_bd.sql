-- Crea la base de datos test_db

CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;

-- Crea la tabla users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

ALTER TABLE users ADD UNIQUE (username);

INSERT INTO users (username, password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3'),
('user4', 'password4'),
('user5', 'password5');
('jmsanz2', 'password6');

-- Crea la tabla posts
CREATE TABLE IF NOT EXISTS posts (
    id INT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL,
    autor VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    FOREIGN KEY (autor) REFERENCES users(username)
);

INSERT INTO posts (id, titulo, fecha, autor, contenido) VALUES
(1, 'Introducción a FastAPI', '2023-01-01', 'user1', 'FastAPI es un framework moderno y rápido para construir APIs con Python.'),
(2, 'Ventajas de usar FastAPI', '2023-01-05', 'user2', 'FastAPI ofrece muchas ventajas como la validación automática de datos y la generación de documentación.'),
(3, 'Cómo empezar con FastAPI', '2023-01-10', 'user3', 'Para empezar con FastAPI, necesitas instalarlo usando pip y crear tu primer endpoint.'),
(4, 'Autenticación en FastAPI', '2023-01-15', 'user1', 'FastAPI soporta varios métodos de autenticación como OAuth2 y JWT.'),
(5, 'Deploy de aplicaciones FastAPI', '2023-01-20', 'user2', 'Puedes desplegar aplicaciones FastAPI en varios servicios de cloud como AWS, GCP y Azure.'),
(6, 'Integración con bases de datos', '2023-01-25', 'user3', 'FastAPI se integra fácilmente con bases de datos como PostgreSQL, MySQL y MongoDB.'),
(7, 'Testing en FastAPI', '2023-01-30', 'user1', 'FastAPI facilita la creación de tests para tus endpoints usando pytest.'),
(8, 'Middleware en FastAPI', '2023-02-01', 'user2', 'Puedes usar middleware en FastAPI para añadir funcionalidades como logging y manejo de errores.'),
(9, 'WebSockets en FastAPI', '2023-02-05', 'user3', 'FastAPI soporta WebSockets para aplicaciones en tiempo real.'),
(10, 'Documentación automática', '2023-02-10', 'user1', 'FastAPI genera automáticamente documentación interactiva para tus APIs usando Swagger y ReDoc.'),
(20, 'Una prueba', '2025-01-02', 'jmsanz2', 'Un contenido a ver si se carga el nuevo elemento en la bd');


-- Crea la tabla revoked_tokens
CREATE TABLE IF NOT EXISTS tokens_revocados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(500) NOT NULL
);

INSERT INTO tokens_revocados (token) VALUES
('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTczNTgxNzU1NH0.5GqkxSSz1zV7vba8LGpZmEezLnn7TevDm3T1KrHrZh0'),
('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMiIsImV4cCI6MTczNTgxOTIyMX0.5EaGo6sPoaKbZVXaJSApz87RdWzwzVqp729z7M-Mth0'),
('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTczNTgxNzYzN30.TsnWUhhPA8uTDheyWloFx40k4ZtFcY6s7n3Slpw_WIk');