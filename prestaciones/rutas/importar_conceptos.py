from .rutas import prestaciones
from flask import render_template, request, jsonify
from flask_login import current_user

from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from prestaciones.modelos.modelos import rEmpleadoConcepto, rEmpleadoSueldo
from rh.gestion_empleados.modelos.empleado import rEmpleado
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc
from datetime import datetime

@prestaciones.route('/prestaciones/importar-conceptos')
def importar_conceptos():

    return render_template('/importar_conceptos.html', title ='Importar conceptos',
                            current_user=current_user)


@prestaciones.route('/prestaciones/filtrar-conceptos-extrae-archivo', methods = ['POST'])
def filtrar_conceptos_extraeArchivo():
    conceptos = db.session.query(kConcepto).filter_by(ExtraeArchivo = 1).all()
    print(type(conceptos))
    lista_conceptos = []
    for elemento in conceptos:
        if elemento is not None:
            elemento_dict = elemento.__dict__
            elemento_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_conceptos.append(elemento_dict)
    if not lista_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_conceptos)

