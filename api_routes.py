from flask import Blueprint, request, jsonify, session
from utils import db_login, db_usuario, db_recuperar_usuario, check_password, db_recuperar_rol

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validación básica
    if not username or not password:
        return jsonify({'message': 'Usuario y contraseña son obligatorios'}), 400

    usuario_instancia = db_recuperar_usuario(username)
    
    if not usuario_instancia:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401
    
    id = usuario_instancia[0][0]
    usuario = usuario_instancia[0][1]
    clave = usuario_instancia[0][2]

    if not check_password(password, clave):
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401
    
    rol = db_recuperar_rol(id)[0][0]

    session['usuario_id'] = id
    session['role'] = rol

    return jsonify({'message': 'Inicio de sesión exitoso'}), 200

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
    
    usuario = db_recuperar_usuario(username)

    if usuario:
        return jsonify({'message': 'El nombre de usuario ya existe'}), 409
    
    user_id = db_login(username, password)
    db_usuario(user_id, username, first_name, last_name, role)

    session['usuario_id'] = user_id
    session['role'] = role

    return jsonify({'message': 'Usuario registrado correctamente'}), 200

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