import requests
from bs4 import BeautifulSoup
import json

def atualizar_assist_Json():
    url = 'https://www.espn.com.br/futebol/estatisticas/_/liga/BRA.1/vista/gols'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Faz o download da página com o cabeçalho definido
    response = requests.get(url, headers=headers)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Analisa a página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra todas as tabelas com a classe Table__Scroller
        tabelas = soup.find_all('div', class_='Table__Scroller')

        # Inicializa uma lista para armazenar todos os dados
        todos_os_dados = []

        # Itera sobre cada tabela encontrada
        for tabela in tabelas:
            # Inicializa uma lista para armazenar os dados da tabela atual
            dados = []

            # Itera sobre as linhas da tabela
            for linha in tabela.find_all('tr'):
                dados_item = {}

                # Encontrar o nome do jogador
                nome_jogador = linha.select_one('td:nth-child(2) span a')
                if nome_jogador:
                    dados_item['Nome'] = nome_jogador.text.strip()

                # Encontrar o time do jogador
                time_jogador = linha.select_one('td:nth-child(3) span a')
                if time_jogador:
                    dados_item['Time'] = time_jogador.text.strip()

                # Encontrar o número de partidas do jogador
                partidas_jogador = linha.select_one('td:nth-child(4) span')
                if partidas_jogador:
                    dados_item['Partidas'] = partidas_jogador.text.strip()

                # Encontrar o número de assistências do jogador
                assist_jogador = linha.select_one('td:nth-child(5) span')
                if assist_jogador:
                    dados_item['Assistencias'] = assist_jogador.text.strip()

                # Adicione os dados do item à lista
                dados.append(dados_item)

            # Adiciona os dados da tabela atual à lista geral
            todos_os_dados.append({f"tabela_{tabelas.index(tabela) + 1}": dados})

        # Exporta todos os dados para um arquivo JSON
        with open('assistencias.json', 'w', encoding='utf-8') as json_file:
            json.dump(todos_os_dados, json_file, ensure_ascii=False, indent=4)
            print("Todos os dados exportados para 'assistencias.json'.")
    else:
        print("Erro ao fazer a solicitação HTTP:", response.status_code)


atualizar_assist_Json()
