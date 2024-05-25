"""
Comandos para instalar as dependencias e executar a API Python.
pip install Flask
pip install flask-cors
pip install flask_sqlalchemy
pip install Flask-WTF
pip install flasgger
python api.py
"""

from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
swagger = Swagger(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@app.route('/')
def index():
  return redirect("/apidocs", code=302)  

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid request data
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
      return jsonify({'message': 'Usuário já existe'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    Login as an existing user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      400:
        description: Invalid request data
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or user.password != password:
        return jsonify({'message': 'Credenciais inválidas'}), 401

    return jsonify({'message': 'Login bem-sucedido', 'token': hash(str(email) + str(password))}), 200

# Rota para cadastrar uma nota
@app.route('/note', methods=['POST'])
@cross_origin()
def note_create():
    """
    Register a new note
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Note
          required:
            - title
            - content
          properties:
            title:
              type: string
            content:
              type: string
    responses:
      201:
        description: Note created successfully
      400:
        description: Invalid request data
    """
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Nota cadastrado com sucesso'}), 201

# Rota para obter todas as notas
@app.route('/note', methods=['GET'])
@cross_origin()
def note_list():
    """
    Get all notes
    ---
    responses:
      200:
        description: All Notes successful
    """
   
    notes = Note.query.all()
    note_list = [{'id': note.id, 'title': note.title, 'content': note.content, 'created_at': note.created_at, 'updated_at': note.updated_at} for note in notes]

    return jsonify({'notes': note_list}), 200

# Rota para obter uma nota pelo ID
@app.route('/note/<int:note_id>', methods=['GET'])
@cross_origin()
def note_get_by_id(note_id):
    """
    Get a note by ID
    ---
    parameters:
      - in: path
        name: note_id
        required: true
        schema:
          type: integer
        description: ID of the note to be retrieved
    responses:
      200:
        description: Note retrieved successfully
      404:
        description: Note not found
    """
    note = Note.query.get(note_id)
    if note:
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content, 'created_at': note.created_at, 'updated_at': note.updated_at}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

# Rota para excluir uma nota pelo ID
@app.route('/note/<int:note_id>', methods=['DELETE'])
@cross_origin()
def note_delete(note_id):
    """
    Delete a note by ID
    ---
    parameters:
      - in: path
        name: note_id
        required: true
        schema:
          type: integer
        description: ID of the note to be deleted
    responses:
      200:
        description: Note deleted successfully
      404:
        description: Note not found
    """
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted successfully'}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

# Rota para atualizar uma nota pelo ID
@app.route('/note/<int:note_id>', methods=['PUT'])
@cross_origin()
def note_update(note_id):
    """
    Update a note by ID
    ---
    parameters:
      - in: path
        name: note_id
        required: true
        schema:
          type: integer
        description: ID of the note to be updated
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
        description: New title and content for the note
    responses:
      200:
        description: Note updated successfully
      404:
        description: Note not found
    """
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    note = Note.query.get(note_id)
    if note:
        note.title = title
        note.content = content
        db.session.commit()
        return jsonify({'message': 'Note updated successfully'}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

# Rota para atualizar parcialmente uma nota pelo ID
@app.route('/note/<int:note_id>', methods=['PATCH'])
@cross_origin()
def note_update_partial(note_id):
    """
    Partially update a note by ID
    ---
    parameters:
      - in: path
        name: note_id
        required: true
        schema:
          type: integer
        description: ID of the note to be partially updated
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
        description: New title and/or content for the note
    responses:
      200:
        description: Note updated successfully
      404:
        description: Note not found
    """
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    note = Note.query.get(note_id)
    if note:
        if title:
            note.title = title
        if content:
            note.content = content
        db.session.commit()
        return jsonify({'message': 'Note updated successfully'}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

if __name__ == '__main__':
    with app.app_context():  # Criando o contexto da aplicação
        db.create_all()
    app.run(debug=True)