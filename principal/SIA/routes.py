from flask import Blueprint, render_template
from flask_login import current_user

from app.general.utils.funciones import permisos_de_consulta
from app.rh.empleado.models.models import Empleados
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from app import db

moduloSIA = Blueprint('principal', __name__, template_folder = 'templates', static_folder='static', static_url_path='/principal/SIA/static') #por ej. 

@moduloSIA.route('/Principal/SIA')
@permisos_de_consulta
def SIA():
    try:
        empleado = db.session.query(Empleados).filter_by(idPersona=current_user.idPersona, Activo=1).one()
    except NoResultFound:
        empleado = None
    return render_template('/SIA.html', title ='Sistema Integral Administrativo',
                            current_user=current_user,
                            empleado = empleado)