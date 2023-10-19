import requests
from bs4 import BeautifulSoup
import json

# URL da página
url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023'

# Faz o download da página
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisa a página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra a tabela de artilheiros
    tabela_artilheiros = soup.find('table', class_='border-body')
    
    # Inicializa uma lista para armazenar os dados dos artilheiros
    artilheiros = []

    if tabela_artilheiros is not None:
        # Agora você pode iterar sobre as linhas e extrair os artilheiros
        for linha in tabela_artilheiros.find_all('tr'):
            dados_artilheiro = {}

            # Encontra o nome do jogador
            nome_jogador = linha.find('a')
            if nome_jogador:
                dados_artilheiro['Nome'] = nome_jogador.text.strip()

            # Encontra o time do jogador
            time_jogador = linha.find('img')
            if time_jogador:
                dados_artilheiro['Time'] = time_jogador['title']

            # Encontra o número de gols do jogador
            gols_jogador = linha.find('th')
            if gols_jogador:
                gols_text = gols_jogador.text.strip()
                if 1 <= len(gols_text) <= 2:
                    dados_artilheiro['Gols'] = gols_text
            # Adicione os dados do artilheiro à lista
            artilheiros.append(dados_artilheiro)

        artilharia = {"artilharia": artilheiros}
        # Exporta os artilheiros para um arquivo JSON
        with open('artilheiros.json', 'w', encoding='utf-8') as json_file:
            json.dump(artilharia, json_file, ensure_ascii=False, indent=4)
            print("Dados dos artilheiros exportados para 'artilheiros.json'.")
    else:
        print("Tabela de artilheiros não encontrada.")

else:
    print("Erro ao fazer a solicitação HTTP:", response.status_code)
