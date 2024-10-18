import pandas as pd
import os
import json

# Caminho da pasta onde os arquivos JSON estão armazenados
LOCAL_STORAGE_PATH = r"D:\NBHelp\noobHelp\venv\data\jSON"

# Caminho do arquivo CSV de classes de campeões
champion_classes_csv = r"D:\NBHelp\noobHelp\venv\data\CSV\champion_classes.csv"

# Carregar o CSV com as classes dos campeões
champions_df = pd.read_csv(champion_classes_csv)

# Lista para armazenar todos os DataFrames
dataframes = []

# Função para obter a classe do campeão a partir do nome
def get_champion_class(champion_name):
    result = champions_df[champions_df["Champion"] == champion_name]["Class"]
    return result.values[0] if not result.empty else "Unknown"

# Função para carregar e processar dados de partidas de JSON
def load_match_data(file_path):
    # Abrir o arquivo JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data_json = json.load(file)

        # Normalizar participantes
        participants_df = pd.json_normalize(data_json['info']['participants'])
        participants_df.columns = ['participant_' + col for col in participants_df.columns]

        # Adicionar classe do campeão usando o CSV
        participants_df['participant_championClass'] = participants_df['participant_championName'].apply(get_champion_class)

        # Adicionar os itens comprados (até 7 slots)
        for i in range(7):
            participants_df[f'participant_item{i}'] = participants_df[f'participant_item{i}']

        # Adicionar runas e perks
        participants_df['participant_primaryRune'] = participants_df['participant_perks.styles'].apply(
            lambda x: x[0]['selections'][0]['perk'] if x and len(x[0]['selections']) > 0 else None
        )
        participants_df['participant_secondaryRune'] = participants_df['participant_perks.styles'].apply(
            lambda x: x[1]['selections'][0]['perk'] if x and len(x[1]['selections']) > 0 else None
        )

        # Normalizar os times
        teams_df = pd.json_normalize(data_json['info']['teams'])
        teams_df.columns = ['team_' + col for col in teams_df.columns]

        # Adicionar a duração do jogo
        game_duration = data_json['info'].get('gameDuration', None)
        participants_df['game_gameDuration'] = game_duration

        # Verificar se existe algum time com 'win' igual a True
        if not teams_df[teams_df['team_win'] == True].empty:
            winning_team_id = teams_df.loc[teams_df['team_win'] == True, 'team_teamId'].values[0]
            participants_df['gameResult'] = participants_df.apply(
                lambda row: 'Win' if row['participant_teamId'] == winning_team_id else 'Loss', axis=1
            )
        else:
            participants_df['gameResult'] = 'Unknown'

        # Retornar o DataFrame processado
        return participants_df

# Carregar todos os arquivos JSON na pasta especificada
for filename in os.listdir(LOCAL_STORAGE_PATH):
    if filename.endswith('.json'):
        file_path = os.path.join(LOCAL_STORAGE_PATH, filename)
        df = load_match_data(file_path)
        dataframes.append(df)

# Concatenar todos os DataFrames em um único DataFrame
data = pd.concat(dataframes, ignore_index=True)

# Salvar os dados tratados em CSV
output_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_processed(2).csv"
data.to_csv(output_path, index=False)

print(f"Dados processados armazenados em {output_path}")
