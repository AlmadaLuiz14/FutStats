import json
import psycopg2
from psycopg2 import sql

def conectar_bd():
    # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="84650052",  # Altere aqui a senha do seu PostgreSQL
        host="localhost",
        port="5432"
    )
    return conn

def criar_tabela_assistencias():
    # Conectar ao banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()

    # Criar a tabela se não existir
    create_table_query = """
    CREATE TABLE IF NOT EXISTS assistencias (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        time TEXT,
        partidas TEXT,
        assistencias TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Fechar a conexão
    cursor.close()
    conn.close()

def inserir_atualizar_assistencias(json_file, tabela_nome):
    # Carregar dados do arquivo JSON
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Obter a tabela específica do JSON
    tabela = None
    for item in data:
        if tabela_nome in item:
            tabela = item[tabela_nome]
            break

    if tabela is None:
        print(f"Tabela '{tabela_nome}' não encontrada no arquivo JSON.")
        return

    # Conectar ao banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()

    # Inserir ou atualizar dados na tabela
    for linha in tabela:
        if linha:  # Ignorar itens vazios
            nome = linha.get('Nome', '')
            time = linha.get('Time', '')
            partidas = linha.get('Partidas', 0)
            assistencias = linha.get('Assistencias', 0)

            # Verificar se o registro já existe
            cursor.execute(sql.SQL("SELECT * FROM assistencias WHERE nome = %s"), (nome,))
            existing_record = cursor.fetchone()

            if existing_record:
                # Atualizar o registro
                update_query = sql.SQL("""
                    UPDATE assistencias
                    SET time = %s, partidas = %s, assistencias = %s
                    WHERE nome = %s
                """)
                cursor.execute(update_query, (time, partidas, assistencias, nome))
            else:
                # Inserir um novo registro
                insert_query = sql.SQL("""
                    INSERT INTO assistencias (nome, time, partidas, assistencias)
                    VALUES (%s, %s, %s, %s)
                """)
                cursor.execute(insert_query, (nome, time, partidas, assistencias))

    # Commit e fechar a conexão
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Dados da tabela '{tabela_nome}' inseridos/atualizados no banco de dados.")

def converte_assist():
    # Crie a tabela se não existir
    criar_tabela_assistencias()

    # Insira ou atualize os dados da tabela "tabela_2"
    inserir_atualizar_assistencias('assistencias_time.json', 'tabela_2')


converte_assist()