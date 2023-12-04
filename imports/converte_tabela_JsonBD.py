import psycopg2
import json
# import pymysql

def converte_tabela():
    # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="84650052",  # Altere aqui a senha do seu PostgreSQL
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    
    # Configuração do MySQL com pymysql
    #conn = pymysql.connect(
    #    database="if0_35525482_futstats",
    #    user="if0_35525482",
    #    password="84650052",
    #    host="sql300.infinityfree.com",
    #    port=3306
    #)
    #
    #cursor = conn.cursor()
    

    tabela = "classificacao_2023"

    caminho_arquivo_json = 'classificacao_brasileirao_2023.json'

    with open(caminho_arquivo_json, 'r', encoding='utf-8') as json_file:
        dados = json.load(json_file)
        dados_equipes = dados.get('tabela', [])

    # Verifique se a tabela existe
    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (tabela,))
    table_exists = cursor.fetchone()[0]

    if not table_exists:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {tabela} (
                    Classificacao TEXT,
                    BrasaoTime TEXT,
                    Nome TEXT,
                    Pontos TEXT,
                    Jogos TEXT,
                    Vitórias TEXT,
                    Empates TEXT,
                    Derrotas TEXT,
                    Gols_Pros TEXT,
                    Gols_Contra TEXT,
                    Saldo_de_Gols TEXT,
                    Cartoes_Amarelos TEXT,
                    Cartoes_Vermelhos TEXT,
                    Porcentagem_de_Vitorias TEXT
                )
            """)

    # Verifique se a tabela está vazia
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
            # Se a tabela estiver vazia, insira os dados
            for dados in dados_equipes:
                cursor.execute(
                    f"INSERT INTO {tabela} (Classificacao, BrasaoTime, Nome, Pontos, Jogos, Vitórias, Empates, Derrotas, Gols_Pros, Gols_Contra, Saldo_de_Gols, Cartoes_Amarelos, Cartoes_Vermelhos, Porcentagem_de_Vitorias) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        dados.get('Classificação', None),
                        dados.get('BrasaoTime', None),
                        dados.get('Nome', None),
                        dados.get('Pontos', None),
                        dados.get('Jogos', None),
                        dados.get('Vitórias', None),
                        dados.get('Empates', None),
                        dados.get('Derrotas', None),
                        dados.get('Gols Prós', None),
                        dados.get('Gols Contra', None),
                        dados.get('Saldo de Gols', None),
                        dados.get('Cartões Amarelos', None),
                        dados.get('Cartões Vermelhos', None),
                        dados.get('Porcentagem de Vitórias', None)
                    )
                )
    else:
            # Se a tabela já contiver dados, atualize os registros
            for dados in dados_equipes:
                # Suponha que você tenha uma coluna de chave primária chamada 'Classificacao'
                cursor.execute(
                    f"UPDATE {tabela} SET Pontos = %s, Jogos = %s, Vitórias = %s, Empates = %s, Derrotas = %s, Gols_Pros = %s, "
                    "Gols_Contra = %s, Saldo_de_Gols = %s, Cartoes_Amarelos = %s, Cartoes_Vermelhos = %s, Porcentagem_de_Vitorias = %s "
                    "WHERE Classificacao = %s",
                    (
                        dados.get('Pontos', None),
                        dados.get('Jogos', None),
                        dados.get('Vitórias', None),
                        dados.get('Empates', None),
                        dados.get('Derrotas', None),
                        dados.get('Gols Prós', None),
                        dados.get('Gols Contra', None),
                        dados.get('Saldo de Gols', None),
                        dados.get('Cartões Amarelos', None),
                        dados.get('Cartões Vermelhos', None),
                        dados.get('Porcentagem de Vitórias', None),
                        dados.get('Classificação', None)
                    )
                )
        
    conn.commit()
    conn.close()

    print("Dados inseridos com sucesso no banco de dados PostgreSQL.")



converte_tabela()