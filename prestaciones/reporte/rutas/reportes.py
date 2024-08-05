from flask import Blueprint
reportes_prestaciones = Blueprint("reportes_prestaciones", __name__, template_folder="../plantillas", static_folder="../estatico", static_url_path="/reporte/estatico")

from . import cifras_control