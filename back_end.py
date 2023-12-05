from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager ,create_access_token, jwt_required, get_jwt_identity
import psycopg2
import json
from werkzeug.security import check_password_hash, generate_password_hash

#from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
#bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'testezao'
jwt = JWTManager(app)

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

        #hSenha = generate_password_hash(senha)

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
            return jsonify({'error': str(e)}), 500

@app.route('/api/usuario/login', methods=['POST'])
def login():
    conn = conectar_bd()
    cursor = conn.cursor()

    data = request.get_json('data')
    emailU = json.dumps(data['email']).replace('"', "'")
    #senhaU = json.dumps(data['senha']).replace('"', "'")

    cursor.execute(f"SELECT senha, tipo_adm FROM public.usuario WHERE email = {emailU};")
    senhaBd = cursor.fetchone()

    conn.close()
    
    if senhaBd == None:
        return jsonify(access=False)
    elif senhaBd[0] == data['senha']:
        access_token = create_access_token(identity=emailU)
        return jsonify(access=True, access_token=access_token, tipo_adm=senhaBd[1]), 200
    else:
        return jsonify(access=False)

@app.route('/api/protegido', methods=['GET'])
@jwt_required()
def retornaUser():
    email_logado = get_jwt_identity()

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(f"SELECT nome FROM public.usuario WHERE email = {email_logado};")
    nome_logado = cursor.fetchone()

    return jsonify(email=email_logado.replace("'", ""), nome=nome_logado[0]), 200


@app.route('/api/protegido/todosUsers', methods=['GET'])
@jwt_required()
def retornaTodosUsers():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT nome, email FROM public.usuario ORDER BY nome;")
    resultado = cursor.fetchall()
    conn.close()

    users = [{'nome': row[0], 'email': row[1]} for row in resultado]
    
    return jsonify(users)


@app.route("/api/protegido/confereSenha", methods=['POST'])
@jwt_required()
def confereSenha():
    try:
        email_logado = get_jwt_identity()
        data = request.get_json('data')
    
        conn = conectar_bd()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT senha FROM public.usuario WHERE email = {email_logado};")
        senhaBD = cursor.fetchone()

        conn.close()

        if data['senha'] == senhaBD[0]:
            return jsonify(verify=True)
        else:
            return jsonify(verify=False)
    except psycopg2.Error as e:
        print("ERROR", str(e))


@app.route('/api/protegido/newInfos', methods=['POST'])
@jwt_required()
def novasInfos():
    email_logado = get_jwt_identity()
    data = request.get_json('data')
    emailU = json.dumps(data['email']).replace('"', "'")
    nomeU = json.dumps(data['nome']).replace('"', "'")
    
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute(f"UPDATE public.usuario SET email = {emailU}, nome = {nomeU} WHERE email = {email_logado}")
        conn.commit()
        conn.close()

        return jsonify(msg="Informações atualizadas com sucesso")
    except psycopg2.Error as e:
        return jsonify(msg="Erro ao atualizar as informações de usuário", erro=str(e))    
    

@app.route('/api/protegido/deleteUser', methods=['POST'])
@jwt_required()
def deleteUser():
    email_logado = get_jwt_identity()
    data = request.get_json('data')
    emailU = json.dumps(data['email']).replace('"', "'")
    print("AAAAAAAA", email_logado, emailU)
    if email_logado == emailU:
        return jsonify(msg="Não é possível deletar seu próprio usuário", verify=False)

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM public.usuario WHERE email = {emailU};")
    conn.commit()
    conn.close()

    return jsonify(msg="Usuário deletado com sucesso", verify=True)


@app.route('/api/protegido/nAdm', methods=['POST'])
@jwt_required()
def tornaAdm():
    data = request.get_json('data')
    emailU = json.dumps(data['email']).replace('"', "'")

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE public.usuario SET tipo_adm = true WHERE email = {emailU};")
    conn.commit()
    conn.close()

    return jsonify(msg="Novo administrador adicionado com sucesso", verify=True)


@app.route('/api/protegido/tirarAdm', methods=['POST'])
@jwt_required()
def tirarAdm():
    email_logado = get_jwt_identity()
    data = request.get_json('data')
    emailU = json.dumps(data['email']).replace('"', "'")
    if email_logado == emailU:
        return jsonify(msg="Não é possível tirar seu próprio poder administrador", verify=False)


    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE public.usuario SET tipo_adm = false WHERE email = {emailU};")
    conn.commit()
    conn.close()

    return jsonify(msg="Administrador retirado com sucesso", verify=True)


@app.route("/api/usuario/recuperarSenha", methods=['POST'])
def recuperarSenha():
    
    try:
        data = request.get_json('data')
        emailU = json.dumps(data['email']).replace('"', "'")
        senhaU = json.dumps(data['senha']).replace('"', "'")

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM public.usuario WHERE email = {emailU};")
        user = cursor.fetchall()
        if len(user) == 0:
            return jsonify(msg="O email informado não está cadastrado", verify="empty")

        cursor.execute(f"UPDATE public.usuario SET senha = {senhaU} WHERE email = {emailU};")
        conn.commit()
        conn.close()

        return jsonify(msg="Senha alterada com sucesso", verify=True)
    
    except psycopg2.Error as e:
        print("ERRO", str(e))



if __name__ == '__main__':
    app.run(debug=True)
