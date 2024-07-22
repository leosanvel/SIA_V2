from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kQuincena

@catalogos.route('/catalogos/quincenas', methods = ['POST', 'GET'])
def catalogo_quincenas():
    Quincenas = db.session.query(kQuincena).all()
    return render_template('/quincenas.html', title = 'Quincenas',
                            Quincenas = Quincenas)

@catalogos.route('/catalogos/cargar_quincenas', methods = ['POST'])
def cargar_quincenas():
    Quincenas = db.session.query(kQuincena).order_by(kQuincena.idQuincena.asc()).all()
    lista_quincenas = []

    for Quincena in Quincenas:
        if Quincena is not None:
            Quincena_dict = Quincena.__dict__
            Quincena_dict.pop("_sa_instance_state", None)
            lista_quincenas.append(Quincena_dict)

    return jsonify(lista_quincenas)

@catalogos.route('/catalogos/guardar_quincenas', methods = ['POST'])
def guardar_quincenas():
    datos = request.get_json()
    idQuincena = datos.pop("idQuincena")

    try:
        Quincena = db.session.query(kQuincena).get(idQuincena)
        data_Quincena = {}
        data_Quincena["idQuincena"] = idQuincena
        data_Quincena["Quincena"] = Quincena.Quincena
        data_Quincena["Fechas"] = datos.pop("Fechas")
        data_Quincena["FechaInicio"] = Quincena.FechaInicio
        data_Quincena["FechaFin"] = Quincena.FechaFin
        data_Quincena["Descripcion"] = datos.pop("Descripcion")
        
        for attr, value in data_Quincena.items():
            if not attr.startswith('_') and hasattr(Quincena, attr):
                setattr(Quincena, attr, value)
        
        db.session.commit()

        return jsonify({"guardado": True})

    except NoResultFound:
        print("No se encontró resultado")
        return jsonify({"guardado": False})
    
@catalogos.route('/Catalogos/actualizar_quincenas', methods = ['POST'])
def actualizar_quincenas():
    Quincenas = db.session.query(kQuincena).all()
    hoy = datetime.now()
    anio = hoy.year
    data_Quincena = {}
    
    if(Quincenas[0].FechaInicio.year != anio):
        for Quincena in Quincenas:
            data_Quincena["idQuincena"] = Quincena.idQuincena
            data_Quincena["Quincena"] = Quincena.Quincena
            data_Quincena["Fechas"] = Quincena.Fechas
            FechaInicio = datetime(anio, Quincena.FechaInicio.month, Quincena.FechaInicio.day, 0, 0, 0, 0)
            data_Quincena["FechaInicio"] = FechaInicio
            if((int(Quincena.Quincena) == 4)):
                if((anio % 4) == 0):
                    FechFin = datetime(anio, Quincena.FechaFin.month, 29, 0, 0, 0, 0)
                else:
                    FechFin = datetime(anio, Quincena.FechaFin.month, 28, 0, 0, 0, 0)
            else:
                FechFin = datetime(anio, Quincena.FechaFin.month, Quincena.FechaFin.day, 0, 0, 0, 0)
            data_Quincena["FechaFin"] = FechFin
            data_Quincena["Descripcion"] = Quincena.Descripcion

            for attr, value in data_Quincena.items():
                if not attr.startswith('_') and hasattr(Quincena, attr):
                    setattr(Quincena, attr, value)

            db.session.commit()


    return jsonify({"guardado": True})