import psycopg2

# Configuração do PostgreSQL
conn = psycopg2.connect(
    database="FutStats",
    user="postgres",
    password="postG000", # altere aqui a senha do seu postgres
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Tabela Time
cursor.execute("""
CREATE TABLE IF NOT EXISTS Time (
    NOME TEXT PRIMARY KEY NOT NULL,
    ESCUDO TEXT,
    PNTS INT GENERATED ALWAYS AS ((VIT * 3) + EMP) STORED,
    VIT INT,
    DER INT,
    EMP INT,
    TECNICO SERIAL,
    GP INT,
    GC INT,
    SC INT GENERATED ALWAYS AS (GP - GC) STORED 
);
""")

# Tabela Jogador
cursor.execute("""
CREATE TABLE IF NOT EXISTS Jogador (
    COD_JOG SERIAL PRIMARY KEY NOT NULL,
    NOME TEXT,
    POS TEXT,
    ASS INT,
    GOLS INT,
    GOLS_C INT,
    TIPO_TEC BOOLEAN,
    TIME_NOME TEXT REFERENCES Time (NOME)
);
""")

# Tabela Jogo
cursor.execute("""
CREATE TABLE IF NOT EXISTS Jogo (
    PLACAR TEXT,
    LOCAL TEXT PRIMARY KEY,
    DATA DATE PRIMARY KEY,
    DIA INT,
    MES INT,
    HOR_INICIO TIME,
    HOR_TERMINO TIME,
    PROR INTERVAL GENERATED ALWAYS AS ((HOR_INICIO - HOT_FIM) - 90) STORED,
    TIME1_NOME TEXT REFERENCES Time(NOME),
    TIME2_NOME TEXT REFERENCES Time(NOME)
);
""")

# Tabela Torneio
cursor.execute("""
CREATE TABLE IF NOT EXISTS Torneio (
    ANO INT PRIMARY KEY NOT NULL,
    SERIE TEXT PRIMARY KEY NOT NULL
);
""")

cursor.execute("""
ALTER TABLE Time
	ADD CONSTRAINT tecnico_fk_jog FOREIGN KEY (TECNICO) REFERENCES Jogador (COD_JOG)
""")

# Fechar a conexão
conn.commit()
conn.close()
