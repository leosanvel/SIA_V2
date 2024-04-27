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
from app import db
from rh.gestion_empleados.modelos.empleado import *
from rh.gestion_empleados.modelos.domicilio import *

@gestion_empleados.route('/rh/gestion-empleados/obtener-info-empleado', methods = ['POST'])
def obtener_info_empleado():
    idPersona = session.get('idPersona', None)
    print("idPersona")
    empleadopuesto_datos = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona, idEstatusEP = 1).first()
    print(idPersona)
    empleado_datos = {}
    if empleadopuesto_datos is not None:
        print("HOOOOOLAAA")
        print("empleadopuesto_datos.idPuesto")
        print(empleadopuesto_datos.idPuesto)
        print(empleadopuesto_datos.Empleado.Persona.Nombre)
        print(empleadopuesto_datos.Puesto.Puesto)
        empleado_datos = {
            "CURP": empleadopuesto_datos.Empleado.Persona.CURP,
            "Nombre": empleadopuesto_datos.Empleado.Persona.Nombre,
            "ApPaterno": empleadopuesto_datos.Empleado.Persona.ApPaterno,
            "ApMaterno": empleadopuesto_datos.Empleado.Persona.ApMaterno,
            "Sexo": empleadopuesto_datos.Empleado.Persona.Sexo,
        }
        # idTipoEmpleado = empleado.Empleado.idTipoEmpleado
        # idPuesto = empleado.Empleado.Puesto.ConsecutivoPuesto
        # idCentroCosto = empleado.Empleado.Puesto.idCentroCosto
        # empleado_dict = empleado.__dict__
        # empleado_dict.pop("_sa_instance_state", None)
        # empleado_dict["idTipoEmpleado"] = idTipoEmpleado
        # empleado_dict["idCentroCosto"] = idCentroCosto
        # empleado_dict["idPuesto"] = idPuesto
        # empleado_dict.pop("Empleado")
        # #print(empleado)
        # print(empleado_dict)
    return jsonify(empleado_datos)

@gestion_empleados.route('/RH/obtener_domicilio', methods = ['POST'])
def obtener_domicilio():
    idPersona = session.get('idPersona', None)
    tipo = request.form.get("tipo")
    domicilio = db.session.query(rDomicilio).filter_by(idPersona = idPersona, idTipoDomicilio=tipo).first()
    if domicilio is not None:
        domicilio = domicilio.__dict__
        domicilio.pop("_sa_instance_state", None)
    return jsonify(domicilio)