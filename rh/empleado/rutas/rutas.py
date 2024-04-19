from flask import Blueprint

empleado = Blueprint('empleado', __name__, template_folder='../plantillas', static_folder="../estatico", static_url_path="/empleado/estatico/scripts")