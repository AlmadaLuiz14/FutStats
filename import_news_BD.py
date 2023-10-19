import requests
from bs4 import BeautifulSoup
import json
import psycopg2

# Função para salvar os dados no PostgreSQL
def salvar_noticias_no_postgresql(noticias_data):
    # Configuração do PostgreSQL
    conn = psycopg2.connect(
        database="FutStats",  # Substitua pelo nome do seu banco de dados
        user="postgres",
        password="84650052",  # Substitua pela senha do seu banco de dados
        host="localhost",  # Substitua pelo host do seu banco de dados
        port="5432"  # Substitua pela porta do seu banco de dados
    )
    cursor = conn.cursor()
    
    # Substitua "nome_da_sua_tabela" pelo nome da sua tabela no PostgreSQL
    tabela = "noticias_ge"

    # Criar a tabela se ela não existir
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {tabela} (
        Título TEXT,
        Link TEXT,
        Imagem TEXT
    );
    """)

    # Inserir os dados na tabela
    for noticia in noticias_data:
        cursor.execute(
            f"INSERT INTO {tabela} (Título, Link, Imagem) VALUES (%s, %s, %s)",
            (
                noticia.get('Título', None),
                noticia.get('Link', None),
                noticia.get('Imagem', None)
            )
        )

    conn.commit()
    conn.close()

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
            
            # Salva os dados no banco de dados PostgreSQL
            salvar_noticias_no_postgresql(news_data)
            print("Dados das notícias salvos no banco de dados PostgreSQL.")
        else:
            print("Contêiner de notícias não encontrado.")
    else:
        print("Erro ao fazer a solicitação HTTP:", response.status_code)

atualizar_noticias()
