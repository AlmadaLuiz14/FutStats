import psycopg2
import json

def converte_simula():
    # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="postG000",  # Altere aqui a senha do seu PostgreSQL
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    tabela = "simula_2023"  # Alteração do nome da tabela

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
                Nome TEXT PRIMARY KEY,
                Pontos INT,
                Jogos INT,
                Vitorias INT,
                Empates INT,
                Derrotas INT,
                Gols_Pros INT,
                Gols_Contra INT,
                Saldo_de_Gols INT,
                Cartoes_Amarelos INT,
                Cartoes_Vermelhos INT,  
                Porcentagem_de_Vitorias INT  
            )
        """)

    # Verifique se a tabela está vazia
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        # Se a tabela estiver vazia, insira os dados
        for dados in dados_equipes[1:]:
            cursor.execute(
                f"INSERT INTO {tabela} (Classificacao, BrasaoTime, Nome, Pontos, Jogos, Vitorias, Empates, Derrotas, Gols_Pros, Gols_Contra, Saldo_de_Gols, Cartoes_Amarelos, Cartoes_Vermelhos, Porcentagem_de_Vitorias) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    dados.get('Classificação', None),
                    dados.get('BrasaoTime', None),
                    dados.get('Nome', None),
                    int(dados.get('Pontos', 0)),  # Conversão para INT
                    int(dados.get('Jogos', 0)),  # Conversão para INT
                    int(dados.get('Vitórias', 0)),  # Conversão para INT
                    int(dados.get('Empates', 0)),  # Conversão para INT
                    int(dados.get('Derrotas', 0)),  # Conversão para INT
                    int(dados.get('Gols Prós', 0)),  # Conversão para INT
                    int(dados.get('Gols Contra', 0)),  # Conversão para INT
                    int(dados.get('Saldo de Gols', 0)),  # Conversão para INT
                    int(dados.get('Cartões Amarelos', 0)),  # Conversão para INT
                    int(dados.get('Cartões Vermelhos', 0)),  # Conversão para INT
                    int(dados.get('Porcentagem de Vitórias', 0))  # Conversão para INT
                )
            )
    else:
        # Se a tabela já contiver dados, atualize os registros
        for dados in dados_equipes[1:]:
            # Suponha que você tenha uma coluna de chave primária chamada 'Classificacao'
            cursor.execute(
                f"UPDATE {tabela} SET Pontos = %s, Jogos = %s, Vitorias = %s, Empates = %s, Derrotas = %s, Gols_Pros = %s, "
                "Gols_Contra = %s, Saldo_de_Gols = %s, Cartoes_Amarelos = %s, Cartoes_Vermelhos = %s, Porcentagem_de_Vitorias = %s "
                "WHERE Classificacao = %s",
                (
                    int(dados.get('Pontos', 0)),  # Conversão para INT
                    int(dados.get('Jogos', 0)),  # Conversão para INT
                    int(dados.get('Vitórias', 0)),  # Conversão para INT
                    int(dados.get('Empates', 0)),  # Conversão para INT
                    int(dados.get('Derrotas', 0)),  # Conversão para INT
                    int(dados.get('Gols Prós', 0)),  # Conversão para INT
                    int(dados.get('Gols Contra', 0)),  # Conversão para INT
                    int(dados.get('Saldo de Gols', 0)),  # Conversão para INT
                    int(dados.get('Cartões Amarelos', 0)),  # Conversão para INT
                    int(dados.get('Cartões Vermelhos', 0)),  # Conversão para INT
                    int(dados.get('Porcentagem de Vitórias', 0)),  # Conversão para INT
                    dados.get('Classificação', None)
                )
            )
        
    conn.commit()
    conn.close()

    print("Dados inseridos com sucesso no banco de dados PostgreSQL.")

converte_simula()
