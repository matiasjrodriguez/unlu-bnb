from functools import wraps
from flask import session, redirect, url_for, flash
import psycopg
import os
from dotenv import load_dotenv
import bcrypt

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    DBNAME = os.getenv("DBNAME")
    DBUSER = os.getenv("DBUSER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    return psycopg.connect(
        dbname=DBNAME,
        user=DBUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
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

def hash_clave(clave):
    clave_bytes = clave.encode('utf-8') # porque bcrypt requiere que este en bytes
    hashed = bcrypt.hashpw(clave_bytes, bcrypt.gensalt())
    return hashed

def check_password(clave, hash):
    return bcrypt.checkpw(clave.encode('utf-8'), hash)

def db_login(user, clave):
    clave = hash_clave(clave)
    result = execute_query("INSERT INTO login (usuario, clave) VALUES (%s, %s) RETURNING id", (user, clave))
    return result[0][0]

def db_usuario(id, user, nombre, apellido, rol):
    execute_query("INSERT INTO usuario (id, usuario, nombre, apellido, rol) VALUES (%s, %s, %s, %s, %s)", (id, user, nombre, apellido, rol))

def db_recuperar_usuario(usuario):
    return execute_query("SELECT * FROM login WHERE usuario = %s", (usuario,))

def db_recuperar_rol(id):
    return execute_query("SELECT rol FROM usuario WHERE id = %s", (id,))

def db_publicacion(titulo, descripcion, barrio, calle, ambientes, balcon, usuario_id, autor, imagenes, precio):

    query = """
        INSERT INTO publicacion (
            titulo, descripcion, barrio, calle, ambientes, balcon, 
            usuario_id, autor, imagenes, precio
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        titulo, 
        descripcion, 
        barrio, 
        calle, 
        ambientes, 
        balcon, 
        usuario_id, 
        autor, 
        imagenes, 
        precio
    )

    execute_query(query, params)
    
def obtener_todas_las_publicaciones():
    
    import json

    query = """
        SELECT titulo, descripcion, barrio, calle, ambientes, balcon, autor, precio, imagenes
        FROM publicacion
        ORDER BY id DESC
    """
    
    filas = execute_query(query)
    publicaciones = []

    for fila in filas:
        publicacion = {
            'titulo': fila[0],
            'descripcion': fila[1],
            'barrio': fila[2],
            'calle': fila[3],
            'ambientes': fila[4],
            'balcon': fila[5],
            'autor': fila[6],
            'precio': fila[7],
            'imagenes': fila[8] if fila[8] else []
        }
        publicaciones.append(publicacion)

    return publicaciones

publicaciones = obtener_todas_las_publicaciones()