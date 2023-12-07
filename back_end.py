from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
import json
from functools import wraps
from flask_jwt_extended import JWTManager ,create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity
from simulação.converte_simula import converte_simula
from simulação.converte_jogos import converte_jogos

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'testezao'
jwt = JWTManager(app)

# Configuração do banco de dados PostgreeSQL
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

    classificacao = [{'classificacao': row[0], 'brasao': row[1], 'nome': row[2], 'pontos': row[3],
                 'jogos': row[4], 'vitorias': row[5], 'empates': row[6], 'derrotas': row[7],
                 'gols_pros': row[8], 'gols_contra': row[9], 'saldo_gols': row[10],
                 'cartoes_amarelos': row[11], 'cartoes_vermelhos': row[12],
                 'porcentagem_vitorias': row[13]} for row in resultados]

    return jsonify(classificacao)

@app.route('/api/nova_partida', methods=['POST'])
def nova_partida():
    try:
        # Receba os dados da nova partida do corpo da requisição
        nova_partida = request.json  # Use request.json para obter os dados do corpo da solicitação JSON
        print(nova_partida)
        
        # Validar os campos obrigatórios
        campos_obrigatorios = ['rodada', 'nome1', 'nome2']
        for campo in campos_obrigatorios:
            if campo not in nova_partida or not nova_partida[campo]:
                return jsonify({'error': f'O campo obrigatório "{campo}" está ausente ou vazio.'}), 400

        conn = conectar_bd()
        cursor = conn.cursor()
        

        # Inserir a nova partida na tabela jogos_simula_2023 usando prepared statement
        cursor.execute(
            "INSERT INTO jogos_simula_2023 (Rodada, Info_Jogo, Nome1, Nome2, Placar, Local) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                int(nova_partida.get('rodada', None)),
                nova_partida.get('info_jogo', None),
                nova_partida.get('nome1', None),
                nova_partida.get('nome2', None),
                nova_partida.get('placar', None),
                nova_partida.get('local', None)
            )
        )


        # Commit para efetivar a inserção
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Partida inserida com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': f'Erro ao inserir partida: {str(e)}'}), 500


@app.route('/api/novo_jogador', methods=['POST'])
def inserir_novo_jogador():
    try:
        # Recebe os dados do novo time do corpo da requisição
        novo_jogador = request.json  # force=True para ignorar o cabeçalho Content-Type
        
        print(novo_jogador)
        
        # Validar os campos obrigatórios
        campos_obrigatorios = ['nome', 'time']
        for campo in campos_obrigatorios:
            if campo not in novo_jogador or not novo_jogador[campo]:
                return jsonify({'error': f'O campo obrigatório "{campo}" está ausente ou vazio.'}), 400

        # Conecta ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insere o novo time na tabela jogadores_2023 usando prepared statement
        cursor.execute(
                f"INSERT INTO jogadores_2023 (NOME, APELIDO, TIME)"
                "VALUES (%s, %s, %s)",
                (
                    novo_jogador.get('nome', None),
                    novo_jogador.get('apelido', None),
                    novo_jogador.get('time', None), 

                )
        )
        
        # Commit para efetivar a inserção
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Time inserido com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': f'Erro ao inserir time: {str(e)}'}), 500
    
@app.route('/api/altera_jogador', methods=['POST'])
def altera_novo_jogador():
    try:
        # Recebe os dados do jogador a ser alterado do corpo da requisição
        altera_jogador = request.json  # force=True para ignorar o cabeçalho Content-Type
        
        print(altera_jogador)
        
        # Validar os campos obrigatórios
        campos_obrigatorios = ['nome', 'time']
        for campo in campos_obrigatorios:
            if campo not in altera_jogador or not altera_jogador[campo]:
                return jsonify({'error': f'O campo obrigatório "{campo}" está ausente ou vazio.'}), 400

        # Conecta ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Atualiza o jogador na tabela jogadores_2023 usando a instrução SQL UPDATE
        cursor.execute(
            "UPDATE jogadores_2023 SET APELIDO = %s WHERE NOME = %s AND TIME = %s",
            (altera_jogador.get('apelido', None), altera_jogador.get('nome', None), altera_jogador.get('time', None))
        )
        
        # Commit para efetivar a atualização
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Jogador atualizado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao atualizar jogador: {str(e)}'}), 500
    

@app.route('/api/deleta_jogador', methods=['POST'])
def deleta_novo_jogador():
    try:
        # Recebe os dados do jogador a ser deletado do corpo da requisição
        deleta_jogador = request.json  # force=True para ignorar o cabeçalho Content-Type
        
        print(deleta_jogador)
        
        # Validar os campos obrigatórios
        campos_obrigatorios = ['nome', 'time']
        for campo in campos_obrigatorios:
            if campo not in deleta_jogador or not deleta_jogador[campo]:
                return jsonify({'error': f'O campo obrigatório "{campo}" está ausente ou vazio.'}), 400

        # Conecta ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Deleta o jogador da tabela jogadores_2023 usando prepared statement
        cursor.execute("DELETE FROM jogadores_2023 WHERE NOME = %s AND TIME = %s", (deleta_jogador['nome'], deleta_jogador['time']))
        
        # Commit para efetivar a exclusão
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Jogador excluído com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao excluir jogador: {str(e)}'}), 500


    
@app.route('/api/novo_time', methods=['POST'])
def inserir_novo_time():
    try:
        # Recebe os dados do novo time do corpo da requisição
        novo_time = request.get_json(force=True)  # force=True para ignorar o cabeçalho Content-Type
        
        # Validar os campos obrigatórios
        campos_obrigatorios = ['brasao', 'nome']
        for campo in campos_obrigatorios:
            if campo not in novo_time or not novo_time[campo]:
                return jsonify({'error': f'O campo obrigatório "{campo}" está ausente ou vazio.'}), 400

        # Conecta ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        print(novo_time)
        # Insere o novo time na tabela simula_2023 usando prepared statement
        cursor.execute(
                f"INSERT INTO simula_2023 (Classificacao, BrasaoTime, Nome, Pontos, Jogos, Vitorias, Empates, Derrotas, Gols_Pros, Gols_Contra, Saldo_de_Gols, Cartoes_Amarelos, Cartoes_Vermelhos, Porcentagem_de_Vitorias) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    None,
                    novo_time.get('brasao', None),
                    novo_time.get('nome', None),
                    int(novo_time.get('pts', 0)),  
                    int(novo_time.get('numJogos', 0)),  
                    int(novo_time.get('numVit', 0)),  
                    int(novo_time.get('numEmp', 0)),  
                    int(novo_time.get('numDer', 0)),  
                    int(novo_time.get('gp', 0)),  
                    int(novo_time.get('gc', 0)), 
                    int(novo_time.get('sg', 0)),  
                    int(novo_time.get('cAmarelo', 0)),  
                    int(novo_time.get('cVermelho', 0)),  
                    int(novo_time.get('porcentagem', 0))  
                )
        )

        # Commit para efetivar a inserção
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Time inserido com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': f'Erro ao inserir time: {str(e)}'}), 500
    
@app.route('/api/altera_time', methods=['POST'])
def alterar_novo_time():
    try:
        # Recebe os dados do novo time do corpo da requisição
        novo_time = request.get_json(force=True)  # force=True para ignorar o cabeçalho Content-Type        

        # Conecta ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        print(novo_time)
        # Insere o novo time na tabela simula_2023 usando prepared statement
        cursor.execute(
            f"UPDATE simula_2023 SET "
            "BrasaoTime = %s, "
            "Pontos = %s, "
            "Jogos = %s, "
            "Vitorias = %s, "
            "Empates = %s, "
            "Derrotas = %s, "
            "Gols_Pros = %s, "
            "Gols_Contra = %s, "
            "Saldo_de_Gols = %s, "
            "Cartoes_Amarelos = %s, "
            "Cartoes_Vermelhos = %s, "
            "Porcentagem_de_Vitorias = %s "
            "WHERE Nome = %s",
            (
                novo_time.get('brasao', None),
                int(novo_time.get('pts', 0)),  
                int(novo_time.get('numJogos', 0)),  
                int(novo_time.get('numVit', 0)),  
                int(novo_time.get('numEmp', 0)),  
                int(novo_time.get('numDer', 0)),  
                int(novo_time.get('gp', 0)),  
                int(novo_time.get('gc', 0)), 
                int(novo_time.get('sg', 0)),  
                int(novo_time.get('cAmarelo', 0)),  
                int(novo_time.get('cVermelho', 0)),  
                int(novo_time.get('porcentagem', 0)),
                novo_time.get('nome', None)  # O Nome é utilizado na cláusula WHERE para identificar o registro a ser atualizado
            )
        )

        # Commit para efetivar a inserção
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Time atualizado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': f'Erro ao atualizar time: {str(e)}'}), 500
   
@app.route('/api/deletar_time', methods=['POST'])
def deletar_time():
    try:
        # Recebe os dados do time a ser excluído do corpo da requisição
        dados_time = request.get_json(force=True)

        print(dados_time['nome'])
        
        # Validar os campos obrigatórios (pode ser apenas o nome)
        if 'nome' not in dados_time or not dados_time['nome']:
            return jsonify({'error': 'O campo obrigatório "nome" está ausente ou vazio.'}), 400

        # Conecta ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Exclui o time da tabela simula_2023
        cursor.execute("DELETE FROM simula_2023 WHERE Nome = %s", (dados_time['nome'],))

        # Commit para efetivar a exclusão
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        return jsonify({'message': 'Time excluído com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao excluir time: {str(e)}'}), 500

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

@app.route('/api/jogos_simula', methods=['GET'])
def obter_jogos_simula_2023():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Ajuste da consulta SQL para a nova tabela
    cursor.execute("SELECT * FROM jogos_simula_2023")
    resultados = cursor.fetchall()
    conn.close()

    # Ajuste na construção do objeto jogos_rodada
    jogos_simula = [
        {   
            'rodada' : row[0],
            'info_jogo': row[1],
            'nome1': row[2],
            'time1': row[3],
            'brasao1': row[4],
            'nome2': row[5],
            'time2': row[6],
            'brasao2': row[7],
            'placar': row[8],
            'local': row[9]
        }
        for row in resultados
    ]

    return jsonify(jogos_simula)


@app.route('/api/jogos_rodada', methods=['GET'])
def obter_jogos_rodada_2023():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Ajuste da consulta SQL para a nova tabela
    cursor.execute("SELECT * FROM jogos_rodada_2023")
    resultados = cursor.fetchall()
    conn.close()

    # Ajuste na construção do objeto jogos_rodada
    jogos_rodada = [
        {   
            'rodada' : row[0],
            'info_jogo': row[1],
            'nome1': row[2],
            'time1': row[3],
            'brasao1': row[4],
            'nome2': row[5],
            'time2': row[6],
            'brasao2': row[7],
            'placar': row[8],
            'local': row[9]
        }
        for row in resultados
    ]

    return jsonify(jogos_rodada)

@app.route('/api/artilheiros', methods=['GET'])
def obter_artilheiros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artilheiros_2023")
    resultados = cursor.fetchall()
    conn.close()

    artilheiros = [{'brasao': row[0], 'nome': row[1], 'apelido': row[2], 'time': row[3], 'gols': row[4]} for row in resultados]
    return jsonify(artilheiros)

@app.route('/api/assistencias', methods=['GET'])
def obter_assistencias():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assistencias_2023")
    resultados = cursor.fetchall()
    conn.close()

    artilheiros = [{'assistencias': row[4], 'nome': row[1], 'time': row[2], 'partidas': row[3]} for row in resultados]
    return jsonify(artilheiros)

@app.route('/api/time/<string:nome_time>', methods=['GET'])
def obter_jogadores_por_time(nome_time):

    conn = conectar_bd()
    cursor = conn.cursor()

    # Correção na consulta SQL para juntar as tabelas corretamente
    cursor.execute("""
        SELECT j.nome, j.apelido, j.time 
        FROM jogadores_2023 j
        JOIN classificacao_2023 c ON j.time = c.nome
        WHERE UPPER(c.nome) = UPPER(%s)
    """, (nome_time,))
    
    resultados = cursor.fetchall()
    conn.close()

    jogadores_time = [{'nome': row[0], 'apelido': row[1], 'time': row[2]} for row in resultados]
    return jsonify(jogadores_time)



@app.route('/api/noticias', methods=['GET'])
def obter_noticias():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tabela_noticias")
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

@app.route('/api/protegido', methods=['GET'])
@jwt_required()
def retornaUser():
    email_logado = get_jwt_identity()

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(f"SELECT nome FROM public.usuario WHERE email = {email_logado};")
    nome_logado = cursor.fetchall()

    return jsonify(email=email_logado, nome=nome_logado), 200

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
