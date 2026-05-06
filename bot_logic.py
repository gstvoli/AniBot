import shutil
from pathlib import Path
import time

def mover_animes(pasta_origem, pasta_destino, atualizar_tela):
    """
    Função responsável por mover os arquivos.
    'atualizar_tela' é uma função que enviaremos lá do main.py para escrever no log.
    """    

    caminho_origem = Path(pasta_origem)
    caminho_destino = Path(pasta_destino)

    # 1. Verifica se a pasta de origem existe
    if not caminho_origem.exists():
        atualizar_tela("Erro: A pasta de origem não foi encontrada.")
        return
    
    # 2. Cria a pasta de destino no G: caso ela ainda não exista
    caminho_destino.mkdir(parents=True, exist_ok=True)
    atualizar_tela(f"Lendo arquivos da pasta: {caminho_origem.name}")

    # 3. Lista de extensões que queremos mover
    extensoes_validas = ['.mkv', '.mp4', '.avi']
    moveu_algo = False

    # 4.Inicia a varredura e movimentação
    for arquivo in caminho_origem.iterdir():
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_validas:

            destino_completo = caminho_destino / arquivo.name

            try:
                # Movendo o arquivo
                shutil.move(str(arquivo), str(destino_completo))
                atualizar_tela(f"Movido: {arquivo.name}")
                moveu_algo = True
                time.sleep(0.5)

            except Exception as erro:
                atualizar_tela(f"Erro ao mover {arquivo.name}: {erro}")
    
    if not moveu_algo:
        atualizar_tela("Nenhum vídeo encontrado para mover.")

    atualizar_tela("Processo finalizado.")