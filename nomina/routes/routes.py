from flask import Blueprint

nomina = Blueprint('nomina', __name__, template_folder='../templates', static_folder='../static', static_url_path='/nomina/static')

from . import enviar_nomina
from . import validar_clabe
from . import generar_CFDI