from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kTipoIncidencia

@catalogos.route('/catalogos/tipos-incidencia', methods = ['POST', 'GET'])
def catalogo_tipoincidencia():
    TipoIncidencia = db.session.query(kTipoIncidencia).all()
    return render_template('/tipo_incidencia.html', title = 'Tipos de Incidencia',
                           TipoIncidencia = TipoIncidencia)

@catalogos.route('/catalogos/guardar_tipoincidencia', methods = ['POST'])
def guardar_tipoincidencia():
    datos = request.get_json()
    idTipoIncidencia = datos.pop("idTipoIncidencia")
    try:
        TipoIncidencia = db.session.query(kTipoIncidencia).filter_by(idTipoIncidencia = idTipoIncidencia).one()
        data = {}
        data["idTipoIncidencia"] = idTipoIncidencia
        data["TipoIncidencia"] = datos.pop("TipoIncidencia")
        data["Activo"] = datos.pop("Activo")
        
        for attr, value in data.items():
            if not attr.startswith('_') and hasattr(TipoIncidencia, attr):
                setattr(TipoIncidencia, attr, value)

        db.session.commit()
    
    except NoResultFound:
        print("No se encontró resultado")

    return jsonify({"guardado": True})