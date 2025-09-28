from flask import Blueprint, redirect, request, jsonify, session, url_for
from utils import db_login, db_usuario, db_recuperar_usuario, check_password, db_recuperar_rol, login_required, roles_required, allowed_file, UPLOAD_FOLDER, obtener_publicacion_por_id
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json

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
    session['usuario'] = usuario
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
    session['usuario'] = username
    session['role'] = role

    return jsonify({'message': 'Usuario registrado correctamente'}), 200

@api_bp.route('/publicar', methods=['POST'])
@login_required
@roles_required(2, 3, 4)
def publicar_api():

    from utils import db_publicacion

    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    barrio = request.form.get('barrio')
    calle = request.form.get('calle')
    ambientes = request.form.get('ambientes')
    balcon = request.form.get('balcon')
    precio = request.form.get('precio')

    imagenes_guardadas = []

    if 'imagenes' in request.files:
        files = request.files.getlist('imagenes')
        for file in files:
            if file and allowed_file(file.filename):
                original = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f'{session['usuario']}_{timestamp}_{original}'
                
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                imagenes_guardadas.append(path)
    
    web_paths = [path.replace('\\', '/') for path in imagenes_guardadas]
    web_paths = json.dumps(web_paths)
    
    db_publicacion(titulo, descripcion, barrio, calle, ambientes, balcon, session['usuario_id'], session['usuario'], web_paths, precio)

    return jsonify({'message': 'Publicación registrada correctamente'}), 200

@api_bp.route('/actualizar/<int:id>', methods=['POST'])
@login_required
@roles_required(2, 3, 4)
def actualizar_publicacion(id):
    from utils import actualizar_publicacion_por_id

    publicacion = obtener_publicacion_por_id(id)

    if not publicacion:
        return jsonify({'error': 'Publicación no encontrada'}), 404
    
    if session['role'] != 4:
        if publicacion['usuario_id'] != session['usuario_id']:
            return jsonify({'error': 'No autorizado'}), 403
        
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    barrio = request.form.get('barrio')
    calle = request.form.get('calle')
    ambientes = request.form.get('ambientes')
    balcon = request.form.get('balcon')
    precio = request.form.get('precio')

    nuevas_imagenes = []
    if 'imagenes' in request.files:
        files = request.files.getlist('imagenes')
        for file in files:
            if file and allowed_file(file.filename):
                original = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                usuario = session.get('usuario')
                nuevo_nombre = f"{usuario}_{timestamp}_{original}"
                path = os.path.join(UPLOAD_FOLDER, nuevo_nombre)
                file.save(path)
                nuevas_imagenes.append(path.replace('\\', '/'))

    todas_imagenes = publicacion['imagenes'] + nuevas_imagenes
    imagenes_json = json.dumps(todas_imagenes)

    actualizar_publicacion_por_id(id, titulo, descripcion, barrio, calle, ambientes, balcon, precio, imagenes_json)

    return redirect(url_for('templates.dashboard'))

@api_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required(2, 3, 4)
def eliminar_publicacion(id):

    from utils import borrar_publicacion_por_id

    publicacion = obtener_publicacion_por_id(id)

    if not publicacion:
        return jsonify({'error': 'Publicación no encontrada'}), 404

    if session['role'] != 4:
        if publicacion['usuario_id'] != session['usuario_id']:
            return jsonify({'error': 'No autorizado'}), 403

    # Eliminar publicación
    borrar_publicacion_por_id(id)

    return redirect(url_for('templates.dashboard'))