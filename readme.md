  <h1 align="center">Anibot</h1>
<p align="center">
  <img src="assets/anibot_exe.png" width="200">
</p>

O **AniBot** é uma aplicação desktop desenvolvida em Python para automatizar a organização de arquivos de vídeo (animes). Ele monitora uma pasta de origem (como a pasta de Downloads) e move automaticamente os arquivos de vídeo válidos para uma pasta de destino, mantendo um log de operações em tempo real na tela.


---

## ✨ Funcionalidades

- **Interface Gráfica Moderna:** Interface construída com `customtkinter`, oferecendo suporte a tema escuro e uma experiência de usuário amigável.
- **Processamento Assíncrono:** Utiliza `threading` para realizar a varredura e movimentação dos arquivos em segundo plano, sem congelar a interface gráfica.
- **Persistência de Dados (ORM):** As configurações de diretórios escolhidas pelo usuário são salvas localmente utilizando **SQLite** em conjunto com **SQLAlchemy**.
- **Controle de Migrações:** Estrutura de tabelas do banco de dados versionada e controlada profissionalmente através do **Alembic**.

---

## 🏗️ Arquitetura do Projeto

O projeto adota o padrão de **Separação de Preocupações (Separation of Concerns - SoC)**, dividindo as responsabilidades em módulos específicos:

```text
AniBot/
├── alembic/              # Histórico de versões e scripts de migração estrutural
├── assets/               # Imagens e capturas de tela para o README
├── core/                 # Cérebro da aplicação (Regras de negócio)
│   └── bot_logic.py      # Motor de varredura e movimentação de arquivos
├── database/             # Camada de persistência e comunicação com SQLite
│   ├── connection.py     # Configuração da Engine e Session
│   └── models.py         # Mapeamento de objetos relacionais (Models)
├── ui/                   # Camada de Apresentação visual
│   └── main_window.py    # Classe principal da interface e modais
├── utils/                # Camada de Fumções Utilitárias
│   └── formatter.py      # Funções de formatação de nome de arquivo
├── alembic.ini           # Configurações de ambiente do motor de migrações
└── main.py               # Ponto de entrada (Entrypoint)
```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos

Certifique-se de ter o [Python 3.x](https://www.python.org/) instalado na sua máquina.

### 2. Clonar o Repositório e Instalar Dependências

Abra o terminal na pasta onde deseja ter o projeto e execute:

```bash
git clone https://github.com/SEU_USUARIO/AniBot.git
cd AniBot

# Crie e ative um ambiente virtual (Recomendado)
python -m venv venv
venv\Scripts\activate  # No Windows

# Instale as dependências do projeto
pip install customtkinter sqlalchemy alembic
```

### 3. Inicializar o Banco de Dados

Antes de rodar a aplicação pela primeira vez, crie a estrutura física do banco de dados local executando as migrações do Alembic:

```bash
alembic upgrade head
```

> Isso vai ler o histórico da pasta `alembic/versions` e gerar o arquivo local `animebot.db`.

### 4. Iniciar o AniBot

Com o banco configurado, dê a partida na interface gráfica:

```bash
python main.py
```

---

## ⚙️ Como Usar

1. Ao abrir o aplicativo, clique no botão **⚙️ Configurações**.
2. Clique em **Procurar** para selecionar a **Pasta de Origem** (Downloads).
3. Clique em **Procurar** para selecionar a **Pasta de Destino** (Armazenamento final).
4. Clique em **Guardar Configurações** (ficará salvo de forma persistente).
5. Na tela principal, clique em **▶ Ativar Bot**. O log mostrará em tempo real os arquivos sendo lidos e movidos.
