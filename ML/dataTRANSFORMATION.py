import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

# Carregar os dados limpos do CSV
data_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_results.csv"  # Arquivo gerado no passo anterior
data = pd.read_csv(data_path, low_memory=False)

# Exibir todas as colunas disponíveis no DataFrame
print("Colunas disponíveis:", data.columns.tolist())

# Verificar se 'game_gameDuration' está disponível no DataFrame
if 'game_gameDuration' not in data.columns:
    print("A coluna 'game_gameDuration' não está presente no DataFrame.")
else:
    print("Coluna 'game_gameDuration' presente no DataFrame.")

# Criar a coluna 'gameResult' com base no campo 'participant_win'
data['gameResult'] = data['participant_win'].apply(lambda x: 'Win' if x else 'Loss')

# Verificar se 'gameResult' foi corretamente preenchido
print(data['gameResult'].value_counts())

# Separar a coluna 'gameResult' (variável alvo)
target = data['gameResult']
data = data.drop(columns=['gameResult'])  # Remover a coluna alvo dos dados

# Definir as colunas categóricas e numéricas baseadas nas colunas disponíveis
categorical_features = ['participant_summonerName', 'participant_championName', 'participant_role', 'participant_teamPosition']
numerical_features = ['participant_kills', 'participant_deaths', 'participant_assists', 'participant_totalDamageDealtToChampions',
                      'participant_goldEarned', 'participant_visionScore', 'participant_totalMinionsKilled', 'game_gameDuration']

# Verifique e trate valores inválidos nas colunas numéricas
for feature in numerical_features:
    if feature in data.columns:
        data[feature] = pd.to_numeric(data[feature], errors='coerce')  # Forçar a conversão para numérico
        data[feature] = data[feature].fillna(0)  # Substituir valores NaN por 0

# Verificar se os dados numéricos e categóricos estão corretos
print(f"Colunas categóricas: {categorical_features}")
print(f"Colunas numéricas: {numerical_features}")

# Transformação das colunas numéricas
print("Iniciando transformação numérica...")
num_transformer = StandardScaler()
data_num_transformed = num_transformer.fit_transform(data[numerical_features])

# Verificar a transformação numérica
print(f"Forma dos dados numéricos transformados: {data_num_transformed.shape}")

# Transformação das colunas categóricas
print("Iniciando transformação categórica...")
cat_transformer = OneHotEncoder(handle_unknown='ignore', drop='first')
data_cat_transformed = cat_transformer.fit_transform(data[categorical_features])

# Verificar a transformação categórica
print(f"Forma dos dados categóricos transformados: {data_cat_transformed.shape}")

# Juntar as duas transformações
data_transformed = pd.concat([pd.DataFrame(data_num_transformed, columns=numerical_features),
                              pd.DataFrame(data_cat_transformed.toarray(),
                                           columns=cat_transformer.get_feature_names_out(categorical_features))],
                             axis=1)

# Adicionar de volta a variável alvo (gameResult)
data_transformed['gameResult'] = target.values  # Corrigir a adição da variável alvo

# Verificar se as formas das colunas estão corretas
print(f"Forma dos dados transformados: {data_transformed.shape}")
print(f"Número de colunas transformadas: {data_transformed.shape[1]}")

# Salvar os dados transformados
output_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_transformed.csv"
data_transformed.to_csv(output_path, index=False)
print(f"Dados transformados armazenados em {output_path}")
