import psycopg2
import json

# Função para salvar os dados do arquivo JSON no PostgreSQL
def salvar_jogos_do_json_no_postgresql(json_file, tabela):
    # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="postG000",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        # Verifica se a tabela existe; se não existir, cria a tabela
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {tabela} (
            Rodada TEXT,
            Info_Jogo TEXT,
            Nome1 TEXT REFERENCES simula_2023 (Nome),
            Time1 TEXT,
            Brasao1 TEXT,
            Nome2 TEXT REFERENCES simula_2023 (Nome),
            Time2 TEXT,
            Brasao2 TEXT,
            Placar TEXT,
            Local TEXT,
            PRIMARY KEY (Nome1, Nome2)
        );
        """)
        conn.commit()

        # Abre o arquivo JSON e carrega os dados
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for rodada, jogos in data['jogosinfo'].items():
            for jogo in jogos:
                # Verifica se os dados já existem na tabela
                cursor.execute(
                    f"SELECT COUNT(*) FROM {tabela} WHERE Info_Jogo = %s",
                    (jogo.get('Info_Jogo', None),)
                )
                count = cursor.fetchone()[0]

                if count == 0:
                    # Se não existirem, insere os dados
                    cursor.execute(
                        f"INSERT INTO {tabela} (Rodada, Info_Jogo,Nome1, Time1, Brasao1,Nome2, Time2, Brasao2, Placar, Local) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            int(rodada[6:]),
                            jogo.get('Info_Jogo', None),
                            jogo.get('Nome1', None),
                            jogo.get('Time1', None),
                            jogo.get('BrasaoTime1', None),
                            jogo.get('Nome2', None),
                            jogo.get('Time2', None),
                            jogo.get('BrasaoTime2', None),
                            jogo.get('Placar', None),
                            jogo.get('Local', None)
                        )
                    )
                else:
                    # Se existirem, atualiza os dados
                    cursor.execute(
                        f"UPDATE {tabela} SET Placar = %s, Local = %s WHERE Info_Jogo = %s",
                        (
                            jogo.get('Placar', None),
                            jogo.get('Local', None),
                            jogo.get('Info_Jogo', None)
                        )
                    )
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        print("Dados inseridos com sucesso no banco de dados PostgreSQL.")

# Chame a função para salvar os dados do arquivo JSON no PostgreSQL
def converte_jogos():    
    salvar_jogos_do_json_no_postgresql("jogos_rodada.json", "jogos_simula_2023")
    

converte_jogos()