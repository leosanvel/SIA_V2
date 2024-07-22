from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kTipoJustificante

@catalogos.route('/catalogos/tipos-justificante', methods = ['POST', 'GET'])
def catalogo_tipojustificante():
    TipoJustificante = db.session.query(kTipoJustificante).all()
    return render_template('/tipo_justificante.html', title = 'Tipos de Justificante',
                           TipoJustificante = TipoJustificante)

@catalogos.route('/catalogos/guardar_tipojustificante', methods = ['POST'])
def guardar_tipojustificante():
    datos = request.get_json()
    idTipoJustificante = datos.pop("idTipoJustificante")
    try:
        TipoJustificante = db.session.query(kTipoJustificante).filter_by(idTipoJustificante = idTipoJustificante).one()
        data = {}
        data["idTipoJustificante"] = idTipoJustificante
        data["TipoJustificante"] = datos.pop("TipoJustificante")
        data["Activo"] = datos.pop("Activo")

        for attr, value in data.items():
            if not attr.startswith('_') and hasattr(TipoJustificante, attr):
                setattr(TipoJustificante, attr, value)
                
        db.session.commit()

    except NoResultFound:
        print("No se encontró resultado")
    
    return jsonify({"guardado": True})