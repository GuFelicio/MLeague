import pandas as pd

# Caminho do arquivo CSV gerado anteriormente
data_path = r".\data\CSV\match_details_processed.csv"
data = pd.read_csv(data_path, low_memory=False)

# Função para determinar o resultado do jogador com base nos dados processados
def get_player_result(row):
    return 'Win' if row['participant_win'] == True else 'Loss'

# Aplicar a função na coluna 'participant_win' para criar uma nova coluna 'gameResult'
data['gameResult'] = data.apply(get_player_result, axis=1)

# Verificar se a coluna game_gameDuration já existe e se não, criá-la
if 'game_gameDuration' not in data.columns:
    if 'gameDuration' in data.columns:
        data['game_gameDuration'] = data['gameDuration']
    else:
        print("A duração do jogo não foi encontrada no arquivo CSV.")
        data['game_gameDuration'] = None  # Definir como None se não encontrar

# Verificar as primeiras linhas para confirmar as colunas adicionadas
print(data[['participant_summonerName', 'gameResult', 'game_gameDuration']].head())

# Salvar os dados transformados em um novo arquivo CSV
output_path = r".\data\CSV\match_details_results.csv"
data.to_csv(output_path, index=False)
print(f"Dados com resultados e duração do jogo armazenados em {output_path}")
