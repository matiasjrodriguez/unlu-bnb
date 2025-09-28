from flask import Blueprint, render_template, session, redirect, url_for
from utils import login_required, roles_required

template_bp = Blueprint('templates', __name__)

@template_bp.route('/')
def home():
    return render_template('index.html')

@template_bp.route('/login')
def login():
    return render_template('login.html')

@template_bp.route('/signup')
def signup():
    return render_template('signup.html')

@template_bp.route('/dashboard')
@login_required
@roles_required(2, 3, 4)
def dashboard():
    from utils import obtener_publicaciones_por_usuario
    from flask import session

    publicaciones = obtener_publicaciones_por_usuario(session['usuario_id'])
    return render_template('dashboard.html', publicaciones=publicaciones)

@template_bp.route('/publicar')
@login_required
@roles_required(2, 3, 4)
def publicar():
    return render_template('publicar.html')

@template_bp.route('/feed')
@login_required
@roles_required(1, 3, 4)
def feed():
    from utils import obtener_todas_las_publicaciones
    publicaciones=obtener_todas_las_publicaciones()
    #publicaciones.clear()
    return render_template('feed.html', publicaciones=publicaciones)

@template_bp.route('/editar/<int:id>')
@login_required
@roles_required(2, 3, 4)
def editar_publicacion(id):
    from utils import obtener_publicacion_por_id

    publicacion = obtener_publicacion_por_id(id)
    print(publicacion['imagenes'])

    if session['role'] != 4:
        if publicacion['usuario_id'] != session['usuario_id']:
            return redirect(url_for('template_bp.dashboard'))
        
    return render_template('editar_publicacion.html', publicacion=publicacion)