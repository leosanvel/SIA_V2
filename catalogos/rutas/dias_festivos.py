from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from rh.gestion_tiempo_no_laboral.modelos.modelos import kDiasFestivos

@catalogos.route('/catalogos/dias-festivos', methods = ['POST', 'GET'])
def catalogo_diasfestivos():
    DiasFestivos = db.session.query(kDiasFestivos).all()
    return render_template('/dias_festivos.html', title = 'Dias Festivos',
                           DiasFestivos = DiasFestivos)