import requests
from bs4 import BeautifulSoup
import json

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
            
            brasao_time = linha.find('img')
            if brasao_time:
                dados_equipe['BrasaoTime'] = brasao_time['src']
            
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

def atualizar_tabela_Json():

    url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023'
    dados_equipes = extrair_dados_tabela(url)

    tabela = {"tabela": dados_equipes}
    # Salvar os dados em um arquivo JSON
    with open('classificacao_brasileirao_2023.json', 'w', encoding='utf-8') as json_file:
        json.dump(tabela, json_file, ensure_ascii=False, indent=4)
        print("Dados da classificação exportados para 'classificacao_brasileirao.json'.")

atualizar_tabela_Json()