import psycopg2
import json

# Configuração do PostgreSQL
conn = psycopg2.connect(
    database="FutStats",
    user="postgres",
    password="84650052",  # Altere aqui a senha do seu PostgreSQL
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Carregar os dados do arquivo JSON
with open("jogadores_serie_a.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Crie a tabela se ela não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS jogadores_2023 (
    NOME TEXT,
    APELIDO TEXT,
    TIME TEXT
);
""")

# Insira os dados na tabela, pulando jogadores com "Time: Team name not found"
for jogador in data:
    if jogador["Time"] != "Team name not found":
        cursor.execute("""
        INSERT INTO jogadores_2023 (NOME, APELIDO, TIME)
        VALUES (%s, %s, %s);
        """, (jogador["Nome"].strip(), jogador["Apelido"].strip(), jogador["Time"]))

# Commit e feche a conexão
conn.commit()
conn.close()

print("Dados dos jogadores foram inseridos na tabela 'jogadores_2023'.")
