from flask import Flask
from api_routes import api_bp
from template_routes import template_bp

app = Flask(__name__)
app.secret_key = 'clave secreta XDDDD' # No nos olvidemos de cambiar esto chicos, lo ideal es que sea una variable de entorno para la vps

app.register_blueprint(api_bp)
app.register_blueprint(template_bp)

if __name__ == '__main__':
    app.run(debug=True)