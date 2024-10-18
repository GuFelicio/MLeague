import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Carregar os dados transformados do CSV
data_path = r".\data\CSV\match_details_transformed.csv"
data = pd.read_csv(data_path)

# Verificar todas as colunas disponíveis no DataFrame
print("Colunas disponíveis:", data.columns.tolist())

# Verificar se o 'gameResult' existe
if 'gameResult' not in data.columns:
    raise KeyError("'gameResult' não encontrado no DataFrame. Verifique se o nome da coluna está correto.")

# Codificar 'gameResult' de categórico ('Win', 'Loss') para numérico (1, 0)
label_encoder = LabelEncoder()
data['gameResult'] = label_encoder.fit_transform(data['gameResult'])  # Transforma Win -> 1 e Loss -> 0

# Salvar o LabelEncoder para uso posterior
label_encoder_path = r"D:\NBHelp\noobHelp\venv\data\ML\label_encoder.pkl"
joblib.dump(label_encoder, label_encoder_path)

# Verificar a distribuição de classes no dataset completo
class_distribution = data['gameResult'].value_counts()
print("Distribuição das classes no dataset completo:")
print(class_distribution)

# Definir as colunas de entrada (X) e a coluna de saída (y)
X = data.drop(columns=['gameResult'])  # Remover a coluna alvo
y = data['gameResult']  # Coluna alvo para prever

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verificar a distribuição de classes no conjunto de treino
train_class_distribution = y_train.value_counts()
print("Distribuição das classes no conjunto de treino:")
print(train_class_distribution)

# Verifique se há pelo menos duas classes no conjunto de treino
if len(y_train.unique()) < 2:
    raise ValueError("O conjunto de treino não contém pelo menos duas classes diferentes.")

# Definir os modelos
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(random_state=42)
}

# Treinar e avaliar cada modelo
results = {}
for model_name, model in models.items():
    print(f"Treinando o modelo {model_name}...")

    # Treinar o modelo
    model.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    y_pred = model.predict(X_test)

    # Calcular as métricas
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    # Armazenar os resultados
    results[model_name] = {
        "accuracy": accuracy,
        "f1_score": f1,
        "precision": precision,
        "recall": recall
    }

    print(f"Resultados para {model_name}:")
    print(f"Acurácia: {accuracy:.2f}")
    print(f"F1 Score: {f1:.2f}")
    print(f"Precisão: {precision:.2f}")
    print(f"Recall: {recall:.2f}")

# Exibir o melhor modelo baseado na acurácia
best_model_name = max(results, key=lambda x: results[x]["accuracy"])
best_model = models[best_model_name]

print(f"Melhor modelo: {best_model_name} com acurácia de {results[best_model_name]['accuracy']:.2f}")

# Salvar o melhor modelo
model_path = r"D:\NBHelp\noobHelp\venv\data\ML\best_model.pkl"
joblib.dump(best_model, model_path)

# Salvar as colunas usadas no treinamento
columns_path = r"D:\NBHelp\noobHelp\venv\data\ML\original_columns.pkl"
joblib.dump(X.columns, columns_path)


print(f"Modelo {best_model_name} salvo em {model_path}")
