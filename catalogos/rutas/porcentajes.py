from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kPorcentajes

@catalogos.route('/catalogos/porcentajes', methods = ['POST', 'GET'])
def catalogo_porcentajes():
    porcentajes = db.session.query(kPorcentajes).all()
    return render_template('/porcentajes.html', title = 'Porcentajes',
                           Porcentajes = porcentajes)

@catalogos.route('/catalogos/guardar_porcentajes', methods = ['POST'])
def guardar_porcentajes():
    datos = request.get_json()
    idPorcentaje = datos.pop("idPorcentaje", None)
    porcentaje_data = {}
    porcentaje_data["idPorcentaje"] = idPorcentaje
    porcentaje_data["Porcentaje"] = datos.pop("Porcentaje")
    porcentaje_data["Activo"] = datos.pop("Activo")
    try:
        Porcentaje = db.session.query(kPorcentajes).filter_by(idPorcentaje = idPorcentaje).one()

        for attr, value in porcentaje_data.items():
            if not attr.startswith('_') and hasattr(Porcentaje, attr):
                setattr(Porcentaje, attr, value)
                
        db.session.commit()
        return jsonify({"guardado": True})

    except NoResultFound:
        ultimoPorcentaje = db.session.query(kPorcentajes.idPorcentaje).order_by(kPorcentajes.idPorcentaje.desc()).first()
        porcentaje_data["idPorcentaje"] = ultimoPorcentaje.idPorcentaje + 1
        nuevo_Porcentaje = kPorcentajes(**porcentaje_data)
        db.session.add(nuevo_Porcentaje)
        db.session.commit()
        return jsonify({"guardado": True})
    
    return jsonify({"guardado": False})