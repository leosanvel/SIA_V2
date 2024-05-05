from .gestion_tiempo_no_laboral import gestion_tiempo_no_laboral
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app import db
from rh.gestion_tiempo_no_laboral.modelos.modelos import kDiasFestivos

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/dias-festivos', methods = ['POST', 'GET'])
def gestiona_diasfestivos():
 
    return render_template('/dias_festivos.html', title='Días Festivos',
                           current_user=current_user)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/guardar-dia-festivo', methods = ['POST'])
def guarda_festividad():
    mapeo_nombres = {
        'Fecha_format': 'Fecha',
        'Descripcion': 'Descripcion'
    }
    Festividad_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    FechaFestiva = Festividad_data.get(mapeo_nombres["Fecha_format"], None)
    nueva_festividad = None
    try:
        festividad_existente = db.session.query(kDiasFestivos).filter_by(Fecha=FechaFestiva).one()
        # Si llegamos aquí, significa que ya existe una festividad
        # Actualizar los atributos de 'festividad_existente' con los valores de 'festividad_data'
        festividad_existente.update(**Festividad_data)
        # for attr, value in festividad_data.items():
        #     if not attr.startswith('_') and hasattr(festividad_existente, attr):
        #         setattr(festividad_existente, attr, value)
                
    except NoResultFound:
            nueva_festividad = kDiasFestivos(**Festividad_data)
            db.session.add(nueva_festividad)

    # Realizar cambios en la base de datos
    db.session.commit()
    return jsonify(Festividad_data)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/consulta-dias-festivos', methods = ['POST'])
def consulta_festividad():
    festividades = db.session.query(kDiasFestivos).all()
    lista_festividades = []
    for festividad in festividades:
        if festividad is not None:
            festividad_dict = festividad.__dict__
            festividad_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_festividades.append(festividad_dict)
    return jsonify(lista_festividades)

@gestion_tiempo_no_laboral.route('/rh/gestion-tiempo-no-laboral/buscar-dia-festivo', methods = ['POST'])
def busca_festividad():
    FechaFestiva = request.form.get('Fecha_formateada')
    if(FechaFestiva != ""):
        festividad_existente  = db.session.query(kDiasFestivos).filter_by(Fecha = FechaFestiva).first()
        if festividad_existente is not None:
            festividad_existente = festividad_existente.__dict__
            festividad_existente.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify(festividad_existente)
    else:
        return jsonify({"Encontrado": False})
