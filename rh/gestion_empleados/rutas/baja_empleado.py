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
    
    return render_template('/bajaempleado.html', title='Baja de empleado',
                           current_user=current_user)


@gestion_empleados.route('/rh/gestion-empleados/obtener-puestos-empleado', methods = ['POST', 'GET'])
def obtener_puestos_empleado():
    idPersona = request.form['idPersona']
    puestos = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idPersona == idPersona).all()
    lista_puestos = []
    for puesto in puestos:
        if puesto is not None:
            puesto_dict = puesto.__dict__
            puesto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_puestos.append(puesto_dict)
    print("lista_puestos")
    print(lista_puestos)
    return jsonify(lista_puestos)
