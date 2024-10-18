import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from hyperopt import hp, tpe, fmin, STATUS_OK, Trials
from tqdm import tqdm  # Biblioteca para barra de progresso
import joblib
import numpy as np

# Carregar os dados
data = pd.read_csv(r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_transformed.csv")

# Feature Engineering: criar novas features
data['kill_death_ratio'] = data['participant_kills'] / (data['participant_deaths'] + 1)
data['assist_death_ratio'] = data['participant_assists'] / (data['participant_deaths'] + 1)
data['gold_per_min'] = data['participant_goldEarned'] / data['game_gameDuration']

# Verificar o balanceamento das classes
print("Distribuição de 'gameResult':")
print(data['gameResult'].value_counts())

# Definir colunas numéricas
numerical_features = ['participant_kills', 'participant_deaths', 'participant_assists',
                      'participant_totalDamageDealtToChampions', 'participant_goldEarned',
                      'participant_visionScore', 'participant_totalMinionsKilled', 'game_gameDuration',
                      'kill_death_ratio', 'assist_death_ratio', 'gold_per_min']

# Amostrar 30% dos dados para reduzir o uso de memória
data_sample = data.sample(frac=0.3, random_state=42)

# Codificar 'gameResult'
label_encoder = LabelEncoder()
data_sample['gameResult'] = label_encoder.fit_transform(data_sample['gameResult'])

# Definir as colunas de entrada e saída
X = data_sample.drop(columns=['gameResult'])
y = data_sample['gameResult']

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline de pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features)
    ], remainder='passthrough')

# Espaço de busca de hiperparâmetros para o SVM
param_space = {
    'classifier__C': hp.uniform('classifier__C', 0.1, 100),  # Controle de regularização
    'classifier__kernel': hp.choice('classifier__kernel', ['linear', 'rbf', 'poly', 'sigmoid']),  # Diferentes kernels
    'classifier__gamma': hp.choice('classifier__gamma', ['scale', 'auto']),  # Controle da influência
    'classifier__degree': hp.choice('classifier__degree', [2, 3, 4, 5])  # Apenas para 'poly' kernel
}

# Função objetivo para Hyperopt com validação cruzada
def objective(params):
    # Criar o pipeline do SVM
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', SVC(random_state=42))])
    
    # Aplicar os parâmetros ao pipeline
    pipeline.set_params(**params)
    
    # Realizar validação cruzada
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
    
    mean_accuracy = scores.mean()
    tqdm.write(f"Acurácia média do SVM: {mean_accuracy:.2f}")
    
    return {'loss': -mean_accuracy, 'status': STATUS_OK}

# Usar Hyperopt para otimização bayesiana
trials = Trials()

# Definir o número de avaliações (max_evals)
max_evals = 50

# Iniciar a barra de progresso
with tqdm(total=max_evals, desc="Otimização de Hiperparâmetros", unit="iter") as pbar:
    best = fmin(fn=objective,
                space=param_space,
                algo=tpe.suggest,
                max_evals=max_evals,  # Número de avaliações
                trials=trials,
                verbose=1,
                show_progressbar=False)
    pbar.update(1)  # Atualiza a barra de progresso a cada iteração

# Configurar o pipeline com os melhores parâmetros
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', SVC(random_state=42))])
pipeline.set_params(**best)
pipeline.fit(X_train, y_train)

# Avaliar o modelo final
y_pred = pipeline.predict(X_test)
final_accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

# Exibir os resultados finais
print(f"\nResultados finais do SVM:")
print(f"Acurácia: {final_accuracy:.2f}, AUC-ROC: {auc:.2f}, Precisão: {precision:.2f}, Recall: {recall:.2f}")

# Salvar o modelo treinado
joblib.dump(pipeline, 'best_svm_model_fine_tuned.pkl')
