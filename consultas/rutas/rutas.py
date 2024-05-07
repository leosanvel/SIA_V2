from flask import Blueprint

consultas = Blueprint('consultas', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/consultas/estatico')

from . import consulta_incidencias
