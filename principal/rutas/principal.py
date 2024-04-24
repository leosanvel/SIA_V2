from flask import Blueprint, render_template
from flask_login import current_user

from general.herramientas.funciones import permisos_de_consulta
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from app import db

moduloSIA = Blueprint('principal', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/principal/estatico') #por ej. 

@moduloSIA.route('/principal/sia')
@permisos_de_consulta
def sia():
    # try:
    #     empleado = db.session.query(Empleados).filter_by(idPersona=current_user.idPersona, Activo=1).one()
    # except NoResultFound:
    #     empleado = None
    empleado = None
    return render_template('/SIA.html', title ='Sistema Integral Administrativo',
                            current_user=current_user,
                            empleado = empleado)

@moduloSIA.route('/conceptos')
@permisos_de_consulta
def conceptos():
    # try:
    #     empleado = db.session.query(Empleados).filter_by(idPersona=current_user.idPersona, Activo=1).one()
    # except NoResultFound:
    #     empleado = None
    return render_template('/conceptos.html', title ='Conceptos',
                            current_user=current_user,
                            TipoConcepto = None)

@moduloSIA.route('/empleado-conceptos')
@permisos_de_consulta
def empleado_conceptos():
    # try:
    #     empleado = db.session.query(Empleados).filter_by(idPersona=current_user.idPersona, Activo=1).one()
    # except NoResultFound:
    #     empleado = None
    return render_template('/empleado_conceptos.html', title ='Empleado Conceptos',
                            current_user=current_user,
                            TipoConcepto = None)