from flask import Blueprint

gestion_tiempo_no_laboral = Blueprint('gestion_tiempo_no_laboral', __name__, template_folder = "../plantillas", static_folder = "../estatico", static_url_path = "/gestion_tiempo_no_laboral/estatico")

from . import dias_festivos
from . import dias_persona
from . import periodo_vacacional
from . import descontar_dias