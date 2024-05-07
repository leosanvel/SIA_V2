from flask import Blueprint

gestion_asistencias = Blueprint('gestion_asistencias', __name__, template_folder='../plantillas', static_folder="../estatico", static_url_path="/gestion_asistencias/estatico")

from . import politicas
from . import checador
from . import sanciones
from . import incidencias
from . import justificantes
from . import reporte_incidencias