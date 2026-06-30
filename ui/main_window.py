import customtkinter as ctk
import datetime
import threading
from tkinter import messagebox, filedialog

from core.bot_logic import move_animes
from database.connection import SessionLocal
from database.models import FolderConfig

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AnimeBotUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AniBot")

        largura_janela = 600
        altura_janela = 450

        self.largura_ecra = self.winfo_screenwidth()
        self.altura_ecra = self.winfo_screenheight()

        pos_x = (self.largura_ecra // 2) - (largura_janela // 2)
        pos_y = (self.altura_ecra // 2) - (altura_janela // 2)        
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        self.load_configs()

        self.label_titulo = ctk.CTkLabel(self, text="Log de Operações do AniBot", font=("Roboto", 18, "bold"))
        self.label_titulo.pack(pady=10)

        self.log_view = ctk.CTkTextbox(self, width=450, height=250)
        self.log_view.pack(padx=20, pady=10)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=10)

        self.btn_start = ctk.CTkButton(self.frame_botoes, text="▶ Ativar Bot", command=self.iniciar_bot)
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_config = ctk.CTkButton(self.frame_botoes, text="⚙️ Configurações", fg_color="#555", hover_color="#333", command=self.open_configs)
        self.btn_config.grid(row=0, column=1, padx=10)

    def load_configs(self):
        db = SessionLocal()

        config = db.query(FolderConfig).filter(FolderConfig.active == 1).first()

        if config:
            self.origin_folder = config.origin_folder
            self.destination_folder = config.destination_folder
        else:
            self.origin_folder = ''
            self.destination_folder = ''

        db.close()

    def add_log(self, message):
        current_hour = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_view.insert("end", f"[{current_hour}] {message}\n")
        self.log_view.see("end")

    def open_configs(self):
        window_config = ctk.CTkToplevel(self)
        window_config.title("Configurações")

        largura_janela = 500
        altura_janela = 300
        pos_x = (self.largura_ecra // 2) - (largura_janela // 2)
        pos_y = (self.altura_ecra // 2) - (altura_janela // 2)
        window_config.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        window_config.grab_set()
        
        var_origin = ctk.StringVar(value=self.origin_folder)
        var_destination = ctk.StringVar(value=self.destination_folder)

        ctk.CTkLabel(window_config, text="Pasta para Observar/Scan (Origem):").pack(anchor="w", padx=20, pady=(15,0))
        origin_frame = ctk.CTkFrame(window_config, fg_color="transparent")
        origin_frame.pack(fill="x", padx=20, pady=5)
        entry_origin = ctk.CTkEntry(origin_frame, textvariable=var_origin, width=350, state="disabled")
        entry_origin.pack(side="left")
        btn_search_origin = ctk.CTkButton(origin_frame, text="Buscar", width=80, command=lambda: var_origin.set(filedialog.askdirectory() or var_origin.get()))
        btn_search_origin.pack(side="right", padx=10)

        ctk.CTkLabel(window_config, text="Pasta do Google Drive (Destino):").pack(anchor="w", padx=20, pady=(15, 0))
        frame_destination = ctk.CTkFrame(window_config, fg_color="transparent")
        frame_destination.pack(fill="x", padx=20, pady=5)
        entry_destination = ctk.CTkEntry(frame_destination, textvariable=var_destination, width=350, state="disabled")
        entry_destination.pack(side="left")
        btn_search_destination = ctk.CTkButton(frame_destination, text="Buscar", width=80, command=lambda: var_destination.set(filedialog.askdirectory() or var_destination.get()))
        btn_search_destination.pack(side="right", padx=10)

        btn_save = ctk.CTkButton(window_config, text="Salvar configurações", fg_color="green", hover_color="#086400",
                                        command=lambda: [self.save_n_exit(var_origin.get(), var_destination.get(), window_config)])
        btn_save.pack(pady=30)

    def save_n_exit(self, origin, destination, window):
        self.origin_folder = origin
        self.destination_folder = destination

        db = SessionLocal()
        config = db.query(FolderConfig).filter(FolderConfig.active == 1).first()

        if config:
            config.origin_folder = origin
            config.destination_folder = destination
        else:
            new_config = FolderConfig(origin_folder=origin, destination_folder=destination)
            db.add(new_config)
            
        db.commit()
        db.close()

        self.add_log("⚙️ Configurações guardadas com sucesso!")
        window.destroy()


    def iniciar_bot(self):
        if not self.origin_folder or not self.destination_folder:
            messagebox.showwarning("Aviso", "Você precisa configurar as pasta de Origem e Destino primeiro!")
            return

        self.add_log("Iniciando bot em segundo plano...")
        self.btn_start.configure(state="disabled")

        thread = threading.Thread(
            target=move_animes,
            args=(self.origin_folder, self.destination_folder, self.add_log),
            daemon=True
        )
        thread.start()

        # Reativa o botão após um tempo
        self.after(3000, lambda: self.btn_start.configure(state="normal"))