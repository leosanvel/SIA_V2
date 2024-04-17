from flask import Flask, session
from config import Config
from general.herramientas.bd import db
from autenticacion.modelos.modelos import User, rUsuario

from datetime import datetime, timezone

app = Flask(__name__, template_folder='general/plantillas', static_folder='general/estatico')
app.config.from_object(Config)

db.init_app(app)

global app_instance

app_instance = app

from flask_login import LoginManager
# Crear la clase LoginManager
login_manager = LoginManager()
# Configurar la aplicación
login_manager.init_app(app)

# Decorador para monitorear actividad antes de acceder a las rutas
@app.before_request
def update_last_activity():
    # Reinicia le tiempo de inactividad
    session['hora_inicio'] = datetime.now(timezone.utc).isoformat()

# Función para recargar el objeto de usuario
@login_manager.user_loader
def load_user(user_id):
    user_db = db.session.query(rUsuario).filter_by(idPersona=user_id).first()
    if user_db:
        return User(user_db)
    return None

# MODULOS BLUEPRINT
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO AUTENTICACIÓN
from autenticacion.rutas.rutas import autenticacion
app.register_blueprint(autenticacion)
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO PRINCIPAL
from principal.rutas.rutas import moduloSIA
app.register_blueprint(moduloSIA)