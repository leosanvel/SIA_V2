from flask import Blueprint, render_template, request, jsonify



from flask_login import current_user
from app import db


catalogos = Blueprint('catalogos', __name__, template_folder='../plantillas', static_folder='../estatico', static_url_path='/catalogos/estatico')

from . import conceptos
from . import centro_costos
from . import grupo
from . import nacionalidad
from . import quincenas
from . import tipo_alta
from . import dias_festivos
from . import escuela
from . import tipos_justificante
from . import tipo_incidencia
from . import estado_civil
from . import porcentajes
from . import tipo_sancion
from . import puestos