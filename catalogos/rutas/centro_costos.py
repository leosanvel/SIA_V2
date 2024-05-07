from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kCentroCostos

@catalogos.route('/catalogos/centro-costos', methods = ['POST', 'GET'])
def catalogos_centro_costos():
    # Consulta de la información en tabla Centro Costo
    centrocostos = db.session.query(kCentroCostos).all()
    return render_template('/centro_costos.html', title='Centro de costos',
                           current_user = current_user,
                           centrocostos = centrocostos)

# Ruta para la página para crear la tabla con la información
@catalogos.route('/catalogos/cargar-centro-costos', methods = ['POST'])
def cargar_centro_costos():
    # Consulta de la información Centro Costos
    centrocostos = db.session.query(kCentroCostos).all()
    #columns = inspect(Centrocostos).all_orm_descriptors.keys()

    ret = '<thead><tr>'

    #for columna in columns:
        #ret += '<th>{}</th>'.format(columna)
    # Nombre de columnas
    ret += '<th> ID Centro Costo </th>'
    ret += '<th> Clave </th>'
    ret += '<th> ID Entidad </th>'
    ret += '<th> Centro Costo </th>'
    ret += '<th> Materia </th>'
    ret += '<th> Abreviatura </th>'
    ret += '<th> Registro Contable </th>'
    ret += '<th> ID Ciudad </th>'
    ret += '<th> ID Centro Costo Real </th>'

    ret += '</thead><tbody>'

    # Información
    for data in centrocostos:
        ret += '<tr>'
        ret += '<td><input type="text" class="form-control" id="idCentroCosto{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.idCentroCosto)
        ret += '<td><input type="text" class="form-control" id="Clave{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.Clave)
        ret += '<td><input type="text" class="form-control" id="Entidad{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.idEntidad)
        ret += '<td><input type="text" class="form-control" id="CentroCosto{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.CentroCosto)
        ret += '<td><input type="text" class="form-control" id="Materia{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.Materia)
        ret += '<td><input type="text" class="form-control" id="Abreviatura{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.Abreviatura) 
        ret += '<td><input type="text" class="form-control" id="RegistroContable{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.RegistroContable)
        ret += '<td><input type="text" class="form-control" id="Ciudad{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.idCiudad)
        ret += '<td><input type="text" class="form-control" id="CentroCostoReal{}" value="{}" readonly></td>'.format(data.idCentroCosto, data.idCentroCostoReal)

        # Botones para modificar información
        ret += '<td><button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar{}" onclick="editar_aceptar({})">Editar</button></td>'.format(data.idCentroCosto, data.idCentroCosto)
        ret += '<td><button type="button" class="btn btn-secondary oculta-empleado" id="Cancelar{}" onclick="cancelar({}, {}, {}, \'{}\', \'{}\', \'{}\', {}, {}, {})" style="display: none">Cancelar</button></td>'.format(data.idCentroCosto, data.idCentroCosto, data.Clave, data.idEntidad, data.CentroCosto, data.Materia, data.Abreviatura, data.RegistroContable, data.idCiudad, data.idCentroCostoReal)
        ret += '</tr>'

    ret += '</tbody>'

    #print(ret)

    return ret

# Ruta para guardar información modificada
@catalogos.route('/catalogos/guardar_centro-costos', methods = ['POST'])
def guardar_centro_costos():
    columnas = inspect(kCentroCostos).all_orm_descriptors.keys()
    # Obtención de información a modificar
    idCC = request.form.get('idCentroCosto')
    CC_data = {key: request.form.get(key) for key in columnas}
    nuevo_CC = None
    try:
        # Si existe el objeto con el ID correspondiente
        CC_existente = db.session.query(kCentroCostos).filter_by(idCentroCosto = idCC).one()
        # Se actualiza la información
        for attr, value in CC_data.items():
            if not attr.startswith('_') and hasattr(CC_existente, attr):
                setattr(CC_existente, attr, value)
    except NoResultFound:
        # Si no existe se crea uno nuevo
        ultimo_CC = db.session.query(kCentroCostos.idCentroCosto).order_by(kCentroCostos.idCentroCosto.desc()).first()
        CC_data["idCentroCosto"] = ultimo_CC.idCentroCosto + 1
        nuevo_CC = kCentroCostos(**CC_data)
        db.session.add(nuevo_CC)
    # Se guardan los cambios
    db.session.commit()

    # Se retorna que se ha guardado correctamente
    return jsonify({"guardado": True})