from .gestion_tiempo_no_laboral import gestion_tiempo_no_laboral
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from app import db
from rh.gestion_tiempo_no_laboral.modelos.modelos import rDiasPersona
from rh.gestion_empleados.modelos.empleado import rEmpleado
from catalogos.modelos.modelos import kPeriodoVacacional

# Dias persona
@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/dias-persona', methods = ['POST', 'GET'])
def gestiona_dias_persona():
    periodovacacional = db.session.query(kPeriodoVacacional).all()
    return render_template('/dias_persona.html', title='Días persona',
                           current_user=current_user,
                           PeriodoVacacional = periodovacacional)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/guardar-dias-persona', methods = ['POST'])
def guarda_diasPersona():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPeriodo' : 'idPeriodo',
        'idPersona' : 'idPersona',
        'DiasGanados' : 'DiasGanados',
        'Fecha' : 'Fecha',
        'Activo': 'Activo'
    }
    idPeriodoVacacional = request.form.get("idPeriodoVacacional")
    diasPersona_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    diasPersona_data['Fecha'] = datetime.now().date()
    diasPersona_data["Activo"] = 1
        
    if(diasPersona_data["idPeriodo"] != "3"):
        PeriodoVacacional = db.session.query(kPeriodoVacacional).filter_by(idPeriodoVacacional = idPeriodoVacacional).first()
        diasPersona_data['idPeriodo'] = PeriodoVacacional.idPeriodo
        Personas = db.session.query(rEmpleado).filter_by(idTipoEmpleado = 2, Activo = 1).all()
        nuevo_diaPersona = None
        for persona in Personas:
            diasPersona_data["idPersona"] = persona.idPersona
            try:
                diasPersona_existente = db.session.query(rDiasPersona).filter_by(idPersona = diasPersona_data["idPersona"],
                                                                                idPeriodo=diasPersona_data["idPeriodo"],
                                                                                DiasGanados = diasPersona_data["DiasGanados"],
                                                                                Fecha = diasPersona_data["Fecha"],
                                                                                ).one()
                diasPersona_existente.update(**diasPersona_data)
            except NoResultFound:
                nuevo_diaPersona = rDiasPersona(**diasPersona_data)
                
                db.session.add(nuevo_diaPersona)
    else:
        try:
            diasPersona_existente = db.session.query(rDiasPersona).filter_by(idPersona = diasPersona_data["idPersona"],
                                                                            idPeriodo=diasPersona_data["idPeriodo"],
                                                                            DiasGanados = diasPersona_data["DiasGanados"],
                                                                            Fecha = diasPersona_data["Fecha"],
                                                                            ).one()
        except NoResultFound:
            nuevo_diaPersona = rDiasPersona(**diasPersona_data)
            db.session.add(nuevo_diaPersona)

    db.session.commit()
    return({"guardado": True})

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/buscar-dias-persona', methods = ['POST'])
def buscar_dias_persona():

    diasPersonas = db.session.query(rDiasPersona).all()

    lista_dias = []
    for dia in diasPersonas:
        if dia is not None:
            Nombre = dia.Empleado.Persona.Nombre
            ApPaterno = dia.Empleado.Persona.ApPaterno
            ApMaterno = dia.Empleado.Persona.ApMaterno
            dia_dict = dia.__dict__
            dia_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            dia_dict.pop("Empleado")
            dia_dict["Nombre"] = Nombre + ' ' + ApPaterno + ' ' + ApMaterno
            lista_dias.append(dia_dict)
    return jsonify(lista_dias)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/buscar-dias-persona-por-empleado', methods = ['POST'])
def buscar_dias_persona_por_empleado():
    idPersona = request.form.get("idPersona")

    diasPersona = db.session.query(rDiasPersona).filter_by(idPersona = idPersona).all()

    lista_dias = []
    for dia in diasPersona:
        if dia is not None:
            dia_dict = dia.__dict__
            dia_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_dias.append(dia_dict)

    return jsonify(lista_dias)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/eliminar-dias', methods = ['POST'])
def eliminar_dias():
    id = request.form.get('id')
    DiasPersonas = db.session.query(rDiasPersona).all()
    Dia_Persona = DiasPersonas[int(id) - 1]
    Dia_Persona.DiasGanados = 0
    db.session.add(Dia_Persona)
    db.session.commit()

    return({"eliminado": True})