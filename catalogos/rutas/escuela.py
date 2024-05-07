from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kEscolaridad, kInstitucionEscolar, rEscolaridadInstitucion
from general.herramientas.funciones import eliminar_caracter

@catalogos.route('/catalogos/escuela', methods = ['POST', 'GET'])
def catalogo_escuela():
    Escolaridad = db.session.query(kEscolaridad).filter_by(Activo = 1).order_by(kEscolaridad.Escolaridad).all()
    columns = inspect(kInstitucionEscolar).all_orm_descriptors.keys()
    return render_template('/escuela.html', title='Escuela',
                           current_user=current_user,
                           Escolaridad = Escolaridad,
                           columns = columns)