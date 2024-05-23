from flask import render_template, request, jsonify, url_for
from datetime import date

from app import db
from .rutas import nomina
from rh.gestion_empleados.modelos.empleado import rEmpleado, tPersona
from rh.gestion_asistencias.modelos.modelos import kTipoProceso
from catalogos.modelos.modelos import kQuincena
from prestaciones.modelos.modelos import rDiasRetroactivo

@nomina.route("/nomina/retroactivos", methods = ['GET', 'POST'])
def retroactivos():
    anio_act = date.today().year

    TipoProceso = db.session.query(kTipoProceso).filter_by(Activo = 1).all()
    Quincenas = db.session.query(kQuincena).filter(kQuincena.FechaInicio >= date(anio_act, 1, 1)).filter(kQuincena.FechaFin <= date(anio_act, 12, 31)).order_by(kQuincena.Quincena).all()

    return render_template('/retroactivos.html', title = 'Retroactivos',
                           TipoProceso = TipoProceso,
                           Quincenas = Quincenas)

@nomina.route("/nomina/guardar-retroactivos", methods = ['POST'])
def guardar_retroactivos():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona': 'idPersona',
        'Quincena': 'idQuincena',
        'DiasRetroactivos': 'Dias',
        'Descripcion': 'Descripcion'
    }

    retroactivos_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    retroactivos_nuevo = None

    if request.form.get('TipoProceso') == '2':
        empleados = db.session.query(rEmpleado.idPersona).join(tPersona).filter(rEmpleado.Activo == 1, tPersona.idTipoPersona ==1).all()
        empleados = [numero[0] for numero in empleados]

        if empleados is not None:
            for id_empleado in empleados:
                retroactivos_data['idPersona'] = int(id_empleado)
                retroactivos_nuevo = rDiasRetroactivo(**retroactivos_data)
                db.session.add(retroactivos_nuevo)

            db.session.commit()
            return({"guardado": True})  

        else:
            return({"guardado": False})
        
    elif request.form.get('TipoProceso') == '1':
        retroactivos_existente = db.session.query(rDiasRetroactivo).filter_by(idPersona = retroactivos_data["idPersona"], idQuincena = retroactivos_data["idQuincena"]).first()
        if retroactivos_existente is None:
            retroactivos_nuevo = rDiasRetroactivo(**retroactivos_data)
            db.session.add(retroactivos_nuevo)
            db.session.commit()
            return({"guardado": True})        
        else:
            return({"guardado": False})
        
@nomina.route("/nomina/buscar-retroactivos", methods = ['POST'])
def buscar_retroactivos():
    idPersona = request.form.get("idPersona")
    lista_retroactivos = []
    retroactivos = db.session.query(rDiasRetroactivo).filter_by(idPersona = idPersona).all()
    for retroactivo in retroactivos:
        retroactivo_dict = retroactivo.__dict__
        retroactivo_dict.pop("_sa_instance_state", None)
        lista_retroactivos.append(retroactivo_dict)

    return jsonify(lista_retroactivos)