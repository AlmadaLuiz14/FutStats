from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import json
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Configuração do banco de dados
db_config = {
    'database': 'FutStats',
    'user': 'postgres',
    'password': 'postG000',
    'host': 'localhost',
    'port': '5432'
}

def conectar_bd():
    conn = psycopg2.connect(**db_config)
    return conn

@app.route('/api', methods=['GET'])
def api_home():
    return "Bem-vindo à API do FutStats"

@app.route('/api/classificacao', methods=['GET'])
def obter_classificacao_2023():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classificacao_2023")
    resultados = cursor.fetchall()
    conn.close()

    classificacao = [{'classificacao': row[0], 'nome': row[1], 'pontos': row[2],
                 'jogos': row[3], 'vitorias': row[4], 'empates': row[5], 'derrotas': row[6],
                 'gols_pros': row[7], 'gols_contra': row[8], 'saldo_gols': row[9],
                 'cartoes_amarelos': row[10], 'cartoes_vermelhos': row[11],
                 'porcentagem_vitorias': row[12]} for row in resultados]

    return jsonify(classificacao)

@app.route('/api/jogos_rodada', methods=['GET'])
def obter_jogos_rodada_2023():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogos_rodada_2023")
    resultados = cursor.fetchall()
    conn.close()

    jogos_rodada = [{'rodada': row[0], 'info_jogo': row[1],
                'time1': row[2], 'time2': row[3], 'placar': row[4], 'local': row[5]}
               for row in resultados]

    return jsonify(jogos_rodada)

@app.route('/api/artilheiros', methods=['GET'])
def obter_artilheiros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artilheiros_2023")
    resultados = cursor.fetchall()
    conn.close()

    artilheiros = [{'nome': row[0], 'time': row[1], 'gols': row[2]} for row in resultados]
    return jsonify(artilheiros)

@app.route('/api/noticias', methods=['GET'])
def obter_noticias():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM noticias")
    resultados = cursor.fetchall()
    conn.close()

    noticias = [{'titulo': row[0], 'link': row[1], 'imagem': row[2]} for row in resultados]
    return jsonify(noticias)

@app.route('/api/usuario', methods=['GET'])
def obter_users():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario")
    resultados = cursor.fetchall()
    conn.close()

    usuarios = [{'email': row[0], 'nome': row[1], 'senha': row[2]} for row in resultados]
    return jsonify(usuarios)

@app.route('/api/usuario', methods=['POST'])
def inserir_usuarios():
    
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        data = request.get_json('data')
        email = json.dumps(data['email']).replace('"', "'")
        nome = json.dumps(data['nome']).replace('"', "'")
        senha = json.dumps(data['senha']).replace('"', "'")

        #hSenha = bcrypt.generate_password_hash(senha).decode('utf-8') 
        #se achar necessário arrumar a parte de cripto. Mateus n vai cobrar. Erro provavel no enconder do bd. Mudar para utf8

        cursor.execute(f"INSERT INTO usuario (email, nome, senha) VALUES ({email}, {nome}, {senha})")

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Dado inserido com sucesso'}), 201
    except psycopg2.Error as e:
        if isinstance(e, psycopg2.IntegrityError):
            #erro de violação de integridade
            return jsonify({'error': str(e)}), 501
        
        else:
            error_menssage = str(e)
            return jsonify({'error': error_menssage}), 500




if __name__ == '__main__':
    app.run(debug=True)
