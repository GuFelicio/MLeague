import requests
import joblib
import asyncio
import requests
from urllib.parse import quote
from services.riot_api import get_current_game_data
from services.dataTRANS2 import transform_game_data
from services.recommendations import convert_predictions_to_recommendations

# Carregar o modelo e o scaler
model = joblib.load("D:/ProjetoMLeague/MLeague/data/ML/best_model(NOVO).pkl")
scaler = joblib.load("D:/ProjetoMLeague/MLeague/data/ML/scaler(NOVO).pkl")

# Substitua pela sua chave de API da Riot
API_KEY = "RGAPI-a9cc00ac-f232-42b6-8cad-5dc9c4228eb0"
BASE_URL = "https://americas.api.riotgames.com"

# Função para obter o PUUID através do Riot ID (gameName e tagLine)
def get_puuid_by_riot_id(game_name, tag_line):
    """Obter o PUUID usando o Riot ID (gameName e tagLine)."""
    encoded_game_name = quote(game_name)
    encoded_tag_line = quote(tag_line)
    
    url = f'{BASE_URL}/riot/account/v1/accounts/by-riot-id/{encoded_game_name}/{encoded_tag_line}?api_key={API_KEY}'

    headers = {
        "X-Riot-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        puuid = response.json().get('puuid')
        if puuid:
            print(f"PUUID obtido com sucesso: {game_name}#{tag_line} -> {puuid}")
            return puuid
    elif response.status_code == 404:
        print(f"Erro 404: Riot ID {game_name}#{tag_line} não encontrado.")
    elif response.status_code == 403:
        print(f"Erro 403: Chave de API inválida ou expirada.")
    else:
        print(f"Erro {response.status_code}: {response.json().get('status', {}).get('message', 'Erro desconhecido')}")
    
    return None

# Função de login atualizada para capturar o Riot ID
def login():
    """Capturar o PUUID diretamente pelo Riot ID (gameName e tagLine)."""
    riot_id = input("Digite o Riot ID no formato (ex: gfelicio#gugu): ")
    
    if "#" in riot_id:
        game_name, tag_line = riot_id.split("#", 1)
        puuid = get_puuid_by_riot_id(game_name, tag_line)
        
        if puuid:
            return puuid
        else:
            print("Erro ao capturar o PUUID.")
            return None
    else:
        print("Formato do Riot ID inválido. Use o formato gameName#tagLine.")
        return None

# Função para ajustar os nomes das features para corresponder aos usados no treinamento
def adjust_feature_names(data):
    """Renomeia as colunas dos dados ao vivo para corresponder aos nomes usados no treinamento."""
    rename_map = {
        'kills': 'participant_kills',
        'deaths': 'participant_deaths',
        'assists': 'participant_assists',
        'totalDamageDealtToChampions': 'participant_totalDamageDealtToChampions',
        'goldEarned': 'participant_goldEarned',
        'visionScore': 'participant_visionScore',
        'totalMinionsKilled': 'participant_totalMinionsKilled',
        'gameDuration': 'game_gameDuration',
        'champLevel': 'participant_champLevel',
        'teamPosition': 'participant_teamPosition',
        'summonerName': 'participant_summonerName',
        'championName': 'participant_championName',
    }
    
    return data.rename(columns=rename_map)

# Função para garantir que as features necessárias estejam presentes
def ensure_features(data):
    """Garante que todas as features usadas no treinamento estejam presentes e remove features desnecessárias."""
    # Definir as features usadas no treinamento
    required_features = [
        'participant_kills', 'participant_deaths', 'participant_assists', 
        'participant_totalDamageDealtToChampions', 'participant_goldEarned',
        'participant_visionScore', 'participant_totalMinionsKilled', 
        'game_gameDuration', 'participant_champLevel', 'participant_teamPosition',
        'participant_summonerName', 'participant_championName',
        'participant_championClass_Fighter', 'participant_championClass_Mage',
        'participant_championClass_Marksman', 'participant_championClass_Support'
    ]
    
    # Adicionar valores padrão para features faltantes
    for feature in required_features:
        if feature not in data.columns:
            data[feature] = 0  # Definir um valor padrão, ajuste conforme necessário
    
    # Remover features desnecessárias
    data = data[required_features]
    
    return data

# Função para capturar os dados do jogo ativo usando o PUUID
def get_live_game_data_by_puuid(puuid):
    """Captura os dados da partida ativa usando o PUUID."""
    url = f"https://br1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
    
    headers = {
        "X-Riot-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    print(f"Status da resposta: {response.status_code}")
    if response.status_code == 200:
        game_data = response.json()
        return game_data  # Retorna os dados da partida se encontrados
    elif response.status_code == 404:
        print("Nenhuma partida ativa encontrada para esse PUUID.")
    elif response.status_code == 403:
        print("Erro 403: Chave de API inválida ou expirada.")
    elif response.status_code == 429:
        print("Erro 429: Limite de requisições excedido.")
    else:
        print(f"Erro ao capturar dados do jogo: {response.status_code}")
    
    return None

# Função para capturar os dados do jogo e gerar recomendações
async def run_game_recommendations(puuid):
    """Função que faz a captura dos dados da partida ativa e gera recomendações em tempo real."""
    while True:
        # Capturar dados do jogo em andamento
        game_data = get_live_game_data_by_puuid(puuid)
        if game_data is None:
            print("Nenhuma partida ativa encontrada para esse PUUID.")
            return

        # Transformar os dados do jogo
        transformed_data = transform_game_data(game_data, puuid)

        # Ajustar os nomes das features para corresponder ao treinamento
        transformed_data = adjust_feature_names(transformed_data)

        # Garantir que todas as features necessárias estejam presentes
        transformed_data = ensure_features(transformed_data)

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
    puuid = login()  # Login e captura do PUUID
    if puuid:
        await run_game_recommendations(puuid)  # Executa as recomendações se o PUUID for válido

# Rodar o script
if __name__ == "__main__":
    asyncio.run(main())