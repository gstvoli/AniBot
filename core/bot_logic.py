import shutil
from pathlib import Path
import time
from tkinter import messagebox

    
def ask_delete_folder(self, nome_pasta):
    return messagebox.askyesno(
        "Pasta Vazia",
        f"A pasta '{nome_pasta}' ficou vazia após a organização.\n Deseja apagá-la?"
    )

def move_animes(pasta_origem, pasta_destino, refresh_screen):
    caminho_origem = Path(pasta_origem)
    caminho_destino = Path(pasta_destino)

    if not caminho_origem.exists():
        refresh_screen("❌ Erro: A pasta de origem não foi encontrada.")
        return
    
    caminho_destino.mkdir(parents=True, exist_ok=True)
    refresh_screen(f"📂Lendo arquivos da pasta: {caminho_origem.name}")

    extensoes_validas = ['.mkv', '.mp4', '.avi']
    moveu_algo = False

    for arquivo in caminho_origem.iterdir():
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_validas:

            destino_completo = caminho_destino / arquivo.name

            try:
                shutil.move(str(arquivo), str(destino_completo))
                refresh_screen(f"✅ Movido: {arquivo.name}")
                moveu_algo = True
                time.sleep(0.5)

            except Exception as erro:
                refresh_screen(f"❌ Erro ao mover {arquivo.name}: {erro}")
    
    if not moveu_algo:
        refresh_screen("⚠️ Nenhum vídeo encontrado para mover.")
    else:
        itens_restantes = list(caminho_origem.iterdir())

        if len(itens_restantes) == 0:
            refresh_screen("A pasta de origem ficou vazia. Aguardando decisão do usuário...")

            deletar_pasta = ask_delete_folder(caminho_origem.name)

            if deletar_pasta:
                try:
                    caminho_origem.rmdir()
                    refresh_screen("🗑️ Pasta '{caminho_origem.name}' excluída com sucesso.")
                except Exception as e:
                    refresh_screen("❌ Erro ao excluir a pasta: {e}")
            else:
                refresh_screen("Ação cancelada: A pasta vazia foi mantida.")

    refresh_screen("Processo finalizado.")    