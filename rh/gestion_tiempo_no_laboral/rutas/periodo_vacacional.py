from .gestion_tiempo_no_laboral import gestion_tiempo_no_laboral
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, time

from app import db
from rh.gestion_asistencias.modelos.modelos import tJustificante, tChecador
from rh.gestion_empleados.modelos.empleado import rEmpleado
from catalogos.modelos.modelos import kPeriodoVacacional


@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/periodo-vacacional', methods = ['POST', 'GET'])
def periodo_vacacional():
    return render_template('/periodo_vacacional.html', title = 'Periodo Vacacional')

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/cargar-periodo-vacacional', methods = ['POST'])
def cargar_periodo_vacacional():
    PeriodoVacacional = db.session.query(kPeriodoVacacional).all()

    lista_periodo = []
    for periodo in PeriodoVacacional:
        if periodo is not None:
            periodo_dict = periodo.__dict__
            periodo_dict.pop("_sa_instance_state", None)
            lista_periodo.append(periodo_dict)

    return jsonify(lista_periodo)


@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/guardar-periodo-vacacional', methods = ['POST'])
def guardar_periodo_vacacional():
    data = {}
    data["FechaInicio"] = request.form.get("fechaInicioFormateada")
    data["FechaFin"] = request.form.get("fechaFinFormateada")
    data["idPeriodo"] = request.form.get("Periodo")
    data["Descripcion"] = request.form.get("Descripcion")

    try:
        PeriodoVacacional_existente = db.session.query(kPeriodoVacacional).filter_by(FechaInicio = data["FechaInicio"], FechaFin = data['FechaFin']).one()
        for attr, value in data.items():
            if not attr.startswith('-') and hasattr(PeriodoVacacional_existente, attr):
                setattr(PeriodoVacacional_existente, attr, value)
    except NoResultFound:
        ultimo_PeriodoVacacional = db.session.query(kPeriodoVacacional.idPeriodoVacacional).order_by(kPeriodoVacacional.idPeriodoVacacional.desc()).first()
        if(ultimo_PeriodoVacacional):
            data["idPeriodoVacacional"] = ultimo_PeriodoVacacional.idPeriodoVacacional + 1
        else:
            data["idPeriodoVacacional"] = 1
        nuevo_PeriodoVacacional = kPeriodoVacacional(**data)
        db.session.add(nuevo_PeriodoVacacional)
    db.session.commit()

    return jsonify({"guardado": True})

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laborarl/generar-periodo-vacacional', methods = ['POST'])
def generar_periodovacacional():
    idPeriodoVacacional = request.form.get("idPeriodoVacacional")

    try:
        Periodo_Vacacional = db.session.query(kPeriodoVacacional).get(idPeriodoVacacional)
        justificante_data = {}
        justificante_data["id"] = None
        justificante_data["descripcion"] = Periodo_Vacacional.Descripcion
        justificante_data["idTipo"] = 7
        justificante_data["fechaInicio"] = Periodo_Vacacional.FechaInicio
        justificante_data["fechaFin"] = Periodo_Vacacional.FechaFin
        justificante_data["NumeroQuincena"] = 3

        try:
            justificante_existente = db.session.query(tJustificante).filter_by(descripcion = Periodo_Vacacional.Descripcion).one()
            return jsonify({"guardado": False})
        
        except NoResultFound:
            Num_empleados = db.session.query(rEmpleado.idPersona).filter_by(Activo = 1).all()
            Num_empleados = [numero[0] for numero in Num_empleados]

            for id_empleado in Num_empleados:
                justificante_data["idPersona"] = int(id_empleado)
                nuevo_justificante = tJustificante(**justificante_data)
                db.session.add(nuevo_justificante)

                lista_checador = db.session.query(tChecador).filter(
                    tChecador.idPersona == justificante_data['idPersona'],
                    tChecador.Fecha >= justificante_data["fechaInicio"],
                    tChecador.Fecha <= justificante_data["fechaFin"]
                ).all()

                for registro in lista_checador:
                    registro.HoraEntrada = time(9, 0, 0)
                    registro.HoraSalida = time(18, 0, 0)
        
            db.session.commit()

            return jsonify({"guardado": True})
    

    except NoResultFound:
        return jsonify({"guardado": False})