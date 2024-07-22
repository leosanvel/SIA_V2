from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kNacionalidad

@catalogos.route('/catalogos/nacionalidad', methods = ['POST', 'GET'])
def catalogo_nacionalidad():
    columns = inspect(kNacionalidad).all_orm_descriptors.keys()
    Nacionalidad = db.session.query(kNacionalidad).order_by(kNacionalidad.Nacionalidad).all()
    return render_template('/nacionalidad.html', title='Nacionalidad',
                           current_user=current_user,
                           columns = columns,
                           Nacionalidad = Nacionalidad)

@catalogos.route('/catalogos/guardar_nacionalidad', methods = ['POST'])
def guardar_nacionalidad():
    columnas = inspect(kNacionalidad).all_orm_descriptors.keys()
    #print(columnas)
    idNacionalidad = request.form.get('idNacionalidad')
    Nacionalidad_data = {key: request.form.get(key) for key in columnas}
    #print(Nacionalidad_data)
    nueva_Nacionalidad = None
    try:
        Nacionalidad_existente = db.session.query(kNacionalidad).filter_by(idNacionalidad = idNacionalidad).one()
        for attr, value in Nacionalidad_data.items():
            if not attr.startswith('_') and hasattr(Nacionalidad_existente, attr):
                setattr(Nacionalidad_existente, attr, value)
    except NoResultFound:
        ultima_Nacionalidad = db.session.query(kNacionalidad.idNacionalidad).order_by(kNacionalidad.idNacionalidad.desc()).first()
        Nacionalidad_data["idNacionalidad"] = ultima_Nacionalidad.idNacionalidad + 1
        nueva_Nacionalidad = kNacionalidad(**Nacionalidad_data)
        db.session.add(nueva_Nacionalidad)
    db.session.commit()

    return jsonify({"guardado": True})