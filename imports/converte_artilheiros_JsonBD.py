import psycopg2
import json

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

def inserir_artilheiros_no_postgresql(json_file, tabela):
    # Conectar ao banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        # Verificar se a tabela existe; se não existir, criar a tabela
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {tabela} (
            Brasao TEXT,
            Nome TEXT,
            Apelido TEXT,
            Time TEXT,
            Gols TEXT
        );
        """)
        conn.commit()

        # Abrir o arquivo JSON e carregar os dados
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Inserir ou atualizar os dados na tabela
        for artilheiro in data.get('artilharia', []):
            # Verificar se os dados já existem na tabela antes de inserir ou atualizar
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabela} WHERE Nome = %s",
                (artilheiro.get('Nome', ''),)
            )
            count = cursor.fetchone()[0]

            if count == 0:
                # Se o registro não existir, inserir
                cursor.execute(
                    f"INSERT INTO {tabela} (Brasao, Nome, Apelido, Time, Gols) VALUES (%s, %s, %s, %s, %s)",
                    (
                        artilheiro.get('BrasaoTime', ''),
                        artilheiro.get('Nome', ''),
                        artilheiro.get('Apelido', ''),
                        artilheiro.get('Time', ''),
                        artilheiro.get('Gols', '')
                    )
                )
            else:
                # Se o registro existir, atualizar
                cursor.execute(
                    f"UPDATE {tabela} SET Brasao = %s, Apelido = %s, Time = %s, Gols = %s WHERE Nome = %s",
                    (
                        artilheiro.get('BrasaoTime', ''),
                        artilheiro.get('Apelido', ''),
                        artilheiro.get('Time', ''),
                        artilheiro.get('Gols', ''),
                        artilheiro.get('Nome', '')
                    )
                )
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        print("Dados inseridos com sucesso no banco de dados PostgreSQL.")

# Chamar a função para inserir ou atualizar os dados no PostgreSQL
def converte_artilheiros():
    inserir_artilheiros_no_postgresql("artilheiros.json", "artilheiros_2023")
    

converte_artilheiros()
