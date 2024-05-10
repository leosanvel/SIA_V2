from .gestion_tiempo_no_laboral import gestion_tiempo_no_laboral
from flask import render_template, request, session, jsonify
from sqlalchemy.orm.exc import NoResultFound

from app import db

from rh.gestion_tiempo_no_laboral.modelos.modelos import rDiasPersona

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/vacaciones-ganadas', methods = ['POST', 'GET'])
def vacaciones_ganadas():
    return render_template('/vacaciones_ganadas.html', title = 'Vacaciones ganadas')

@gestion_tiempo_no_laboral.route('/rh/gestion-*tiempo-no-laboral/obtener-dias-persona', methods = ['POST'])
def obtener_dias_persona():
    idPersona = request.form.get("idPersona")

    DiasPersona = db.session.query(rDiasPersona).filter(rDiasPersona.idPersona == idPersona, rDiasPersona.DiasGanados != 0, rDiasPersona.Activo != 0).order_by(rDiasPersona.DiasGanados.asc()).all()

    lista_diaspersona = []
    for DiasPersona_aux in DiasPersona:
        if DiasPersona_aux is not None:
            DiasPersona_dict = DiasPersona_aux.__dict__
            DiasPersona_dict.pop("_sa_instance_state", None)
            lista_diaspersona.append(DiasPersona_dict)

    return jsonify(lista_diaspersona)