from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Back.schemas.user_schemas import LoginSchema
from Back.services.auth import create_user, login_user
from Back.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
def register(credentials: LoginSchema, db: Session = Depends(get_db)):
    user = create_user(db, credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Erro ao registrar o usuário.")
    return {"message": "Usuário registrado com sucesso!"}

@router.post("/login")
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    token = login_user(db, credentials)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    return {"access_token": token, "token_type": "bearer"}
