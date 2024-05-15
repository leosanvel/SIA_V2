from .gestion_asistencias import gestion_asistencias
from flask_login import current_user
from flask import render_template, request, jsonify
from sqlalchemy import and_, inspect, func
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date, timedelta

from app import db
from rh.gestion_empleados.modelos.empleado import rEmpleado
from rh.gestion_asistencias.modelos.modelos import tChecador, tIncidencia
from datetime import time
from catalogos.modelos.modelos import *

@gestion_asistencias.route('/rh/gestion-asistencias/checador', methods = ['GET', 'POST'])
def checador():
    
    hoy = datetime.now()
    mes = hoy.month
    quincena = mes*2
    if((hoy.day//16) == 0):
        quincena = quincena - 1

    quincenas = db.session.query(kQuincena).filter(kQuincena.idQuincena.in_([quincena, quincena + 1, quincena + 2])).all()
    return render_template('/checador.html', title='Generar Checador',
                           current_user=current_user,
                           quincenas = quincenas)

@gestion_asistencias.route('/rh/gestion-asistencias/generar-checador', methods = ['POST'])
def generar_checador():
    Checador = {}
    inicio = 0
    fin = 0
    mes = 0
    Checador["idQuincena"] = request.form.get("NumQuincena")
    Personas = db.session.query(rEmpleado).filter_by(Activo = 1).all()
    for Persona in Personas:
        Checador["idPersona"] = Persona.idPersona
        if(int(Checador['idQuincena']) % 2):
            inicio = 1
            fin = 16
            mes = (int(Checador['idQuincena']) // 2) + 1
        
        else:
            inicio = 16
            mes = int(Checador['idQuincena']) // 2
            if((int(Checador['idQuincena'])//2) == 4 or (int(Checador['idQuincena'])//2) == 6 or (int(Checador['idQuincena'])//2) == 9 or (int(Checador['idQuincena'])//2) == 11):
                fin = 31
            elif((int(Checador['idQuincena'])//2) == 2):
                if((date.today().year % 4) == 0):
                    fin = 30
                else:
                    fin = 29
            else:
                fin = 32
        
        for i in range(inicio, fin, 1):
                Checador["Fecha"] = date(date.today().year, mes, i)
                Checador["HoraEntrada"] = time(9, 0, 0)
                Checador["HoraSalida"] = time(18, 0, 0)
                Checador["idQuincenaReportada"] = None
                Checador["idIncidencia"] = None
                Checador["idJustificante"] = None
                
                try:
                    checador_existente = db.session.query(tChecador).filter_by(idPersona = Checador['idPersona'], Fecha = Checador['Fecha'], idQuincena = Checador['idQuincena']).one()
                    checador_ya_generado = 0
                except NoResultFound:
                    Nuevo_checador = tChecador(**Checador)
                    db.session.add(Nuevo_checador)
                    db.session.commit()
                    checador_ya_generado = 1

    # checar_incidencias(Checador['NumeroQuincena'])


    return jsonify({"guardado": checador_ya_generado})

@gestion_asistencias.route('/rh/gestion-asistencias/checar-incidencias', methods = ['POST'])
def checar_incidencias(NumQuincena):
    try:
        incidencias_existentes = db.session.query(tIncidencia).filter_by(NumeroQuincena = NumQuincena).all()
        for incidencia in incidencias_existentes:
            dias = incidencia.FechaFin - incidencia.FechaInicio
            fecha_aux = incidencia.FechaInicio
            for i in range(0, dias.days + 1, 1):
                fecha_aux += timedelta(days = i)
                checador = db.session.query(tChecador).filter_by(idPersona = incidencia.idPersona, NumeroQuincena = NumQuincena, Fecha = fecha_aux).first()
                if(incidencia.idTipo == 1):
                    checador.HoraEntrada = time(0, 0, 0)
                    checador.HoraSalida = time(0, 0, 0)
                elif(incidencia.idTipo == 2):
                    checador.HoraEntrada = time(0, 0, 0)
                elif(incidencia.idTipo == 6):
                    checador.HoraSalida = time(0, 0, 0)
        
        db.session.commit()
                
    except NoResultFound:
        print("No hay incidencias")

    return jsonify({"redirect": True}) 