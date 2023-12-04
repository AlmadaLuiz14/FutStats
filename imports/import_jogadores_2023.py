import requests
from bs4 import BeautifulSoup
import json

# Lista de URLs para os times da Série A
times_urls = [
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20003",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/59897",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20052",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/61377",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/60175",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20001",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/61590",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/59849",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20800",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20016",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20014",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20048",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20028",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20013",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20011",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20002",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20007",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20008",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/20005",
    "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023/60646"
]


# Inicializa uma lista para armazenar os dados dos jogadores
jogadores = []

for url in times_urls:
    # Faz o download da página
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Analisa a página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra a tabela de jogadores
        table = soup.find(class_='table m-t-30')
        
        for tbody in table.find_all('tbody'):
            for tr_element in tbody.find_all('tr'):
                th_element = tr_element.find('th')
                td_element = tr_element.find('td')
                titles = tr_element.find('img')
                nome_jogador = th_element.get_text()
                apelido = td_element.get_text()
                time = titles.get('title') if titles else "Team name not found"
                
                jogadores.append({
                    "Nome": nome_jogador,
                    "Apelido": apelido,
                    "Time": time
                })

    else:
        print(f"Erro ao fazer a solicitação HTTP para {url}")

# Crie um conjunto para acompanhar os nomes dos jogadores
nomes_jogadores = set()

# Crie uma nova lista para armazenar os jogadores sem duplicatas
jogadores_sem_duplicatas = []

# Percorra a lista de jogadores
for jogador in jogadores:
    nome = jogador['Nome'].strip()
    # Verifique se o nome do jogador já está no conjunto
    if nome not in nomes_jogadores:
        nomes_jogadores.add(nome)
        jogadores_sem_duplicatas.append(jogador)

# Salve os dados sem duplicatas em um novo arquivo JSON
with open('jogadores_serie_a.json', 'w', encoding='utf-8') as novo_json_file:
    json.dump(jogadores_sem_duplicatas, novo_json_file, ensure_ascii=False, indent=4)

print('dados salvos em "jogadores_serie_a.json".')