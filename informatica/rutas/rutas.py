from flask import Blueprint

informatica = Blueprint('informatica', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/informatica/estatico')

from . import gestion_usuarios
from . import solicitudes

