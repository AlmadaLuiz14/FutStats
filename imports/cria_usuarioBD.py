import psycopg2

def cria_User():
     # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="84650052",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    tabela = "usuario"

    try:
        cursor.execute(f"""               
        CREATE TABLE IF NOT EXISTS {tabela} (
            EMAIL TEXT PRIMARY KEY NOT NULL,
            NOME TEXT,
            SENHA TEXT NOT NULL,
            TIPO_ADM BOOLEAN DEFAULT FALSE
        );

        INSERT INTO public.{tabela}(email, nome, senha, tipo_adm)
            VALUES('admin', 'adm0', 'admin', true);
        """
        )
    except:
        print("Erro padrão ao atualizar os bd's")
        
    conn.commit()
    cursor.close()
    conn.close()