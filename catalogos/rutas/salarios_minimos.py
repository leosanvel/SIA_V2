from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import inspect, func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from calendar import monthrange

from .rutas import catalogos
from catalogos.modelos.modelos import kAnioFiscal, kuma
from app import db

@catalogos.route("/catalogos/salarios-minimos", methods = ["GET", "POST"])
def salarios_minimos():
    AnioFiscal = db.session.query(kAnioFiscal).all()
    AnioActual = datetime.today().year

    return render_template("/salarios_minimos.html", title = "Salarios mínimos",
                           AnioFiscal = AnioFiscal,
                           AnioActual = AnioActual)

@catalogos.route("/catalogos/salarios-minimos/obtener-salarios-minimos", methods = ["POST"])
def obtener_salarios_minimos():
    respuesta = 0
    AnioFiscal = request.form.get("AnioFiscal")

    salarios_minimos_existente = db.session.query(kuma).filter_by(EjercicioFiscal = int(AnioFiscal)).first()

    if salarios_minimos_existente:
        salarios_minimos_existente = salarios_minimos_existente.__dict__
        salarios_minimos_existente.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy

    return jsonify({"SalariosMinimos": salarios_minimos_existente})

@catalogos.route("/catalogos/salarios-minimos/guardar-salarios-minimos", methods = ["POST"])
def guardar_salarios_minimos():
    respuesta = 0
    AnioFiscal = request.form.get("AnioFiscal")
    
    if AnioFiscal != "":
        try:
            SalarioMinimo_existente = db.session.query(kuma).filter_by(EjercicioFiscal = int(AnioFiscal)).first()
            if SalarioMinimo_existente:
                SalarioMinimo_existente.MontoDiario = request.form.get("MontoDiario")
                SalarioMinimo_existente.MontoMensual = request.form.get("MontoMensual")
                SalarioMinimo_existente.MontoAnual = request.form.get("MontoAnual")

                respuesta = 98
            else:
                nuevo_SalariosMinimos = kuma(EjercicioFiscal=int(AnioFiscal),
                                             MontoDiario=request.form.get("MontoDiario"),
                                             MontoMensual=request.form.get("MontoMensual"),
                                             MontoAnual=request.form.get("MontoAnual"))

                db.session.add(nuevo_SalariosMinimos)
                respuesta = 99

            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            print(e.orig)
            respuesta = 1


    return jsonify({"respuesta": respuesta})