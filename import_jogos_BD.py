import requests
from bs4 import BeautifulSoup
import psycopg2

# Função para salvar os dados no PostgreSQL
def salvar_jogos_no_postgresql(jogos_data):
    # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="84650052",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    
    # Substitua "nome_da_sua_tabela" pelo nome da sua tabela no PostgreSQL
    tabela = "jogos_rodada_2023"

    # Criar a tabela se ela não existir
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {tabela} (
        Rodada INT,
        Info_Jogo TEXT,
        Time1 TEXT,
        Time2 TEXT,
        Placar TEXT,
        Local TEXT
    );
    """)

    # Inserir os dados na tabela
    for rodada, jogos in jogos_data.items():
        for jogo in jogos:
            cursor.execute(
                f"INSERT INTO {tabela} (Rodada, Info_Jogo, Time1, Time2, Placar, Local) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    int(rodada[6:]),  # Extraindo o número da rodada
                    jogo.get('Info_Jogo', None),
                    jogo.get('Time1', None),
                    jogo.get('Time2', None),
                    jogo.get('Placar', None),
                    jogo.get('Local', None)
                )
            )

    conn.commit()  # Adicione esta linha para confirmar as alterações no banco de dados
    cursor.close()  # Feche o cursor
    conn.close()    # Feche a conexão
    
    # URL da página
url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023'

# Faz o download da página
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisa a página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra o elemento que contém todas as rodadas
    rodadas_element = soup.select("#menu-panel > article > div.container > div > div > section > div.col-md-4.col-lg-3 > aside > div > div")

    if rodadas_element:
        # Inicializa um dicionário para armazenar os dados de todas as rodadas
        todos_jogos = {}

        # Itera pelas rodadas
        for index, rodada_element in enumerate(rodadas_element, start=1):
            # Encontra todos os jogos da rodada
            jogos_rodada = rodada_element.find_all('li')

            # Inicializa uma lista para armazenar os dados dos jogos da rodada atual
            jogos = []

            for jogo in jogos_rodada:
                # Extrai informações sobre o jogo
                info_jogo = jogo.find(class_='partida-desc').text.strip()
                time1 = jogo.find(class_='time pull-left').text.strip()
                time2 = jogo.find(class_='time pull-right').text.strip()
                placar = jogo.find('strong').text.strip()
                local_element = jogo.find_all('span')
                # Tamanho mínimo para ser considerado um placar
                tamanho_minimo_local = 5

                if len(local_element) > 4 and len(local_element[4].text.strip()) > tamanho_minimo_local:
                    local = local_element[4].text.strip()
                else:
                    local_element = jogo.find('div', class_='partida-desc')
                    local = local_element.get_text(strip=True) if local_element else '-'

                local = local.replace('Como foi o jogo', '')

                # Adicione os dados do jogo à lista de jogos
                jogo_info = {
                    'Info_Jogo': info_jogo,
                    'Time1': time1,
                    'Time2': time2,
                    'Placar': placar,
                    'Local': local
                }
                jogos.append(jogo_info)

            # Adicione os dados da rodada atual ao dicionário de todas as rodadas
            todos_jogos["Rodada{}".format(index)] = jogos

        # Salva os dados no banco de dados PostgreSQL
        salvar_jogos_no_postgresql(todos_jogos)
        print("Dados de todas as rodadas salvos no banco de dados PostgreSQL.")
    else:
        print("Elemento 'div' das rodadas não encontrado.")
else:
    print("Erro ao fazer a solicitação HTTP:", response.status_code)
