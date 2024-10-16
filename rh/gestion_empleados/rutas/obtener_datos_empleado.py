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
import json
import datetime

from .gestion_empleados import gestion_empleados
from app import db
from rh.gestion_empleados.modelos.empleado import *
from rh.gestion_empleados.modelos.domicilio import *
from general.herramientas.funciones import serialize_datetime

@gestion_empleados.route('/rh/gestion-empleados/obtener-info-empleado', methods = ['POST'])
def obtener_info_empleado():
    idPersona = session.get('idPersona', None)
    empleadopuesto_datos = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona).order_by(rEmpleadoPuesto.FechaInicio.desc()).first()
    empleado_datos = {}
    if empleadopuesto_datos is not None:
        idCentroCosto = empleadopuesto_datos.Puesto.idCentroCosto
        Puesto = empleadopuesto_datos.Puesto.Puesto
        idQuincena = empleadopuesto_datos.Empleado.idQuincena
        persona_data = empleadopuesto_datos.Empleado.Persona
        empleado_data = empleadopuesto_datos.Empleado
        puesto_data = empleadopuesto_datos.Puesto
        empleadopuesto_datos_dict = empleadopuesto_datos.__dict__
        empleadopuesto_datos_dict.pop("_sa_instance_state", None)
        empleadopuesto_datos_dict.pop("Empleado")
        empleadopuesto_datos_dict.pop("Puesto")
        persona_data_dict = persona_data.__dict__
        persona_data_dict.pop("_sa_instance_state", None)
        empleado_data_dict = empleado_data.__dict__
        empleado_data_dict.pop("_sa_instance_state", None)
        empleado_data_dict.pop("Persona")
        puesto_data_dict = puesto_data.__dict__
        puesto_data_dict.pop("_sa_instance_state", None)
        empleado_datos = {**persona_data_dict, **empleado_data_dict, **empleadopuesto_datos_dict, 'idCentroCosto': idCentroCosto, 'Puesto': Puesto}
        empleado_datos["idQuincena"] = idQuincena
    print("empleado_datos")
    print(empleado_datos)    
    return jsonify(empleado_datos)

@gestion_empleados.route('/rh/gestion-empleados/obtener-domicilio', methods = ['POST'])
def obtener_domicilio():
    idPersona = session.get('idPersona', None)
    tipo = request.form.get("tipo")
    domicilio = db.session.query(rDomicilio).filter_by(idPersona = idPersona, idTipoDomicilio=tipo).first()
    if domicilio is not None:
        domicilio = domicilio.__dict__
        domicilio.pop("_sa_instance_state", None)
    return jsonify(domicilio)

@gestion_empleados.route('/rh/gestion-empleados/obtener-escolaridad', methods = ['POST'])
def obtener_escolaridad():
    idPersona = session.get('idPersona', None)
    escolaridad = db.session.query(rPersonaEscolaridad).filter_by(idPersona = idPersona).first()
    if escolaridad is not None:
        escolaridad = escolaridad.__dict__
        escolaridad.pop("_sa_instance_state", None)
    
    return jsonify(escolaridad)

@gestion_empleados.route('/rh/gestion-empleados/obtener-datos-bancarios', methods = ["POST"])
def obtener_datos_bancarios():
    idPersona = session.get('idPersona', None)
    datos_bancarios = db.session.query(rBancoPersona).filter_by(idPersona = idPersona, Activo = 1).first()
    if(datos_bancarios is not None):
        Banco = datos_bancarios.Banco.Nombre
        datos_bancarios = datos_bancarios.__dict__
        datos_bancarios.pop("_sa_instance_state", None)
        datos_bancarios["Banco"] = Banco


    return jsonify(datos_bancarios)