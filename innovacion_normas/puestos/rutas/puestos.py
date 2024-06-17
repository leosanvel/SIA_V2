from flask import Blueprint

puestos = Blueprint('puestos', __name__, template_folder="../plantillas", static_folder="../estatico", static_url_path="/puestos/estatico")

from . import cargar_puestos
from . import crear_modificar_puestos