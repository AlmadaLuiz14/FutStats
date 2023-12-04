import json
from unidecode import unidecode

def criar_apelido(nome):
    # Obter o último nome
    partes_nome = nome.split()
    ultimo_nome = partes_nome[-1]

    # Remover acentos
    apelido = unidecode(ultimo_nome)

    return apelido

def criar_apelidos_na_tabela(tabela):
    mapeamento_times = {
        "Grêmio": "Grêmio-RS",
        "Atlético-MG": "Atlético Mineiro S.a.f.-MG",
        "Flamengo": "Flamengo-RJ",
        "Palmeiras": "Palmeiras-SP",
        "Fluminense": "Fluminense-RJ",
        "Red Bull Bragantino": "Red Bull Bragantino-SP",
        "Goiás": "Goiás-GO",
        "Santos": "Santos-SP",
        "Internacional": "Internacional-RS",
        "Botafogo": "Botafogo-RJ",
        "Coritiba": "Coritiba S.a.f.-PR",
        "São Paulo": "São Paulo-SP",
        "Bahia": "Bahia-BA",
        "Athletico-PR": "Athletico Paranaense-PR",
        "América-MG": "America Saf-MG",
        "Vasco da Gama": "Vasco da Gama S.a.f.-RJ",
        "Cruzeiro": "Cruzeiro Saf-MG",
        "Fortaleza": "Fortaleza-CE",
        "Corinthians": "Corinthians-SP",
        "Cuiabá": "Cuiabá Saf-MT"
    }

    for item in tabela:
        for jogador in item.get("tabela_2", []):
            nome_time = jogador.get("Time", "")
            nome_time_convertido = mapeamento_times.get(nome_time, nome_time)
            jogador["Time"] = nome_time_convertido

            nome_jogador = jogador.get("Nome", "")
            apelido = criar_apelido(nome_jogador)
            jogador["Apelido"] = apelido

def converte_time():
    # Carregar a tabela de assistências
    with open("assistencias.json", "r", encoding="utf-8") as arquivo_json:
        tabela_assistencias = json.load(arquivo_json)

    # Criar apelidos na tabela de assistências
    criar_apelidos_na_tabela(tabela_assistencias)

    # Salvar a tabela atualizada com apelidos
    with open("assistencias_time.json", "w", encoding="utf-8") as arquivo_json:
        json.dump(tabela_assistencias, arquivo_json, ensure_ascii=False, indent=4)

    print("Apelidos criados e tabela salva em assistencias_time.json")

converte_time()