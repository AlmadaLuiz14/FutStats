from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json


app = Flask(_name_)

# Nome do arquivo JSON
COMMENTS_FILE = 'comments.json'

# Verifica se o arquivo JSON existe, cria se não existir
if not os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, 'w') as file:
        file.write('[]')

def get_comments():
    try:
        with open(COMMENTS_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        return {'error': f'Erro ao ler o arquivo JSON: {e}'}

def add_comment(comment):
    try:
        comments = get_comments()
        comments.append(comment)
        with open(COMMENTS_FILE, 'w') as file:
            json.dump(comments, file, indent=2)
        return {'success': 'Comentário adicionado com sucesso'}
    except Exception as e:
        return {'error': f'Erro ao escrever no arquivo JSON: {e}'}

@app.route('/api/comentarios', methods=['GET'])
def get_comments_route():
    comments = get_comments()
    return jsonify(comments)

@app.route('/api/comentarios', methods=['POST'])
def add_comment_route():
    data = request.get_json()
    response = add_comment(data)
    return jsonify(response)

CORS(app)

if _name_ == '_main_':
    app.run(debug=True)