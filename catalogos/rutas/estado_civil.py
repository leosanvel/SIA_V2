from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from catalogos.modelos.modelos import Kestadocivil
from app import db
#from general.utils.funciones import permisos_de_consulta, permisos_de_edicion

estadocivil = Blueprint('estadocivil', __name__, template_folder = 'templates', static_folder='static', static_url_path='/catalogos/estadocivil/static') #por ej. 

@estadocivil.route('/Catalogos/estadocivil', methods = ['POST', 'GET'])
@permisos_de_consulta
def catalogo_estadocivil():
    columns = inspect(Kestadocivil).all_orm_descriptors.keys()
    estadocivil_t = db.session.query(Kestadocivil).all()
    return render_template('/estadocivil.html', title='Estado Civil',
                           current_user=current_user,
                           columns = columns,
                           estadocivil_t = estadocivil_t)

@estadocivil.route('/Catalogos/guardar_estadocivil', methods = ['POST'])
@permisos_de_edicion
def guardar_estadocivil():
    columnas = inspect(Kestadocivil).all_orm_descriptors.keys()
    #print(columnas)
    idEstCiv = request.form.get('idEstadoCivil')
    EstCiv_data = {key: request.form.get(key) for key in columnas}
    #print(EstCiv_data)
    nuevo_EstCiv = None
    try:
        EstCiv_existente = db.session.query(Kestadocivil).filter_by(idEstadoCivil = idEstCiv).one()
        for attr, value in EstCiv_data.items():
            if not attr.startswith('_') and hasattr(EstCiv_existente, attr):
                setattr(EstCiv_existente, attr, value)
        #print(EstCiv_existente.EstadoCivil)
    except NoResultFound:
        ultimoEstCiv = db.session.query(Kestadocivil.idEstadoCivil).order_by(Kestadocivil.idEstadoCivil.desc()).first()
        EstCiv_data["idEstadoCivil"] = ultimoEstCiv.idEstadoCivil + 1
        nuevo_EstCiv = Kestadocivil(**EstCiv_data)
        db.session.add(nuevo_EstCiv)
        #print(ultimoEstCiv.idEstadoCivil)
    db.session.commit()

    return jsonify({"guardado": True})