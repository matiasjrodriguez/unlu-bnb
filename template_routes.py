from flask import Blueprint, render_template
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
def dashboard():
    return render_template('dashboard.html')

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
