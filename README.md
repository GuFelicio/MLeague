
markdown
Copiar código
# 🎮 League of Legends Real-Time Game Recommendations 🏆

Seja bem-vindo ao **League of Legends Real-Time Game Recommendations**! Este projeto usa **aprendizado de máquina** para oferecer recomendações estratégicas em tempo real durante as partidas de **League of Legends**, ajudando você a maximizar suas chances de vitória. 🚀

---

## 🚀 Funcionalidades

### **Autenticação e Identificação**
🔑 Login seguro utilizando Riot ID no formato `Nome#Tag`.  
🛡️ Obtenção do **PUUID** diretamente da API da Riot Games.  

### **Coleta de Dados em Tempo Real**
📡 Acompanhamento em tempo real das partidas com a **Spectator API**.  
📊 Coleta de métricas essenciais dos jogadores, times e da partida, incluindo:
- Abates, assistências, dragões abatidos, barões, torres, entre outros.  
- Itens comprados, níveis e ouro ganho pelos jogadores.  

### **Recomendações Estratégicas Baseadas em IA**
🧠 Machine Learning gera recomendações em tempo real, como:
- Atacar objetivos prioritários (Barão, Dragões, Torres).  
- Melhorar o farm ou visão.  
- Ajustar estratégias de combate conforme o andamento do jogo.  

---

## 🔧 Tecnologias Utilizadas

### **Backend**
- **Python 🐍**: Linguagem principal do projeto.  
- **FastAPI ⚡**: Framework para APIs rápidas e eficientes.  
- **Riot Games API 🎮**: Coleta de dados diretamente das partidas.  

### **Machine Learning**
- **Scikit-Learn 🤖**: Modelos de classificação e predição.  
- **Random Forest 🌲, Gradient Boosting 🔥, e SVM** para análise de padrões de jogo.  
- **Predição e Classificação**: As ações recomendadas são baseadas no histórico de dados tratados e normalizados.  

### **Outros**
- **Pandas e NumPy 📊**: Para preparação e manipulação dos dados.  
- **JSON 📂**: Estrutura de armazenamento para análise futura.  

---

## 📈 Modelos Utilizados e Resultados

| Modelo                | Acurácia        | Observações                      |
|------------------------|-----------------|----------------------------------|
| **Random Forest**      | 83%            | Excelente para predição geral.  |
| **Gradient Boosting**  | 83%            | Bom equilíbrio entre precisão e recall.  |
| **SVM**                | 85%            | Melhor acurácia para classificação. |

> **Conclusão**: A abordagem de **ensemble** foi adotada para maior robustez e consistência nos resultados.  

---

## 🎮 Como Usar

### **Pré-requisitos**
- Instale as dependências:  
```bash
pip install -r requirements.txt
Execução Inicial
Obtenha sua chave de API da Riot Games em Riot Developer Portal.
Adicione sua chave de API no arquivo de configuração.
Coleta de Dados em Tempo Real
Para iniciar a coleta:

bash
Copiar código
python src/capture_game_data.py
Digite o Riot ID e acompanhe o progresso.

Recomendações em Tempo Real
Após capturar os dados:

bash
Copiar código
python src/run_recommendations.py
Receba dicas estratégicas baseadas na análise da partida!

📁 Estrutura do Projeto
bash
Copiar código
📦 League of Legends Recommendations
├── 📂 src/
│   ├── auth.py             # Módulo de autenticação.
│   ├── riot_api.py         # Interação com a Riot API.
│   ├── data_processing/    # Scripts de normalização e transformação.
│   ├── recommendations/    # Geração de recomendações baseadas em ML.
├── 📂 data/
│   ├── raw/                # Dados brutos capturados das APIs.
│   ├── processed/          # Dados tratados para análise.
├── 📂 models/
│   ├── best_model.pkl      # Modelo treinado para recomendações.
│   ├── scaler.pkl          # Scaler para normalização.
├── requirements.txt        # Dependências do projeto.
└── README.md               # Documentação do projeto.
🌟 Diferenciais do Projeto
Interatividade: As recomendações são geradas em tempo real com base na situação atual da partida.
Adaptabilidade: Utilização de IA para identificar padrões e ajustar estratégias.
Escalabilidade: O sistema pode ser facilmente integrado a outras ferramentas, como aplicativos mobile.****
