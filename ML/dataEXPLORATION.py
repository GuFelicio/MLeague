import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados transformados do CSV
data_path = r"F:\Devs\helpNBlol\match_details_transformed.csv"
data = pd.read_csv(data_path)

# Exibir as primeiras linhas para entender a estrutura
print("Primeiras linhas do dataset:")
print(data.head())

# Verificar informações básicas sobre os dados (tipos e dados faltantes)
print("\nInformações do dataset:")
print(data.info())

# Verificar estatísticas descritivas para as colunas numéricas
print("\nEstatísticas descritivas:")
print(data.describe())

# Visualizar a correlação entre variáveis numéricas
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Mapa de calor de correlação")
plt.show()

# Exibir histogramas para visualizar a distribuição das variáveis numéricas
data.hist(bins=30, figsize=(20, 15))
plt.suptitle("Distribuição das variáveis numéricas")
plt.show()

# Identificar possíveis correlações e outliers para variáveis de interesse
for column in data.columns:
    if pd.api.types.is_numeric_dtype(data[column]):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[column])
        plt.title(f"Boxplot para {column}")
        plt.show()
