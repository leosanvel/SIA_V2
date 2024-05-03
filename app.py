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
    user_db = db.session.query(rUsuario).filter_by(Usuario=user_id).first()
    if user_db:
        return User(user_db)
    return None

# MODULOS BLUEPRINT
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO AUTENTICACIÓN
from autenticacion.rutas.autenticacion import autenticacion
app.register_blueprint(autenticacion)
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO GENERAL
from general.rutas.general import general
app.register_blueprint(general)

#----------------------------------------------------------------------------------------------------------------------
# MÓDULO INFORMATICA
from informatica.rutas.informatica import informatica
app.register_blueprint(informatica)


# MÓDULO PRINCIPAL
from principal.rutas.principal import moduloSIA
app.register_blueprint(moduloSIA)
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO GESTIÓN DE EMPLEADOS
from rh.gestion_empleados.rutas.gestion_empleados import gestion_empleados
app.register_blueprint(gestion_empleados)
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO GESTIÓN DE ASISTENCIAS
from rh.gestion_asistencias.rutas.gestion_asistencias import gestion_asistencias
app.register_blueprint(gestion_asistencias)
#----------------------------------------------------------------------------------------------------------------------
# MÓDULO NOMINA
from nomina.rutas.rutas import nomina
app.register_blueprint(nomina)

#----------------------------------------------------------------------------------------------------------------------
# MÓDULO NOMINA
from catalogos.rutas.rutas import catalogos
app.register_blueprint(catalogos)

#----------------------------------------------------------------------------------------------------------------------
# MÓDULO PRESTACIONES
from prestaciones.rutas.rutas import prestaciones
app.register_blueprint(prestaciones)

with app.app_context():
    db.create_all()
