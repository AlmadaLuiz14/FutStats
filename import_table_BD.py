import requests
from bs4 import BeautifulSoup
import psycopg2

def extrair_dados_tabela(url):
    # Faz o download da página
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Analisa a página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra a tabela de classificação
        tabela = soup.find('table')

        # Inicializa uma lista para armazenar os dados das equipes
        dados_equipes = []

        # Itera sobre as linhas da tabela
        for linha in tabela.find_all('tr'):
            dados_equipe = {}

            # Encontra a classificação da equipe
            classificacao = linha.find('b', class_=['m-l-10 sobe', 'm-l-10' , 'm-l-10 desce'])
            if classificacao:
                dados_equipe['Classificação'] = classificacao.text.strip()

            # Encontra o nome da equipe
            nome = linha.find('span', class_='hidden-xs')
            if nome:
                dados_equipe['Nome'] = nome.text.strip()
            
            # Encontra os Pontos da equipe
            pontos = linha.find('th', scope='row')
            if pontos:
                dados_equipe['Pontos'] = pontos.text.strip()
                

            # Encontra os outros dados da equipe, como vitórias, empates, derrotas, etc.
            dados = linha.find_all(['td', 'th'])
            if len(dados) >= 9:
                dados_equipe['Jogos'] = dados[2].text.strip()
                dados_equipe['Vitórias'] = dados[3].text.strip()
                dados_equipe['Empates'] = dados[4].text.strip()
                dados_equipe['Derrotas'] = dados[5].text.strip()
                dados_equipe['Gols Prós'] = dados[6].text.strip()
                dados_equipe['Gols Contra'] = dados[7].text.strip()
                dados_equipe['Saldo de Gols'] = dados[8].text.strip()
                dados_equipe['Cartões Amarelos'] = dados[9].text.strip()
                dados_equipe['Cartões Vermelhos'] = dados[10].text.strip()
                dados_equipe['Porcentagem de Vitórias'] = dados[11].text.strip()

                # Adicione os dados da equipe à lista
                dados_equipes.append(dados_equipe)

        return dados_equipes

    else:
        print("Erro ao fazer a solicitação HTTP:", response.status_code)

def salvar_dados_no_postgresql(dados_equipes):
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
    tabela = "classificacao_2023"

    # Inserir os dados na tabela
    for dados in dados_equipes:
        cursor.execute(
            f"INSERT INTO {tabela} (Classificacao, Nome, Pontos, Jogos, Vitórias, Empates, Derrotas, Gols_Pros, Gols_Contra, Saldo_de_Gols, Cartoes_Amarelos, Cartoes_Vermelhos, Porcentagem_de_Vitorias) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                dados.get('Classificação', None),
                dados.get('Nome', None),
                dados.get('Pontos', None),
                dados.get('Jogos', None),
                dados.get('Vitórias', None),
                dados.get('Empates', None),
                dados.get('Derrotas', None),
                dados.get('Gols Prós', None),
                dados.get('Gols Contra', None),
                dados.get('Saldo de Gols', None),
                dados.get('Cartões Amarelos', None),
                dados.get('Cartões Vermelhos', None),
                dados.get('Porcentagem de Vitórias', None)
            )
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023'
    dados_equipes = extrair_dados_tabela(url)
    
    if dados_equipes:
        salvar_dados_no_postgresql(dados_equipes)
        print("Dados salvos no banco de dados PostgreSQL.")
