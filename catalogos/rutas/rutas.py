from flask import Blueprint

catalogos = Blueprint('catalogos', __name__, template_folder='../plantillas', static_folder='../estatico', static_url_path='/catalogos/estatico')

