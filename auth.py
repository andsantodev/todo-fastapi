from fastapi import Header, HTTPException, status
import os

TOKEN_ESPERADO = os.getenv("TOKEN", "meu-token-secreto")

def verificar_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Formato de token inválido")
    
    token = authorization.split(" ")[1]
    if token != TOKEN_ESPERADO:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")