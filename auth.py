# auth.py
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from funciones import load_user_data, create_jwt_token, verify_jwt_token, save_revoked_tokens, load_revoked_tokens

# Inicializar el router
router = APIRouter()

# Middleware de seguridad
security = HTTPBearer()

# Inicializar la lista de tokens revocados
revoked_tokens = load_revoked_tokens()

# Modelo para los datos de login
class LoginData(BaseModel):
    username: str
    password: str

# Endpoint para hacer logout y revocar un token
@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)  # Verifica que el token sea válido
    revoked_tokens.add(token)  # Añade el token a la lista de revocados
    save_revoked_tokens(revoked_tokens)  # Guarda la lista en el archivo
    return {"message": f"User {payload['sub']} has been logged out successfully."}

# Endpoint de login
@router.post("/login")
async def login(login_data: dict):
    users = load_user_data()
    user = next(
        (user for user in users if user["username"] == login_data["username"] and user["password"] == login_data["password"]),
        None,
    )
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Generar el token JWT
    token = create_jwt_token(login_data["username"])
    return {"access_token": token, "token_type": "bearer"}

# Endpoint protegido que requiere autenticación con JWT
@router.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    return {"message": "Access granted", "user": payload["sub"]}

