from .gestion_tiempo_no_laboral import gestion_tiempo_no_laboral
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app import db
from rh.gestion_tiempo_no_laboral.modelos.modelos import rDiasPorciento
from catalogos.modelos.modelos import kQuincena, kPorcentajes
from general.herramientas.funciones import calcular_quincena

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/descontar-dias', methods = ['GET', 'POST'])
def descontar_dias():
    quincena = calcular_quincena()
    Quincenas = db.session.query(kQuincena).all()
    #Quincenas = db.session.query(kQuincena).filter(kQuincena.idQuincena.in_([quincena, quincena + 1, quincena + 2])).order_by(kQuincena.idQuincena).all()
    Porcentaje = db.session.query(kPorcentajes).get(100)

    return render_template('/descontar_dias.html', title = 'Descontar días',
                           current_user = current_user,
                           Quincenas = Quincenas,
                           Porcentaje = Porcentaje)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/guardar-descontar-dias', methods = ['POST'])
def guardar_descontar_dias():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona': 'idPersona',
        'Quincena': 'idQuincena',
        'Porcentaje': 'idPorcentaje',
        'DescontarDias' : 'Dias'
    }

    nuevo_descontar_dias = None

    descontar_dias_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    print(descontar_dias_data)

    descontar_dias_existente = db.session.query(rDiasPorciento).filter_by(idPersona = descontar_dias_data["idPersona"], idQuincena = descontar_dias_data["idQuincena"]).first()
    if(descontar_dias_existente):
        descontar_dias_existente.update(**descontar_dias_data)
    else:
        nuevo_descontar_dias = rDiasPorciento(**descontar_dias_data)
        db.session.add(nuevo_descontar_dias)
    
    db.session.commit()

    return({"guardado": True})

@gestion_tiempo_no_laboral.route("/rh/gestion-tiempo-no-laboral/buscar-descontar-dias", methods = ['POST'])
def buscar_descontar_dias():
    idPersona = request.form.get("idPersona")
    descontar_dias_existente = db.session.query(rDiasPorciento).filter_by(idPersona = idPersona).all()

    lista_porcentajes = []
    Porcentajes = db.session.query(kPorcentajes).order_by(kPorcentajes.idPorcentaje.asc()).all()
    for porcentaje in Porcentajes:
        if porcentaje is not None:
            porcentaje_dict = porcentaje.__dict__
            porcentaje_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_porcentajes.append(porcentaje_dict)

    descontar_dias_lista = []

    for descontar_dias in descontar_dias_existente:
        if descontar_dias is not None:
            descontar_dias_existente_dict = descontar_dias.__dict__
            descontar_dias_existente_dict.pop("_sa_instance_state", None)
            descontar_dias_lista.append(descontar_dias_existente_dict)

    return({
        'descontar_dias_lista': descontar_dias_lista,
        'porcentajes': lista_porcentajes})

@gestion_tiempo_no_laboral.route("/rh/gestion-tiempo-no-laboral/eliminar-descontar-dias", methods = ['POST'])
def eliminar_descontar_dias():
    mapeo_nombres = {
        "idPersona": "idPersona",
        "idQuincena": "idQuincena",
        "idPorcentaje": "idPorcentaje",
        "Dias": "Dias"
    }

    descontar_dias_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    descontar_dias_eliminar = db.session.query(rDiasPorciento).filter_by(idPersona = descontar_dias_data["idPersona"], idQuincena = descontar_dias_data["idQuincena"], idPorcentaje = descontar_dias_data["idPorcentaje"], Dias = descontar_dias_data["Dias"]).delete()
    db.session.commit()
    if descontar_dias_eliminar > 0:
        print("Los días a descontar se eliminaron correctamente.")
        return jsonify({"eliminado": True})
    else: 
        print("No se elimnaron los días a descontar.")
        return jsonify({"eliminado": False})

    