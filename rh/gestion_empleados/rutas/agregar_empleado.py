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
from catalogos.modelos.modelos import *
from app import db
from general.herramientas.funciones import *

@gestion_empleados.route('/rh/gestion-empleados/busqueda-empleado', methods = ['POST', 'GET'])
def busqueda_empleado():
    session["idPersona"] = None
    return render_template('/buscarempleado.html', title='Búsqueda de empleado',
                           current_user=current_user)

@gestion_empleados.route('/rh/gestion-empleados/agregar-empleado', methods = ['POST', 'GET'])
@gestion_empleados.route('/rh/gestion-empleados/modificar-empleado', methods = ['POST', 'GET'])
def modificar_empleado():
    if request.path == '/rh/gestion-empleados/modificar-empleado':
            idSelec = session.get("idPersona",None)
            if idSelec is None:
                return redirect('/rh/gestion-empleados/agregar-empleado')
            titulo = "Modifica empleado"
    else:
            if current_user.idRol == 2 :
                return redirect('/rh/gestion-empleados/busqueda-empleado')
            idSelec = None
            session["idPersona"] = None
            titulo = "Agrega empleado"
    empleado  = db.session.query(Persona).filter_by(idPersona = idSelec).first()

    return render_template('/formularioEstatus.html', title = titulo,
                           current_user = current_user)