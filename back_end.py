from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager ,create_access_token, jwt_required, get_jwt_identity
import psycopg2
import json
from werkzeug.security import check_password_hash, generate_password_hash
from simulação.converte_simula import converte_simula
from simulação.converte_jogos import converte_jogos


app = Flask(__name__)
CORS(app)
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

@app.route('/api/simula', methods=['GET'])
def obter_simula_2023():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM simula_2023")
    resultados = cursor.fetchall()
    conn.close()

    classificacao = [{'classificacao': row[0], 'brasao': row[1], 'nome': row[2], 'pontos': row[3],
                 'jogos': row[4], 'vitorias': row[5], 'empates': row[6], 'derrotas': row[7],
                 'gols_pros': row[8], 'gols_contra': row[9], 'saldo_gols': row[10],
                 'cartoes_amarelos': row[11], 'cartoes_vermelhos': row[12],
                 'porcentagem_vitorias': row[13]} for row in resultados]

    return jsonify(classificacao)

@app.route('/api/simula', methods=['POST'])
def simular_partidas():
    try:
        print("Requisição POST recebida para /api/simula")

        # Obtenha os dados da solicitação
        data = request.json

        # Extraindo dados da solicitação
        time1 = data.get('time1')
        sigla1 = data.get('sigla1')
        input1 = data.get('input1')
        time2 = data.get('time2')
        sigla2 = data.get('sigla2')
        input2 = data.get('input2')
        passado = data.get('passado')
        placar1 = data.get('placar1')
        placar2 = data.get('placar2')

        # Calcula os resultados da simulação
        goalsFor1 = max(input1, 0)
        goalsAgainst1 = max(input2, 0)
        goalsFor2 = max(input2, 0)
        goalsAgainst2 = max(input1, 0)
        

        print(f"Simulação para {time1['nome']} - Gols Prós: {goalsFor1}, Gols Contra: {goalsAgainst1}")
        print(f"Simulação para {time2['nome']} - Gols Prós: {goalsFor2}, Gols Contra: {goalsAgainst2}")

        # Adiciona os resultados ao banco de dados PostgreSQL
        conn = conectar_bd()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE jogos_simula_2023
            SET placar = %s
            WHERE time1 = %s AND time2 = %s
        """, ("%s x %s" % (input1, input2), sigla1, sigla2))
                
        #verifica se é jogo passado
        if passado:
            
            real = placar1 - placar2
            diff1 = input1 - placar1
            diff2 = input2 - placar2
            
            if real > 0: #time 1 venceu o jogo real
                # Atualiza os dados para o time 1
                if goalsFor1 > goalsFor2:  # Time 1 vence
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                elif goalsFor1 < goalsFor2:  # Time 1 perde
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos - 3,
                            Vitorias = Vitorias - 1,
                            Derrotas = Derrotas + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias - 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                else:  # Empate
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos - 2,
                            Vitorias = Vitorias - 1,
                            Empates = Empates + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias - 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                    
            elif real == 0: #time 1 empatou o jogo real
                    # Atualiza os dados para o time 1
                if goalsFor1 > goalsFor2:  # Time 1 vence
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos + 2,
                            Empates = Empates - 1,
                            Vitorias = Vitorias + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias + 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                elif goalsFor1 < goalsFor2:  # Time 1 perde
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos - 1,
                            Empates = Empates - 1,
                            Derrotas = Derrotas + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                else:  # Empate
                    cursor.execute("""
                        UPDATE simula_2023
                        SET 
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                    
            elif real < 0: #time 1 perdeu o jogo real    
                  # Atualiza os dados para o time 1
                if goalsFor1 > goalsFor2:  # Time 1 vence
                    cursor.execute("""
                        UPDATE simula_2023
                        SET 
                            Pontos = Pontos + 3,
                            Vitorias = Vitorias + 1,
                            Derrotas = Derrotas - 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias + 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                elif goalsFor1 < goalsFor2:  # Time 1 perde
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                else:  # Empate
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos + 1,
                            Empates = Empates + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))  
                    
            #atualiza time 2        
            if real < 0: #time 2 venceu o jogo real
                # Atualiza os dados para o time 2
                if goalsFor2 > goalsFor1:  # Time 2 vence
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff2, diff1, diff2 - diff1, time2['nome']))
                elif goalsFor2 < goalsFor1:  # Time 2 perde
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos - 3,
                            Vitorias = Vitorias - 1,
                            Derrotas = Derrotas + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias - 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff2, diff1, diff2 - diff1, time2['nome']))
                else:  # Empate
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos - 2,
                            Vitorias = Vitorias - 1,
                            Empates = Empates + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias - 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff2, diff1, diff2 - diff1, time2['nome']))
                    
            elif real == 0: #time 2 empatou o jogo real
                    # Atualiza os dados para o time 2
                if goalsFor2 > goalsFor1:  # Time 1 vence
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos + 2,
                            Empates = Empates - 1,
                            Vitorias = Vitorias + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias + 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff2, diff1, diff2 - diff1, time2['nome']))
                elif goalsFor2 < goalsFor1:  # Time 1 perde
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos - 1,
                            Empates = Empates - 1,
                            Derrotas = Derrotas + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff2, diff1, diff2 - diff1, time2['nome']))
                else:  # Empate
                    cursor.execute("""
                        UPDATE simula_2023
                        SET 
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff2, diff1, diff2 - diff1, time2['nome']))
                    
            elif real > 0: #time 2 perdeu o jogo real    
                  # Atualiza os dados para o time 1
                if goalsFor1 > goalsFor2:  # Time 1 vence
                    cursor.execute("""
                        UPDATE simula_2023
                        SET 
                            Pontos = Pontos + 3,
                            Vitorias = Vitorias + 1,
                            Derrotas = Derrotas - 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias + 1) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                elif goalsFor1 < goalsFor2:  # Time 1 perde
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))
                else:  # Empate
                    cursor.execute("""
                        UPDATE simula_2023
                        SET
                            Pontos = Pontos + 1,
                            Empates = Empates + 1,
                            Gols_Pros = Gols_Pros + %s,
                            Gols_Contra = Gols_Contra + %s,
                            Saldo_de_Gols = Saldo_de_Gols + %s,
                            Porcentagem_de_Vitorias = (Vitorias) / Jogos::FLOAT * 100
                        WHERE Nome = %s
                    """, (diff1, diff2, diff1 - diff2, time1['nome']))  
            
                
        # não é jogo passado:
        elif passado == False :
            # Atualiza os dados para o time 1
            if goalsFor1 > goalsFor2:  # Time 1 vence
                cursor.execute("""
                    UPDATE simula_2023
                    SET
                        Pontos = Pontos + 3,
                        Jogos = Jogos + 1,
                        Vitorias = Vitorias + 1,
                        Gols_Pros = Gols_Pros + %s,
                        Gols_Contra = Gols_Contra + %s,
                        Saldo_de_Gols = Saldo_de_Gols + %s,
                        Porcentagem_de_Vitorias = (Vitorias + 1) / Jogos::FLOAT * 100
                    WHERE Nome = %s
                """, (goalsFor1, goalsAgainst1, goalsFor1 - goalsAgainst1, time1['nome']))
            elif goalsFor1 < goalsFor2:  # Time 1 perde
                cursor.execute("""
                    UPDATE simula_2023
                    SET
                        Jogos = Jogos + 1,
                        Derrotas = Derrotas + 1,
                        Gols_Pros = Gols_Pros + %s,
                        Gols_Contra = Gols_Contra + %s,
                        Saldo_de_Gols = Saldo_de_Gols + %s,
                        Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                    WHERE Nome = %s
                """, (goalsFor1, goalsAgainst1, goalsFor1 - goalsAgainst1, time1['nome']))
            else:  # Empate
                cursor.execute("""
                    UPDATE simula_2023
                    SET
                        Pontos = Pontos + 1,
                        Jogos = Jogos + 1,
                        Empates = Empates + 1,
                        Gols_Pros = Gols_Pros + %s,
                        Gols_Contra = Gols_Contra + %s,
                        Saldo_de_Gols = Saldo_de_Gols + %s,
                        Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                    WHERE Nome = %s
                """, (goalsFor1, goalsAgainst1, goalsFor1 - goalsAgainst1, time1['nome']))


            # Atualiza os dados para o time 2
            if goalsFor2 > goalsFor1:  # Time 2 vence
                cursor.execute("""
                    UPDATE simula_2023
                    SET
                        Pontos = Pontos + 3,
                        Jogos = Jogos + 1,
                        Vitorias = Vitorias + 1,
                        Gols_Pros = Gols_Pros + %s,
                        Gols_Contra = Gols_Contra + %s,
                        Saldo_de_Gols = Saldo_de_Gols + %s,
                        Porcentagem_de_Vitorias = (Vitorias + 1) / Jogos::FLOAT * 100
                    WHERE Nome = %s
                """, (goalsFor2, goalsAgainst2, goalsFor2 - goalsAgainst2, time2['nome']))
            elif goalsFor2 < goalsFor1:  # Time 2 perde
                cursor.execute("""
                    UPDATE simula_2023
                    SET
                        Jogos = Jogos + 1,
                        Derrotas = Derrotas + 1,
                        Gols_Pros = Gols_Pros + %s,
                        Gols_Contra = Gols_Contra + %s,
                        Saldo_de_Gols = Saldo_de_Gols + %s,
                        Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                    WHERE Nome = %s
                """, (goalsFor2, goalsAgainst2, goalsFor2 - goalsAgainst2, time2['nome']))
            else:  # Empate
                cursor.execute("""
                    UPDATE simula_2023
                    SET
                        Pontos = Pontos + 1,
                        Jogos = Jogos + 1,
                        Empates = Empates + 1,
                        Gols_Pros = Gols_Pros + %s,
                        Gols_Contra = Gols_Contra + %s,
                        Saldo_de_Gols = Saldo_de_Gols + %s,
                        Porcentagem_de_Vitorias = Vitorias / Jogos::FLOAT * 100
                    WHERE Nome = %s
                """, (goalsFor2, goalsAgainst2, goalsFor2 - goalsAgainst2, time2['nome']))


        conn.commit()
        conn.close()

        return jsonify({'message': 'Dados inseridos com sucesso no banco de dados.'}), 200

    except Exception as e:
        print(f"Erro durante a simulação: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-simulation', methods=['POST'])
def reset_simulation():
    try:
        print("Requisição POST recebida para /api/reset-simulation")

        # Chame a função converte_simula para resetar a simulação
        converte_simula()
        converte_jogos()

        return jsonify({'message': 'Simulação resetada com sucesso.'}), 200
    except Exception as e:
        print(f"Erro ao resetar a simulação: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
