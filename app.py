from flask import Flask
from config import Config
from general.utils.db import db
from auth.models import User, Tusuario

app = Flask(__name__, template_folder='general/templates', static_folder='general/static')
app.config.from_object(Config)

# MÓDULO AUTENTICACIÓN
from auth.routes import auth
app.register_blueprint(auth)

db.init_app(app)

global app_instance

app_instance = app

from flask_login import LoginManager
# Crear la clase LoginManager
login_manager = LoginManager()
# Configurar la aplicación
login_manager.init_app(app)

# Función para recargar el objeto de usuario
@login_manager.user_loader
def load_user(user_id):
    user_db = db.session.query(Tusuario).filter_by(idPersona=user_id).first()
    if user_db:
        return User(user_db)
    return None