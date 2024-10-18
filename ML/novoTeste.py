import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
import joblib
from tqdm import tqdm  # Importando a barra de progresso

#Carregar os dados
data = pd.read_csv(r".\data\CSV\match_details_transformed.csv")

#Feature Engineering: criar novas features
data['kill_death_ratio'] = data['participant_kills'] / (data['participant_deaths'] + 1)
data['assist_death_ratio'] = data['participant_assists'] / (data['participant_deaths'] + 1)
data['gold_per_min'] = data['participant_goldEarned'] / data['game_gameDuration']

#Definir colunas numéricas
numerical_features = ['participant_kills', 'participant_deaths', 'participant_assists',
                      'participant_totalDamageDealtToChampions', 'participant_goldEarned',
                      'participant_visionScore', 'participant_totalMinionsKilled', 'game_gameDuration',
                      'kill_death_ratio', 'assist_death_ratio', 'gold_per_min']

#Usar 30% dos dados para reduzir o uso de memória
data_sample = data.sample(frac=0.3, random_state=42)

#Codificar 'gameResult'
data_sample['gameResult'] = data_sample['gameResult'].map({'Win': 1, 'Loss': 0})

#Definir as colunas de entrada e saída
X = data_sample.drop(columns=['gameResult'])
y = data_sample['gameResult']

#Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Pipeline de pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features)
    ], remainder='passthrough')

#Definir os modelos base
rf = RandomForestClassifier(random_state=42)
gb = GradientBoostingClassifier(random_state=42)
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
svm = SVC(probability=True, random_state=42)

# Definir o metamodelo para o ensemble (usaremos uma regressão logística)
meta_model = LogisticRegression()

#Criar o Stacking Classifier (ensemble)
ensemble = StackingClassifier(
    estimators=[
        ('rf', rf),
        ('gb', gb),
        ('xgb', xgb),
        ('svm', svm)
    ],
    final_estimator=meta_model,
    cv=5,  # Usar validação cruzada para o ensemble
    passthrough=False  # Para passar os dados originais para o metamodelo
)

#Criar o pipeline completo com o pré-processamento e o ensemble
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('ensemble', ensemble)
])

# Treinar o ensemble com barra de progresso
n_splits = 5  # Número de folds para validação cruzada

with tqdm(total=n_splits, desc="Treinando Ensemble", unit="fold") as pbar:
    for i in range(n_splits):
        pipeline.fit(X_train, y_train)
        pbar.update(1)

# Avaliar o ensemble
y_pred = pipeline.predict(X_test)
final_accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(f"\nResultados do Ensemble:")
print(f"Acurácia: {final_accuracy:.2f}, AUC-ROC: {auc:.2f}, Precisão: {precision:.2f}, Recall: {recall:.2f}")

# Salvar o modelo treinado
joblib.dump(pipeline, 'ensemble_model.pkl')

print(f"\nModelo ensemble salvo como 'ensemble_model.pkl'")
