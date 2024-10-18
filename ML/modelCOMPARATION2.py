import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

# Carregar os dados transformados
data_path = r"D:\ProjetoMLeague\MLeague\data\CSV\match_details_transformed(2).csv"
data = pd.read_csv(data_path)

# Função para rotular as ações recomendadas com base nos dados
def label_action(row):
    # Usar os nomes de colunas corretos conforme o arquivo dataTRANSFORMATION.py
    if row['participant_goldEarned'] > 10000:
        return 'Voltar à base e comprar itens'
    elif row['participant_kills'] > row['participant_deaths']:
        return 'Atacar o inimigo'
    elif row['participant_visionScore'] < 10:
        return 'Focar em visão e warding'
    
    # Ações relacionadas a objetivos globais (dragões, arautos, barões)
    if row['dragonKills'] > 0 and row['teamId'] == 100:
        return 'Atacar o Dragão'
    elif row['heraldKills'] > 0 and row['teamId'] == 100:
        return 'Atacar o Arauto'
    elif row['baronKills'] > 0 and row['teamId'] == 100:
        return 'Atacar o Barão'
    elif row['dragonKills'] > 0 and row['teamId'] == 200:
        return 'Contestar o Dragão'
    elif row['heraldKills'] > 0 and row['teamId'] == 200:
        return 'Contestar o Arauto'
    elif row['baronKills'] > 0 and row['teamId'] == 200:
        return 'Contestar o Barão'
    
    return 'Recuar e farmar'

# Aplicar a função de rotulação aos dados
data['recommended_action'] = data.apply(label_action, axis=1)

# Separar as features (X) da variável alvo (y)
X = data.drop(['recommended_action'], axis=1)
y = data['recommended_action']

# Selecionar apenas colunas numéricas
X_numeric = X.select_dtypes(include=[np.number])

# Normalizar as features numéricas usando StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_numeric)

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# Treinamento dos modelos
models = {
    "RandomForest": RandomForestClassifier(),
    "GradientBoosting": GradientBoostingClassifier(),
    "SVM": SVC()
}

# Avaliar cada modelo
best_model = None
best_accuracy = 0
for model_name, model in models.items():
    print(f"Treinando o modelo: {model_name}")
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred = model.predict(X_test)
    
    # Avaliar a performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do {model_name}: {accuracy}")
    print(classification_report(y_test, y_pred))
    
    # Comparar para encontrar o melhor modelo
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model

# Salvar o melhor modelo treinado e o scaler
joblib.dump(best_model, "D:/ProjetoMLeague/MLeague/data/ML/best_model(NOVO).pkl")
joblib.dump(scaler, "D:/ProjetoMLeague/MLeague/data/ML/scaler(NOVO).pkl")

print(f"Melhor modelo: {best_model.__class__.__name__} com acurácia: {best_accuracy}")
