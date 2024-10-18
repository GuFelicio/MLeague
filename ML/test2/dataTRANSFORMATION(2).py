import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

# Carregar os dados limpos do CSV gerado anteriormente
data_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_results(2).csv"  
data = pd.read_csv(data_path, low_memory=False)

# Exibir todas as colunas disponíveis no DataFrame
print("Colunas disponíveis:", data.columns.tolist())

# Criar a coluna 'gameResult' com base no campo 'participant_win' (variável alvo já existente)
target = data['gameResult']

# Remover a coluna 'gameResult' dos dados, pois ela será nossa variável alvo
data = data.drop(columns=['gameResult'])

# Definir as colunas categóricas e numéricas
categorical_features = ['participant_summonerName', 'participant_championName', 'participant_role', 'participant_teamPosition', 'participant_championClass']  
numerical_features = ['participant_kills', 'participant_deaths', 'participant_assists', 'participant_totalDamageDealtToChampions', 
                      'participant_goldEarned', 'participant_visionScore', 'participant_totalMinionsKilled', 'game_gameDuration']

# Adicionar colunas numéricas para os itens comprados e as runas
numerical_features.extend([f'participant_item{i}' for i in range(7)])  # Itens comprados
numerical_features.extend(['participant_primaryRune', 'participant_secondaryRune'])  # Runas

# Verificar e tratar valores inválidos nas colunas numéricas
for feature in numerical_features:
    if feature in data.columns:
        data[feature] = pd.to_numeric(data[feature], errors='coerce')  # Converter para numérico, forçando erros para NaN
        data[feature] = data[feature].fillna(0)  # Substituir NaN por 0

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
data_transformed['gameResult'] = target.values

# Verificar se as formas das colunas estão corretas
print(f"Forma dos dados transformados: {data_transformed.shape}")
print(f"Número de colunas transformadas: {data_transformed.shape[1]}")

# Salvar os dados transformados
output_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_transformed(2).csv"
data_transformed.to_csv(output_path, index=False)
print(f"Dados transformados armazenados em {output_path}")
