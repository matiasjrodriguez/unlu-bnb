from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/login')
def login_api():
    # Lógica de negocio
    return {'status': 'ok'}

@api_bp.route('/signup', methods=['POST'])
def signup_api():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    role = data.get('role')

    if not all([first_name, last_name, username, role]):
        return jsonify({'message': 'Faltan datos obligatorios'}), 400

    # TODO: Persistir en DB

    return jsonify({'message': 'Usuario registrado correctamente'})