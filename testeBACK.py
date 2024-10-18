import requests
import joblib
import asyncio
import requests
from Back.services.riot_api import get_current_game_data
from Back.services.dataTRANS2 import transform_game_data
from Back.services.recommendations import convert_predictions_to_recommendations

# Carregar o modelo e o scaler
model = joblib.load("D:/ProjetoMLeague/MLeague/data/ML/best_model(NOVO).pkl")
scaler = joblib.load("D:/ProjetoMLeague/MLeague/data/ML/scaler(NOVO).pkl")


# Substitua pela sua chave de API da Riot
API_KEY = "API RIOT"

# Função para obter o PUUID a partir do nome de invocador usando a API da Riot
def get_puuid_by_summoner_name(summoner_name, region):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data["puuid"]  # Retorna o PUUID do jogador
    else:
        print(f"Erro: {response.status_code}")
        return None

# Função de login atualizada
def login():
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")
    
    summoner_name = input("Digite seu nome de invocador: ")  # Capturar o nome de invocador
    region = input("Digite a # (ex: br1): ")  # Capturar a região do jogador (ex: br1, na1, etc.)
    
    # Obter o PUUID usando o nome de invocador e a API da Riot
    puuid = get_puuid_by_summoner_name(summoner_name, region)
    
    if puuid:
        print(f"PUUID capturado: {puuid}")
        return puuid
    else:
        print("Erro ao capturar o PUUID.")
        return None


# Função para capturar os dados do jogo e gerar recomendações
async def run_game_recommendations(puuid):
    while True:
        # Capturar dados do jogo em andamento
        game_data = await get_current_game_data(puuid)
        if game_data is None:
            print("Nenhuma partida ativa encontrada para esse PUUID.")
            return

        # Transformar os dados do jogo
        transformed_data = transform_game_data(game_data, puuid)
        if transformed_data.empty:
            print("Erro na transformação dos dados.")
            return

        # Normalizar os dados transformados
        data_scaled = scaler.transform(transformed_data)

        # Fazer predições com o modelo de Machine Learning
        predictions = model.predict(data_scaled)

        # Converter predições em recomendações
        recommendations = convert_predictions_to_recommendations(predictions)

        # Exibir recomendações
        print("Recomendações durante o jogo: ")
        for rec in recommendations:
            print(f"- {rec}")

        # Definir o intervalo para a próxima requisição (simulando tempo real)
        await asyncio.sleep(10)  

# Função principal
async def main():
    puuid = login()  
    await run_game_recommendations(puuid)  

# Rodar o script
if __name__ == "__main__":
    asyncio.run(main())
