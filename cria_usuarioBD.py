import psycopg2

def cria_User():
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="postG000",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    tabela = "usuario"

    cursor.execute(f"""               
    CREATE TABLE IF NOT EXISTS {tabela} (
        EMAIL TEXT PRIMARY KEY NOT NULL,
        NOME TEXT,
        SENHA TEXT NOT NULL
    );
    """)