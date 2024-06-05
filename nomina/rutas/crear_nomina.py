from flask import render_template, request, jsonify, url_for, current_app
from datetime import date, datetime

from app import db
from .rutas import nomina
from catalogos.modelos.modelos import kQuincena
from nomina.modelos.modelos import tNomina
from catalogos.modelos.modelos import kTipoNomina

@nomina.route("/nomina/crear-nomina", methods = ['GET', 'POST'])
def crear_nomina():
    anio_act = date.today().year
    
    Quincenas = db.session.query(kQuincena).filter(kQuincena.FechaInicio >= date(anio_act, 1, 1)).filter(kQuincena.FechaFin <= date(anio_act, 12, 31)).order_by(kQuincena.Quincena).all()
    TipoNominas = db.session.query(kTipoNomina).order_by(kTipoNomina.idTipoNomina).all()

    return render_template('/crear_nomina.html', title = 'Crear Nómina',
                           Quincenas = Quincenas,
                           TipoNominas = TipoNominas)

@nomina.route("/nomina/cargar-info-crear-nomina", methods = ['POST'])
def cargar_info_crear_nomina():
    idQuincena = request.form.get("idQuincena")
    Quincena = db.session.query(kQuincena).filter_by(idQuincena = idQuincena).first()
    if Quincena is not None:
        Quincena_dict = Quincena.__dict__
        Quincena_dict.pop("_sa_instance_state", None)

    return jsonify(Quincena_dict)

@nomina.route("/nomina/guardar-crear-nomina", methods = ['POST'])
def guardar_crear_nomina():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'Quincena': 'idQuincena',
        'NombreNomina': 'Nomina',
        'Descripcion': 'Descripcion',
        'Estatus': 'Estatus',
        'FechaPago': 'FechaPago',
        'idPersonaEmisor': 'idPersonaEmisor',
        'PeriodoQuincena': 'PeriodoQuincena',
        'SMM': 'SMM',
        'SueldoMensual': 'SueldoMensual'
    }

    nomina_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    nomina_nueva = None
    
    nomina_existente = db.session.query(tNomina).filter_by(idQuincena = nomina_data["idQuincena"]).first()
    if nomina_existente is None:
        nomina_data["FechaPago"] = datetime.strptime(nomina_data['FechaPago'], '%d/%m/%Y')
        nomina_data["PeriodoQuincena"] = nomina_data["FechaPago"].year
        nomina_data["Estatus"] = 1
        nomina_nueva = tNomina(**nomina_data)
        db.session.add(nomina_nueva)
        db.session.commit()

        return jsonify({"guardado": True})
    
    else:
        return jsonify({"guardado": False})