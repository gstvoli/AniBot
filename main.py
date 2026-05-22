import customtkinter as ctk
import datetime
import threading
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
        self.geometry("600x450")

        # Titulo na janela
        self.label_titulo = ctk.CTkLabel(self, text="Log de Operações do AniBot", font=("Roboto", 18, "bold"))
        self.label_titulo.pack(pady=10) #pack() joga o elemento na tela

        # Caixa de texto onde as ações vão aparecer
        self.log_view = ctk.CTkTextbox(self, width=450, height=250)
        self.log_view.pack(padx=20, pady=10)

        # Botão para simular ação
        self.btn_start = ctk.CTkButton(self, text="Ativar Bot", command=self.iniciar_bot)
        self.btn_start.pack(pady=10)

    # 3. Função que roda quando clica no botão
    def adicionar_log(self, mensagem):
        """Função para escrever na tela"""
        hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_view.insert("end", f"[{hora_atual}] {mensagem}\n")
        self.log_view.see("end")
    
    def iniciar_bot(self):
        # Lembre-se de usar o 'r' antes das aspas no Windows 
        pasta_raiz = r"G:\Meu Drive\SERVER\Animes\0temp\Animes_Teste"
        pasta_no_drive = r"G:\Meu Drive\SERVER\Animes\0temp\Testes_origem"

        self.adicionar_log("Iniciando bot em segundo plano...")
        self.btn_start.configure(state="disabled")

        # O threading faz o trabalho pesado sem travar a tela
        thread = threading.Thread(
            target=mover_animes,
            args=(pasta_raiz, pasta_no_drive, self.adicionar_log),
            daemon=True
        )
        thread.start()

        # Reativa o botão após um tempo
        self.after(3000, lambda: self.btn_start.configure(state="normal"))

# 4. Ponto de partida do scriot
if __name__ == "__main__":
    app = AnimeBotUI()
    app.mainloop() # Mantém a janela aberta e escutando os clicks