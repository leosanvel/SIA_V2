from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory, url_for
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
from rh.gestion_empleados.modelos.empleado import rEmpleado, tPersona
from rh.gestion_empleados.modelos.domicilio import rDomicilio
from catalogos.modelos.modelos import kCodigoPostal, kTipoAsentamiento, kMunicipio, kEntidad

@gestion_empleados.route('/rh/gestion-empleados/generar-contratos', methods = ['POST', 'GET'])
def generar_contratoshonorarios():
    Empleados = db.session.query(tPersona).join(rEmpleado).filter(rEmpleado.idTipoEmpleado == 1, rEmpleado.Activo == 1).order_by(tPersona.ApPaterno).all()
    
    return render_template('/generar_contratohonorarios.html', title = 'Generar Contrato de Honorarios',
                           Empleados = Empleados)

#Generar Contratos de Honorarios
@gestion_empleados.route("/RH/generarContrato", methods = ['POST'])
def generar_contrato():
    idPersona = request.form.get("idPersona")
    empleado = db.session.query(tPersona).filter_by(idPersona = idPersona).first()
    Domicilio = db.session.query(rDomicilio).filter_by(idPersona = idPersona, idTipoDomicilio = 1).first()
    Asentamiento = db.session.query(kCodigoPostal).filter(kCodigoPostal.CodigoPostal == Domicilio.idCP).order_by(kCodigoPostal.Consecutivo.desc()).first()
    TipoAsentamiento = db.session.query(kTipoAsentamiento).filter_by(idTipoAsentamiento = Domicilio.idTipoAsentamiento).first()
    Municipio = db.session.query(kMunicipio).filter(kMunicipio.idMunicipio == Domicilio.idMunicipio).order_by(kMunicipio.Consecutivo.desc()).first()
    Entidad = db.session.query(kEntidad).filter(kEntidad.idEntidad == Domicilio.idEntidad).order_by(kEntidad.Consecutivo.desc()).first()
    hoy = datetime.now()

    meses = {
    "1":'ENERO',
    "2":'FEBRERO',
    "3":'MARZO',
    "4":'ABRIL',
    "5":'MAYO',
    "6":'JUNIO',
    "7":'JULIO',
    "8":'AGOSTO',
    "9":'SEPTIEMBRE',
    "10":'OCTUBRE',
    "11":'NOVIEMBRE',
    "12":'DICIEMBRE'
}

    nombre = empleado.ApPaterno + " " + empleado.ApMaterno + " " + empleado.Nombre
    dom = Domicilio.Vialidad + " NO. " + str(Domicilio.NumExterior) + ", "+ str(TipoAsentamiento.TipoAsentamiento).upper() + " " + Asentamiento.Asentamiento + ", " + "C.P. "+ str(Domicilio.idCP)+ ", " + Municipio.Municipio + ", " + Entidad.Entidad
    #Abrir documento .docx
    template = DocxTemplate("rh/gestion_empleados/archivos/prueba.docx")
    #Diccionario con la información
    data_contrato = {
        'Nombre': nombre,
        'dia': str(hoy.day),
        'mes': meses[str(hoy.month)],
        'anio': str(hoy.year),
        'RFC': empleado.RFC,
        'NivelEscolar': "",
        'FormacionEducativa': "",
        'Domicilio': dom
    }

    # Escribir información en el archivo .docx
    template.render(data_contrato)

    # 
    dir = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "contratos")
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Directorio %s creado" % dir)
    else:
        print("Directorio %s ya existe" % dir)

    # Guardar documento generado
    template.save(f"rh/gestion_empleados/archivos/contratos/Contrato " + nombre + ".docx")

    # Convertir archivo .docx a archivo .pdf
    pythoncom.CoInitialize()
    convert("rh/gestion_empleados/archivos/contratos/Contrato " + nombre + ".docx", "rh/gestion_empleados/archivos/contratos/Contrato " + nombre + ".pdf")

    return jsonify({"url_descarga": url_for('gestion_empleados.descargar_contrato', nombre_archivo="Contrato " + nombre + ".pdf"), "generado": True})

@gestion_empleados.route('/RH/descargar_contrato/<nombre_archivo>')
def descargar_contrato(nombre_archivo):
    directorio_archivos = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "contratos")

    return send_from_directory(directorio_archivos, nombre_archivo, as_attachment=True)