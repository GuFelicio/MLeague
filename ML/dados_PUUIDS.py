import mysql.connector
from mysql.connector import errorcode
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

API_KEY = 'RGAPI-a8e188a1-e9df-4fb3-bc2a-6a5c4a9fb490'  
BASE_URL = 'https://americas.api.riotgames.com'  

# Conexão inicial ao MySQL sem especificar o banco de dados
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="n45fad9x")
    cursor = db.cursor()


    # Conectar ao banco de dados criado
    db.database = "league_data"

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro de acesso: Verifique seu usuário e senha.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Erro: Banco de dados não encontrado.")
    else:
        print(err)


def check_and_create_tables():

    databaseSCRIPT  = r'D:\NBHelp\noobHelp\venv\league_data.sql'

    """Verifica se as tabelas existem e cria, se necessário, usando o arquivo league_data.sql."""
    try:
        cursor.execute("SHOW TABLES LIKE 'players';")
        result = cursor.fetchone()
        if not result:
            print("Tabelas não encontradas. Executando script de criação de tabelas...")
            with open(databaseSCRIPT, 'r') as file:
                sql_script = file.read()
                for statement in sql_script.split(';'):
                    if statement.strip():
                        cursor.execute(statement + ';')
            db.commit()
            print("Tabelas criadas com sucesso.")
        else:
            print("Tabelas já existem no banco de dados.")
    except Exception as e:
        print(f"Erro ao executar o script SQL: {e}")


def get_top_players(region='br'):
    """Coletar nomes dos melhores jogadores de uma região específica no OP.GG."""
    url = f'https://{region}.op.gg/ranking/ladder/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao acessar o OP.GG: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Verificar os elementos que possuem o link dos jogadores
    player_elements = soup.select('a.summoner-link')

    # Extrair os nomes dos jogadores a partir do atributo href
    top_players = []
    for player in player_elements:
        href = player.get('href')
        if href and '/summoners/br/' in href:
            player_name = href.split('/summoners/br/')[1]
            top_players.append(player_name)

    if not top_players:
        print("Nenhum jogador encontrado. Verifique o seletor CSS ou a estrutura da página do OP.GG.")
    return top_players


def extract_riot_id(name):
    """Extrair o gameName e tagLine a partir do formato do nome 'NOMEDOINVOCADOR-TAG'."""
    if '-' in name:
        game_name, tag_line = name.split('-', 1)
        return game_name, tag_line
    else:
        return name, 'BR1'  # Assume 'BR1' como tag padrão se não houver


def get_puuid_by_riot_id(game_name, tag_line):
    """Obter PUUID usando o Riot ID (gameName e tagLine)."""
    encoded_game_name = quote(game_name)
    encoded_tag_line = quote(tag_line)
    url = f'{BASE_URL}/riot/account/v1/accounts/by-riot-id/{encoded_game_name}/{encoded_tag_line}?api_key={API_KEY}'

    response = requests.get(url)
    if response.status_code == 200:
        puuid = response.json().get('puuid')
        if puuid:
            print(f"Sucesso ao obter PUUID para Riot ID {game_name}#{tag_line}.")
            insert_player(game_name, tag_line, f"{game_name}#{tag_line}", puuid, 'br1')
        return puuid
    else:
        print(
            f"Erro ao obter PUUID para Riot ID {game_name}#{tag_line}: {response.status_code} - {response.json().get('status', {}).get('message', 'Unknown Error')}")
        return None


def insert_player(game_name, tag_line, riot_id, puuid, region):
    """Inserir um jogador na tabela players."""
    query = "INSERT INTO players (game_name, tag_line, riot_id, puuid, region) VALUES (%s, %s, %s, %s, %s)"
    values = (game_name, tag_line, riot_id, puuid, region)
    try:
        cursor.execute(query, values)
        db.commit()
        print(f"Jogador {game_name}#{tag_line} inserido com sucesso.")
    except mysql.connector.IntegrityError:
        print(f"Jogador {game_name}#{tag_line} já existe no banco de dados.")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir jogador {game_name}#{tag_line}: {err}")


def main():
    # Verifica se as tabelas existem e cria, se necessário
    check_and_create_tables()

    top_players = get_top_players()
    print(f"Jogadores Top Rank encontrados: {top_players}")

    for player in top_players:
        game_name, tag_line = extract_riot_id(player)
        get_puuid_by_riot_id(game_name, tag_line)
        time.sleep(1)  # Pausa para respeitar limites de requisição


if __name__ == "__main__":
    main()
