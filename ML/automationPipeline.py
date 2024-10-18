import time
import subprocess

# Função para rodar cada script em sequência
def run_script(script_path):
    print(f"Executando {script_path}...")
    subprocess.run(['python', script_path])
    print(f"{script_path} finalizado.")

def run_games_request_for_duration(duration, script_path):
    """
    Executa o script gamesREQUEST.py continuamente por uma duração específica (em segundos).
    """
    print(f"Executando {script_path} por {duration / 60} minutos...")
    
    # Executar o script gamesREQUEST.py apenas uma vez e deixar rodar
    run_script(script_path)

    # Aguardar o tempo definido (sem executar o script novamente)
    time.sleep(duration)

    print(f"Tempo de execução de {script_path} finalizado.")

def main():
    # Definir o intervalo de tempo para captura de dados (em segundos)
    capture_duration = 1800  # 30 minutos, ajuste conforme necessário

    # Definir os caminhos completos dos scripts
    path_dados_puuids = r'.\ML\dados_PUUIDS.py'
    path_games_request = r'.\ML\gamesREQUEST.py'
    path_game_details = r'.\ML\gameDETAILSrequest.py'
    path_outliers_treatment = r'.\ML\outliersTREATMENT.py'
    path_data_win_results = r'.\ML\dataWINResults.py'
    path_data_transformation = r'.\ML\dataTRANSFORMATION.py'
    path_model_comparation = r'.\ML\modelCOMPARATION.py'

    # Passo 1: Coletar novos PUUIDs de jogadores
    run_script(path_dados_puuids)

    # Passo 2: Capturar novas partidas por um período determinado
    run_games_request_for_duration(capture_duration, path_games_request)

    # Passo 3: Coletar detalhes das partidas
    run_script(path_game_details)

    # Passo 4: Tratamento de outliers
    run_script(path_outliers_treatment)

    # Passo 5: Processar os resultados das partidas
    run_script(path_data_win_results)

    # Passo 6: Transformar os dados para ML
    run_script(path_data_transformation)

    # Passo 7: Treinar e comparar modelos
    run_script(path_model_comparation)

    print("Treino completo!")

if __name__ == "__main__":
    main()
