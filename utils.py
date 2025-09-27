from functools import wraps
from flask import session, redirect, url_for, flash
import psycopg2
import os
from dotenv import load_dotenv

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

def get_db_connection():
    load_dotenv()
    return psycopg2.connect(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )

def execute_query(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        conn.commit()
        result = cur.fetchall() if cur.description else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
    return result

def db_login(user, clave):
    execute_query("INSERT INTO login (username, clave) VALUES (%s, %s)", (user, clave))

def db_usuario(user, nombre, apellido, rol):
    execute_query("INSERT INTO usuario (nombre_usuario, nombre, apellido, rol) VALUES (%s, %s, %s, %s)", (user, nombre, apellido, rol))

def db_recuperar_usuario(usuario):
    return execute_query("SELECT * FROM login WHERE username = %s", (usuario,))