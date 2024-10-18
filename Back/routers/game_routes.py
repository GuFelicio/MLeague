from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Back.schemas.user_schemas import PUUIDSchema
from Back.models.user import User
from Back.services.auth import get_current_user  # Função para obter o usuário autenticado
from Back.database import get_db

router = APIRouter(
    prefix="/game",
    tags=["game"],
)

# Rota para atualizar o PUUID do usuário autenticado
@router.post("/update_puuid")
def update_puuid(puuid_data: PUUIDSchema, db: Session = Depends(get_db), user_authenticated: User = Depends(get_current_user)):
    # Verifica se o PUUID já está registrado para outro usuário
    user = db.query(User).filter(User.puuid == puuid_data.puuid).first()
    if user:
        raise HTTPException(status_code=400, detail="PUUID já registrado para outro usuário.")
    
    # Atualiza o PUUID do usuário autenticado
    user_authenticated.puuid = puuid_data.puuid
    db.commit()
    return {"message": "PUUID atualizado com sucesso!"}
