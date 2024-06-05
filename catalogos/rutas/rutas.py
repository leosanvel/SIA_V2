from flask import Blueprint, render_template, request, jsonify



from flask_login import current_user
from app import db


catalogos = Blueprint('catalogos', __name__, template_folder='../plantillas', static_folder='../estatico', static_url_path='/catalogos/estatico')

from . import conceptos
from . import centro_costos
from . import dias_festivos
from . import escuela
from . import puestos