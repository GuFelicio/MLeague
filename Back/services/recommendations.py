import joblib
from services.riot_api import fetch_data_periodically
from services.dataTRANS2 import transform_game_data  
import pandas as pd
import asyncio

# Carregar o modelo de Machine Learning treinado
model = joblib.load("path_para_o_modelo/best_model(2).pkl")  
scaler = joblib.load("path_para_o_scaler/scaler.pkl")  

# Função para processar dados de jogo e realizar predições
def process_game_data(game_data, puuid):
    data = transform_game_data(game_data, puuid)  
    if data.empty:
        return

    # Normalizar os dados para o modelo
    data_scaled = scaler.transform(data)

    # Fazer a previsão com o modelo de Machine Learning
    predictions = model.predict(data_scaled)

    # Converter as previsões em recomendações
    recommendations = convert_predictions_to_recommendations(predictions)
    print(recommendations)  # Aqui você pode enviar para o frontend ou salvar as recomendações

# Função para converter previsões em recomendações legíveis
def convert_predictions_to_recommendations(predictions):
    recommendations = []
    for prediction in predictions:
        if prediction == 1:
            recommendations.append("Ação recomendada: Atacar o inimigo!")
        elif prediction == 2:
            recommendations.append("Ação recomendada: Recuar e farmar!")
        
    return recommendations
