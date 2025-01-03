from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import inspect, func
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date
from calendar import monthrange
import locale

from .rutas import catalogos
from catalogos.modelos.modelos import kQuincena, kAnioFiscal
from app import db

locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

@catalogos.route('/catalogos/quincenas', methods = ["GET", "POST"])
def catalogos_quincenas():
    AnioFiscal = db.session.query(kAnioFiscal).all()

    return render_template('/quincenas.html', title = 'Quincenas',
                           AnioFiscal = AnioFiscal)

@catalogos.route('/catalogos/quincenas/cargar-quincenas', methods = ['POST'])
def cargar_quincenas():
    AnioFiscal = request.form.get("AnioFiscal")

    FechaInicio = datetime(int(AnioFiscal), 1, 1)
    FechaFin = datetime(int(AnioFiscal), 12, 31)
    
    Quincenas = db.session.query(kQuincena).filter(kQuincena.FechaInicio >= FechaInicio, kQuincena.FechaFin <= FechaFin).order_by(kQuincena.Quincena.asc()).all()
    lista_quincenas = []

    for Quincena in Quincenas:
        if Quincena is not None:
            Quincena_dict = Quincena.__dict__
            Quincena_dict.pop("_sa_instance_state", None)
            lista_quincenas.append(Quincena_dict)

    return jsonify(lista_quincenas)

@catalogos.route('/catalogos/quincenas/generar-quincenas', methods = ["POST"])
def generar_quincenas():
    respuesta = 0
    idQuincena = 1
    AnioFiscal = request.form.get("AnioFiscal")
    print(AnioFiscal)

    ultimo_idQuincena = db.session.query(func.max(kQuincena.idQuincena)).scalar()
    if ultimo_idQuincena is None:
        idQuincena = 1
    else:
        idQuincena = ultimo_idQuincena

    if AnioFiscal != "":
        num_quincena = 1

        for mes in range(1, 13):
            idQuincena = idQuincena + 1
            FechaInicio = datetime(int(AnioFiscal), mes, 1)
            FechaFin = datetime(int(AnioFiscal), mes, 15)
            Quincena_data = {
                "idQuincena": idQuincena,
                "Quincena": num_quincena,
                "FechaInicio": FechaInicio,
                "FechaFin": FechaFin,
                "Descripcion": f"1RA QUINCENA DE {FechaInicio.strftime('%B').upper()}"
            }

            print(Quincena_data)
            if db.session.query(kQuincena).filter_by(FechaInicio = FechaInicio, FechaFin = FechaFin).first() is None:
                nueva_quincena = kQuincena(**Quincena_data)
                db.session.add(nueva_quincena)

            FechaInicio = datetime(int(AnioFiscal), mes, 16)
            ultimo_dia_mes = monthrange(int(AnioFiscal), mes)[1]
            FechaFin = datetime(int(AnioFiscal), mes, ultimo_dia_mes)
            idQuincena = idQuincena + 1
            num_quincena = num_quincena + 1
            Quincena_data = {
                "idQuincena": idQuincena,
                "Quincena": num_quincena,
                "FechaInicio": FechaInicio,
                "FechaFin": FechaFin,
                "Descripcion": f"2DA QUINCENA DE {FechaInicio.strftime('%B').upper()}"
            }

            print(Quincena_data)
            if db.session.query(kQuincena).filter_by(FechaInicio = FechaInicio, FechaFin = FechaFin).first() is None:
                nueva_quincena = kQuincena(**Quincena_data)
                db.session.add(nueva_quincena)
            
            num_quincena = num_quincena + 1

        db.session.commit()

        total_quincenas = db.session.query(kQuincena).filter(func.extract('year', kQuincena.FechaInicio) == int(AnioFiscal)).count()

        print(total_quincenas)

        if total_quincenas == 24:
            respuesta = 99
        else:
            respuesta = 2

    else:
        respuesta = 1

    return({"respuesta": respuesta})