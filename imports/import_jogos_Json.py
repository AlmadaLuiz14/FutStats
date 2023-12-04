import requests
from bs4 import BeautifulSoup
import json
import re

def atualizar_jogos_Json():
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
            todos_jogos = {"jogosinfo": {}}

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
                    tamanho_minimo_local = 12

                    local = local_element[4].text.strip() if len(local_element) > 4 else ""
                    local1 = jogo.find('div', class_='partida-desc')
                    local2 = jogo.select("span.partida-desc:last-child")
                    local3 = local_element[3].text.strip() if len(local_element) > 3 else ""
                    local4 = local_element[5].text.strip() if len(local_element) > 5 else ""

                    maior_local = local  # Comece com o primeiro local como o maior

                    if local1 and len(local1.get_text(strip=True)) > len(maior_local):
                        maior_local = local1.get_text(strip=True)

                    if local2 and len(local2[0].text.strip()) > len(maior_local):
                        maior_local = local2[0].text.strip()

                    if local3 and len(local3) > len(maior_local):
                        maior_local = local3

                    if local4 and len(local4) > len(maior_local):
                        maior_local = local4

                    local = maior_local.replace('Como foi o jogo', '')
                    local = local.replace('Detalhes do jogo', '')

                    # Encontre os elementos que contêm as imagens dos brasões para cada time
                    brasao_time1_element = jogo.find('div', class_='time pull-left').find('img')
                    brasao_time2_element = jogo.find('div', class_='time pull-right').find('img')

                    # Extraia os URLs das imagens dos brasões
                    brasao_time1_url = brasao_time1_element['src'] if brasao_time1_element else ''
                    brasao_time2_url = brasao_time2_element['src'] if brasao_time2_element else ''

                    # Adicione os URLs dos brasões aos dados do jogo
                    jogo_info = {
                        'Info_Jogo': info_jogo,
                        'Time1': time1,
                        'BrasaoTime1': brasao_time1_url,
                        'Time2': time2,
                        'BrasaoTime2': brasao_time2_url,
                        'Placar': placar,
                        'Local': local
                    }
                    jogos.append(jogo_info)

                # Adicione os dados da rodada atual ao dicionário de todas as rodadas
                todos_jogos["jogosinfo"]["Rodada{}".format(index)] = jogos
                
            # Exporta os dados de todas as rodadas para um arquivo JSON
            with open('jogos_rodada.json', 'w', encoding='utf-8') as json_file:
                json.dump(todos_jogos, json_file, ensure_ascii=False, indent=4)
                print("Dados de todas as rodadas exportados para 'jogos_rodada.json'.")
        else:
            print("Elemento 'div' das rodadas não encontrado.")
    else:
        print("Erro ao fazer a solicitação HTTP:", response.status_code)

atualizar_jogos_Json()