import requests
from bs4 import BeautifulSoup
import json

def atualizar_noticias():

    # URL da página que você deseja analisar
    url = 'https://ge.globo.com/'

    # Faz o download da página
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Analisa a página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra o elemento HTML que contém todas as notícias
        news_container = soup.select_one("#feed-placeholder > div > div > div._evg > div > div > div > div:nth-child(1) > div > div > div > div.feed-media-wrapper > a > div > picture > img")
        
        if news_container:
            # Inicializa uma lista para armazenar os dados das notícias
            news_data = []
            
            # Encontra todas as notícias dentro do contêiner
            news_items = soup.select(".feed-post-body-title a")

            # Itera sobre as notícias e adiciona seus títulos, links e imagens à lista
            for news_item in news_items:
                title = news_item.text
                link = news_item["href"] if "href" in news_item.attrs else ""
                image = news_item.find_previous("img")["src"] if news_item.find_previous("img") else ""
                news_data.append({
                    "Título": title,
                    "Link": link,
                    "Imagem": image
                })

            noticias = {"noticias": news_data}
            
            # Exporta os dados para um arquivo JSON
            with open("noticias_ge.json", "w", encoding="utf-8") as json_file:
                json.dump(noticias, json_file, ensure_ascii=False, indent=4)
            
            print("Dados das notícias exportados para 'noticias_ge.json'.")
        else:
            print("Contêiner de notícias não encontrado.")
    else:
        print("Erro ao fazer a solicitação HTTP:", response.status_code)

atualizar_noticias()