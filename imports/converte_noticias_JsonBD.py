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

def criar_tabela_noticias(conn, tabela):
    cursor = conn.cursor()

    try:
        # Verificar se a tabela existe; se não existir, criar a tabela
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {tabela} (
            Titulo TEXT PRIMARY KEY,
            Link TEXT,
            Imagem TEXT
        );
        """)
        conn.commit()
    except Exception as e:
        print(f"Erro ao criar a tabela no banco de dados: {e}")
    finally:
        cursor.close()

def inserir_atualizar_noticias_no_postgresql(conn, json_file, tabela):
    # Conectar ao banco de dados
    cursor = conn.cursor()

    try:
        # Verificar se a tabela existe; se não existir, criar a tabela
        criar_tabela_noticias(conn, tabela)

        # Abrir o arquivo JSON e carregar os dados
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Inserir ou atualizar os dados na tabela
        for noticia in data.get('noticias', []):
            cursor.execute(
                f"SELECT COUNT(*) FROM {tabela} WHERE Titulo = %s",
                (noticia.get('Título', ''),)
            )
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute(
                    f"INSERT INTO {tabela} (Titulo, Link, Imagem) VALUES (%s, %s, %s)",
                    (
                        noticia.get('Título', ''),
                        noticia.get('Link', ''),
                        noticia.get('Imagem', '')
                    )
                )
            else:
                cursor.execute(
                    f"UPDATE {tabela} SET Link = %s, Imagem = %s WHERE Titulo = %s",
                    (
                        noticia.get('Link', ''),
                        noticia.get('Imagem', ''),
                        noticia.get('Título', '')
                    )
                )
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
    finally:
        conn.commit()
        cursor.close()

# Chamar a função para inserir ou atualizar os dados no PostgreSQL


def converte_noticias():
    conn = conectar_bd()
    inserir_atualizar_noticias_no_postgresql(conn, "noticias_ge.json", "tabela_noticias")
    conn.close()

converte_noticias()