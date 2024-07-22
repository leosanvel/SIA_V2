from flask import Blueprint

reportes = Blueprint("reportes", __name__, template_folder="../plantillas", static_folder="../estatico", static_url_path="/reportes/estatico")

from . import por_movimientos