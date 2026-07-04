import shutil
from pathlib import Path
import time
from tkinter import messagebox

from database.connection import SessionLocal
from database.models import Medias, ExistentsFolders, RemovableTags

from utils.formatter import clean_file_tags, find_media_folder
    
def ask_delete_folder(self, nome_pasta):
    return messagebox.askyesno(
        "Pasta Vazia",
        f"A pasta '{nome_pasta}' ficou vazia após a organização.\n Deseja apagá-la?"
    )

def move_animes(origin_folder, destination_folder, refresh_screen):
    origin_path = Path(origin_folder)
    destination_path = Path(destination_folder)
    moved_media = 0
    created_folders = 0

    if not origin_path.exists():
        refresh_screen("❌ Erro: A pasta de origem não foi encontrada.")
        return
    
    destination_path.mkdir(parents=True, exist_ok=True)
    refresh_screen(f"📂Lendo files da pasta: {origin_path.name}")

    extensoes_validas = ['.mkv', '.mp4', '.avi']
    db = SessionLocal()
    moveu_algo = False

    for file in origin_path.iterdir():
        if file.is_file() and file.suffix.lower() in extensoes_validas:

            tag_list, clean_name = clean_file_tags(file.name)
            related_folder = find_media_folder(clean_name, destination_folder)
            related_folder.mkdir(parents=True, exist_ok=True)

            folder_exists = db.query(ExistentsFolders).filter_by(folder_name=related_folder.name).first()

            if not folder_exists:
                new_folder = ExistentsFolders(folder_name=related_folder.name, folder_location=destination_folder)
                db.add(new_folder)
                refresh_screen(f"Pasta criada e salva no banco: {related_folder.name}")
                created_folders += 1
            else:
                refresh_screen(f"Direcionado para pasta existente: {related_folder.name}")

            full_destination = related_folder / clean_name

            try:
                shutil.move(str(file), str(full_destination))
                moved_media += 1
                refresh_screen(f"✅ Movido: {clean_name}")

                new_media = Medias(media_name=clean_name)
                db.add(new_media)

                for tag in tag_list:
                    tag_exists = db.query(RemovableTags).filter_by(tag_name=tag).first()

                    if not tag_exists:
                        new_tag = RemovableTags(tag_name=tag)
                        db.add(new_tag)          
                        
                db.commit()
                
                moveu_algo = True
                time.sleep(0.5)
                
                if created_folders == 3:
                    return

            except Exception as erro:
                refresh_screen(f"❌ Erro ao mover {file.name}: {erro}")
    
    if not moveu_algo:
        refresh_screen("⚠️ Nenhum vídeo encontrado para mover.")
    else:
        itens_restantes = list(origin_path.iterdir())

    
        if len(itens_restantes) == 0:
            refresh_screen("A pasta de origem ficou vazia. Aguardando decisão do usuário...")

            deletar_pasta = ask_delete_folder(origin_path.name)

            if deletar_pasta:
                try:
                    origin_path.rmdir()
                    refresh_screen("🗑️ Pasta '{origin_path.name}' excluída com sucesso.")
                except Exception as e:
                    refresh_screen("❌ Erro ao excluir a pasta: {e}")
            else:
                refresh_screen("Ação cancelada: A pasta vazia foi mantida.")

    refresh_screen("Processo finalizado.")    