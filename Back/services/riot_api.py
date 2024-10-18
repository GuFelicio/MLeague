import requests
import asyncio

API_KEY = "sua_chave_api_riot"  # Substitua pela sua chave de API da Riot
REQUEST_INTERVAL = 5  # Intervalo de 5 segundos entre as requisições

# Função para obter dados do jogo atual usando o PUUID do jogador
async def get_current_game_data(puuid: str):
    url = f"https://<região>.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{puuid}?api_key={API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Retorna os dados do jogo em JSON
        elif response.status_code == 404:
            return None  # Jogador não está em uma partida ativa no momento
        else:
            return None  # Tratar erros HTTP como uma falha na conexão
    except requests.RequestException as e:
        print(f"Erro na conexão com a API da Riot: {e}")
        return None

# Função para realizar requisições repetidas e capturar dados em tempo real
async def fetch_data_periodically(puuid: str, process_data_function):
    while True:
        game_data = await get_current_game_data(puuid)
        if game_data:
            process_data_function(game_data)  # Processa os dados do jogo e faz predições
        await asyncio.sleep(REQUEST_INTERVAL)  # Espera o intervalo definido antes da próxima requisição
