from fastapi import APIRouter
from Back.services.recommendations import start_real_time_recommendations
import asyncio

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.post("/start")
async def start_recommendations(puuid: str):
    # Iniciar as recomendações em tempo real para o PUUID fornecido
    asyncio.create_task(start_real_time_recommendations(puuid))
    return {"message": "Iniciando recomendações em tempo real"}
