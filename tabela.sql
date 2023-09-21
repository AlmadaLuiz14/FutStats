-- Tabela de Times
CREATE TABLE IF NOT EXISTS Times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    pontos INTEGER,
    jogos INTEGER,
    vitorias INTEGER,
    empates INTEGER,
    derrotas INTEGER,
    gols_marcados INTEGER,
    gols_sofridos INTEGER,
    saldo_gols INTEGER,
    porcentagem_vitorias REAL
);

-- Tabela de Jogadores
CREATE TABLE IF NOT EXISTS Jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    time_id INTEGER,  -- Referência ao time a que o jogador pertence
    cartoes_amarelos INTEGER,
    cartoes_vermelhos INTEGER,
    gols_marcados INTEGER,
    assistencias INTEGER
);

-- Tabela de Jogos
CREATE TABLE IF NOT EXISTS Jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    hora TIME,
    estadio TEXT,
    time_casa_id INTEGER,  -- Referência ao time da casa
    time_visitante_id INTEGER,  -- Referência ao time visitante
    placar_time_casa INTEGER,
    placar_time_visitante INTEGER
);
