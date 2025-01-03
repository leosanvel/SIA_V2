from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import inspect, func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from calendar import monthrange
import locale

from .rutas import catalogos
from catalogos.modelos.modelos import kAnioFiscal, kCalculoISR
from app import db

@catalogos.route("/catalogos/tabulador-impuestos", methods = ["POST", "GET"])
def tabulador_impuestos():
    AnioFiscal = db.session.query(kAnioFiscal).all()

    return render_template("/tabulador_impuestos.html", title = "Tabulador de impuestos",
                           AnioFiscal = AnioFiscal)

@catalogos.route("/catalogos/tabulador-impuestos/obtener-tabulador-impuestos", methods = ["POST"])
def obtener_tabulador_impuestos():
    respuesta = 0
    lista_TabuladorImpuestos = []
    AnioFiscal = request.form.get("AnioFiscal")
    print(AnioFiscal)

    TabuladoresImpuestos = db.session.query(kCalculoISR).filter_by(idAnioFiscal = int(AnioFiscal)).all()
    
    for TabuladorImpuesto in TabuladoresImpuestos:
        if TabuladorImpuesto is not None:
            TabuladorImpuesto_dict = TabuladorImpuesto.__dict__
            TabuladorImpuesto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy

            lista_TabuladorImpuestos.append(TabuladorImpuesto_dict)

    return jsonify({"TabuladorImpuestos": lista_TabuladorImpuestos})

@catalogos.route("/catalogos/tabulador-impuestos/guardar-tabulador-impuestos", methods = ["POST"])
def guardar_tabulador_impuestos():
    respuesta = 0
    AnioFiscal = request.form.get("AnioFiscal")

    if AnioFiscal != "":
        try:
            for i in range(1, 12):
                TabuladorImpuestos_Existente = db.session.query(kCalculoISR).filter_by(idAnioFiscal = int(AnioFiscal),  Consecutivo = i).first()
                if TabuladorImpuestos_Existente is None:
                    nuevo_TabuladorImpuestos = kCalculoISR(idAnioFiscal=AnioFiscal,
                                                           TipoCalculo="M",
                                                           Consecutivo=i,
                                                           LimiteInferior=request.form.get("LimiteInferior" + str(i)),
                                                           LimiteSuperior=request.form.get("LimiteSuperior" + str(i)),
                                                           CuotaFija=request.form.get("CuotaFija" + str(i)),
                                                           Porcentaje=request.form.get("Porcentaje" + str(i)))
                    db.session.add(nuevo_TabuladorImpuestos)
                    respuesta = 99

                else:
                    TabuladorImpuestos_Existente.LimiteInferior = request.form.get("LimiteInferior" + str(i))
                    TabuladorImpuestos_Existente.LimiteSuperior = request.form.get("LimiteSuperior" + str(i))
                    TabuladorImpuestos_Existente.CuotaFija = request.form.get("CuotaFija" + str(i))
                    TabuladorImpuestos_Existente.Porcentaje = request.form.get("Porcentaje" + str(i))
                    respuesta = 98

            db.session.commit()
        
        except IntegrityError as e:
            db.session.rollback()
            print(e.orig)
            respuesta = 1

    return jsonify({"respuesta": respuesta})