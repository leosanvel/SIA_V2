from .rutas import informatica
from flask import render_template, jsonify, request
from flask_login import current_user
from sqlalchemy import asc
from rh.gestion_empleados.modelos.empleado import rEmpleado
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from app import db


from catalogos.modelos.modelos import kEstadoSolicitud
from informatica.modelos.modelos import rSolicitudEstado

from general.herramientas.funciones import *

@informatica.route('/informatica/solicitudes')
@permisos_de_consulta
def solicitudes():
    return render_template('/solicitudes.html', title ='Solicitudes',
                            current_user=current_user)

@informatica.route('/informatica/solicitudes/cargar-solicitudes', methods=['POST', 'GET'])
@permisos_de_consulta
def carga_solicitudes():
    empleado_existente =  db.session.query(rEmpleado).order_by(asc(rEmpleado.idPersona)).first()

    try:
        # solicitudes = db.session.query(rSolicitudEstado).all()
        solicitudes = db.session.query(rSolicitudEstado).order_by(asc(rSolicitudEstado.idEstadoSolicitud)).all()
        lista_solicitudes = []
        for solicitud in solicitudes:
            if solicitud is not None:
                solicitud_dict = solicitud.__dict__
                solicitud_dict.pop("_sa_instance_state", None)
                
                estado = db.session.query(kEstadoSolicitud).filter_by(idEstadoSolicitud = solicitud_dict["idEstadoSolicitud"]).first()
                solicitud_dict["Estado"] = estado.Estado
                lista_solicitudes.append(solicitud_dict)


    except NoResultFound:
        lista_solicitudes = None


    try:
        estados = db.session.query(kEstadoSolicitud).all()
        lista_estados = []
        for estado in estados:
            if estado is not None:
                estado_dict = estado.__dict__
                estado_dict.pop("_sa_instance_state", None)
                lista_estados.append(estado_dict)
    except NoResultFound:
        lista_estados = None

    return jsonify({
        "estadosSolicitud" : lista_estados,    
        "Solicitudes" : lista_solicitudes})    

@informatica.route("/informatica/solicitudes/guarda-solicitud", methods = ['POST'])
def guarda_solicitud():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idSolicitud': 'idSolicitud',
        'idEstadoSolicitud': 'idEstadoSolicitud',
    }
    solicitud_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    guardar_o_modificar_solicitud(solicitud_data)
    return jsonify(solicitud_data)

def guardar_o_modificar_solicitud(solicitud_data):
    nueva_solicitud = None
    try:
        solicitud_a_modificar = db.session.query(rSolicitudEstado).filter(rSolicitudEstado.idSolicitud == solicitud_data["idSolicitud"]).one()
        # Actualizar los atributos de 'solicitud_existente' con los valores de 'solicitud_data'
        for attr, value in solicitud_data.items():
            if not attr.startswith('_') and hasattr(solicitud_a_modificar, attr):
                setattr(solicitud_a_modificar, attr, value)
                
    except NoResultFound:
        nueva_solicitud = rSolicitudEstado(**solicitud_data)
        db.session.add(nueva_solicitud)
        
    # Realizar cambios en la base de datos
    db.session.commit()
    if int(solicitud_data["idEstadoSolicitud"]) == 3:
        print("MARCADO COMO COMPLETADO")
        envia_correo("rh","solicitud_completada",solicitud_a_modificar)


@informatica.route("/informatica/solicitudes/cancela-solicitud", methods = ['POST', 'GET'])
@permisos_de_consulta
def cancela_solicitud():
    idSolicitud = request.form.get('idSolicitud')
    solicitud = db.session.query(rSolicitudEstado).filter_by(idSolicitud = idSolicitud).first()
    if solicitud is not None:
        solicitud_dict = solicitud.__dict__
        solicitud_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify(solicitud_dict)
    else:
        return jsonify(False)