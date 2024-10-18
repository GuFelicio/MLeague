import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Função para transformar os dados do jogo em tempo real
def transform_game_data(game_data, puuid):
    # Vamos extrair os dados relevantes do jogador com base no PUUID
    player_data = next((p for p in game_data['participants'] if p['puuid'] == puuid), None)
    if not player_data:
        return pd.DataFrame()  # Retorna DataFrame vazio se não encontrar o jogador

    # Dados numéricos e categóricos que queremos extrair
    numerical_features = ['kills', 'deaths', 'assists', 'totalDamageDealtToChampions',
                          'goldEarned', 'visionScore', 'totalMinionsKilled', 'champLevel']
    
    categorical_features = ['teamId', 'championId']

    # Extrair os dados numéricos e categóricos do jogador
    data = {**{k: player_data.get(k, 0) for k in numerical_features},
            **{k: player_data.get(k, 0) for k in categorical_features}}

    # Criar DataFrame com os dados extraídos
    data_df = pd.DataFrame([data])

    # Aplicar transformação numérica (StandardScaler)
    num_transformer = StandardScaler()
    data_num_transformed = num_transformer.fit_transform(data_df[numerical_features])

    # Aplicar transformação categórica (OneHotEncoder)
    cat_transformer = OneHotEncoder(handle_unknown='ignore', drop='first')
    data_cat_transformed = cat_transformer.fit_transform(data_df[categorical_features])

    # Combinar dados numéricos e categóricos transformados em um DataFrame
    transformed_data = pd.concat([pd.DataFrame(data_num_transformed, columns=numerical_features),
                                  pd.DataFrame(data_cat_transformed.toarray(), columns=cat_transformer.get_feature_names_out(categorical_features))],
                                 axis=1)

    return transformed_data
