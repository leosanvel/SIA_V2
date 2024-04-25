from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from datetime import time, date, datetime
import os

from .routes import nomina
from app import db
from app.general.utils.funciones import permisos_de_edicion, permisos_de_consulta
from app.catalogos.models.models import *
from app.rh.empleado.models.models import Rbancopersona


@nomina.route('/Nomina/validarClabe', methods = ['POST', 'GET'])
@permisos_de_consulta
def validar_clabe():

    return render_template('/validarclabe.html', title = 'Validar Clabe')

@nomina.route('/Nomina/buscarClaveMasivo', methods = ['POST'])
@permisos_de_consulta
def obtener_clave_masivo():
    resultado = {}
    try:
        Clabes = db.session.query(Rbancopersona).filter_by(Activo = 1, Verificado = 0).all()
        lista_clabes = []
        for clabe in Clabes:
            try:
                Banco = db.session.query(Kbancos).filter_by(Codigo = clabe.Clabe[0:3]).one()
                clabe_dict = clabe.__dict__
                clabe_dict.pop("_sa_instance_state", None)
                clabe_dict["Banco"] = Banco.Nombre
                dir = url_for('nomina.descargar_EdoCuenta', nombre_archivo = clabe_dict["Clabe"] + '_' + str(clabe_dict["idPersona"]) + '.pdf')
                clabe_dict["url_descarga"] = dir
                lista_clabes.append(clabe_dict)

                resultado["banco"] = True
            except NoResultFound:
                resultado["banco"] = False
        resultado["encontrado"] = True
        return jsonify(lista_clabes)

    except NoResultFound:
        resultado["encontrado"] = False

        return jsonify(resultado)


@nomina.route('/Nomina/buscarClabe', methods = ['POST', 'GET'])
@permisos_de_consulta
def obtener_clabe():
    respuesta = {}
    idPersona = request.form.get("idPersona")
    try:
        Clabe = db.session.query(Rbancopersona).filter_by(idPersona = idPersona, Activo = 1).one()
        respuesta["encontrado"] = True
        if(Clabe.Verificado):
            respuesta["verificado"] = True
            return jsonify(respuesta)
        else:
            Clabe = Clabe.__dict__
            Clabe.pop("_sa_instance_state", None)

            try:
                Banco = db.session.query(Kbancos).filter_by(Codigo = Clabe["Clabe"][0:3]).one()
                Clabe["Banco"] = Banco.Nombre
            except NoResultFound:
                respuesta["Banco"] = False

            dir = url_for('nomina.descargar_EdoCuenta', nombre_archivo=Clabe["Clabe"] + '_' + idPersona + '.pdf')
            Clabe["url_descarga"] = dir
            return jsonify(Clabe)
            

    except NoResultFound:
        respuesta["encontrado"] = False

        return jsonify(respuesta)
    
@nomina.route('/Nomina/descargar_EdoCuenta/<nombre_archivo>')
def descargar_EdoCuenta(nombre_archivo):
    directorio_EdoCuenta = os.path.join(current_app.root_path, "rh", "empleado", "docs", "estados_cuenta")
    return send_from_directory(directory=directorio_EdoCuenta, path=nombre_archivo, as_attachment=True)

@nomina.route('/Nomina/verificarClabe', methods = ['POST'])
@permisos_de_edicion
def verificar_clabe():
    idPersona = request.form.get("idPersona")
    Clabe = request.form.get("Clabe")

    try:
        Clabe_existente = db.session.query(Rbancopersona).filter_by(idPersona = idPersona, Clabe = Clabe, Activo = 1).one()
        print(Clabe_existente)

        Clabe_existente.Verificado = 1
        db.session.commit()

        return({"verificado": True})
    except NoResultFound:
        return({"verificado": False})