from .rutas import prestaciones
from flask import render_template, request, jsonify
from flask_login import current_user

from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from prestaciones.modelos.modelos import rEmpleadoConcepto
from rh.gestion_empleados.modelos.empleado import rEmpleado
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc

@prestaciones.route('/prestaciones/empleado-concepto')
def empleado_conceptos():
    tiposConcepto = db.session.query(kTipoConcepto).all()
    return render_template('/empleado_conceptos.html', title ='Empleado Conceptos',
                            current_user=current_user,
                            TipoConcepto = tiposConcepto)

@prestaciones.route('/prestaciones/crear-empleado-concepto', methods = ['POST'])
def crear_empleado_concepto():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona' : 'idPersona',
        'TipoConcepto' : 'idTipoConcepto',
        'Concepto' : 'idConcepto',
        'Porcentaje' : 'Porcentaje',
        'Monto' : 'Monto'
    }
    concepto_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    idPersona = concepto_data.get('idPersona', None)
    idTipoConcepto = concepto_data.get('idTipoConcepto', None)
    idConcepto = concepto_data.get('idConcepto', None)

    nuevo_concepto = None
    try:
        concepto_a_modificar = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = idTipoConcepto, idConcepto = idConcepto).one()
        concepto_a_modificar.update(**concepto_data)

    except NoResultFound:
        nuevo_concepto = rEmpleadoConcepto(**concepto_data)
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@prestaciones.route('/prestaciones/buscar-empleado-concepto', methods = ['POST'])
def buscar_empleado_concepto():
    idPersona = request.form.get('idPersona')
    empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
    empleadoConceptos = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona).all()

    lista_empleado_conceptos = []
    for emp_con in empleadoConceptos:
        concepto = db.session.query(kConcepto).filter_by(idConcepto = emp_con.idConcepto, idTipoConcepto = emp_con.idTipoConcepto).first()
        if emp_con is not None:
            emp_con_dict = emp_con.__dict__
            emp_con_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            emp_con_dict["NumeroEmpleado"] = empleado.NumeroEmpleado
            emp_con_dict["Concepto"] = concepto.Concepto
            lista_empleado_conceptos.append(emp_con_dict)
    if not lista_empleado_conceptos:
        return jsonify({"NoEncontrado":True}) 

    return jsonify(lista_empleado_conceptos)


@prestaciones.route('/prestaciones/filtrar-conceptos', methods = ['POST'])
def filtrar_concepto():

    datos = request.get_json()
    TipoConcepto = datos.pop("TipoConcepto", None)
    idPersona = datos.pop("idPersona", None)
    BuscarRepetidos = datos.pop("BuscarRepetidos", None)
    print("BuscarRepetidos")
    print(BuscarRepetidos)
    conceptos = db.session.query(kConcepto).filter_by(idTipoConcepto=TipoConcepto).order_by(asc(kConcepto.Concepto)).all()

    lista_conceptos = []
    for concepto in conceptos:
        empleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idConcepto = concepto.idConcepto, idTipoConcepto = concepto.idTipoConcepto).first()

        if empleadoConcepto is None or BuscarRepetidos=="true":

            if concepto is not None:
                concepto_dict = concepto.__dict__
                concepto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                lista_conceptos.append(concepto_dict)
    if not lista_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_conceptos)



@prestaciones.route('/prestaciones/obtener-concepto', methods = ['POST'])
def obtener_concepto():

    TipoConcepto = request.form.get('TipoConcepto')
    Concepto = request.form.get('Concepto')

    conceptos = db.session.query(kConcepto).filter_by(idTipoConcepto=TipoConcepto, idConcepto=Concepto).first()

    if conceptos is not None:
        concepto_dict = conceptos.__dict__
        concepto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy

    if not concepto_dict:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(concepto_dict)


@prestaciones.route('/prestaciones/eliminar-empleado-concepto', methods = ['POST'])
def eliminar_empleado_concepto():

    idPersona = request.form.get('idPersona')
    idTipoConcepto = request.form.get('TipoConcepto')
    idConcepto = request.form.get('Concepto')

    concepto_a_eliminar = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = idTipoConcepto, idConcepto = idConcepto).delete()
    if concepto_a_eliminar > 0:
        print("El registro fue eliminado correctamente.")
    else:
        print("No se encontró ningún registro para eliminar.")
    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify({"eliminado":True})