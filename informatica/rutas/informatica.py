from flask import Blueprint, render_template
from flask_login import current_user

# from app import app_instance

informatica = Blueprint('informatica', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/scripts')

@informatica.route('/informatica/permisos-usuario', methods=['POST', 'GET'])
def permisos_usuario():
    return render_template('/permisos_usuario.html', title='Usuario',
                           current_user=current_user)