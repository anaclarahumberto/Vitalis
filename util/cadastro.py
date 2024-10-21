import os
import jwt
from datetime import datetime, timedelta

def criar_token_id(id: int) -> str:
    payload = {
        "id" : id,
        "exp": datetime.now() + timedelta(days=1)
    }
    token = jwt.encode(payload, 
        os.getenv("JWT_SECRET"),
        os.getenv("JWT_ALGORITHM"))
    return token

def validar_token_id(token: str) -> dict:
    try:
        playload = jwt.decode(token, 
            os.getenv("JWT_SECRET"),
            os.getenv("JWT_ALGORITHM"))
        print(playload)
        return playload
    except jwt.ExpiredSignatureError:
        return { "id": None, "mensagem": "Sessão expirada" }
    except jwt.InvalidTokenError:
        return { "id": None, "mensagem": "Token inválido" }
    except Exception as e:
        return { "id": None, "mensagem": f"Erro: {e}" }