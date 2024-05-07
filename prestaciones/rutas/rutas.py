from flask import Blueprint

prestaciones = Blueprint('prestaciones', __name__, template_folder='../plantillas', static_folder='../estatico', static_url_path='/prestaciones/estatico')

from . import empleado_concepto
from . import prestacion

