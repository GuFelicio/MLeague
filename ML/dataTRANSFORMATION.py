import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np


data_path = r".\data\CSV\match_details_results.csv"  
data = pd.read_csv(data_path, low_memory=False)


print("Colunas disponíveis:", data.columns.tolist())


if 'game_gameDuration' not in data.columns:
    print("A coluna 'game_gameDuration' não está presente no DataFrame.")
else:
    print("Coluna 'game_gameDuration' presente no DataFrame.")


data['gameResult'] = data['participant_win'].apply(lambda x: 'Win' if x else 'Loss')


print(data['gameResult'].value_counts())


target = data['gameResult']
data = data.drop(columns=['gameResult'])  


categorical_features = ['participant_summonerName', 'participant_championName', 'participant_role', 'participant_teamPosition']
numerical_features = ['participant_kills', 'participant_deaths', 'participant_assists', 'participant_totalDamageDealtToChampions',
                      'participant_goldEarned', 'participant_visionScore', 'participant_totalMinionsKilled', 'game_gameDuration']


for feature in numerical_features:
    if feature in data.columns:
        data[feature] = pd.to_numeric(data[feature], errors='coerce')  
        data[feature] = data[feature].fillna(0)  


print(f"Colunas categóricas: {categorical_features}")
print(f"Colunas numéricas: {numerical_features}")


print("Iniciando transformação numérica...")
num_transformer = StandardScaler()
data_num_transformed = num_transformer.fit_transform(data[numerical_features])


print(f"Forma dos dados numéricos transformados: {data_num_transformed.shape}")


print("Iniciando transformação categórica...")
cat_transformer = OneHotEncoder(handle_unknown='ignore', drop='first')
data_cat_transformed = cat_transformer.fit_transform(data[categorical_features])


print(f"Forma dos dados categóricos transformados: {data_cat_transformed.shape}")


data_transformed = pd.concat([pd.DataFrame(data_num_transformed, columns=numerical_features),
                              pd.DataFrame(data_cat_transformed.toarray(),
                                           columns=cat_transformer.get_feature_names_out(categorical_features))],
                             axis=1)


data_transformed['gameResult'] = target.values 


print(f"Forma dos dados transformados: {data_transformed.shape}")
print(f"Número de colunas transformadas: {data_transformed.shape[1]}")

# Salvar os dados transformados
output_path = r".\data\CSV\match_details_transformed.csv"
data_transformed.to_csv(output_path, index=False)
print(f"Dados transformados armazenados em {output_path}")
