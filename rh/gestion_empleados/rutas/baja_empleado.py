from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory
from flask_login import current_user
from sqlalchemy import or_, inspect, func, and_
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from docx.shared import Cm, Inches, Mm, Emu
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import pythoncom
import os

from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *
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
    idPersona = request.form['idPersona']
    try:
        empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona, Activo = 1).one()
        puesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idPersona == idPersona, rEmpleadoPuesto.idEstatusEP == 1).first()
        respuesta = {}
        if puesto is not None:
            tipoEmpleado = db.session.query(kTipoEmpleado).filter_by(idTipoEmpleado = empleado.idTipoEmpleado).first()

            respuesta["NumeroEmpleado"] = empleado.NumeroEmpleado
            respuesta["TipoEmpleado"] = tipoEmpleado.TipoEmpleado
            respuesta["TipoAlta"] = empleado.NumeroEmpleado
            respuesta["TipoBaja"] = empleado.NumeroEmpleado
            
            
            causas = db.session.query(kCausaBaja).filter(kCausaBaja.idTipoEmpleado == empleado.idTipoEmpleado).all()
            lista_causas_baja = []
            for causa in causas:
                causa_dict = causa.__dict__
                causa_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                lista_causas_baja.append(causa_dict)
            respuesta["CausasBaja"] = lista_causas_baja
        
            puesto_dict = puesto.__dict__
            puesto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            respuesta["Puesto"] = puesto_dict
        else:
            respuesta["NoEncontrado"] = True
    except NoResultFound:    
        respuesta["NoEncontrado"] = True
    return jsonify(respuesta)


@gestion_empleados.route('/rh/gestion-empleados/dar-baja-empleado', methods = ['POST', 'GET'])
def dar_baja_empleado():
    
    idPersona = request.form['idPersona']
    idPuesto = request.form['idPuesto']
    FechaEfecto = request.form['FechaEfecto']
    respuesta = {}
    try:
        empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona, Activo = 1).one()

        puesto = db.session.query(tPuesto).filter_by(ConsecutivoPuesto = idPuesto).one()
        empleadoPuesto = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona, idPuesto = idPuesto).one()
        
        # cambiar en tPuesto idEstatusPuesto (a vacante (2))
        puesto.idEstatusPuesto = 2

        # (1 = Ocupada, 2 = Vacante
        empleadoPuesto.idEstatusEP = 2
        empleadoPuesto.FechaTermino = datetime.strptime(FechaEfecto, '%d/%m/%Y')


        # estatus baja, observaciones, fecha que se hizo y fecha de efecto
        # vaciar: rconcepto empleado

        db.session.commit()
        respuesta["Exito"] = True
    except NoResultFound:
        respuesta["Error"] = True

    return respuesta
