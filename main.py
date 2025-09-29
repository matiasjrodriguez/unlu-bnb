from flask import Flask
from api_routes import api_bp
from template_routes import template_bp
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SUPERSECRET") # No nos olvidemos de cambiar esto chicos, lo ideal es que sea una variable de entorno para la vps
app.config['UPLOAD_FOLDER'] = 'static/img'

app.register_blueprint(api_bp)
app.register_blueprint(template_bp)

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True)