from flask import request, session, jsonify, url_for, current_app, send_from_directory
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
        TipoEmpleado = empleadopuesto_datos.Empleado.idTipoEmpleado
        if TipoEmpleado == 2:
            idCentroCosto = empleadopuesto_datos.Puesto.idCentroCosto
            Puesto = empleadopuesto_datos.Puesto.Puesto
        elif TipoEmpleado == 1:
            Puesto = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = empleadopuesto_datos.idPuesto).first()
            idCentroCosto = empleadopuesto_datos.idCentroCosto
            Puesto = Puesto.PuestoHonorarios

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
        if TipoEmpleado == 2:
            puesto_data_dict = puesto_data.__dict__
            puesto_data_dict.pop("_sa_instance_state", None)
        empleado_datos = {**persona_data_dict, **empleado_data_dict, **empleadopuesto_datos_dict, 'idCentroCosto': idCentroCosto, 'Puesto': Puesto}
        empleado_datos["idQuincena"] = idQuincena

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
    url = None
    if(datos_bancarios is not None):
        Banco = datos_bancarios.Banco.Nombre
        datos_bancarios = datos_bancarios.__dict__
        datos_bancarios.pop("_sa_instance_state", None)
        datos_bancarios["Banco"] = Banco

        filename = datos_bancarios["Clabe"] + "_" + str(idPersona) + ".pdf"
        dir = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "estados_cuenta", filename)
        if os.path.exists(dir):
            datos_bancarios["EstadoCuenta"] = True
            url = url_for("gestion_empleados.descargar_estado_cuenta", nombre_archivo = filename)
            print(dir)
        else:
            url = None

    return jsonify({"datos_bancarios": datos_bancarios, "url": url})

@gestion_empleados.route("/rh/gestion-empleados/obtener-expediente", methods = ["POST"])
def obtener_expediente():
    idPersona = session.get('idPersona', None)
    Empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
    NumEmpleado = Empleado.NumeroEmpleado
    Nombre = Empleado.Persona.Nombre
    ApPaterno = Empleado.Persona.ApPaterno
    ApMaterno = Empleado.Persona.ApMaterno
    url = None

    expediente = db.session.query(rPersonaExpediente).filter_by(idPersona = idPersona).first()
    if expediente is not None:
        expediente = expediente.__dict__
        expediente.pop("_sa_instance_state", None)

        filename = str(NumEmpleado) + "_" + Nombre + " " + ApPaterno + " " + ApMaterno + ".pdf"

        if os.path.exists(os.path.join("rh", "gestion_empleados", "archivos", "expedientes", filename)):
            print("Existe expediente")
            url = url_for("gestion_empleados.descargar_expediente", nombre_archivo = filename)
        else:
            print("No existe expediente")
            url = None

    return jsonify({"expediente":expediente, "url":url})

@gestion_empleados.route("/rh/gestion-empleados/obtener-mas-informacion", methods = ["POST"])
def obtener_mas_informacion():
    idPersona = session.get("idPersona", None)
    

    mas_informacion = db.session.query(rPersonaMasInformacion).filter_by(idPersona = idPersona).first()
    if mas_informacion is not None:
        mas_informacion = mas_informacion.__dict__
        mas_informacion.pop("_sa_instance_state", None)

    Idiomas = db.session.query(rPersonaIdioma).filter_by(idPersona = idPersona).all()
    lista_Idiomas = []

    for idioma in Idiomas:
        if idioma is not None:
            idioma = idioma.__dict__
            idioma.pop("_sa_instance_state", None)
            lista_Idiomas.append(idioma)

    Indigenas = db.session.query(rPersonaIndigena).filter_by(idPersona = idPersona).all()
    lista_Indigenas = []

    for indigena in Indigenas:
        if indigena is not None:
            indigena = indigena.__dict__
            indigena.pop("_sa_instance_state", None)
            lista_Indigenas.append(indigena)

    return jsonify({"mas_informacion": mas_informacion, "Idiomas": lista_Idiomas, "Indigenas": lista_Indigenas})

@gestion_empleados.route("/rh/gestion-empleados/descargar-expediente/<nombre_archivo>")
def descargar_expediente(nombre_archivo):
    dir = os.path.join("rh", "gestion_empleados", "archivos", "expedientes")
    return send_from_directory(directory=dir, path=nombre_archivo, as_attachment=True)

@gestion_empleados.route("/rh/gestion-empleados/descargar-estado-cuenta/<nombre_archivo>")
def descargar_estado_cuenta(nombre_archivo):
    dir = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "estados_cuenta")
    return send_from_directory(directory=dir, path=nombre_archivo, as_attachment=True)