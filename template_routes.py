from flask import Blueprint, render_template

template_bp = Blueprint('templates', __name__)

@template_bp.route('/')
def home():
    return render_template('index.html')

@template_bp.route('/login')
def login():
    return render_template('login.html')