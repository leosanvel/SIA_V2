from flask import Blueprint

prestaciones = Blueprint('prestaciones', __name__, template_folder='../plantillas', static_folder='../estatico', static_url_path='/PRESTACIONES/estatico')

from . import empleado_concepto

