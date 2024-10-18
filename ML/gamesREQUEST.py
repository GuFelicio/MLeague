import mysql.connector
from mysql.connector import errorcode
import requests
from datetime import datetime, timedelta
import time

API_KEY = 'RGAPI-a8e188a1-e9df-4fb3-bc2a-6a5c4a9fb490'
BASE_URL = 'https://americas.api.riotgames.com'

# Conexão ao MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="n45fad9x",
        database="league_data"
    )
    cursor = db.cursor()
    print("Conectado ao banco de dados MySQL com sucesso.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro de acesso: Verifique seu usuário e senha.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Erro: Banco de dados não encontrado.")
    else:
        print(err)


def get_puuids_from_db():
    try:
        cursor.execute("SELECT puuid FROM players")
        puuids = [row[0] for row in cursor.fetchall()]
        print(f"Encontrados {len(puuids)} PUUIDS no BD")
        return puuids
    except mysql.connector.Error as err:
        print("Erro ao buscar no BD: {err}")
        return []


def get_matches_by_puuid(puuid, start_time):
    url = f'{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids'
    params = {
        'startTime': start_time,
        'type': 'ranked',  #Aqui escolho o tipo de partida
        'start': 0,
        'count': 100,  # Qtd máxima de partidas por requisição
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        match_ids = response.json()
        print(f"{len(match_ids)} Partidas encontradas para o jogador: {puuid}")
        return match_ids
    else:
        print(f"Erro ao buscar partidas do(a): {puuid}! {response.status_code} - {response.text}")
        return []


def armazenar_detalhes_partida(match_id, puuid):
    url = f'{BASE_URL}/lol/match/v5/matches/{match_id}?api_key={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        match_data = response.json()
        try:
            # Extração de dados relevantes da partida
            cursor.execute("""
                   INSERT INTO matches (match_id, puuid, game_duration, game_creation, game_mode, champion_id, kills, deaths, assists, win)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                   game_duration=VALUES(game_duration), game_creation=VALUES(game_creation), game_mode=VALUES(game_mode),
                   champion_id=VALUES(champion_id), kills=VALUES(kills), deaths=VALUES(deaths), assists=VALUES(assists), win=VALUES(win)
               """, (
                match_id,
                puuid,
                match_data['info']['gameDuration'],
                match_data['info']['gameCreation'],
                match_data['info']['gameMode'],
                match_data['info']['participants'][0]['championId'],
                match_data['info']['participants'][0]['kills'],
                match_data['info']['participants'][0]['deaths'],
                match_data['info']['participants'][0]['assists'],
                match_data['info']['participants'][0]['win']
            ))
            db.commit()
            print(f"Detalhes da partida {match_id} armazenados com sucesso.")
        except mysql.connector.Error as err:
            print(f"Erro ao armazenar detalhes da partida {match_id}: {err}")
    else:
        print(f"Erro ao obter detalhes da partida {match_id}: {response.status_code} - {response.text}")


def main():
    start_time = int((datetime.now() - timedelta(days=360)).timestamp())

    puuids = get_puuids_from_db()

    request_count = 0
    start_time_intervalo: float = time.time()

    for puuid in puuids:
        match_ids = get_matches_by_puuid(puuid, start_time)
        for match_id in match_ids:
            armazenar_detalhes_partida(match_id, puuid)
            request_count += 1

            # Controle de requisições
            if request_count >= 20:
                elapsed_time = time.time() - start_time_intervalo
                if elapsed_time < 1:
                    time.sleep(1 - elapsed_time)  # Espera até completar 1 segundo para resetar o limite
                request_count = 0
                start_time_interval = time.time()
            time.sleep(1)  # Pausa para respeitar o limite de 100 requisições a cada 2 minutos


if __name__ == '__main__':
    main()
