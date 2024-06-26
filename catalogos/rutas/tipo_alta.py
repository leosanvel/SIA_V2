from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kTipoEmpleado, kTipoAlta

@catalogos.route('/catalogos/tipo-alta', methods = ['POST', 'GET'])
def catalogo_tipoalta():
    Tipoempleado = db.session.query(kTipoEmpleado).filter_by(Activo = 1).order_by(kTipoEmpleado.idTipoEmpleado).all()
    columns = inspect(kTipoAlta).all_orm_descriptors.keys()
    TipoAlta = db.session.query(kTipoAlta).order_by(kTipoAlta.idTipoAlta).all()
    return render_template('/tipo_alta.html', title='Tipo de alta',
                           current_user=current_user,
                           Tipoempleado = Tipoempleado,
                           columns = columns,
                           TipoAlta = TipoAlta)

@catalogos.route('/catalogos/guardar_Tipoalta', methods = ['POST'])
def guardar_Tipoalta():
    columnas = inspect(kTipoAlta).all_orm_descriptors.keys()
    #print(columnas)
    idTipoAlta = request.form.get("idTipoAlta")
    TipoAlta_data = {key: request.form.get(key) for key in columnas}
    nuevo_TipoAlta = None
    #print(TipoAlta_data)
    try:
        TipoAlta_existente = db.session.query(kTipoAlta).filter_by(idTipoAlta = idTipoAlta).one()
        for attr, value in TipoAlta_data.items():
            if not attr.startswith('_') and hasattr(TipoAlta_existente, attr):
                setattr(TipoAlta_existente, attr, value)
    except NoResultFound:
        ultimo_TipoAlta = db.session.query(kTipoAlta.idTipoAlta).order_by(kTipoAlta.idTipoAlta.desc()).first()
        TipoAlta_data["idTipoAlta"] = ultimo_TipoAlta.idTipoAlta + 1
        nuevo_TipoAlta = kTipoAlta(**TipoAlta_data)
        db.session.add(nuevo_TipoAlta)
    db.session.commit()

    return jsonify({"guardado": True})