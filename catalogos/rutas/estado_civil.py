from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kEstadoCivil

@catalogos.route('/catalogos/estado-civil', methods = ['POST', 'GET'])
def catalogo_estadocivil():
    columns = inspect(kEstadoCivil).all_orm_descriptors.keys()
    estadocivil_t = db.session.query(kEstadoCivil).all()
    return render_template('/estado_civil.html', title='Estado Civil',
                           current_user=current_user,
                           columns = columns,
                           estadocivil_t = estadocivil_t)

@catalogos.route('/catalogos/guardar_estadocivil', methods = ['POST'])
def guardar_estadocivil():
    columnas = inspect(kEstadoCivil).all_orm_descriptors.keys()
    #print(columnas)
    idEstCiv = request.form.get('idEstadoCivil')
    EstCiv_data = {key: request.form.get(key) for key in columnas}
    #print(EstCiv_data)
    nuevo_EstCiv = None
    try:
        EstCiv_existente = db.session.query(kEstadoCivil).filter_by(idEstadoCivil = idEstCiv).one()
        for attr, value in EstCiv_data.items():
            if not attr.startswith('_') and hasattr(EstCiv_existente, attr):
                setattr(EstCiv_existente, attr, value)
        #print(EstCiv_existente.EstadoCivil)
    except NoResultFound:
        ultimoEstCiv = db.session.query(kEstadoCivil.idEstadoCivil).order_by(kEstadoCivil.idEstadoCivil.desc()).first()
        EstCiv_data["idEstadoCivil"] = ultimoEstCiv.idEstadoCivil + 1
        nuevo_EstCiv = kEstadoCivil(**EstCiv_data)
        db.session.add(nuevo_EstCiv)
        #print(ultimoEstCiv.idEstadoCivil)
    db.session.commit()

    return jsonify({"guardado": True})