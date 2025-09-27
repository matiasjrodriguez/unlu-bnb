from flask import Blueprint, request, jsonify, session
from utils import db_login

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validación básica
    if not username or not password:
        return jsonify({'message': 'Usuario y contraseña son obligatorios'}), 400

    # TODO: Recuperar de base de datos y comparar
    return jsonify({'message': 'Inicio de sesión exitoso'})

@api_bp.route('/signup', methods=['POST'])
def signup_api():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not all([first_name, last_name, username, password, role]):
        return jsonify({'message': 'Faltan datos obligatorios'}), 400

    db_login(username, password)

    session['usuario_id'] = username # Esto es temporal hasta que tengamos la db
    session['role'] = role

    return jsonify({'message': 'Usuario registrado correctamente'})

@api_bp.route('/publicar', methods=['POST'])
def publicar_api():
    data = request.get_json()

    required_fields = ['titulo', 'descripcion', 'barrio', 'calle', 
                       'ambientes', 'balcon', 'precio']
    
    if not all(field in data and data[field] != '' for field in required_fields):
        return jsonify({'message': 'Faltan campos obligatorios'}), 400
    
    print("Nueva publicación recibida:")
    for k, v in data.items():
        print(f"{k}: {v}")

    return jsonify({'message': 'Publicación registrada correctamente'}), 200