import requests
from bs4 import BeautifulSoup
import psycopg2

def extrair_dados_tabela(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela_artilheiros = soup.find('table', class_='border-body')
        
        artilheiros = []

        if tabela_artilheiros:
            for linha in tabela_artilheiros.find_all('tr'):
                dados_artilheiro = {}
                
                nome_jogador = linha.find('a')
                if nome_jogador:
                    dados_artilheiro['Nome'] = nome_jogador.text.strip()

                time_jogador = linha.find('img')
                if time_jogador:
                    dados_artilheiro['Time'] = time_jogador['title']

                gols_jogador = linha.find('th')
                if gols_jogador:
                    gols_text = gols_jogador.text.strip()
                    if gols_text.isdigit():
                        dados_artilheiro['Gols'] = gols_text
                
                if dados_artilheiro:
                    artilheiros.append(dados_artilheiro)
        
        return artilheiros
    else:
        print("Erro ao fazer a solicitação HTTP:", response.status_code)
        return []

def salvar_dados_no_postgresql(dados_arbitros):
    conn = psycopg2.connect(
        database="FutStats",
        user="postgres",
        password="postG000",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    tabela = "artilheiros_2023"

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {tabela} (
        Nome TEXT,
        Time TEXT,
        Gols INT
    );
    """)

    for dados in dados_arbitros:
        cursor.execute(
            f"INSERT INTO {tabela} (Nome, Time, Gols) VALUES (%s, %s, %s)",
            (
                dados.get('Nome', None),
                dados.get('Time', None),
                int(dados.get('Gols', 0))
            )
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023'
    dados_arbitros = extrair_dados_tabela(url)
    
    if dados_arbitros:
        salvar_dados_no_postgresql(dados_arbitros)
        print("Dados salvos no banco de dados PostgreSQL.")
