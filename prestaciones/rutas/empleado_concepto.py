from .rutas import prestaciones
from flask import render_template, request, jsonify
from flask_login import current_user

from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from prestaciones.modelos.modelos import rEmpleadoConcepto
from sqlalchemy.orm.exc import NoResultFound


@prestaciones.route('/prestaciones/empleado-concepto')
def empleado_conceptos():
    tiposConcepto = db.session.query(kTipoConcepto).all()
    return render_template('/empleado_conceptos.html', title ='Empleado Conceptos',
                            current_user=current_user,
                            TipoConcepto = tiposConcepto)

@prestaciones.route('/crear-empleado-concepto', methods = ['POST'])
def crear_empleado_concepto():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona' : 'idPersona',
        'TipoConcepto' : 'idTipoConcepto',
        'idConcepto' : 'idConcepto',
        'Porcentaje' : 'Porcentaje',
        'Monto' : 'Monto'
    }
    concepto_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    concepto_data['idPersona'] = 1
    print("concepto_data")
    print(concepto_data)

    idPersona = concepto_data.get('idPersona', None)
    idTipoConcepto = concepto_data.get('idTipoConcepto', None)
    idConcepto = concepto_data.get('idConcepto', None)
    nuevo_concepto = None
    try:
        concepto_a_modificar = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = idTipoConcepto, idConcepto = idConcepto).one()
        print("Ya existe")
    except NoResultFound:
        nuevo_concepto = rEmpleadoConcepto(**concepto_data)
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@prestaciones.route('/buscar-empleado-concepto', methods = ['POST'])
def buscar_empleado_concepto():
    idtipoConcepto = request.form.get('TipoConcepto')
    idconcepto = request.form.get('Concepto')
    idPersona = request.form.get('idPersona')

    query = db.session.query(rEmpleadoConcepto)

    if idPersona:
        query = query.filter(rEmpleadoConcepto.idPersona == idPersona)
    if idtipoConcepto != "0":
        query = query.filter(rEmpleadoConcepto.idTipoConcepto == idtipoConcepto)
    if idconcepto:
        query = query.filter(rEmpleadoConcepto.idConcepto.contains(idconcepto))
    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not idconcepto and idtipoConcepto == "0":
        empleadoConceptos = []
    else:
        empleadoConceptos = query.all()


    lista_empleado_conceptos = []
    for emp_con in empleadoConceptos:
        if emp_con is not None:
            emp_con_dict = emp_con.__dict__
            emp_con_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_empleado_conceptos.append(emp_con_dict)
    if not lista_empleado_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_empleado_conceptos)
