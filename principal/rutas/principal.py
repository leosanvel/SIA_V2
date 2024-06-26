from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from general.herramientas.funciones import permisos_de_consulta
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from rh.gestion_empleados.modelos.empleado import tPersona
from app import db



moduloSIA = Blueprint('principal', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/principal/estatico') #por ej. 

@moduloSIA.route('/principal/sia')
@permisos_de_consulta
def sia():
    try:
        empleado = db.session.query(tPersona).filter_by(idPersona=current_user.idPersona).one()
    except NoResultFound:
        empleado = None

    return render_template('/SIA.html', title ='Sistema Integral Administrativo',
                            current_user=current_user,
                            empleado = empleado)
