Projeto League of Legends - Recomendador de Ações em Tempo Real
Visão Geral
Este projeto utiliza Machine Learning para atuar como um coach virtual em partidas de League of Legends, oferecendo recomendações em tempo real com base nos dados coletados durante o jogo. A aplicação captura informações da API da Riot Games e utiliza um modelo de ML para sugerir estratégias ao jogador, auxiliando-o a maximizar as chances de vitória.

Funcionalidades Principais
Autenticação de Usuário: Login usando o Riot ID e autenticação via JWT.
Captura de Dados em Tempo Real: Coleta informações sobre os participantes, times e progresso da partida através da API Spectator da Riot.
Processamento de Dados: Transformação dos dados capturados para o formato necessário pelo modelo de ML.
Geração de Recomendações: Com base nos dados processados, o modelo de ML sugere ações em tempo real, como focar em dragões, controlar visão ou atacar torres.
Estrutura do Projeto
Diretórios Principais
Back/ - Contém o código backend, com autenticação, captura de dados e geração de recomendações.
ML/ - Contém o modelo de Machine Learning, incluindo o arquivo treinado e o scaler.
data/ - Reúne os dados capturados e processados das partidas, usados para treinamento e ajustes do modelo.
services/ - Módulos para captura de dados da API, transformação de dados e recomendações.
Arquivos Principais
auth.py: Autenticação do usuário via JWT, permite o login seguro e acesso às funcionalidades da aplicação.
recommendations.py: Função para converter as predições do modelo em recomendações compreensíveis para o jogador.
dataTRANSFORMATION.py: Realiza transformações nos dados para que correspondam ao formato de entrada esperado pelo modelo de ML.
riot_api.py: Lida com as requisições à API da Riot, incluindo a Spectator API para captura de dados ao vivo.
modelCOMPARATION.py: Treinamento e validação de diferentes modelos de ML, com o objetivo de otimizar a acurácia nas recomendações.
Configuração e Instalação
Clone o repositório para sua máquina local:

bash
Copiar código
git clone https://github.com/seu-usuario/seu-repositorio.git
Instale as dependências necessárias listadas em requirements.txt:

bash
Copiar código
pip install -r requirements.txt
Configure a variável de ambiente com a sua chave de API da Riot Games:

Altere API_KEY nos scripts para a sua chave obtida em Riot Developer Portal.
Endpoints e Funcionamento
1. Autenticação de Usuário
Rota: /token
Método: POST
Entrada: username e password
Saída: Token JWT para autenticação.
2. Captura de Dados da Partida
Rota: /game/current
Método: GET
Entrada: PUUID do jogador
Saída: Dados em tempo real da partida.
3. Geração de Recomendações
Rota: /recommendations
Método: POST
Entrada: Dados processados da partida
Saída: Sugestões de ações para o jogador.
Fluxo Completo
Login: O jogador entra com seu Riot ID e recebe um token JWT.
Captura do PUUID: O backend obtém o PUUID do jogador via API da Riot.
Captura de Dados em Tempo Real: Durante o jogo, o backend captura dados ao vivo da Spectator API.
Geração de Recomendações: Os dados são processados e usados pelo modelo de ML para fornecer recomendações em tempo real ao jogador.
Modelo de Machine Learning
O modelo foi treinado para prever ações estratégicas durante a partida, como atacar dragões, controlar visão, ou focar em torres. As features utilizadas incluem:

Estatísticas do Jogador: Abates, mortes, assistências, ouro ganho, nível do campeão, etc.
Objetivos de Time: Barões, dragões, torres, inibidores.
Duração da Partida: Tempo decorrido, modo de jogo e tipo de partida.
A aplicação atualmente usa um ensemble de modelos, sendo os mais eficazes o Random Forest e o Gradient Boosting, com um SVM de apoio.
