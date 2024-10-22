import requests
import json
import asyncio
from datetime import datetime

# Substitua pela sua chave de API da Riot
API_KEY = "RGAPI-a9cc00ac-f232-42b6-8cad-5dc9c4228eb0"

# Função para capturar os dados da partida ativa usando o PUUID (API v5)
def get_live_game_data_by_puuid(puuid):
    """Captura os dados da partida ativa usando o PUUID."""
    url = f"https://br1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
    
    headers = {
        "X-Riot-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    print(f"Status da resposta (live game): {response.status_code}")
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

# Função para salvar os dados capturados em um arquivo JSON
def save_game_data(live_game_data, filename="game_data_complete.json", interval_number=0):
    """Salva os dados da partida em um arquivo JSON para análise posterior."""
    try:
        with open(filename, 'a') as file:
            # Adicionar marcador de intervalo
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            interval_marker = {
                "interval": interval_number,
                "timestamp": timestamp,
                "message": f"Nova requisição capturada no intervalo {interval_number}"
            }
            # Salvar o marcador no arquivo
            json.dump(interval_marker, file, indent=4)
            file.write("\n")

            # Salvar os dados capturados da partida ativa
            json.dump({"live_game_data": live_game_data}, file, indent=4)
            file.write("\n")

        print(f"Dados da partida salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

# Função para capturar os dados do jogo continuamente até o fim da partida
async def capture_game_data(puuid):
    """Captura dados do jogo a cada intervalo até o fim da partida."""
    interval_number = 1
    while True:
        live_game_data = get_live_game_data_by_puuid(puuid)
        
        if live_game_data is None:
            print("Nenhuma partida ativa encontrada ou a partida terminou.")
            break

        # Salvar os dados capturados em um arquivo JSON, com o número do intervalo
        save_game_data(live_game_data, interval_number=interval_number)

        # Incrementar o contador de intervalos
        interval_number += 1

        # Definir um intervalo para a próxima captura (ex: 30 segundos)
        await asyncio.sleep(30)

# Função principal para capturar e armazenar dados da partida
async def main():
    puuid = input("Digite o PUUID do jogador: ")
    print("Capturando dados da partida... pressione Ctrl+C para parar.")
    try:
        await capture_game_data(puuid)
    except KeyboardInterrupt:
        print("Captura de dados interrompida pelo usuário.")

# Executa o script
if __name__ == "__main__":
    asyncio.run(main())
