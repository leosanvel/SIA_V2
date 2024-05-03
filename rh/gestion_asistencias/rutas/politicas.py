from .gestion_asistencias import gestion_asistencias
from flask import Blueprint, render_template, request, session, jsonify
from catalogos.modelos.modelos import *
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app import db
from rh.gestion_asistencias.modelos.modelos import rPoliticaPersona

@gestion_asistencias.route('/rh/gestion-asistencias/politicas', methods = ['GET'])
def politicas():
    return render_template('/politicas.html', title='Políticas',
                           current_user=current_user)

@gestion_asistencias.route('/rh/gestion-asistencias/buscar-politica', methods = ['GET','POST'])
def busca_politicas():
    idPersona = request.form.get('idPersona')

    lista_politicas = []
    politicas = db.session.query(kPoliticas)
    for politica in politicas:
        if politica is not None:
            politicas_dict = politica.__dict__
            politicas_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_politicas.append(politicas_dict)

    politicasPersona = db.session.query(rPoliticaPersona).filter_by(idPersona = idPersona).all()
    lista_politicas_persona = []
    for politica in politicasPersona:
        if politica is not None:
            politica_dict = politica.__dict__
            politica_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_politicas_persona.append(politica_dict)

    resultado = {
        'politicas': lista_politicas,
        'politicas_persona': lista_politicas_persona
    }

    return jsonify(resultado)

@gestion_asistencias.route('/rh/gestion-asistencias/guarda-politicas-persona', methods = ['GET','POST'])
def guarda_politicas_persona():

    data = request.get_json()

    idPersona = data.get('idPersona')
    checkboxes_data = data.get('checkboxesData')

    politicasPersona = db.session.query(rPoliticaPersona).filter_by(idPersona = idPersona).all()

    db.session.query(rPoliticaPersona).filter_by(idPersona=idPersona).delete()
    nuevas_politicas_persona = []

    for checkbox_id, checked in checkboxes_data.items():
        # Verificar si el checkbox está marcado
        if checked:
            # Crear una nueva instancia de Rpoliticapersona y agregarla a la lista
            nueva_politica_persona = rPoliticaPersona(idPersona=idPersona, idPolitica=checkbox_id)
            nuevas_politicas_persona.append(nueva_politica_persona)

    # Agregar las nuevas instancias a la sesión y hacer commit para guardar en la base de datos
    db.session.add_all(nuevas_politicas_persona)
    db.session.commit()
    
    return jsonify({"mensaje": "Formulario procesado con éxito"})