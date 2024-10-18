import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
from tqdm import tqdm  # Importar a barra de progresso
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier

# Carregar os dados transformados do CSV
data_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_transformed(2).csv"
data = pd.read_csv(data_path)

# Codificar 'gameResult' de categórico ('Win', 'Loss') para numérico (1, 0)
label_encoder = LabelEncoder()
data['gameResult'] = label_encoder.fit_transform(data['gameResult'])

# Definir as colunas de entrada (X) e a coluna de saída (y)
X = data.drop(columns=['gameResult'])  # Remover a coluna alvo
y = data['gameResult']

# Escalar os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# --------------------------------------------
# Barra de Progresso para o Tuning de Hiperparâmetros
# --------------------------------------------

# Função para realizar tuning com barra de progresso
def perform_grid_search(model, param_grid, X_train, y_train, model_name):
    print(f"Iniciando tuning para {model_name}...")
    grid_search = GridSearchCV(model, param_grid, cv=3)
    for _ in tqdm(grid_search.fit(X_train, y_train), desc=f"Tuning {model_name}"):
        pass  # A barra de progresso acompanhará o processo
    print(f"Melhores parâmetros para {model_name}: {grid_search.best_params_}")
    return grid_search.best_estimator_

# Parâmetros e tuning do Random Forest
param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10]
}
best_rf = perform_grid_search(RandomForestClassifier(random_state=42), param_grid_rf, X_train, y_train, "Random Forest")

# Parâmetros e tuning do Gradient Boosting
param_grid_gb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}
best_gb = perform_grid_search(GradientBoostingClassifier(random_state=42), param_grid_gb, X_train, y_train, "Gradient Boosting")

# Parâmetros e tuning do XGBoost
param_grid_xgb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}
best_xgb = perform_grid_search(XGBClassifier(random_state=42), param_grid_xgb, X_train, y_train, "XGBoost")

# Parâmetros e tuning do LightGBM
param_grid_lgbm = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'num_leaves': [31, 50, 100]
}
best_lgbm = perform_grid_search(LGBMClassifier(random_state=42), param_grid_lgbm, X_train, y_train, "LightGBM")

# --------------------------------------------
# Treinar o Stacking com os Modelos Ajustados
# --------------------------------------------
print("Treinando o modelo Stacking...")

# Definir os modelos de base com os hiperparâmetros ajustados
base_models = [
    ('rf', best_rf),
    ('gb', best_gb),
    ('xgb', best_xgb),
    ('lgbm', best_lgbm)
]

# Meta-modelo: Logistic Regression
meta_model = LogisticRegression()

# Criar o StackingClassifier
stacking_model = StackingClassifier(estimators=base_models, final_estimator=meta_model)

# Treinar o Stacking com barra de progresso
for _ in tqdm(stacking_model.fit(X_train, y_train), desc="Treinando Stacking Model"):
    pass  # A barra de progresso acompanhará o treinamento

# Prever e avaliar o modelo de stacking
y_pred_stack = stacking_model.predict(X_test)
accuracy_stack = accuracy_score(y_test, y_pred_stack)
print(f"Acurácia do modelo Stacking: {accuracy_stack:.2f}")

# Salvar o modelo ajustado
model_path_stacking = r"D:\NBHelp\noobHelp\venv\data\ML\best_stacking_model(3).pkl"
joblib.dump(stacking_model, model_path_stacking)

print(f"Modelo Stacking ajustado salvo em {model_path_stacking}")
