import sqlite3

def initialize_database():
    connection = sqlite3.connect("anibot.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS folder_config (
            id_config INTEGER PRIMARY KEY AUTOINCREMENT,
            origin_folder TEXT NOT NULL,
            destination_folder TEXT NOT NULL,
            active INTEGER DEFAULT 1
            )
        """)
    
    cursor.execute("SELECT COUNT(*) FROM folder_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO folder_config (origin_folder, destination_folder)
            VALUES('', '')
        """)

    connection.commit()
    connection.close()

initialize_database()