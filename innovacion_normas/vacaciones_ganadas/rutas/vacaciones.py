from flask import Blueprint

vacaciones = Blueprint("vacaciones", __name__, template_folder = "../plantillas", static_folder = "../estatico", static_url_path = "/vacaciones_ganadas/estatico")

from . import vacaciones_ganadas