from flask import Blueprint

gestion_empleados = Blueprint('gestion_empleados', __name__, template_folder='../plantillas', static_folder="../estatico", static_url_path="/empleado/estatico/scripts")

from . import agregar_empleado
from . import baja_empleado
from . import obtener_datos_empleado
from . import carga_selects
from . import generar_contrato