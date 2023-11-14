import psycopg2

def cria_User():
    #Fazer a conexão com o bd
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="postG000",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    tabela = "usuario"

    #Criar, se n existir, a tabela usuario
    cursor.execute(f"""               
    CREATE TABLE IF NOT EXISTS {tabela} (
        EMAIL TEXT PRIMARY KEY NOT NULL,
        NOME TEXT,
        SENHA TEXT NOT NULL
    );
    """)

    #Encerrar a conexão
    conn.commit()
    conn.close()