from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date

from .rutas import catalogos
from catalogos.modelos.modelos import kAnioFiscal
from app import db

@catalogos.route('/catalogos/anio-fiscal', methods = ["GET", "POST"])
def catalogos_anio_fiscal():
    AnioFiscal = db.session.query(kAnioFiscal).all()

    return render_template('/anio_fiscal.html', title = "Año Fiscal",
                           AnioFiscal = AnioFiscal)

@catalogos.route("/catalogos/anio-fiscal/guardar-anio-fiscal", methods = ["POST"])
def guardar_anio_fiscal():
    AnioFiscal = request.form.get("AnioFiscal")
    
    AnioFiscal_existente = db.session.query(kAnioFiscal).filter_by(AnioFiscal = AnioFiscal).first()

    respuesta = 0
    
    if AnioFiscal_existente is None:
        nuevo_AnioFiscal = kAnioFiscal(idAnioFiscal=int(AnioFiscal),
                                       AnioFiscal=int(AnioFiscal))
        
        db.session.add(nuevo_AnioFiscal)
        db.session.commit()

        estado = inspect(nuevo_AnioFiscal)
        if estado.persistent:
            respuesta = 99
        else:
            respuesta = 2

    else:
        respuesta = 1

    return jsonify({"respuesta": respuesta})