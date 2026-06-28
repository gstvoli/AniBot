import shutil
from pathlib import Path
import time
from tkinter import messagebox

    
def pergunta_excluir_pasta(self, nome_pasta):
    return messagebox.askyesno(
        "Pasta Vazia",
        f"A pasta '{nome_pasta}' ficou vazia após a organização.\n Deseja apagá-la?"
    )

def mover_animes(pasta_origem, pasta_destino, atualizar_tela):
    """
    Função responsável por mover os arquivos.
    'atualizar_tela' é uma função que enviaremos lá do main.py para escrever no log.
    """    

    caminho_origem = Path(pasta_origem)
    caminho_destino = Path(pasta_destino)

    # 1. Verifica se a pasta de origem existe
    if not caminho_origem.exists():
        atualizar_tela("❌ Erro: A pasta de origem não foi encontrada.")
        return
    
    # 2. Cria a pasta de destino no G: caso ela ainda não exista
    caminho_destino.mkdir(parents=True, exist_ok=True)
    atualizar_tela(f"📂Lendo arquivos da pasta: {caminho_origem.name}")

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
                atualizar_tela(f"✅ Movido: {arquivo.name}")
                moveu_algo = True
                time.sleep(0.5)

            except Exception as erro:
                atualizar_tela(f"❌ Erro ao mover {arquivo.name}: {erro}")
    
    if not moveu_algo:
        atualizar_tela("⚠️ Nenhum vídeo encontrado para mover.")
    else:
        itens_restantes = list(caminho_origem.iterdir())

        if len(itens_restantes) == 0:
            atualizar_tela("A pasta de origem ficou vazia. Aguardando decisão do usuário...")

            deletar_pasta = pergunta_excluir_pasta(caminho_origem.name)

            if deletar_pasta:
                try:
                    caminho_origem.rmdir()
                    atualizar_tela("🗑️ Pasta '{caminho_origem.name}' excluída com sucesso.")
                except Exception as e:
                    atualizar_tela("❌ Erro ao excluir a pasta: {e}")
            else:
                atualizar_tela("Ação cancelada: A pasta vazia foi mantida.")

    atualizar_tela("Processo finalizado.")    