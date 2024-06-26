from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kTipoSancion

@catalogos.route('/catalogos/tipos-sancion', methods = ['POST', 'GET'])
def catalogo_tiposancion():
    Sanciones = db.session.query(kTipoSancion).all()
    return render_template('/tipo_sancion.html', title = 'Tipos de sanción',
                           Sanciones = Sanciones)

@catalogos.route('/catalogos/guardar_tiposancion', methods = ['POST'])
def guardar_tiposancion():
    datos = request.get_json()
    idSancion = datos.pop("idSancion", None)
    sancion_data = {}
    sancion_data["idSancion"] = idSancion
    sancion_data["TipoSancion"] = datos.pop("Sancion")
    sancion_data["Activo"] = datos.pop("Activo")
    try:
        Sancion = db.session.query(kTipoSancion).filter_by(idSancion = idSancion).one()

        for attr, value in sancion_data.items():
            if not attr.startswith('_') and hasattr(Sancion, attr):
                setattr(Sancion, attr, value)
                
        db.session.commit()
        return jsonify({"guardado": True})

    except NoResultFound:
        ultimaSancion = db.session.query(kTipoSancion.idSancion).order_by(kTipoSancion.idSancion.desc()).first()
        sancion_data["idSancion"] = ultimaSancion.idSancion + 1
        nueva_Sancion = kTipoSancion(**sancion_data)
        db.session.add(nueva_Sancion)
        db.session.commit()
        return jsonify({"guardado": True})
    
    return jsonify({"guardado": False})