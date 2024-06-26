from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy.orm.exc import NoResultFound

from .rutas import catalogos
from app import db
from catalogos.modelos.modelos import kTipoEmpleado, kGrupo

@catalogos.route('/catalogos/grupo', methods = ['POST', 'GET'])
def catalogo_grupo():
    Tipoempleado = db.session.query(kTipoEmpleado).all()
    columns = inspect(kGrupo).all_orm_descriptors.keys()
    return render_template('/grupo.html', title='Grupo',
                           current_user=current_user,
                           Tipoempleado = Tipoempleado,
                           columns = columns)

@catalogos.route('/catalogos/cargar_Grupo', methods = ['POST'])
def cargar_Grupo():
    TipEmp = request.form.get('TipEmp')
    TipAlt = request.form.get('TipAlt')

    Grupos = db.session.query(kGrupo).filter_by(idTipoAlta = TipAlt).all()
    columns = inspect(kGrupo).all_orm_descriptors.keys()

    ret = '<thead><tr>'

    for columna in columns:
        ret += '<th>{}</th>'.format(columna)

    ret += '</thead><tbody>'

    for data in Grupos:
        ret += '<tr>'
        ret += '<td><input type="text" class="form-control" id="idGrupo{}" value="{}" readonly></td>'.format(data.idGrupo, data.idGrupo)
        ret += '<td><input type="text" class="form-control" id="idTipAlt{}" value="{}" readonly></td>'.format(data.idGrupo, data.idTipoAlta)
        ret += '<td><input type="text" class="form-control" id="Grupo{}" value="{}" readonly></td>'.format(data.idGrupo, data.Grupo)
        ret += '<td>\
                <select id="ActGrupo{}" name="ActGrupo{}" class="obligatorio form-control" disabled value={}>\
                    <option value="0">Inactivo</option>\
                    <option value="1">Activo</option>\
                </select>'.format(data.idGrupo, data.idGrupo, data.Activo)
        ret += '<script>\
                    document.ready = document.getElementById("ActGrupo{}").value = "{}"\
                </script>\
                </td>'.format(data.idGrupo, data.Activo)
        ret += '<td><input type="text" class="form-control" id="idEsqHon{}" value="{}" readonly></td>'.format(data.idGrupo, data.idEsquemaHonorarios)
        ret += '<td><button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar{}" onclick="editar_aceptar({})">Editar</button></td>'.format(data.idGrupo, data.idGrupo)
        ret += '<td><button type="button" class="btn btn-secondary oculta-empleado" id="Cancelar{}" onclick="cancelar({}, {}, \'{}\', {}, {})" style="display: none">Cancelar</button></td>'.format(data.idGrupo, data.idGrupo, data.idTipoAlta, data.Grupo, data.Activo, data.idEsquemaHonorarios)
        ret += '</tr>'

    ret += '</tbody>'

    #print(ret)

    return ret

@catalogos.route('/catalogos/guardar_Grupo', methods = ['POST'])
def guardar_grupo():
    columnas = inspect(kGrupo).all_orm_descriptors.keys()
    #print(columnas)
    idGrupo = request.form.get("idGrupo")
    Grupo_data = {key: request.form.get(key) for key in columnas}
    nuevo_Grupo = None
    #print(Grupo_data)
    try:
        Grupo_existente = db.session.query(kGrupo).filter_by(idGrupo = idGrupo).one()
        for attr, value in Grupo_data.items():
            if not attr.startswith('_') and hasattr(Grupo_existente, attr):
                setattr(Grupo_existente, attr, value)
    except NoResultFound:
        ultimo_Grupo = db.session.query(kGrupo.idGrupo).order_by(kGrupo.idGrupo.desc()).first()
        Grupo_data["idGrupo"] = ultimo_Grupo.idGrupo + 1
        nuevo_Grupo = kGrupo(**Grupo_data)
        db.session.add(nuevo_Grupo)
    db.session.commit()

    return jsonify({"guardado": True})