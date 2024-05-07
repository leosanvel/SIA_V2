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

from app import db
from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import rBancoPersona

@gestion_empleados.route('/rh/gestion-empleados/clabe-interbancaria', methods = ['POST', 'GET'])
def catalogo_clabe():

    return render_template('/clabe_interbancaria.html', title = 'Clabe Interbancaria')

@gestion_empleados.route('/rh/gestion-empleados/buscar-clabe', methods = ['POST'])
def buscar_clabe():
    idPersona = request.form.get("idPersona")
    try:
        Clabes = db.session.query(rBancoPersona).filter_by(idPersona = idPersona).all()
        lista_clabes = []
        for clabe in Clabes:
            if clabe is not None:
                clabe_dict = clabe.__dict__
                clabe_dict.pop("_sa_instance_state", None)
                lista_clabes.append(clabe_dict)

        return jsonify(lista_clabes)

    except NoResultFound:
        return jsonify({"encontrado": False})
    
@gestion_empleados.route('/rh/gestion-empleados/modificar-clabe', methods = ['POST'])
def modificar_clabe():
    mapeo_nombres = {
        'idPersona': 'idPersona',
        'Clabe': 'Clabe',
        'Activo': 'Activo'
    }
    clabe_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    try:
        Clabe_existente = db.session.query(rBancoPersona).filter_by(idPersona = clabe_data["idPersona"], Clabe = clabe_data["Clabe"]).one()
        Clabe_existente.Activo = clabe_data["Activo"]
        db.session.commit()

        return jsonify({"encontrado": True})

    except NoResultFound:
        return jsonify({"encontrado": False})