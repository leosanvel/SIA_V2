from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory
from flask_login import current_user
from sqlalchemy import or_, inspect, func, and_, cast, String
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from docx.shared import Cm, Inches, Mm, Emu
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import pythoncom
import os

from prestaciones.modelos.modelos import rEmpleadoConcepto
from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *
from rh.gestion_tiempo_no_laboral.modelos.modelos import *
#from catalogos.modelos.modelos import *
from app import db
from general.herramientas.funciones import *

@gestion_empleados.route('/rh/gestion-empleados/baja-empleado', methods = ['POST', 'GET'])
def baja_empleado():
    quincena = db.session.query(kQuincena).all()
    return render_template('/bajaempleado.html', title='Baja de empleado',
                           current_user=current_user,
                           Quincena = quincena)


@gestion_empleados.route('/rh/gestion-empleados/obtener-puestos-empleado', methods = ['POST', 'GET'])
def obtener_puestos_empleado():
    idPersona = request.form.get('idPersona')
    try:
        empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona, Activo = 1).one()
        empleadoPuesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idPersona == idPersona, rEmpleadoPuesto.idEstatusEP == 1).first()
        puesto = db.session.query(tPuesto).filter_by(ConsecutivoPuesto = empleadoPuesto.idPuesto).one()
        
        respuesta = {}
        if empleadoPuesto is not None:
            tipoEmpleado = db.session.query(kTipoEmpleado).filter_by(idTipoEmpleado = empleado.idTipoEmpleado).first()

            respuesta["NumeroEmpleado"] = empleado.NumeroEmpleado
            respuesta["TipoEmpleado"] = tipoEmpleado.TipoEmpleado
            respuesta["Puesto"] = puesto.Puesto
            respuesta["idPuesto"] = puesto.ConsecutivoPuesto

        
            tipoAlta = db.session.query(kTipoAlta).filter_by(idTipoEmpleado = empleado.idTipoEmpleado, idTipoAlta = empleado.idTipoAlta).first()
            if tipoAlta:
                respuesta["TipoAlta"] = tipoAlta.TipoAlta
            else:
                respuesta["TipoAlta"] = "No especificado"

            
            causas = db.session.query(kCausaBaja).filter(kCausaBaja.idTipoEmpleado == empleado.idTipoEmpleado).all()
            lista_causas_baja = []
            for causa in causas:
                causa_dict = causa.__dict__
                causa_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                lista_causas_baja.append(causa_dict)
            respuesta["CausasBaja"] = lista_causas_baja
        
            empleadoPuesto_dict = empleadoPuesto.__dict__
            empleadoPuesto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            respuesta["empleadoPuesto"] = empleadoPuesto_dict
        else:
            respuesta["NoEncontrado"] = True
    except NoResultFound:    
        respuesta["NoEncontrado"] = True
    return jsonify(respuesta)


@gestion_empleados.route('/rh/gestion-empleados/dar-baja-empleado', methods = ['POST', 'GET'])
def dar_baja_empleado():
    idPersona = request.form.get('idPersona')
    idPuesto = request.form.get('idPuesto')

    idCausaBaja = request.form.get('CausaBaja')
    Observaciones = request.form.get('Observaciones')
    FechaEfecto = request.form.get('FechaEfecto')
    FechaEfectoFormateado = datetime.strptime(FechaEfecto, '%d/%m/%Y')

    checkboxConservarVacaciones = request.form.get("checkboxConservarVacaciones")
    
    try:
        quincena = db.session.query(kQuincena).filter(
            and_(
                kQuincena.FechaInicio <= FechaEfectoFormateado,
                kQuincena.FechaFin >= FechaEfectoFormateado
            )
        ).one()
        NumQuincena = quincena.idQuincena
    except NoResultFound:
        NumQuincena = "-"

    respuesta = {}
    try:
        empleadoPuesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idPersona == idPersona, rEmpleadoPuesto.idPuesto == idPuesto, or_(cast(rEmpleadoPuesto.FechaTermino, String).like("0000-00-00"), rEmpleadoPuesto.FechaTermino == None), rEmpleadoPuesto.idEstatusEP == 1).one()
        print(empleadoPuesto)

        
        # estatus baja, observaciones, fecha que se hizo y fecha de efecto
        empleadoPuesto.idCausaBaja = idCausaBaja
        empleadoPuesto.Observaciones = Observaciones
        empleadoPuesto.FechaEfecto = FechaEfectoFormateado

        empleadoPuesto.idQuincena = NumQuincena

        if checkboxConservarVacaciones is not None:
            empleadoPuesto.ConservaVacaciones = 1
        else:
            empleadoPuesto.ConservaVacaciones = 0

     
        db.session.commit()
        respuesta["Guardado"] = True
        hoy = hoy = datetime.today().date()

        if empleadoPuesto.FechaEfecto == hoy:
            print("ES HOY!")
            revision_baja_empleados(idPersona)
            respuesta["DadoBaja"] = True
        
    except NoResultFound:
        respuesta["Error"] = True

    return respuesta
