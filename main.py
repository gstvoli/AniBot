import customtkinter as ctk
import datetime
import threading
import os
import sqlite3
from tkinter import messagebox, filedialog
from bot_logic import mover_animes

# 1. Configuraçções visuais da janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 2; Criando a classe principal do app
class AnimeBotUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("AniBot")

        largura_janela = 600
        altura_janela = 450

        self.largura_ecra = self.winfo_screenwidth()
        self.altura_ecra = self.winfo_screenheight()

        pos_x = (self.largura_ecra // 2) - (largura_janela // 2)
        pos_y = (self.altura_ecra // 2) - (altura_janela // 2)        

        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        self.pasta_origem = ""
        self.pasta_destino = ""
        # Titulo na janela
        self.label_titulo = ctk.CTkLabel(self, text="Log de Operações do AniBot", font=("Roboto", 18, "bold"))
        self.label_titulo.pack(pady=10) #pack() joga o elemento na tela

        # Caixa de texto onde as ações vão aparecer
        self.log_view = ctk.CTkTextbox(self, width=450, height=250)
        self.log_view.pack(padx=20, pady=10)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=10)

        # Botão para simular ação
        self.btn_start = ctk.CTkButton(self.frame_botoes, text="▶ Ativar Bot", command=self.iniciar_bot)
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_config = ctk.CTkButton(self.frame_botoes, text="⚙️ Configurações", fg_color="#555", hover_color="#333", command=self.abrir_configuracoes)
        self.btn_config.grid(row=0, column=1, padx=10)

    def carregar_configuracoes():
        conexao = sqlite3.connect("anibot.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                origin_folder,
                destination_folder
            FROM folder_config
            WHERE
                id_config = 1
                AND active = 1
        """)

        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            return {"origem": resultado[0], "destino": resultado[1]}
        return {"origem": "", "destino": ""}

    def salvar_configuracoes(self, nova_origem, novo_destino):
        conexao = sqlite3.connect("anibot.db")
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE folder_config
            SET
                pasta_origem = ?,
                pasta_destino = ?
            WHERE id_config = 1
            and ativo = 1
        """, (nova_origem, novo_destino))

        conexao.commit()
        conexao.close();


    def abrir_configuracoes(self):
        janela_config = ctk.CTkToplevel(self)
        janela_config.title("Configurações")

        largura_janela = 500
        altura_janela = 300

        pos_x = (self.largura_ecra // 2) - (largura_janela // 2)
        pos_y = (self.altura_ecra // 2) - (altura_janela // 2)

        janela_config.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        janela_config.grab_set()
        
        var_origem = ctk.StringVar(value=self.pasta_origem)
        var_destino = ctk.StringVar(value=self.pasta_destino)

        ctk.CTkLabel(janela_config, text="Pasta para Observar/Scan (Origem):").pack(anchor="w", padx=20, pady=(15,0))
        frame_origem = ctk.CTkFrame(janela_config, fg_color="transparent")
        frame_origem.pack(fill="x", padx=20, pady=5)

        entry_origem = ctk.CTkEntry(frame_origem, textvariable=var_origem, width=350, state="disabled")
        entry_origem.pack(side="left")

        btn_procurar_origem = ctk.CTkButton(frame_origem, text="Buscar", width=80, command=lambda: var_origem.set(filedialog.askdirectory() or var_origem.get()))
        btn_procurar_origem.pack(side="right", padx=10)

        ctk.CTkLabel(janela_config, text="Pasta do Google Drive (Destino):").pack(anchor="w", padx=20, pady=(15, 0))
        frame_destino = ctk.CTkFrame(janela_config, fg_color="transparent")
        frame_destino.pack(fill="x", padx=20, pady=5)

        entry_destino = ctk.CTkEntry(frame_destino, textvariable=var_destino, width=350, state="disabled")
        entry_destino.pack(side="left")

        btn_procurar_destino = ctk.CTkButton(frame_destino, text="Buscar", width=80, command=lambda: var_destino.set(filedialog.askdirectory() or var_destino.get()))
        btn_procurar_destino.pack(side="right", padx=10)

        btn_salvar = ctk.CTkButton(janela_config, text="Salvar configurações", fg_color="green", hover_color="#086400",
                                        command=lambda: [self.salvar_configuracoes(var_origem.get(), var_destino.get()), janela_config.destroy()])
        btn_salvar.pack(pady=30)

    def adicionar_log(self, mensagem):
        """Função para escrever na tela"""
        hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_view.insert("end", f"[{hora_atual}] {mensagem}\n")
        self.log_view.see("end")
    
    def pergunta_excluir_pasta(self, nome_pasta):
        return messagebox.askyesno(
            "Pasta Vazia",
            f"A pasta '{nome_pasta}' ficou vazia após a organização.\n Deseja apagá-la?"
        )

    def iniciar_bot(self):
        # Lembre-se de usar o 'r' antes das aspas no Windows 
        if not self.pasta_origem or not self.pasta_destiino:
            messagebox.showwarning("Aviso", "Você precisa configurar as pasta de Origem e Destino primeiro!")
            return

        self.adicionar_log("Iniciando bot em segundo plano...")
        self.btn_start.configure(state="disabled")

        # O threading faz o trabalho pesado sem travar a tela
        thread = threading.Thread(
            target=mover_animes,
            args=(self.pasta_origem, self.pasta_destiino, self.adicionar_log, self.pergunta_excluir_pasta),
            daemon=True
        )
        thread.start()

        # Reativa o botão após um tempo
        self.after(3000, lambda: self.btn_start.configure(state="normal"))
# 4. Ponto de partida do scriot
if __name__ == "__main__":
    app = AnimeBotUI()
    app.mainloop() # Mantém a janela aberta e escutando os clicks