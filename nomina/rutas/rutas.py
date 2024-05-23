from flask import Blueprint

nomina = Blueprint('nomina', __name__, template_folder='../plantillas', static_folder='../estatico', static_url_path='/nomina/estatico')

# from . import enviar_nomina
# from . import validar_clabe
from . import generar_CFDI
from . import validar_clabe
from . import generar_Nomina