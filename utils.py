from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debés iniciar sesión para acceder a esta página.')
            return redirect(url_for('templates.login'))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            role = session.get('role')
            if role not in allowed_roles:
                flash('No tenés permisos para acceder a esta página.')
                return redirect(url_for('templates.dashboard'))
            return f(*args, **kwargs)
        return wrapped
    return decorator