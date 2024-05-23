from flask import render_template, request, jsonify, url_for
from datetime import date, datetime

from app import db
from .rutas import nomina
from nomina.modelos.modelos import kMeses, kQuincenaCalendario, kActividadCalendario, tFechasCalendario

@nomina.route("/nomina/calendario-pagos", methods = ['GET', 'POST'])
def calendario_pagos():
    Meses = db.session.query(kMeses).order_by(kMeses.idMes).all()
    QuincenasCalendario = db.session.query(kQuincenaCalendario).filter(kQuincenaCalendario.idQuincenaCalendario.in_([1, 2])).order_by(kQuincenaCalendario.idQuincenaCalendario).all()
    Actividades = db.session.query(kActividadCalendario).order_by(kActividadCalendario.idActividadCalendario).all()

    Anio = date.today().year

    return render_template("/calendario_pagos.html", title = "Calendario de pagos",
                           Meses = Meses,
                           QuincenasCalendario = QuincenasCalendario,
                           Actividades = Actividades,
                           Anio = Anio)

@nomina.route("/nomina/obtener-select-concepto", methods = ['POST'])
def obtener_select_concepto():
    idMes = request.form.get('idMes')
    if(idMes != '12'):
        quincenas = db.session.query(kQuincenaCalendario).filter(kQuincenaCalendario.idQuincenaCalendario.in_([1, 2])).order_by(kQuincenaCalendario.idQuincenaCalendario).all()
    else:
        quincenas = db.session.query(kQuincenaCalendario).filter(kQuincenaCalendario.idQuincenaCalendario.in_([3, 4])).order_by(kQuincenaCalendario.idQuincenaCalendario).all()

    ret = '<option value="0">-- Seleccione --</option>'

    for registro in quincenas:
        ret += '<option value="{}">{}</option>'.format(registro.idQuincenaCalendario, registro.QuincenaCalendario)

    return ret

@nomina.route("/nomina/agregar-fecha-calendario", methods = ['POST'])
def agregar_fecha_calendario():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'Mes': 'idMes',
        'Concepto': 'idQuincenaCalendario',
        'Actividad': 'idActividadCalendario',
        'FechaInicio': 'FechaInicio',
        'FechaFin': 'FechaFin',
        'Anio': 'Periodo'
    }

    fechas_a_agregar = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    fechas_a_agregar["FechaInicio"] = datetime.strptime(fechas_a_agregar["FechaInicio"], '%d/%m/%Y')
    fechas_a_agregar["FechaFin"] = datetime.strptime(fechas_a_agregar["FechaFin"], '%d/%m/%Y')
    nuevo_fecha_calendario = None
    fechas_calendario_existente = db.session.query(tFechasCalendario).filter_by(idMes = fechas_a_agregar["idMes"], idQuincenaCalendario = fechas_a_agregar["idQuincenaCalendario"], idActividadCalendario = fechas_a_agregar["idActividadCalendario"], Periodo = fechas_a_agregar["Periodo"]).first()
    if fechas_calendario_existente is None:
        nuevo_fecha_calendario = tFechasCalendario(**fechas_a_agregar)
        db.session.add(nuevo_fecha_calendario)
        db.session.commit()
        return jsonify({"guardado": True})
    else:
        fechas_calendario_existente.update(**fechas_a_agregar)
        db.session.commit()
        return jsonify({"actualizado": True})
